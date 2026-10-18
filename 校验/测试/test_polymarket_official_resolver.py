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

    def test_parse_match_info_from_1x2d(self):
        """测试从 1x2d.js 提取主客队、日期与联赛信息"""
        from 校验.src.domain.polymarket_official_resolver import parse_match_info_from_1x2d
        sample_js = '''
var matchname="Veikkausliiga";
var matchname_cn="芬超冠";
var MatchTime="2026,10-1,18,20,00,00";
var ScheduleID=3085218;
var hometeam="KuPS";
var guestteam="VPS";
'''
        h, g, d, l_cn, l_en = parse_match_info_from_1x2d(sample_js)
        self.assertEqual(h, "KuPS")
        self.assertEqual(g, "VPS")
        self.assertEqual(d, "2026-10-18")
        self.assertEqual(l_cn, "芬超冠")
        self.assertEqual(l_en, "Veikkausliiga")

    def test_official_soccer_leagues_coverage(self):
        """测试官方 /sports 联赛库覆盖芬超、瑞典超、挪超等主流赛事"""
        from 校验.src.domain.polymarket_official_resolver import OFFICIAL_SOCCER_LEAGUES
        self.assertIn("芬超", OFFICIAL_SOCCER_LEAGUES)
        self.assertEqual(OFFICIAL_SOCCER_LEAGUES["芬超"][0], "fin1")
        self.assertEqual(OFFICIAL_SOCCER_LEAGUES["芬超"][1], 105243)
        self.assertIn("西甲", OFFICIAL_SOCCER_LEAGUES)
        self.assertIn("瑞典超", OFFICIAL_SOCCER_LEAGUES)
        self.assertIn("挪超", OFFICIAL_SOCCER_LEAGUES)

    def test_resolve_raw_bundle_missing_js_fails(self):
        """测试当缺少 1x2d.js 时返回明确失败信息"""
        resolver = PolymarketOfficialResolver()
        ok, msg = resolver.resolve_raw_bundle({"payloads": {}})
        self.assertFalse(ok)
        self.assertIn("缺少 1x2d.js", msg)


if __name__ == "__main__":
    unittest.main()
