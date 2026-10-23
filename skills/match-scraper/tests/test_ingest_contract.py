import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills" / "match-scraper" / "scripts"
RAW_3073801 = ROOT / "data" / "2026-10-22" / "raw" / "3073801.json"
RAW_3019164 = ROOT / "data" / "2026-10-23" / "raw" / "3019164.json"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ingest_contract import (  # noqa: E402
    EURO_CIDS,
    assess_payload,
    build_bundle,
    decode_body,
    extract_euro_cids,
    load_contract,
    parse_euro_history,
    validate_bundle,
)

JS_HEADER = 'var game=Array({entries});{game_detail}ScheduleID={match_id};hometeam_cn="主队";guestteam_cn="客队";'


def js_payload(match_id="3073801", cids=None, detail_cids=None, bad_detail=False, reverse=False):
    cids = list(EURO_CIDS if cids is None else cids)
    entries = ",".join(f'"{cid}|{1000 + cid}|Book {cid}|2.0|3.0|4.0"' for cid in cids)
    detail_cids = list(cids if detail_cids is None else detail_cids)
    details = []
    for cid in detail_cids:
        points = [
            "2.00|3.00|4.00|10-22 11:00|0.90|0.95|0.98|2026",
            "2.10|3.10|3.90|10-22 10:00|0.91|0.96|0.99|2026",
        ]
        if reverse:
            points.reverse()
        body = "broken" if bad_detail else ";".join(points)
        details.append(f'"{1000 + cid}^{body}"')
    game_detail = "var gameDetail=Array(" + ",".join(details) + ");"
    return JS_HEADER.format(entries=entries, game_detail=game_detail, match_id=match_id)


def table_payload(label="时间 | 盘口 | 水位"):
    return (
        f"| {label} |\n"
        "| :--- | :--- | :--- |\n"
        "| 2026-10-22 10:00 | 0.90 | 1.00 |\n"
        "| 2026-10-22 11:00 | 1.00 | 0.90 |"
    )


def header_only_payload():
    return "| 时间 | 盘口 | 水位 |\n| :--- | :--- | :--- |"


def html_table_payload():
    return (
        "<table><thead><tr><th>时间</th><th>盘口</th><th>水位</th></tr></thead>"
        "<tbody>"
        "<tr><td>2026-10-22 10:00</td><td>0.90</td><td>1.00</td></tr>"
        "<tr><td>2026-10-22 11:00</td><td>1.00</td><td>0.90</td></tr>"
        "</tbody></table>"
    )


class IngestContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load_contract(ROOT)

    def test_contract_loads_28_endpoints_and_23_slots(self):
        self.assertEqual(len(self.contract.endpoints), 28)
        self.assertEqual(len(self.contract.bookmakers), 23)
        self.assertEqual(len(self.contract.euro_cids), 21)
        self.assertEqual(len(self.contract.change_cids), 7)

    def test_decode_gb18030_and_utf8(self):
        raw = "澳彩 盘口".encode("gb18030")
        self.assertEqual(decode_body(raw, "gb18030"), "澳彩 盘口")
        self.assertEqual(decode_body("平博".encode("utf-8"), "utf-8"), "平博")

    def test_extract_euro_cids_and_duplicates(self):
        all_cids, duplicates = extract_euro_cids(js_payload())
        self.assertEqual(set(all_cids), set(EURO_CIDS))
        self.assertEqual(duplicates, [])
        _, duplicates = extract_euro_cids(js_payload(cids=list(EURO_CIDS) + [80]))
        self.assertEqual(duplicates, [80])

    def test_parse_euro_history_returns_all_core_cids(self):
        histories = parse_euro_history(js_payload())
        self.assertEqual(set(histories), set(EURO_CIDS))
        self.assertTrue(all(len(points) >= 2 for points in histories.values()))
        self.assertGreaterEqual(sum(len(points) for points in histories.values()), 42)

    def test_parse_euro_history_missing_cid_fails(self):
        missing = EURO_CIDS[-1]
        result = assess_payload(
            self.contract,
            "1x2d.js",
            js_payload(detail_cids=list(EURO_CIDS)[:-1]),
        )
        self.assertEqual(result.state, "failed")
        self.assertIn(f"missing_euro_history:{missing}", result.errors)

    def test_parse_euro_history_invalid_detail_fails(self):
        result = assess_payload(self.contract, "1x2d.js", js_payload(bad_detail=True))
        self.assertEqual(result.state, "failed")
        self.assertTrue(any(error.startswith("game_detail_invalid") for error in result.errors))

    def test_parse_euro_history_sorts_by_timestamp(self):
        histories = parse_euro_history(js_payload(reverse=True))
        for points in histories.values():
            timestamps = [point.timestamp for point in points]
            self.assertEqual(timestamps, sorted(timestamps))

    def test_1x2d_missing_cid_fails(self):
        result = assess_payload(self.contract, "1x2d.js", js_payload(cids=list(EURO_CIDS)[:-1]))
        self.assertEqual(result.state, "failed")
        self.assertTrue(any(error.startswith("missing_euro_cid") for error in result.errors))

    def test_1x2d_entity_mismatch_fails(self):
        result = assess_payload(
            self.contract, "1x2d.js", js_payload(match_id="9999999"), match_id="3073801"
        )
        self.assertEqual(result.state, "failed")
        self.assertIn("entity_mismatch", result.errors)

    def test_legal_empty_states(self):
        self.assertEqual(assess_payload(self.contract, "polymarket.json", "[]").state, "not_offered")
        self.assertEqual(assess_payload(self.contract, "analy.json", '{"had": null}').state, "not_offered")
        self.assertEqual(assess_payload(self.contract, "eu_42.html", "").state, "not_offered")

    def test_core_empty_table_fails(self):
        result = assess_payload(self.contract, "ah_1.html", "")
        self.assertEqual(result.state, "failed")
        self.assertIn("empty_required_endpoint", result.errors)

    def test_header_only_table_fails_even_with_pipe_delimiters(self):
        markdown = assess_payload(self.contract, "ah_1.html", header_only_payload())
        self.assertEqual(markdown.state, "failed")
        self.assertIn("empty_required_endpoint", markdown.errors)

        html = assess_payload(self.contract, "ah_1.html", "<table><tr><th>时间</th><th>盘口</th><th>水位</th></tr></table>")
        self.assertEqual(html.state, "failed")
        self.assertIn("empty_required_endpoint", html.errors)

    def test_jammed_mobile_stream_rows_pass(self):
        jammed = (
            "| 公司 | 指数变化 | | | | | | --- | --- | --- | --- | --- | "
            "| 即 | 0.82 | -0.5 | 0.96 | 10-23 10:15 | "
            "| 即 | 0.81 | -0.5 | 0.97 | 10-23 09:52 | "
            "| 即 | 0.82 | -0.5 | 0.96 | 10-23 09:47 | |"
        )
        result = assess_payload(self.contract, "ah_1.html", jammed)
        self.assertEqual(result.state, "ok", result.errors)

    def test_populated_markdown_and_html_tables_pass(self):
        self.assertEqual(assess_payload(self.contract, "ah_1.html", table_payload()).state, "ok")
        self.assertEqual(assess_payload(self.contract, "ah_1.html", html_table_payload()).state, "ok")

    def test_empty_eu_table_is_secondary_not_offered(self):
        result = assess_payload(self.contract, "eu_1.html", "")
        self.assertEqual(result.state, "not_offered")
        self.assertEqual(result.errors, [])

    def test_duplicate_table_rows_fail(self):
        duplicated = (
            "| 时间 | 盘口 | 水位 |\n"
            "| :--- | :--- | :--- |\n"
            "| 2026-10-22 10:00 | 0.90 | 1.00 |\n"
            "| 2026-10-22 10:00 | 0.90 | 1.00 |"
        )
        result = assess_payload(self.contract, "ah_1.html", duplicated)
        self.assertEqual(result.state, "failed")
        self.assertIn("duplicate_odds_triplet", result.errors)

    def test_waf_and_replacement_char_fail(self):
        self.assertIn("waf_blocked", assess_payload(self.contract, "analysis.html", "Just a moment...").errors)
        self.assertIn("replacement_char", assess_payload(self.contract, "analysis.html", "坏\ufffd").errors)

    def test_analysis_and_table_payloads_pass(self):
        self.assertEqual(assess_payload(self.contract, "analysis.html", '<div id="porlet_8">阵容</div>').state, "ok")
        self.assertEqual(assess_payload(self.contract, "ah_1.html", table_payload()).state, "ok")
        self.assertEqual(assess_payload(self.contract, "asian_odds.html", table_payload()).state, "ok")

    def test_mobile_handicap_json_and_anti_mismatch(self):
        json_ok = json.dumps({
            "scheduleId": 3073801,
            "companies": [{"companyId": 1, "nameCn": "澳彩", "details": [{"firstHomeOdds": 1.0}]}]
        })
        self.assertEqual(
            assess_payload(self.contract, "asian_odds.html", json_ok, match_id="3073801").state,
            "ok",
        )
        # 实体 ID 不匹配断言拦截 (Anti-Mismatch)
        res_mismatch = assess_payload(self.contract, "asian_odds.html", json_ok, match_id="9999999")
        self.assertEqual(res_mismatch.state, "failed")
        self.assertIn("schedule_id_mismatch", res_mismatch.errors)

    def test_mobile_lineup_and_events_pass(self):
        lineup_html = '<html><body><script>var lineupObj={"lineup":{"homeFormation":"4-2-3-1"}};</script></body></html>'
        events_html = '<html><body><div>比赛事件 入球 15`</div></body></html>'
        change_stream = '即 0.88 -0/0.5 1.01 10-23 00:44\n早 1.00 -0/0.5 0.82 10-16 19:35'
        self.assertEqual(assess_payload(self.contract, "odds.html", lineup_html).state, "ok")
        self.assertEqual(assess_payload(self.contract, "analy.json", events_html).state, "ok")
        self.assertEqual(assess_payload(self.contract, "ah_3.html", change_stream).state, "ok")

    def _full_payloads(self):
        payloads = {key: table_payload() for key in self.contract.endpoint_keys}
        payloads.update(
            {
                "1x2d.js": js_payload(),
                "analysis.html": '<div id="porlet_8">阵容</div>',
                "odds.html": '<div id="analy_sbAllOdds">波胆</div>',
                "analy.json": '{"had": null}',
                "polymarket.json": "[]",
            }
        )
        return payloads

    def test_bundle_polymarket_empty_is_not_offered(self):
        payloads = self._full_payloads()
        results = {key: assess_payload(self.contract, key, text) for key, text in payloads.items()}
        bundle = build_bundle(
            match={"match_id": "3073801", "sales_date": "2026-10-22", "home": "主队", "away": "客队"},
            results=results,
            contract=self.contract,
        )
        self.assertTrue(bundle["gates"]["ok"], bundle["gates"]["errors"])
        self.assertEqual(bundle["gates"]["slots"]["Polymarket"], "not_offered")

    def test_bundle_188bet_identity_conflict_is_not_supported(self):
        payloads = self._full_payloads()
        payloads["ah_42.html"] = table_payload("18Bet | 时间 | 水位")
        results = {key: assess_payload(self.contract, key, text) for key, text in payloads.items()}
        results["ah_42.html"] = assess_payload(
            self.contract, "ah_42.html", payloads["ah_42.html"], enforce_bookmaker_title=True
        )
        bundle = build_bundle(
            match={"match_id": "3073801", "sales_date": "2026-10-22", "home": "主队", "away": "客队"},
            results=results,
            contract=self.contract,
        )
        self.assertFalse(bundle["gates"]["ok"])
        self.assertEqual(bundle["gates"]["slots"]["188Bet"], "identity_conflict")

    def test_bundle_188bet_empty_evidence_is_not_offered_without_extra_error(self):
        payloads = self._full_payloads()
        payloads["ah_42.html"] = ""
        payloads["ou_42.html"] = ""
        results = {key: assess_payload(self.contract, key, text) for key, text in payloads.items()}
        bundle = build_bundle(
            match={"match_id": "3073801", "sales_date": "2026-10-22", "home": "主队", "away": "客队"},
            results=results,
            contract=self.contract,
        )
        self.assertTrue(bundle["gates"]["ok"], bundle["gates"]["errors"])
        self.assertEqual(bundle["gates"]["slots"]["188Bet"], "not_offered")

    def test_change_tables_only_counts_data_bearing_tables(self):
        payloads = self._full_payloads()
        payloads["eu_1.html"] = ""
        results = {key: assess_payload(self.contract, key, text) for key, text in payloads.items()}
        bundle = build_bundle(
            match={"match_id": "3073801", "sales_date": "2026-10-22", "home": "主队", "away": "客队"},
            results=results,
            contract=self.contract,
        )
        self.assertEqual(bundle["gates"]["counts"]["change_tables"], 20)

    def test_slots_have_a_status_for_all_23_bookmakers(self):
        payloads = self._full_payloads()
        results = {key: assess_payload(self.contract, key, text) for key, text in payloads.items()}
        bundle = build_bundle(
            match={"match_id": "3073801", "sales_date": "2026-10-22", "home": "主队", "away": "客队"},
            results=results,
            contract=self.contract,
        )
        self.assertEqual(len(bundle["gates"]["slots"]), 23)
        self.assertTrue(all(bundle["gates"]["slots"].values()))

    def test_build_and_validate_bundle(self):
        payloads = {
            "1x2d.js": js_payload(),
            "analysis.html": '<div id="porlet_8">阵容</div>',
            "odds.html": '<div id="analy_sbAllOdds">波胆</div>',
            "analy.json": '{"had": null}',
            "polymarket.json": "[]",
            "asian_odds.html": table_payload(),
            "over_under.html": table_payload(),
        }
        for key in self.contract.endpoint_keys:
            if key not in payloads:
                payloads[key] = table_payload()
        results = {
            key: assess_payload(self.contract, key, text)
            for key, text in payloads.items()
        }
        bundle = build_bundle(
            match={"match_id": "3073801", "sales_date": "2026-10-22", "home": "主队", "away": "客队"},
            results=results,
            contract=self.contract,
        )
        report = validate_bundle(bundle, self.contract)
        self.assertTrue(report.ok, report.errors)
        self.assertEqual(report.counts["payload_keys"], 28)
        self.assertEqual(report.counts["bookmaker_slots"], 23)

    def test_validate_bundle_rejects_missing_key_and_bad_receipt(self):
        payloads = {key: table_payload() for key in self.contract.endpoint_keys}
        payloads["1x2d.js"] = js_payload()
        results = {key: assess_payload(self.contract, key, text) for key, text in payloads.items()}
        bundle = build_bundle(
            match={"match_id": "3073801", "sales_date": "2026-10-22", "home": "主队", "away": "客队"},
            results=results,
            contract=self.contract,
        )
        del bundle["payloads"]["over_under.html"]
        report = validate_bundle(bundle, self.contract)
        self.assertFalse(report.ok)
        self.assertIn("missing_payload:over_under.html", report.errors)

        payloads = {key: table_payload() for key in self.contract.endpoint_keys}
        payloads["1x2d.js"] = js_payload()
        results = {key: assess_payload(self.contract, key, text) for key, text in payloads.items()}
        bundle = build_bundle(
            match={"match_id": "3073801", "sales_date": "2026-10-22", "home": "主队", "away": "客队"},
            results=results,
            contract=self.contract,
        )
        bundle["receipt"]["endpoints"]["analysis.html"]["chars"] += 1
        report = validate_bundle(bundle, self.contract)
        self.assertFalse(report.ok)
        self.assertIn("receipt_chars_mismatch:analysis.html", report.errors)

    def test_validate_bundle_rejects_failed_endpoint(self):
        payloads = {key: table_payload() for key in self.contract.endpoint_keys}
        payloads["1x2d.js"] = js_payload()
        payloads["ah_1.html"] = ""
        results = {key: assess_payload(self.contract, key, text) for key, text in payloads.items()}
        bundle = build_bundle(
            match={"match_id": "3073801", "sales_date": "2026-10-22", "home": "主队", "away": "客队"},
            results=results,
            contract=self.contract,
        )
        report = validate_bundle(bundle, self.contract)
        self.assertFalse(report.ok)
        self.assertTrue(any(error.startswith("endpoint_failed:ah_1.html") for error in report.errors))


    @unittest.skipUnless(RAW_3073801.exists(), "saved 3073801 raw is not available")
    def test_saved_3073801_raw_is_not_green_under_the_new_gate(self):
        raw = json.loads(RAW_3073801.read_text(encoding="utf-8"))
        payloads = raw["payloads"]
        histories = parse_euro_history(payloads["1x2d.js"])
        self.assertTrue(set(EURO_CIDS).issubset(histories))
        self.assertTrue(all(len(histories[cid]) >= 1 for cid in EURO_CIDS))
        self.assertEqual(assess_payload(self.contract, "1x2d.js", payloads["1x2d.js"]).state, "ok")

        self.assertEqual(
            assess_payload(self.contract, "polymarket.json", payloads["polymarket.json"]).state,
            "not_offered",
        )
        for key in ("eu_1.html", "eu_3.html", "eu_8.html", "eu_12.html", "eu_42.html", "eu_47.html", "eu_48.html"):
            self.assertNotEqual(
                assess_payload(self.contract, key, payloads[key]).state,
                "ok",
                f"{key} must not pass on a header-only table",
            )


    @unittest.skipUnless(RAW_3019164.exists(), "saved 3019164 raw is not available")
    def test_saved_3019164_bundle_is_complete(self):
        raw = json.loads(RAW_3019164.read_text(encoding="utf-8"))
        self.assertTrue(raw["gates"]["ok"], raw["gates"]["errors"])
        self.assertEqual(len(raw["payloads"]), 28)
        self.assertEqual(len(raw["receipt"]["endpoints"]), 28)
        self.assertEqual(len(raw["gates"]["slots"]), 23)
        self.assertEqual(raw["gates"]["slots"]["Polymarket"], "not_offered")
        self.assertEqual(raw["receipt"]["endpoints"]["eu_42.html"]["state"], "not_offered")
        self.assertEqual(raw["gates"]["counts"]["euro_cids"], 21)


if __name__ == "__main__":
    unittest.main()
