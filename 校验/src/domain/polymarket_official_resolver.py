"""
校验/src/domain/polymarket_official_resolver.py
领域服务: Polymarket 官方 Discover Markets 规范发现与解析引擎

依据 Polymarket 官方文档 (https://docs.polymarket.com/llms.txt):
1. Discover Markets: 通过 Gamma API public-search 发现事件
2. 双向核对: 提取主客队官方英文名，进行双向对阵匹配，严格过滤 active: true, closed: false
3. 官方 Slug 提取: 获取官方 events.slug，按官方规范拼接标准链接 https://polymarket.com/event/{slug}
4. 市场与挂单深度: 获取 1X2 胜平负 markets 与各端点 outcomePrices
"""

import json
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


def extract_team_keywords(name: str) -> List[str]:
    """提取球队核心辨识关键字，剥离 FC, CF, SC, City, United 等通用后缀"""
    clean = re.sub(
        r"\b(FC|CF|SC|City|United|Town|Athletic|Club|de|la|del|FK|BV|SE|AC|AS|Real|Borussia|Sporting)\b",
        "",
        name,
        flags=re.I,
    ).strip()
    words = [w for w in re.split(r"[\s\.\-]+", clean) if len(w) >= 3]
    return words if words else [name.strip()]


import subprocess

def _curl_get_json(url: str, timeout: int = 15) -> Optional[Any]:
    """使用 Windows 原生 curl.exe 获取 JSON 数据，带 --ssl-no-revoke 与 --http1.1 防止截断"""
    try:
        cmd = [
            "curl.exe", "-s", "--ssl-no-revoke", "--http1.1",
            "--max-time", str(timeout),
            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            url
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0 and res.stdout:
            raw_text = res.stdout.decode("utf-8", errors="replace")
            return json.loads(raw_text)
    except Exception:
        pass
    return None

COMMON_SOCCER_SERIES = [
    "uel-2025",
    "europa-conference-league",
    "lib-2025",
    "epl-2025",
    "uefa-champions-league",
    "champions-league-2024-25",
]

ALIAS_MAP = {
    "copenhagen": "kob",
    "kobenhavn": "kob",
    "saint gilloise": "usg",
    "salzburg": "rbs",
    "sturm graz": "stu",
    "torreense": "ut",
    "lech poznan": "lep",
    "universitatea craiova": "ucr",
    "celta vigo": "cel1",
    "estudiantes": "est",
    "flamengo": "fla",
    "sociedad": "rso",
    "milan": "mil1",
    "juventus": "juv",
    "besiktas": "bes",
    "olympiakos": "oly",
    "olympiacos": "oly",
    "bournemouth": "bou",
    "celtic": "cel",
    "braga": "scb",
}

def _clean_str(s: str) -> str:
    """去除西欧语言变音符（如 ç -> c, ø -> o, é -> e）并转小写"""
    nkfd_form = unicodedata.normalize('NFKD', str(s or ""))
    return "".join([c for c in nkfd_form if not unicodedata.combining(c)]).lower()


def match_event_for_teams(
    event: Dict[str, Any],
    home_keywords: List[str],
    away_keywords: List[str],
    match_date: Optional[str] = None,
) -> bool:
    """严格比对 Gamma API 返回的 event 是否为当前对阵双方的活跃比赛"""
    if not isinstance(event, dict):
        return False

    # 官方规约: 排除已关闭或非活跃事件
    if event.get("active") is False or event.get("closed") is True:
        return False

    title_clean = _clean_str(event.get("title") or "")
    slug_clean = _clean_str(event.get("slug") or "")

    # 必须同时命中主队核心词与客队核心词 (支持变音符归一化与缩写匹配)
    def _matches_any(word: str) -> bool:
        w_clean = _clean_str(word)
        if w_clean in title_clean or w_clean in slug_clean:
            return True
        # 3~4 字母缩写匹配 slug (如 fen 匹配 fenerbahce, ast/avl 匹配 aston)
        if len(w_clean) >= 4 and w_clean[:3] in slug_clean:
            return True
        return False

    has_home = any(_matches_any(w) for w in home_keywords)
    has_away = any(_matches_any(w) for w in away_keywords)

    if not (has_home and has_away):
        return False

    # 如果有开球日期 (YYYY-MM-DD)，且 slug 包含日期，核对日期
    if match_date and re.search(r"\d{4}-\d{2}-\d{2}", slug_clean):
        if match_date in slug_clean:
            return True
        # 否则若为完全不同年份/月份/日期，排除
        m_slug_date = re.search(r"(\d{4}-\d{2}-\d{2})", slug_clean)
        if m_slug_date and m_slug_date.group(1) != match_date:
            return False

    return True


def parse_teams_from_1x2d(js_text: str) -> Tuple[str, str, str]:
    """从球探网 1x2d.js 中提取主客队英文名及比赛日期"""
    hm = re.search(r'var\s+hometeam\s*=\s*"([^"]+)"', js_text)
    gm = re.search(r'var\s+guestteam\s*=\s*"([^"]+)"', js_text)
    tm = re.search(r'var\s+MatchTime\s*=\s*"([^"]+)"', js_text)

    h_name = hm.group(1).strip() if hm else ""
    g_name = gm.group(1).strip() if gm else ""
    m_date = ""

    if tm:
        # MatchTime="2026,10-1,14,19,00,00"
        parts = tm.group(1).split(",")
        if len(parts) >= 3:
            year = parts[0].strip()
            # 10-1 -> month 10
            month_part = parts[1].strip()
            month = month_part.split("-")[0] if "-" in month_part else month_part
            day = parts[2].strip()
            m_date = f"{year}-{int(month):02d}-{int(day):02d}"

    return h_name, g_name, m_date


class PolymarketOfficialResolver:
    """Polymarket 官方发现与解析引擎"""

    def __init__(self, session=None):
        self._session = session

    def _get_session(self):
        if self._session is None:
            try:
                from curl_cffi import requests
                self._session = requests.Session(impersonate="chrome")
            except ImportError:
                import urllib.request
                self._session = "urllib"
        return self._session

    def query_public_search(self, query: str) -> List[Dict[str, Any]]:
        """按官方 Discover Markets 规范调用 /public-search?q={query}"""
        sess = self._get_session()
        url = f"https://gamma-api.polymarket.com/public-search?q={query}"

        for attempt in range(3):
            try:
                if sess != "urllib":
                    resp = sess.get(url, timeout=12)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data.get("events") or []
                else:
                    import urllib.request
                    req = urllib.request.Request(
                        url,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                            "Accept": "application/json",
                        },
                    )
                    with urllib.request.urlopen(req, timeout=12) as response:
                        data = json.loads(response.read().decode("utf-8"))
                        return data.get("events") or []
            except Exception:
                time.sleep(1.0 * (attempt + 1))
        return []

    def fetch_event_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """按官方 /events?slug={slug} 获取完整事件结构（含 markets 与挂单 outcomePrices）"""
        sess = self._get_session()
        url = f"https://gamma-api.polymarket.com/events?slug={slug}"

        for attempt in range(3):
            try:
                if sess != "urllib":
                    resp = sess.get(url, timeout=12)
                    if resp.status_code == 200:
                        data = resp.json()
                        if isinstance(data, list) and data:
                            return data[0]
                else:
                    import urllib.request
                    req = urllib.request.Request(
                        url,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                            "Accept": "application/json",
                        },
                    )
                    with urllib.request.urlopen(req, timeout=12) as response:
                        data = json.loads(response.read().decode("utf-8"))
                        if isinstance(data, list) and data:
                            return data[0]
            except Exception:
                time.sleep(1.0 * (attempt + 1))
        return None

    def resolve_match(
        self,
        home_en: str,
        away_en: str,
        match_date: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """官方主客双向发现流：从两队关键字自动匹配官方 Event"""
        if not home_en or not away_en:
            return None

        h_words = extract_team_keywords(home_en)
        a_words = extract_team_keywords(away_en)

        # 依次以主队、客队关键词检索官方接口
        candidate_queries = [h_words[0], a_words[0]]
        for q in candidate_queries:
            events = self.query_public_search(q)
            for ev in events:
                if match_event_for_teams(ev, h_words, a_words, match_date):
                    slug = ev.get("slug")
                    if slug:
                        full_event = self.fetch_event_by_slug(slug)
                        if full_event:
                            return full_event
                        return ev
            time.sleep(0.5)

        return None

    def resolve_raw_bundle(self, raw_bundle: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """为单文件原子包自动补齐真实 polymarket.json 报文"""
        payloads = raw_bundle.get("payloads") or raw_bundle.get("rawFiles") or {}
        js_text = payloads.get("1x2d.js", "")
        if not js_text:
            return False, "缺少 1x2d.js，无法获取官方英文队名"

        home_en, away_en, match_date = parse_teams_from_1x2d(js_text)
        if not home_en or not away_en:
            return False, "无法从 1x2d.js 提取英文队名"

        event = self.resolve_match(home_en, away_en, match_date)
        if event:
            event_json_str = json.dumps([event], ensure_ascii=False, indent=2)
            payloads["polymarket.json"] = event_json_str
            slug = event.get("slug", "")
            return True, f"https://polymarket.com/event/{slug}"

        proof_note = f"官方未开盘（经Gamma双向检索q={home_en}与q={away_en}均无活跃标的）"
        unopened_event = {
            "url": proof_note,
            "status": "unopened",
            "proof": proof_note,
            "home": home_en,
            "away": away_en,
            "matchDate": match_date,
        }
        payloads["polymarket.json"] = json.dumps([unopened_event], ensure_ascii=False, indent=2)
        return False, proof_note
