import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills" / "match-scraper" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from scrapling.spiders.result import ItemList  # noqa: E402
from ingest_spider import (  # noqa: E402
    EndpointAssessment,
    IngestSpider,
    _cached_capture_is_valid,
    build_request_plan,
    content_type_for,
    load_contract,
    main,
)


class IngestSpiderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load_contract(ROOT)

    def test_request_plan_without_polymarket_slug_has_26_urls(self):
        plans = build_request_plan(self.contract, "3073801", None)
        self.assertEqual(len(plans), 26)
        keys = {plan.key for plan in plans}
        self.assertNotIn("polymarket.json", keys)
        self.assertNotIn("eu_42.html", keys)
        self.assertTrue(all("{match_id}" not in plan.url for plan in plans))

    def test_request_plan_with_slug_has_27_urls(self):
        plans = build_request_plan(self.contract, "3073801", "uel-sturm-marseille-2026-10-22")
        self.assertEqual(len(plans), 27)
        keys = {plan.key for plan in plans}
        self.assertNotIn("eu_42.html", keys)
        polymarket = next(plan for plan in plans if plan.key == "polymarket.json")
        self.assertIn("uel-sturm-marseille-2026-10-22", polymarket.url)
        self.assertNotIn("{", polymarket.url)

    def test_request_plan_tier1_precedes_tier2(self):
        plans = build_request_plan(self.contract, "3073801", "uel-test-slug")
        tier1_keys = {"1x2d.js", "analysis.html", "odds.html", "analy.json", "polymarket.json"}
        tier1_indices = [i for i, p in enumerate(plans) if p.key in tier1_keys]
        tier2_indices = [i for i, p in enumerate(plans) if p.key not in tier1_keys]
        self.assertEqual(len(tier1_indices), 5)
        self.assertEqual(len(tier2_indices), 22)
        self.assertLess(max(tier1_indices), min(tier2_indices))

    def test_spider_initializes_with_proxy(self):
        from ingest_spider import IngestSpider
        spider = IngestSpider(
            match_id="3073801",
            sales_date="2026-10-22",
            proxy="http://127.0.0.1:10808",
            root=ROOT,
        )
        self.assertEqual(spider.proxy, "http://127.0.0.1:10808")
        self.assertEqual(spider.concurrent_requests, 1)
        self.assertEqual(spider.concurrent_requests_per_domain, 1)
        self.assertGreaterEqual(spider.download_delay, 1.0)
        self.assertLessEqual(spider.download_delay, 2.0)
        self.assertTrue(spider.autothrottle_enabled)

    def _fake_results(self):
        spider = IngestSpider(match_id="3073801", sales_date="2026-10-22", root=ROOT)
        for key in self.contract.endpoint_keys:
            if key == "polymarket.json":
                continue
            spec = self.contract.endpoint(key)
            text = "" if key == "eu_42.html" else "| 0.90 | -0.5 | 1.00 |"
            state = "not_offered" if key == "eu_42.html" else "ok"
            spider.results[key] = EndpointAssessment(
                key=key,
                url=f"https://example.test/{key}",
                status=200,
                text=text,
                encoding=spec.encoding,
                state=state,
            )
        return spider

    def test_export_items_have_exactly_27_analysis_keys(self):
        spider = self._fake_results()
        items = spider.build_export_items()
        self.assertEqual(len(items), 27)
        self.assertEqual(
            {item["endpoint_key"] for item in items},
            set(self.contract.endpoint_keys) - {"polymarket.json"},
        )
        eu42 = next(item for item in items if item["endpoint_key"] == "eu_42.html")
        self.assertEqual(eu42["content_type"], "empty")
        self.assertEqual(eu42["state"], "not_offered")
        self.assertEqual(eu42["content"], "")

    def test_html_doctype_wins_over_json_suffix(self):
        text = '<!DOCTYPE html><html><script>var jsonData = {"x": 1};</script></html>'
        self.assertEqual(content_type_for("analy.json", text, "html"), "html")
        self.assertEqual(content_type_for("analy.json", '\ufeff' + text, "html"), "html")
        self.assertEqual(content_type_for("analy.json", '{"x": 1}', "json"), "json")
        self.assertEqual(content_type_for("1x2d.js", "var game=[];", "javascript"), "javascript")

    def test_official_item_exporter_writes_27_jsonl_lines(self):
        spider = self._fake_results()
        items = spider.build_export_items()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "capture.jsonl"
            ItemList(items).to_jsonl(path)
            lines = path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 27)
        self.assertTrue(all(line.startswith("{") for line in lines))

    def test_recent_valid_output_is_skipped_before_network(self):
        rows = [
            {"match_id": "3073801", "endpoint_key": f"endpoint_{i}", "state": "ok"}
            for i in range(27)
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "capture.jsonl"
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            stream = io.StringIO()
            with redirect_stdout(stream):
                code = main([
                    "--match-id", "3073801",
                    "--sales-date", "2026-10-24",
                    "--output", str(path),
                ])
        self.assertEqual(code, 0)
        payload = json.loads(stream.getvalue())
        self.assertIs(payload["ok"], False)
        self.assertIs(payload["cached"], True)
        self.assertEqual(payload["skipped"], "cooldown")

    def test_invalid_or_foreign_output_is_not_a_cache_hit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "capture.jsonl"
            path.write_text(
                json.dumps({"match_id": "9999999", "endpoint_key": "endpoint_0", "state": "ok"}) + "\n",
                encoding="utf-8",
            )
            self.assertFalse(_cached_capture_is_valid(path, "3073801"))
            self.assertFalse(_cached_capture_is_valid(path, "9999999"))

    def test_adapter_has_no_sqlite_or_raw_write_path(self):
        source = (SCRIPTS / "ingest_spider.py").read_text(encoding="utf-8")
        self.assertNotIn("import sqlite", source)
        self.assertNotIn("raw/{matchId}.json", source)
        self.assertNotIn("build_bundle", source)
        self.assertNotIn("validate_bundle", source)


if __name__ == "__main__":
    unittest.main()
