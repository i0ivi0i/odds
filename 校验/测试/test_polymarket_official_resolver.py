import unittest
from 校验.src.domain.polymarket_official_resolver import (
    PolymarketOfficialResolver,
    extract_team_keywords,
    match_event_for_teams,
    parse_teams_from_1x2d,
)


class TestPolymarketOfficialResolver(unittest.TestCase):
    def test_extract_team_keywords(self):
        """测试球队关键词提取与剥离"""
        self.assertEqual(extract_team_keywords("Aston Villa FC"), ["Aston", "Villa"])
        self.assertEqual(extract_team_keywords("Norwich City"), ["Norwich"])
        self.assertEqual(extract_team_keywords("Manchester City FC"), ["Manchester"])
        self.assertEqual(extract_team_keywords("Real Madrid CF"), ["Madrid"])
        self.assertEqual(extract_team_keywords("Fenerbahce"), ["Fenerbahce"])

    def test_match_event_for_teams(self):
        """测试对阵双方事件精准匹配（过滤同队不同场次与关闭事件）"""
        target_event = {
            "title": "Aston Villa FC vs. Fenerbahçe SK",
            "slug": "ucl-ast-fen-2026-10-14",
            "active": True,
            "closed": False,
        }
        other_event = {
            "title": "UCL: RB Leipzig vs. Aston Villa",
            "slug": "ucl-rb-leipzig-vs-aston-villa",
            "active": True,
            "closed": False,
        }
        closed_event = {
            "title": "Aston Villa FC vs. Fenerbahçe SK",
            "slug": "ucl-ast-fen-2026-10-14",
            "active": False,
            "closed": True,
        }

        h_words = ["Aston", "Villa"]
        a_words = ["Fenerbahce"]

        self.assertTrue(match_event_for_teams(target_event, h_words, a_words, "2026-10-14"))
        self.assertFalse(match_event_for_teams(other_event, h_words, a_words, "2026-10-14"))
        self.assertFalse(match_event_for_teams(closed_event, h_words, a_words, "2026-10-14"))

    def test_parse_teams_from_1x2d(self):
        """测试从 1x2d.js 报文提取英文队名与比赛日期"""
        sample_js = '''
var matchname="UEFA Champions League";
var MatchTime="2026,10-1,14,19,00,00";
var ScheduleID=3073156;
var hometeam="Aston Villa";
var guestteam="Fenerbahce";
'''
        h, g, d = parse_teams_from_1x2d(sample_js)
        self.assertEqual(h, "Aston Villa")
        self.assertEqual(g, "Fenerbahce")
        self.assertEqual(d, "2026-10-14")

    def test_resolve_raw_bundle_missing_js_fails(self):
        """测试当缺少 1x2d.js 时返回明确失败信息"""
        resolver = PolymarketOfficialResolver()
        ok, msg = resolver.resolve_raw_bundle({"payloads": {}})
        self.assertFalse(ok)
        self.assertIn("缺少 1x2d.js", msg)


if __name__ == "__main__":
    unittest.main()
