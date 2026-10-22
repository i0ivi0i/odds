import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills" / "match-scraper" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ingest_contract import (  # noqa: E402
    EURO_CIDS,
    assess_payload,
    build_bundle,
    decode_body,
    extract_euro_cids,
    load_contract,
    validate_bundle,
)

JS_HEADER = 'var game=Array({entries});ScheduleID={match_id};hometeam_cn="主队";guestteam_cn="客队";'


def js_payload(match_id="3073801", cids=None):
    cids = list(EURO_CIDS if cids is None else cids)
    entries = ",".join(f'"{cid}|1|Book {cid}|2.0|3.0|4.0"' for cid in cids)
    return JS_HEADER.format(entries=entries, match_id=match_id)


def table_payload(label="时间 | 盘口 | 水位"):
    return f"| {label} |\n| :--- |\n| 2026-10-22 10:00 | 0.90 |"


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


if __name__ == "__main__":
    unittest.main()
