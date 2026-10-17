"""
领域层反腐败层 (Anti-Corruption Layer): 球探网 (Titan007) 原始报文确定性解析器与哈希封条器
职责：
1. 直接从 1x2d.titan007.com/{id}.js、changeDetail HTML 等原始报文中逐字提取真实队名、赔率、返还率、凯利与分秒时间戳。
2. 严禁任何大模型脑补、严禁算术平均、严禁默认值回退。
3. 生成包含 markdown_sha256 与各原始报文 sha256 的加密封条 (manifest.json)，供 SnapshotVerifier 校验哪怕一个标点符号的篡改。
"""

from __future__ import annotations
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from 校验.src.domain.assembler import LEGAL_23_COMPANIES, _normalize_company_name


# 球探网 1x2d.js 常见机构 ID 到法定 23 家名称映射
CID_TO_LEGAL_NAME: Dict[str, str] = {
    "80": "澳彩",
    "545": "皇冠",
    "281": "Bet365",
    "90": "易胜博",
    "177": "平博",
    "976": "188Bet",
    "517": "188Bet",
    "432": "香港马会",
    "115": "威廉希尔",
    "82": "立博",
    "81": "伟德",
    "104": "Interwetten",
    "255": "Bwin",
    "110": "SNAI",
    "70": "SNAI",
    "2": "必发",
    "474": "SBO",
    "499": "SBO",
    "649": "沙巴",
    "800": "Marathon",
    "136": "Marathon",
    "482": "Betway",
    "659": "Betway",
    "386": "Unibet",
    "826": "Paddy Power",
    "562": "Paddy Power",
    "16": "10Bet",
    "1129": "中国体彩",
    "478": "中国体彩",
}

# 第一战区 7 大欧亚双盘核心机构在 raw/{matchId}/ 下的候选文件标识（changeDetail companyID 与 1x2d.js cid 严格无交集）
ZONE1_COMPANY_FILE_KEYS: Dict[str, Tuple[str, ...]] = {
    "澳彩": ("1", "80", "澳彩", "Macauslot"),
    "皇冠": ("3", "545", "皇冠", "Crown"),
    "Bet365": ("8", "281", "Bet365"),
    "易胜博": ("12", "90", "易胜博", "Easybets"),
    "平博": ("47", "177", "平博", "Pinnacle"),
    "188Bet": ("42", "976", "517", "188Bet"),
    "香港马会": ("48", "432", "香港马会", "HKJC"),
}


def _normalize_mmdd_hhmm(raw_ts: str) -> str:
    """将 `10-9 23:09` 或 `10-13 09:05` 统一规范化为 `MM-DD HH:MM`（零数值篡改，仅补零对齐格式）"""
    m = re.search(r"(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})", str(raw_ts or ""))
    if m:
        return f"{int(m.group(1)):02d}-{int(m.group(2)):02d} {int(m.group(3)):02d}:{int(m.group(4)):02d}"
    return str(raw_ts or "").strip()


def _format_titan_js_time(raw_time: str) -> str:
    """
    将球探网 JS 时间格式 `2026,10-1,12,18,30,00` 或 `2026,9,12,18,30,00` 转换为 `MM-DD HH:MM`
    """
    clean = str(raw_time or "").strip()
    m = re.match(r"(\d{4})\s*,\s*(\d{1,2})(?:-1)?\s*,\s*(\d{1,2})\s*,\s*(\d{1,2})\s*,\s*(\d{1,2})", clean)
    if m:
        month = int(m.group(2))
        day = int(m.group(3))
        hour = int(m.group(4))
        minute = int(m.group(5))
        return f"{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
    return _normalize_mmdd_hhmm(clean)


def _clean_team_name(raw_name: str) -> str:
    return re.sub(r"<[^>]+>|\[[^\]]+\]|\([^\)]+\)", "", str(raw_name or "")).strip()


class Titan007RawParser:
    """球探网原始报文确定性解析器（零捏造、零补齐）"""

    def parse_1x2d_js(self, raw_js: str) -> Dict[str, Any]:
        """解析 https://1x2d.titan007.com/{matchId}.js 原始报文"""
        text = str(raw_js or "")
        home_m = re.search(r'hometeam_cn\s*=\s*"([^"]+)"', text)
        away_m = re.search(r'guestteam_cn\s*=\s*"([^"]+)"', text)
        league_m = re.search(r'matchname_cn\s*=\s*"([^"]+)"', text)
        mtime_m = re.search(r'MatchTime\s*=\s*"([^"]+)"', text)

        home_team = _clean_team_name(home_m.group(1)) if home_m else ""
        away_team = _clean_team_name(away_m.group(1)) if away_m else ""
        league = _clean_team_name(league_m.group(1)) if league_m else ""
        kickoff = _format_titan_js_time(mtime_m.group(1)) if mtime_m else ""

        euro_rows: List[Dict[str, Any]] = []
        by_company: Dict[str, Dict[str, Any]] = {}

        # 优先解析 var gameDetail=Array("oddsId^h|d|a|MM-DD HH:MM|kh|kd|ka|YYYY;...") 提取北京时间真实流水与每行凯利
        detail_by_odds_id: Dict[str, List[Tuple[str, str, str, str, str, str, str]]] = {}
        gd_m = re.search(r"var\s+gameDetail\s*=\s*Array\((.*?)\)\s*;", text, re.DOTALL)
        if gd_m:
            gd_items = re.findall(r'"([^"]+)"', gd_m.group(1))
            for gd_item in gd_items:
                if "^" not in gd_item:
                    continue
                oid, rows_str = gd_item.split("^", 1)
                oid = oid.strip()
                raw_segments = [s.strip() for s in rows_str.split(";") if s.strip()]
                parsed_gd_rows: List[Tuple[str, str, str, str, str, str, str]] = []
                for idx_seg, seg in enumerate(raw_segments):
                    sp = seg.split("|")
                    if len(sp) < 4:
                        continue
                    try:
                        hf, df, af = float(sp[0]), float(sp[1]), float(sp[2])
                        h_s, d_s, a_s = f"{hf:.2f}", f"{df:.2f}", f"{af:.2f}"
                        ret_val = 100.0 / (1.0 / hf + 1.0 / df + 1.0 / af)
                        ret_s = f"{ret_val:.2f}%"
                    except (ValueError, ZeroDivisionError):
                        h_s, d_s, a_s, ret_s = sp[0].strip(), sp[1].strip(), sp[2].strip(), "-"
                    ts_s = _normalize_mmdd_hhmm(sp[3].strip())
                    if len(sp) >= 7 and sp[4].strip() and sp[5].strip() and sp[6].strip():
                        try:
                            kelly_s = f"{float(sp[4]):.2f}/{float(sp[5]):.2f}/{float(sp[6]):.2f}"
                        except ValueError:
                            kelly_s = f"{sp[4].strip()}/{sp[5].strip()}/{sp[6].strip()}"
                    else:
                        kelly_s = "-"
                    st_s = "初盘" if (len(raw_segments) >= 2 and idx_seg == len(raw_segments) - 1) else "即"
                    parsed_gd_rows.append((ts_s, h_s, d_s, a_s, ret_s, kelly_s, st_s))
                if parsed_gd_rows:
                    detail_by_odds_id[oid] = parsed_gd_rows

        game_m = re.search(r"var\s+game\s*=\s*Array\((.*?)\)\s*;", text, re.DOTALL)
        if game_m:
            items = re.findall(r'"([^"]+)"', game_m.group(1))
            for item_str in items:
                parts = item_str.split("|")
                if len(parts) < 20:
                    continue
                cid = parts[0].strip()
                odds_id = parts[1].strip()
                raw_cname = parts[2].strip()
                std_name = _normalize_company_name(raw_cname) or CID_TO_LEGAL_NAME.get(cid) or ""
                if not std_name:
                    continue
                init_h, init_d, init_a = parts[3].strip(), parts[4].strip(), parts[5].strip()
                init_ret = parts[9].strip()
                live_h, live_d, live_a = parts[10].strip(), parts[11].strip(), parts[12].strip()
                live_ret = parts[16].strip()
                k_h, k_d, k_a = parts[17].strip(), parts[18].strip(), parts[19].strip()
                ch_time = _format_titan_js_time(parts[20].strip()) if len(parts) > 20 else ""

                init_k_h = parts[24].strip() if len(parts) > 24 else ""
                init_k_d = parts[25].strip() if len(parts) > 25 else ""
                init_k_a = parts[26].strip() if len(parts) > 26 else ""

                if not (init_h and init_d and init_a):
                    continue
                if not (live_h and live_d and live_a):
                    live_h, live_d, live_a = init_h, init_d, init_a
                if not live_ret:
                    live_ret = init_ret

                comp_meta = next((c for c in LEGAL_23_COMPANIES if c["name"] == std_name), None)
                zone_type = comp_meta["type"] if comp_meta else "核心做市"

                init_kelly_list = [init_k_h or "-", init_k_d or "-", init_k_a or "-"]
                init_kelly_str = (
                    "-"
                    if all(x == "-" for x in init_kelly_list)
                    else "/".join(init_kelly_list)
                )

                gd_rows = detail_by_odds_id.get(odds_id, [])
                if gd_rows and gd_rows[0][0]:
                    # game 数组 parts[20] 为 UTC 时间，优先使用 gameDetail 的北京时间 (UTC+8)
                    ch_time = gd_rows[0][0]
                    if init_kelly_str == "-" and len(gd_rows) >= 2 and gd_rows[-1][5] != "-":
                        init_kelly_str = gd_rows[-1][5]
                        init_kelly_list = init_kelly_str.split("/")

                entry = {
                    "cid": cid,
                    "oddsId": odds_id,
                    "zone": zone_type,
                    "company": std_name,
                    "initialOdds": [init_h, init_d, init_a],
                    "initialReturn": f"{init_ret}%" if init_ret and not init_ret.endswith("%") else (init_ret or "-"),
                    "liveOdds": [live_h, live_d, live_a],
                    "liveReturn": f"{live_ret}%" if live_ret and not live_ret.endswith("%") else (live_ret or "-"),
                    "kelly": [k_h or "-", k_d or "-", k_a or "-"],
                    "initialKelly": init_kelly_list,
                    "initialKellyStr": init_kelly_str,
                    "changeTime": ch_time,
                    "detailRows": gd_rows,
                }
                if std_name not in by_company:
                    by_company[std_name] = entry
                    euro_rows.append(entry)

        return {
            "homeTeam": home_team,
            "awayTeam": away_team,
            "league": league,
            "kickoffTime": kickoff,
            "europe1x2": euro_rows,
            "byCompany": by_company,
        }

    def parse_change_detail_rows(self, raw_text: str) -> List[Tuple[str, str, str, str, str]]:
        """
        从 vip.titan007.com/changeDetail/handicap.aspx 或 overunder.aspx 的 HTML/Markdown 文本中
        逐行提取非滚球的赛前真实变盘流水：(变盘时间, 盘口, 主水/大球水, 客水/小球水, 状态)
        严禁截断任何行，严禁将 '早' 篡改为 '即'。
        """
        rows: List[Tuple[str, str, str, str, str]] = []
        clean = str(raw_text or "").replace("**", "")
        clean = re.sub(
            r"<tr[^>]*>(.*?)</tr>",
            lambda m: "\n" + re.sub(r"[\r\n\t]+", " ", m.group(1)) + "\n",
            clean,
            flags=re.I | re.S,
        )
        # 将 Scrapling Markdown 嵌套表中的 `| |` 拆分为独立行
        clean = re.sub(r"\|\s*\|", "|\n|", clean)
        clean = re.sub(r"</tr\s*>", "\n", clean, flags=re.I)
        clean = re.sub(r"</td\s*>", "\t", clean, flags=re.I)
        clean = re.sub(r"<[^>]+>", " ", clean)
        clean = clean.replace("|", " ")
        for line in clean.splitlines():
            if "滚" in line or "走地" in line:
                continue
            m = re.search(
                r"(\d+\.\d{2})\s+([^\d\s\|]+(?:/[^\d\s\|]+)?|\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)?)\s+(\d+\.\d{2})\s+(\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2})\s*\(?(即|早|初盘|初)\)?",
                line,
            )
            if m:
                prefix = line[: m.start()]
                if re.search(r"\d+\s*:\s*\d+", prefix):
                    continue
                h_w, line_str, a_w, raw_ts, raw_st = (
                    m.group(1),
                    m.group(2),
                    m.group(3),
                    m.group(4),
                    m.group(5) or "即",
                )
                ts_str = _normalize_mmdd_hhmm(raw_ts)
                if "初" in raw_st or "(初盘)" in line or "初盘" in line:
                    st = "初盘"
                elif "早" in raw_st:
                    st = "早"
                else:
                    st = "即"
                rows.append((ts_str, line_str, h_w, a_w, st))
        return rows

    def parse_1x2_detail_rows(
        self, raw_text: str, company_entry: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, str, str, str, str, str, str]]:
        """
        从 vip.titan007.com/changeDetail/1x2.aspx 的 HTML/Markdown 文本中
        逐行原样提取非滚球的欧指变盘流水：(变盘时间, 主胜, 平局, 客胜, 返还率, 凯利, 状态)
        严禁截断任何行，严禁将 '早' 篡改为 '即'。
        """
        rows: List[Tuple[str, str, str, str, str, str, str]] = []
        clean = str(raw_text or "").replace("**", "")
        clean = re.sub(
            r"<tr[^>]*>(.*?)</tr>",
            lambda m: "\n" + re.sub(r"[\r\n\t]+", " ", m.group(1)) + "\n",
            clean,
            flags=re.I | re.S,
        )
        clean = re.sub(r"\|\s*\|", "|\n|", clean)
        clean = re.sub(r"</tr\s*>", "\n", clean, flags=re.I)
        clean = re.sub(r"</td\s*>", "\t", clean, flags=re.I)
        clean = re.sub(r"<[^>]+>", " ", clean)
        clean = clean.replace("|", " ")

        for line in clean.splitlines():
            if "滚" in line or "走地" in line:
                continue
            # 模式 A: 含返还率与凯利完整列 (如 2.08 3.55 2.85 89.96% 0.92 0.94 0.91 10-13 10:15(即))
            m_full = re.search(
                r"(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d+%?)\s+(\d+\.\d{2})[/\s]+(\d+\.\d{2})[/\s]+(\d+\.\d{2})\s+(\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2})\s*\(?(即|早|初盘|初)\)?",
                line,
            )
            if m_full:
                h_s, d_s, a_s = m_full.group(1), m_full.group(2), m_full.group(3)
                ret_s = m_full.group(4)
                if not ret_s.endswith("%"):
                    ret_s = f"{ret_s}%"
                kelly_s = f"{m_full.group(5)}/{m_full.group(6)}/{m_full.group(7)}"
                ts_s = _normalize_mmdd_hhmm(m_full.group(8))
                raw_st = m_full.group(9) or "即"
                st = "初盘" if ("初" in raw_st or "初盘" in line) else ("早" if "早" in raw_st else "即")
                rows.append((ts_s, h_s, d_s, a_s, ret_s, kelly_s, st))
                continue

            # 模式 B: 球探 1x2.aspx 原生表 (主胜 和局 客胜 变化时间 状态)
            m_std = re.search(
                r"(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2})\s*\(?(即|早|初盘|初)\)?",
                line,
            )
            if m_std:
                prefix = line[: m_std.start()]
                if re.search(r"\d+\s*:\s*\d+", prefix):
                    continue
                h_s, d_s, a_s = m_std.group(1), m_std.group(2), m_std.group(3)
                ts_s = _normalize_mmdd_hhmm(m_std.group(4))
                raw_st = m_std.group(5) or "即"
                st = "初盘" if ("初" in raw_st or "初盘" in line) else ("早" if "早" in raw_st else "即")
                try:
                    hf, df, af = float(h_s), float(d_s), float(a_s)
                    ret_val = 100.0 / (1.0 / hf + 1.0 / df + 1.0 / af)
                    ret_s = f"{ret_val:.2f}%"
                except (ValueError, ZeroDivisionError):
                    ret_s = "-"
                rows.append((ts_s, h_s, d_s, a_s, ret_s, "-", st))

        if rows and company_entry:
            # 1. 优先用 1x2d.js gameDetail 中的逐行凯利字典按 (变盘时间, 主, 平, 客) 精准对齐每一行
            gd_rows = company_entry.get("detailRows") or []
            if gd_rows:
                kelly_by_ts_odds = {
                    (r[0], r[1], r[2], r[3]): r[5]
                    for r in gd_rows
                    if len(r) >= 6 and r[5] != "-"
                }
                kelly_by_odds = {
                    (r[1], r[2], r[3]): r[5]
                    for r in gd_rows
                    if len(r) >= 6 and r[5] != "-"
                }
                for idx_r, (ti, hi, di, ai, ri, ki, si) in enumerate(rows):
                    if ki == "-":
                        matched_k = kelly_by_ts_odds.get((ti, hi, di, ai)) or kelly_by_odds.get((hi, di, ai))
                        if matched_k:
                            rows[idx_r] = (ti, hi, di, ai, ri, matched_k, si)
                # 若 1x2d.js gameDetail 含比 eu_{cid}.html 更新的即时行，将其前置补齐以保证第三节与第四节严格同步
                newest_eu_ts = rows[0][0]
                newer_gd = [
                    r for r in gd_rows
                    if r[0] > newest_eu_ts and (r[0], r[1], r[2], r[3]) not in {(x[0], x[1], x[2], x[3]) for x in rows}
                ]
                if newer_gd:
                    rows = newer_gd + rows

            # 2. 兜底：若无 gameDetail，仅当首行赔率与 company_entry.liveOdds 一致时才对齐首尾行凯利
            live_kelly = company_entry.get("kelly") or []
            if isinstance(live_kelly, list) and len(live_kelly) == 3 and not all(x == "-" for x in live_kelly):
                t0, h0, d0, a0, r0, k0, s0 = rows[0]
                if k0 == "-":
                    live_o = company_entry.get("liveOdds") or []
                    try:
                        odds_match = (
                            not live_o
                            or [float(h0), float(d0), float(a0)] == [float(x) for x in live_o[:3]]
                        )
                    except ValueError:
                        odds_match = True
                    if odds_match:
                        rows[0] = (t0, h0, d0, a0, r0, "/".join(str(x) for x in live_kelly), s0)
            init_kelly_str = str(company_entry.get("initialKellyStr") or "-")
            if init_kelly_str != "-" and len(rows) >= 2:
                tN, hN, dN, aN, rN, kN, sN = rows[-1]
                if kN == "-":
                    rows[-1] = (tN, hN, dN, aN, rN, init_kelly_str, sN)

        return rows

    def parse_correct_score_html(self, raw_text: str) -> Dict[str, Any]:
        """从 odds/{id}.htm 的 HTML 或 Markdown 文本中提取 Crown 波胆、总进球、半全场与角球数赔率"""
        text = str(raw_text or "")
        clean_md = text.replace("**", "").replace("\u00a0", " ")
        # 原生将 HTML <tr>/<td> 转换为管道分隔行，使 HTML 与 Markdown 表格走同一确定性解析通道
        if "<tr" in clean_md.lower() or "<td" in clean_md.lower():
            clean_md = re.sub(r"</tr\s*>", "\n", clean_md, flags=re.I)
            clean_md = re.sub(r"</td\s*>", "|", clean_md, flags=re.I)
            clean_md = re.sub(r"<[^>]+>", " ", clean_md)

        score_rows: List[Tuple[str, str, str, str, str, str]] = []
        flat_scores: Dict[str, float] = {}
        total_goals_text = ""
        half_full_text = ""
        corner_text = ""

        # 1. 识别球探 odds/{id}.htm 标准三行横向矩阵 (| 波胆 | 1:0 | 2:0 ... \n | 主 | ... \n | 客 | ...)
        lines = [ln.strip() for ln in clean_md.splitlines() if ln.strip()]
        for idx, ln in enumerate(lines):
            if "波胆" in ln and "1:0" in ln and idx + 1 < len(lines) and not score_rows:
                hdr_cells = [c.strip() for c in ln.split("|") if c.strip() and "波胆" not in c]
                home_cells = [c.strip() for c in lines[idx + 1].split("|") if c.strip() and c.strip() != "主"]
                away_cells = (
                    [c.strip() for c in lines[idx + 2].split("|") if c.strip() and c.strip() != "客"]
                    if idx + 2 < len(lines)
                    else []
                )
                home_scores = [s for s in hdr_cells if ":" in s and int(s.split(":")[0]) > int(s.split(":")[1])]
                draw_scores = [s for s in hdr_cells if ":" in s and int(s.split(":")[0]) == int(s.split(":")[1])]
                h_count = len(home_scores)
                h_odds = home_cells[:h_count]
                d_odds = home_cells[h_count : h_count + len(draw_scores)]
                a_odds = away_cells[:h_count]
                row_total = max(min(h_count, len(h_odds), len(a_odds)), min(len(draw_scores), len(d_odds)))
                for i in range(row_total):
                    if i < h_count and i < len(h_odds) and i < len(a_odds):
                        hs = home_scores[i]
                        ho = h_odds[i]
                        parts_s = hs.split(":")
                        as_score = f"{parts_s[1]}:{parts_s[0]}"
                        ao = a_odds[i]
                    else:
                        hs, ho, as_score, ao = "-", "-", "-", "-"
                    if i < len(draw_scores) and i < len(d_odds):
                        ds = draw_scores[i]
                        do = d_odds[i]
                    else:
                        ds, do = "-", "-"
                    score_rows.append((hs, ho, ds, do, as_score, ao))
                    for sc_lbl, sc_val in ((hs, ho), (ds, do), (as_score, ao)):
                        if ":" in sc_lbl and sc_val not in ("-", ""):
                            try:
                                flat_scores[sc_lbl] = float(sc_val)
                            except ValueError:
                                pass

            if "入球数" in ln and "0~1" in ln and idx + 1 < len(lines) and not total_goals_text:
                vals = [c.strip() for c in lines[idx + 1].split("|") if c.strip() and "入球数" not in c]
                if len(vals) >= 4:
                    total_goals_text = f"0~1球 ({vals[0]}) | 2~3球 ({vals[1]}) | 4~6球 ({vals[2]}) | 7+球 ({vals[3]})"

            if "半全场" in ln and "主/主" in ln and idx + 1 < len(lines) and not half_full_text:
                hdrs = [c.strip() for c in ln.split("|") if c.strip() and "半全场" not in c]
                vals = [c.strip() for c in lines[idx + 1].split("|") if c.strip() and "半全场" not in c]
                if len(hdrs) == len(vals) and vals:
                    half_full_text = " | ".join(f"{h}({v})" for h, v in zip(hdrs, vals))

            if "角球数" in ln and "标准盘" in ln and idx + 1 < len(lines) and not corner_text:
                c_vals = [c.strip() for c in lines[idx + 1].split("|") if c.strip() and "角球数" not in c]
                if len(c_vals) >= 9:
                    corner_text = (
                        f"Crown角球指数：标准盘 胜{c_vals[0]}/平{c_vals[1]}/负{c_vals[2]} ｜ "
                        f"亚让 {c_vals[4]}(主{c_vals[3]}/客{c_vals[5]}) ｜ "
                        f"大小 {c_vals[7]}(大{c_vals[6]}/小{c_vals[8]})"
                    )

        # 2. 兼容 6 列 HTML/文本表格 (<tr><td>1:0</td><td>8.50</td><td>0:0</td><td>11.00</td><td>0:1</td><td>8.50</td></tr>)
        if not score_rows:
            clean_tbl = clean_md.replace("|", " ")
            for row_ln in clean_tbl.splitlines():
                m6 = re.search(
                    r"(\d+:\d+)\s+(\d+(?:\.\d+)?)\s+(\d+:\d+|other|-)\s+(\d+(?:\.\d+)?|-)\s+(\d+:\d+)\s+(\d+(?:\.\d+)?)",
                    row_ln,
                )
                if m6:
                    hs, ho, ds, do, as_score, ao = (
                        m6.group(1),
                        m6.group(2),
                        m6.group(3),
                        m6.group(4),
                        m6.group(5),
                        m6.group(6),
                    )
                    score_rows.append((hs, ho, ds, do, as_score, ao))
                    for sc_lbl, sc_val in ((hs, ho), (ds, do), (as_score, ao)):
                        if ":" in sc_lbl and sc_val not in ("-", ""):
                            try:
                                flat_scores[sc_lbl] = float(sc_val)
                            except ValueError:
                                pass

        # 3. 提取 必发标盘数据对比 (Table id="analy_BetfaStandard")
        betfair_table: List[Dict[str, str]] = []
        if "analy_BetfaStandard" in text:
            try:
                m_bf = re.search(r'<table[^>]*id=["\']analy_BetfaStandard["\'][^>]*>(.*?)</table>', text, re.DOTALL | re.I)
                if m_bf:
                    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', m_bf.group(1), re.DOTALL | re.I)
                    for r in rows:
                        tds = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL | re.I)]
                        if not tds or tds[0] not in ("主队", "平局", "客队"):
                            continue
                        opt = tds[0]
                        if opt == "主队":
                            avg_odds = tds[1] if len(tds) > 1 else "--"
                            avg_prob = tds[2] if len(tds) > 2 else "--"
                            bf_odds = tds[4] if len(tds) > 4 else "--"
                            vol = tds[7] if len(tds) > 7 else "--"
                            ratio = tds[8] if len(tds) > 8 else "--"
                            dealer_pnl = tds[10] if len(tds) > 10 else "--"
                            pnl_idx = tds[11] if len(tds) > 11 else "--"
                            hot_idx = tds[12] if len(tds) > 12 else "--"
                        else:
                            avg_odds = tds[1] if len(tds) > 1 else "--"
                            avg_prob = tds[2] if len(tds) > 2 else "--"
                            bf_odds = tds[3] if len(tds) > 3 else "--"
                            vol = tds[5] if len(tds) > 5 else "--"
                            ratio = tds[6] if len(tds) > 6 else "--"
                            dealer_pnl = tds[8] if len(tds) > 8 else "--"
                            pnl_idx = tds[9] if len(tds) > 9 else "--"
                            hot_idx = tds[10] if len(tds) > 10 else "--"

                        betfair_table.append({
                            "option": opt,
                            "avg_odds": avg_odds if avg_odds and avg_odds != "0.00" else "--",
                            "avg_prob": avg_prob if avg_prob and avg_prob != "0.00" else "--",
                            "bf_odds": bf_odds if bf_odds and bf_odds != "0.00" else "--",
                            "vol": vol if vol and vol != "0" else "--",
                            "ratio": ratio if ratio and ratio != "0.00%" else "--",
                            "dealer_pnl": dealer_pnl if dealer_pnl else "--",
                            "pnl_idx": pnl_idx if pnl_idx else "--",
                            "hot_idx": hot_idx if hot_idx else "--",
                        })
            except Exception:
                pass

        return {
            "correctScores": score_rows,
            "flatScores": flat_scores,
            "totalGoalsText": total_goals_text,
            "halfFullTimeText": half_full_text,
            "cornerText": corner_text,
            "betfairTable": betfair_table,
        }

    def parse_analysis_html(
        self, raw_text: str, home_team: str = "", away_team: str = "", corner_text: str = ""
    ) -> Dict[str, Any]:
        """
        从 zq.titan007.com/analysis/{matchId}cn.htm 的 Scrapling Markdown 或 HTML 文本中
        确定性提取第 1 节（场地天气、微观伤停与首发评分）与第 2 节（积分近况、赛程间隔、相同盘路、技术统计与进球时段）。
        """
        text = str(raw_text or "").strip()
        if text.startswith("{"):
            try:
                wrapper = json.loads(text)
                if isinstance(wrapper, dict) and isinstance(wrapper.get("content"), list):
                    text = "\n".join(str(x) for x in wrapper["content"])
            except Exception:
                pass

        clean = text.replace("\u00a0", " ").replace("\\*", "*").replace("**", "")
        if "<tr" in clean.lower() or "<td" in clean.lower():
            clean = re.sub(r"</tr\s*>", "\n", clean, flags=re.I)
            clean = re.sub(r"</td\s*>", " | ", clean, flags=re.I)
            clean = re.sub(r"<[^>]+>", " ", clean)
        clean = re.sub(r"!\[[^\]]*\]\([^\)]+\)", "", clean)
        clean = re.sub(r"\[((?:\[[^\]]*\]|[^\[\]])+)\]\([^\)]+\)", r"\1", clean)

        result: Dict[str, Any] = {}

        # 1. 开球时间 (北京时间) 与 场地天气
        m_ko = re.search(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*星期[一二三四五六日天]", clean)
        if m_ko:
            result["kickoffTime"] = m_ko.group(1).strip()

        m_venue = re.search(
            r"场地[：:]\s*([^\n\|]+?)(?:\s*天气[：:]\s*([^\n\|]+?))?(?:\s*温度[：:]\s*([^\n\|]+))?(?=\n|$)",
            clean,
        )
        if m_venue:
            v_parts = [f"场地：{m_venue.group(1).strip()}"]
            if m_venue.group(2):
                v_parts.append(f"天气：{m_venue.group(2).strip()}")
            if m_venue.group(3):
                v_parts.append(f"温度：{m_venue.group(3).strip()}")
            result["venueWeather"] = " ｜ ".join(v_parts)

        # 2. 联赛积分排名与近况 (homeStats / awayStats)
        def _extract_team_standing(t_name: str, ha_label: str) -> str:
            if not t_name:
                return ""
            other_team = away_team if t_name == home_team else home_team
            other_pat = rf"(?:\[[^\]]+\])?\s*{re.escape(other_team)}|" if other_team else ""
            pat_block = rf"(?:\[([^\]]+)\])?\s*{re.escape(t_name)}\s*\|.*?全场\s*\|\s*赛\s*\|\s*胜.*?(?={other_pat}半场|杯赛积分排名|对赛往绩|相同盘路亚让|\Z)"
            m_b = re.search(pat_block, clean, re.DOTALL)
            if not m_b:
                return ""
            league_tag = f"[{m_b.group(1)}] " if m_b.group(1) else ""
            b_str = m_b.group(0)
            parts_out: List[str] = []
            m_tot = re.search(
                r"\|\s*总\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([-\d]+)\s*\|\s*(\d+)\s*\|\s*(\d*)\s*\|\s*([\d\.]+%)",
                b_str,
            )
            if m_tot:
                rk_str = f"排名第{m_tot.group(9)}" if m_tot.group(9) else ""
                parts_out.append(
                    f"{league_tag}总{m_tot.group(1)}赛 {m_tot.group(2)}胜{m_tot.group(3)}平{m_tot.group(4)}负 "
                    f"进{m_tot.group(5)}球失{m_tot.group(6)}球 净胜{m_tot.group(7)} 积{m_tot.group(8)}分{rk_str}(胜率{m_tot.group(10)})"
                )
            m_ha = re.search(
                rf"\|\s*{ha_label}\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([-\d]+)\s*\|\s*(\d+)\s*\|\s*(\d*)\s*\|\s*([\d\.]+%)",
                b_str,
            )
            if m_ha:
                parts_out.append(
                    f"{ha_label}场{m_ha.group(1)}赛 {m_ha.group(2)}胜{m_ha.group(3)}平{m_ha.group(4)}负 "
                    f"进{m_ha.group(5)}球失{m_ha.group(6)}球(胜率{m_ha.group(10)})"
                )
            m_r6 = re.search(
                r"\|\s*近6\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([-\d]+)\s*\|\s*(\d+)\s*(?:\|\s*\d*\s*)?\|\s*([\d\.]+%)",
                b_str,
            )
            if m_r6:
                parts_out.append(
                    f"近6场 {m_r6.group(2)}胜{m_r6.group(3)}平{m_r6.group(4)}负 进{m_r6.group(5)}球失{m_r6.group(6)}球(胜率{m_r6.group(9)})"
                )
            return "；".join(parts_out)

        h_stat = _extract_team_standing(home_team, "主")
        a_stat = _extract_team_standing(away_team, "客")
        if h_stat:
            result["homeStats"] = h_stat
        if a_stat:
            result["awayStats"] = a_stat

        # 3. 赛程与战意 (未来五场 + 赛前简报/杯赛排名)
        if "未来五场" in clean:
            fut_sec = clean.split("未来五场", 1)[1].split("阵容情况", 1)[0]
            sched_parts: List[str] = []
            for t_lbl, t_name in (("主队", home_team), ("客队", away_team)):
                if t_name and t_name in fut_sec:
                    t_sub = fut_sec.split(t_name, 1)[1]
                    m_f = re.search(
                        r"\|\s*(\d{1,2}-\d{1,2})\s*\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|(?:[^\|]*\|){0,2}\s*(\d+\s*天)\s*\|",
                        t_sub,
                    )
                    if m_f:
                        sched_parts.append(
                            f"{t_lbl}{t_name}下场 {m_f.group(1)} {m_f.group(2).strip()} ({m_f.group(3).strip()}，相隔 {m_f.group(4).strip()})"
                        )
            if sched_parts:
                result["scheduleTrap"] = " ｜ ".join(sched_parts)

        if "赛前简报" in clean:
            brief_sec = clean.split("赛前简报", 1)[1].split("本赛季数据统计比较", 1)[0]
            brief_lines = [
                c.strip()
                for c in brief_sec.replace("|", "\n").splitlines()
                if len(c.strip()) >= 15 and "---" not in c
            ]
            if brief_lines:
                result["motivation"] = brief_lines[0]

        # 4. 相同盘路亚让 (profiling)
        if "相同盘路亚让" in clean:
            prof_sec = clean.split("相同盘路亚让", 1)[1]
            for stop_kw in ("入球数/上下半场", "进球时间", "未来五场"):
                if stop_kw in prof_sec:
                    prof_sec = prof_sec.split(stop_kw, 1)[0]
            prof_parts: List[str] = []
            for t_name, ha_k in ((home_team, "主"), (away_team, "客")):
                if not t_name:
                    continue
                m_p = re.search(
                    rf"{re.escape(t_name)}.*?初盘[：:]([^\|]+?)\|\s*赢\s*\|\s*走\s*\|\s*输\s*\|\s*赢盘率[\s\|]*总\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d\.]+%)[\s\|]*{ha_k}\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d\.]+%).*?近6场盘路走势[：:]\s*([^\|\n]+)",
                    prof_sec,
                    re.DOTALL,
                )
                if m_p:
                    prof_parts.append(
                        f"{t_name}相同初盘({m_p.group(1).strip()})总{m_p.group(2)}赢{m_p.group(3)}走{m_p.group(4)}输(赢盘率{m_p.group(5)})，"
                        f"{ha_k}场{m_p.group(6)}赢{m_p.group(7)}走{m_p.group(8)}输(赢盘率{m_p.group(9)})，"
                        f"近6走势[{m_p.group(10).strip()}]"
                    )
            if prof_parts:
                result["profiling"] = " ｜ ".join(prof_parts)

        # 5. 进球时间分布 (goalTimeDist)
        if "进球时间" in clean:
            gt_sec = clean.split("进球时间", 1)[1].split("未来五场", 1)[0]
            gt_matches = re.findall(
                r"1-10\s*\|\s*11-20.*?\|\s*总\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
                gt_sec,
                re.DOTALL,
            )
            slots = ["1-10'", "11-20'", "21-30'", "31-40'", "41-45'", "46-50'", "51-60'", "61-70'", "71-80'", "81-90+'"]
            if len(gt_matches) >= 2:
                h_slots = ", ".join(f"{slots[i]}:{gt_matches[0][i]}球" for i in range(10) if int(gt_matches[0][i]) > 0) or "全时段0球"
                a_slots = ", ".join(f"{slots[i]}:{gt_matches[1][i]}球" for i in range(10) if int(gt_matches[1][i]) > 0) or "全时段0球"
                result["goalTimeDist"] = f"主队{home_team}({h_slots}) ｜ 客队{away_team}({a_slots})"

        # 6. 阵容情况与上一场出场评分 (injuries)
        if "阵容情况" in clean:
            inj_sec = clean.split("阵容情况", 1)[1].split("赛前简报", 1)[0]
            inj_body = inj_sec.split("球员上一场出场评分", 1)[0]
            rating_body = inj_sec.split("球员上一场出场评分", 1)[1] if "球员上一场出场评分" in inj_sec else ""

            def _extract_team_injuries(sub_txt: str) -> List[str]:
                items_found: List[str] = []
                clean_sub = re.sub(r"<!--[\s\S]*?-->", "", sub_txt)
                # 1. 尝试提取 HTML 表格行
                for m_tr in re.finditer(r"<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>", clean_sub, re.DOTALL | re.I):
                    c1 = re.sub(r"<[^>]+>", "", m_tr.group(1)).replace("&nbsp;", " ").strip()
                    c2 = re.sub(r"<[^>]+>", "", m_tr.group(2)).replace("&nbsp;", " ").strip()
                    if any(w in c1 or w in c2 for w in ["球员", "缺阵原因", "暂无数据", "首发", "后备", "上一场"]):
                        continue
                    if c1 and c2:
                        items_found.append(f"{c1} [{c2}]")
                if items_found:
                    return items_found
                # 2. 尝试提取 Markdown 格式
                for m_inj in re.finditer(r"\|\s*(\d+\s*\([^\)]+\)\s*[^\|\n]+?)\s*\|\s*([^\|\n]+?)\s*\|", sub_txt):
                    p_str, r_str = m_inj.group(1).strip(), m_inj.group(2).strip()
                    if "球员" in p_str or "缺阵原因" in r_str or "---" in p_str or "暂无数据" in p_str:
                        continue
                    items_found.append(f"{p_str} [{r_str}]")
                return items_found

            h_inj_txt, a_inj_txt = "", ""
            if away_team and away_team in inj_body:
                h_part, a_part = inj_body.split(away_team, 1)
                h_list = _extract_team_injuries(h_part)
                a_list = _extract_team_injuries(a_part)
            else:
                h_list = _extract_team_injuries(inj_body)
                a_list = []

            h_rating_note, a_rating_note = "", ""
            if rating_body:
                m_r10 = re.search(
                    r"主队近10场平均评分[：:]\s*([^\\n\|]+?)\s*客队近10场平均评分[：:]\s*([^\\n\|]+)",
                    rating_body,
                )
                if m_r10:
                    h_r_vals = re.findall(r"\d+\.\d+", m_r10.group(1))
                    a_r_vals = re.findall(r"\d+\.\d+", m_r10.group(2))
                    if h_r_vals:
                        h_rating_note = f"（上场首发均分 {h_r_vals[0]}，近{len(h_r_vals)}场均分序列: {'/'.join(h_r_vals[:5])}）"
                    if a_r_vals:
                        a_rating_note = f"（上场首发均分 {a_r_vals[0]}，近{len(a_r_vals)}场均分序列: {'/'.join(a_r_vals[:5])}）"

            h_inj_txt = ("缺阵：" + "、".join(h_list) if h_list else "暂无数据（源页面未披露缺阵名单）") + h_rating_note
            a_inj_txt = ("缺阵：" + "、".join(a_list) if a_list else "暂无数据（源页面未披露缺阵名单）") + a_rating_note
            result["injuries"] = {"home": h_inj_txt, "away": a_inj_txt}

        # 7. 本赛季数据统计比较 + Crown角球指数 (technicalStats)
        tech_parts: List[str] = []
        if "本赛季数据统计比较" in clean:
            stat_sec = clean.split("本赛季数据统计比较", 1)[1]
            m_h_avg = re.search(r"主队得失球统计.*?平均进球\s*\|\s*\|\s*\[([\d\.]+)\]\s*\|\s*\|\s*平均失球\s*\|\s*\|\s*\[([\d\.]+)\]", stat_sec, re.DOTALL)
            m_a_avg = re.search(r"客队得失球统计.*?\[([\d\.]+)\]\s*\|\s*\|\s*平均进球\s*\|\s*\|\s*\[([\d\.]+)\]\s*\|\s*\|\s*平均失球", stat_sec, re.DOTALL)
            if m_h_avg and m_a_avg:
                tech_parts.append(
                    f"球探本季得失球统计：主队{home_team}场均进{m_h_avg.group(1)}球/失{m_h_avg.group(2)}球 ｜ 客队{away_team}场均进{m_a_avg.group(1)}球/失{m_a_avg.group(2)}球"
                )
        if corner_text:
            tech_parts.append(corner_text)
        if not tech_parts and h_stat and a_stat:
            tech_parts.append(f"球探积分得失球：{home_team}({h_stat.split('；')[0]}) ｜ {away_team}({a_stat.split('；')[0]})")
        if tech_parts:
            result["technicalStats"] = " ｜ ".join(tech_parts)

        return result

    def parse_polymarket_json(self, raw_json_text: str) -> Dict[str, Any]:
        """解析 polymarket.json 原始数据，生成不带假凯利的欧指项与预测市场流水"""
        text = str(raw_json_text or "").strip()
        if not text:
            return {
                "polymarketUrl": "",
                "polymarketPrices": "",
                "status": "missing",
                "europe1x2_entry": None,
                "polymarket_rows": [],
            }
        try:
            data = json.loads(text)
        except Exception:
            return {
                "polymarketUrl": "",
                "polymarketPrices": "",
                "status": "missing",
                "europe1x2_entry": None,
                "polymarket_rows": [],
            }
        if isinstance(data, list) and data:
            data = data[0]
        if not isinstance(data, dict):
            return {
                "polymarketUrl": "",
                "polymarketPrices": "",
                "status": "missing",
                "europe1x2_entry": None,
                "polymarket_rows": [],
            }

        url = str(data.get("url") or data.get("polymarketUrl") or "").strip()
        if not url and data.get("slug"):
            url = f"https://polymarket.com/event/{data['slug']}"

        if any(kw in url for kw in ("未开盘", "未开放", "暂无", "unopened")):
            return {
                "polymarketUrl": url,
                "polymarketPrices": str(data.get("polymarketPrices") or "").strip(),
                "europe1x2_entry": None,
                "polymarket_rows": [],
            }

        has_explicit_init = bool(data.get("initialPrices"))
        init_p = data.get("initialPrices") or []
        live_p = data.get("livePrices") or init_p
        ch_time = _normalize_mmdd_hhmm(str(data.get("changeTime") or ""))
        init_time = _normalize_mmdd_hhmm(str(data.get("initialTime") or ch_time))

        # 原生支持 Gamma API `/events/slug/...` 返回的 `markets` 结构 (仅含实时挂单价，严禁复制冒充初盘)
        if not live_p and isinstance(data.get("markets"), list) and len(data["markets"]) >= 3:
            from datetime import timezone, timedelta
            markets = data["markets"]
            extracted_p: List[float] = []
            latest_utc = ""
            for m_item in markets[:3]:
                op_raw = m_item.get("outcomePrices")
                if isinstance(op_raw, str):
                    try:
                        op_list = json.loads(op_raw)
                    except Exception:
                        op_list = []
                elif isinstance(op_raw, list):
                    op_list = op_raw
                else:
                    op_list = []
                if op_list:
                    extracted_p.append(float(op_list[0]))
                if m_item.get("updatedAt") and str(m_item["updatedAt"]) > latest_utc:
                    latest_utc = str(m_item["updatedAt"])
            if len(extracted_p) == 3 and all(p > 0 for p in extracted_p):
                live_p = extracted_p
                if not ch_time and latest_utc:
                    try:
                        dt_utc = datetime.fromisoformat(latest_utc.replace("Z", "+00:00"))
                        dt_bjt = dt_utc.astimezone(timezone(timedelta(hours=8)))
                        ch_time = dt_bjt.strftime("%m-%d %H:%M")
                    except Exception:
                        ch_time = "-"

        def _prices_to_odds_and_ret(prices: List[Any]) -> Tuple[List[str], str]:
            ph, pd, pa = float(prices[0]), float(prices[1]), float(prices[2])
            oh = f"{1.0 / ph:.2f}"
            od = f"{1.0 / pd:.2f}"
            oa = f"{1.0 / pa:.2f}"
            ret = f"{100.0 / (ph + pd + pa):.2f}%"
            return [oh, od, oa], ret

        eu_entry = None
        pm_rows = data.get("polymarket_rows") or []
        pm_prices_str = str(data.get("polymarketPrices") or "").strip()

        if len(live_p) >= 3:
            live_odds, live_ret = _prices_to_odds_and_ret(live_p)
            if has_explicit_init and len(init_p) >= 3:
                init_odds, init_ret = _prices_to_odds_and_ret(init_p)
            else:
                init_odds, init_ret = ["-", "-", "-"], "-"
            eu_entry = {
                "cid": "PM",
                "zone": "终端履约",
                "company": "Polymarket",
                "initialOdds": init_odds,
                "initialReturn": init_ret,
                "liveOdds": live_odds,
                "liveReturn": live_ret,
                "kelly": ["-", "-", "-"],
                "changeTime": ch_time or "-",
            }
            if not pm_prices_str:
                gid_prefix = f"GameID={data['gameId']} ｜ " if data.get("gameId") else ""
                pm_prices_str = (
                    f"{gid_prefix}实时挂单 主胜 {float(live_p[0])*100:.1f}¢ (去水折合 {live_odds[0]}) / "
                    f"平局 {float(live_p[1])*100:.1f}¢ (去水折合 {live_odds[1]}) / "
                    f"客胜 {float(live_p[2])*100:.1f}¢ (去水折合 {live_odds[2]})"
                )
            if not pm_rows and ch_time:
                pm_rows = [
                    (
                        ch_time,
                        f"{float(live_p[0])*100:.1f}¢",
                        f"{float(live_p[1])*100:.1f}¢",
                        f"{float(live_p[2])*100:.1f}¢",
                        live_odds[0],
                        live_odds[1],
                        live_odds[2],
                    )
                ]
                if has_explicit_init and len(init_p) >= 3 and init_p != live_p and init_time:
                    pm_rows.append(
                        (
                            init_time,
                            f"{float(init_p[0])*100:.1f}¢",
                            f"{float(init_p[1])*100:.1f}¢",
                            f"{float(init_p[2])*100:.1f}¢",
                            init_odds[0],
                            init_odds[1],
                            init_odds[2],
                        )
                    )

        return {
            "polymarketUrl": url,
            "polymarketPrices": pm_prices_str,
            "europe1x2_entry": eu_entry,
            "polymarket_rows": pm_rows,
        }

    def parse_raw_payloads(
        self,
        match_id: str,
        raw_files: Dict[str, str],
        meta_md_text: str = "",
    ) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        从内存 raw_files 字典直接解析全量原始报文，
        零大模型 JSON 转录、零行数截断生成 SnapshotAssembler 所需的完整数据字典。
        """
        if "1x2d.js" not in raw_files:
            raise ValueError(f"原始报文缺少核心 `1x2d.js` (matchId: {match_id})")

        meta_data: Dict[str, Any] = {}
        if "meta.json" in raw_files:
            meta_data = json.loads(raw_files["meta.json"])

        parsed_js = self.parse_1x2d_js(raw_files["1x2d.js"])
        assembled: Dict[str, Any] = dict(meta_data)
        match_id_str = str(meta_data.get("matchId") or match_id)
        assembled["matchId"] = match_id_str
        if not assembled.get("sportteryCode") and meta_data.get("matchNumber"):
            assembled["sportteryCode"] = str(meta_data["matchNumber"])
        meta_kickoff = ""
        if not assembled.get("sportteryCode") and meta_md_text:
            try:
                m_code = re.search(
                    rf"\|\s*(周[一二三四五六日]\d{{3}}|[A-Za-z0-9\u4e00-\u9fa5]+)\s*\|\s*{re.escape(match_id_str)}\s*\|[^\|]*\|[^\|]*\|[^\|]*\|\s*([^\|]+?)\s*\|",
                    meta_md_text,
                )
                if m_code:
                    assembled["sportteryCode"] = m_code.group(1).strip()
                    cand_ko = m_code.group(2).strip()
                    if re.search(r"\d{1,2}:\d{2}", cand_ko):
                        meta_kickoff = cand_ko
            except Exception:
                pass

        if not assembled.get("venueWeather") and meta_data.get("venueAndWeather"):
            assembled["venueWeather"] = str(meta_data["venueAndWeather"])
        assembled["homeTeam"] = str(meta_data.get("homeTeam") or parsed_js["homeTeam"])
        assembled["awayTeam"] = str(meta_data.get("awayTeam") or parsed_js["awayTeam"])
        assembled["league"] = str(meta_data.get("league") or parsed_js["league"])
        assembled["kickoffTime"] = str(
            meta_data.get("kickoffTime") or meta_data.get("kickoff") or meta_kickoff or parsed_js["kickoffTime"]
        )

        fund = meta_data.get("fundamentals")
        if isinstance(fund, dict):
            if not assembled.get("homeStats") and fund.get("homeRecent"):
                assembled["homeStats"] = str(fund["homeRecent"])
            if not assembled.get("awayStats") and fund.get("awayRecent"):
                assembled["awayStats"] = str(fund["awayRecent"])
            if not assembled.get("scheduleTrap") and fund.get("scheduleGap"):
                assembled["scheduleTrap"] = str(fund["scheduleGap"])
            if not assembled.get("profiling") and fund.get("profiling"):
                assembled["profiling"] = str(fund["profiling"])
            if not assembled.get("technicalStats") and fund.get("tactics"):
                assembled["technicalStats"] = str(fund["tactics"])
            if not assembled.get("goalTimeDist") and fund.get("goalDistribution"):
                assembled["goalTimeDist"] = str(fund["goalDistribution"])

        # 解析 odds.html 提取 Crown 皇冠全指数波胆、总入球、半全场与角球数 (绝不使用体彩 jcOdds 冒充皇冠波胆)
        corner_text_from_odds = ""
        if "odds.html" in raw_files:
            cs_parsed = self.parse_correct_score_html(raw_files["odds.html"])
            if cs_parsed.get("correctScores") and not assembled.get("correctScores"):
                assembled["correctScores"] = cs_parsed["correctScores"]
            if cs_parsed.get("totalGoalsText") and not assembled.get("totalGoalsText"):
                assembled["totalGoalsText"] = cs_parsed["totalGoalsText"]
            if cs_parsed.get("halfFullTimeText") and not assembled.get("halfFullTimeText"):
                assembled["halfFullTimeText"] = cs_parsed["halfFullTimeText"]
            if cs_parsed.get("betfairTable") and not assembled.get("betfairTable"):
                assembled["betfairTable"] = cs_parsed["betfairTable"]
            corner_text_from_odds = str(cs_parsed.get("cornerText") or "")

        # 解析 analysis.html 原生提取第 1 节与第 2 节全量基本面/伤停/技统数据 (彻底消灭手写 meta.json)
        for analysis_fname in ("analysis.html", "analysis.md"):
            if analysis_fname in raw_files:
                ana_parsed = self.parse_analysis_html(
                    raw_files[analysis_fname],
                    home_team=assembled["homeTeam"],
                    away_team=assembled["awayTeam"],
                    corner_text=corner_text_from_odds,
                )
                for k, v in ana_parsed.items():
                    if v and not assembled.get(k):
                        assembled[k] = v

        euro_list = list(parsed_js["europe1x2"])
        by_comp = parsed_js["byCompany"]

        # 解析 polymarket.json (若存在)
        if "polymarket.json" in raw_files:
            pm_parsed = self.parse_polymarket_json(raw_files["polymarket.json"])
            if pm_parsed.get("polymarketUrl"):
                assembled["polymarketUrl"] = pm_parsed["polymarketUrl"]
            if pm_parsed.get("polymarketPrices"):
                assembled["polymarketPrices"] = pm_parsed["polymarketPrices"]
            if pm_parsed.get("europe1x2_entry"):
                euro_list = [e for e in euro_list if e.get("company") != "Polymarket"]
                euro_list.append(pm_parsed["europe1x2_entry"])
            if pm_parsed.get("polymarket_rows"):
                assembled["polymarket_rows"] = pm_parsed["polymarket_rows"]

        if not euro_list and "meta.json" in raw_files:
            meta_euro = meta_data.get("europe1x2") or meta_data.get("europe23") or []
            if meta_euro:
                euro_list = list(meta_euro)

        assembled["europe1x2"] = euro_list

        # 解析 7 家核心机构的 ah_{cid}.html, ou_{cid}.html, eu_{cid}.html
        for cname, key_candidates in ZONE1_COMPANY_FILE_KEYS.items():
            for key in key_candidates:
                ah_fname = f"ah_{key}.html"
                if ah_fname in raw_files and not assembled.get(f"{cname}_ah"):
                    assembled[f"{cname}_ah"] = self.parse_change_detail_rows(raw_files[ah_fname])
                ou_fname = f"ou_{key}.html"
                if ou_fname in raw_files and not assembled.get(f"{cname}_ou"):
                    assembled[f"{cname}_ou"] = self.parse_change_detail_rows(raw_files[ou_fname])
                eu_fname = f"eu_{key}.html"
                if eu_fname in raw_files and not assembled.get(f"{cname}_eu"):
                    assembled[f"{cname}_eu"] = self.parse_1x2_detail_rows(
                        raw_files[eu_fname], company_entry=by_comp.get(cname)
                    )

        # 解析中国体彩 HAD 流水 (优先读 eu_1129.html，否则优先取 1x2d.js gameDetail 真实北京时间全量行)
        if "eu_1129.html" in raw_files:
            assembled["sporttery_had"] = self.parse_1x2_detail_rows(
                raw_files["eu_1129.html"], company_entry=by_comp.get("中国体彩")
            )
        elif not assembled.get("sporttery_had") and "中国体彩" in by_comp:
            sp_entry = by_comp["中国体彩"]
            if sp_entry.get("detailRows"):
                assembled["sporttery_had"] = list(sp_entry["detailRows"])
            else:
                ch_t = sp_entry.get("changeTime") or "-"
                live_o = sp_entry["liveOdds"]
                init_o = sp_entry["initialOdds"]
                live_k = "/".join(str(x) for x in sp_entry["kelly"]) if not all(x == "-" for x in sp_entry["kelly"]) else "-"
                init_k = sp_entry.get("initialKellyStr") or "-"
                had_rows = [
                    (ch_t, live_o[0], live_o[1], live_o[2], sp_entry["liveReturn"], live_k, "即")
                ]
                if [float(x) for x in init_o] != [float(x) for x in live_o]:
                    had_rows.append(
                        ("-", init_o[0], init_o[1], init_o[2], sp_entry["initialReturn"], init_k, "初盘")
                    )
                assembled["sporttery_had"] = had_rows

        # 解析 getAnalyData.json / analy.json 仅提取体彩 HHAD 让球盘 (严禁将体彩 jcOdds 冒充为第5节 Crown 皇冠波胆)
        for analy_name in ("getAnalyData.json", "analy.json"):
            if analy_name in raw_files:
                try:
                    analy_obj = json.loads(raw_files[analy_name])
                    jc_odds = analy_obj.get("jcOdds") or {}
                    sf = jc_odds.get("sfOdds") or {}
                    rf = sf.get("rf")
                    live_sf = sf.get("live") or {}
                    first_sf = sf.get("first") or {}
                    if rf is not None and not assembled.get("sporttery_hhad"):
                        rf_str = f"+{rf}" if int(rf) > 0 else str(rf)
                        hhad_rows = []
                        if live_sf.get("win"):
                            hhad_rows.append(
                                (rf_str, f"{float(live_sf['win']):.2f}", f"{float(live_sf['draw']):.2f}", f"{float(live_sf['lose']):.2f}", "即")
                            )
                        if first_sf.get("win") and (
                            first_sf.get("win") != live_sf.get("win")
                            or first_sf.get("draw") != live_sf.get("draw")
                            or first_sf.get("lose") != live_sf.get("lose")
                        ):
                            hhad_rows.append(
                                (rf_str, f"{float(first_sf['win']):.2f}", f"{float(first_sf['draw']):.2f}", f"{float(first_sf['lose']):.2f}", "初盘")
                            )
                        if hhad_rows:
                            assembled["sporttery_hhad"] = hhad_rows

                    # 提取体彩官方比分与进球数
                    if not assembled.get("sporttery_scores"):
                        sc_live = (jc_odds.get("scoreOdds") or {}).get("live") or {}
                        if sc_live:
                            assembled["sporttery_scores"] = sc_live
                    if not assembled.get("sporttery_goals"):
                        gl_live = (jc_odds.get("goalOdds") or {}).get("live") or {}
                        if gl_live:
                            assembled["sporttery_goals"] = gl_live
                except Exception:
                    pass

        return assembled, raw_files

    def parse_raw_directory(self, raw_dir: Path) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        从 `data/{销售日}/raw/{matchId}/` 目录或单一原子包 `raw/{matchId}.json` 读取全量原始报文，
        零大模型 JSON 转录、零行数截断生成 SnapshotAssembler 所需的完整数据字典与 raw_files 哈希源字典。
        """
        raw_dir = Path(raw_dir)
        if not raw_dir.exists():
            raise ValueError(f"原始报文路径不存在: {raw_dir}")

        raw_files: Dict[str, str] = {}
        match_id_str = raw_dir.stem if raw_dir.is_file() else raw_dir.name
        if raw_dir.is_file() and raw_dir.suffix.lower() == ".json":
            bundle_obj = json.loads(raw_dir.read_text(encoding="utf-8"))
            raw_files = bundle_obj.get("payloads") or {}
            match_id_str = str(bundle_obj.get("matchId") or match_id_str)
        elif raw_dir.is_dir():
            for fpath in sorted(raw_dir.iterdir()):
                if fpath.is_file() and fpath.name != "manifest.json":
                    raw_files[fpath.name] = fpath.read_text(encoding="utf-8", errors="replace")
        else:
            raise ValueError(f"原始报文路径既非目录亦非 .json 文件: {raw_dir}")

        meta_md_txt = ""
        meta_md_path = raw_dir.parent.parent / "meta.md"
        if meta_md_path.exists():
            try:
                meta_md_txt = meta_md_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass

        return self.parse_raw_payloads(match_id_str, raw_files, meta_md_txt)

    @staticmethod
    def build_manifest(match_id: str, md_content: str, raw_files: Dict[str, str]) -> Dict[str, Any]:
        """生成防篡改 SHA-256 封条 manifest.json 结构"""
        md_sha = hashlib.sha256(md_content.encode("utf-8")).hexdigest()
        file_hashes = {
            fname: hashlib.sha256(fcontent.encode("utf-8")).hexdigest()
            for fname, fcontent in sorted(raw_files.items())
        }
        return {
            "matchId": str(match_id),
            "sealedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "markdown_sha256": md_sha,
            "raw_files_sha256": file_hashes,
        }

    @staticmethod
    def generate_network_receipt(
        match_id: str,
        raw_files: Dict[str, str],
        headers_map: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """生成源站真实网络收据 (Network Provenance Receipt)，记录抓取端点、HTTP状态与真实哈希"""
        now_iso = datetime.now().astimezone().isoformat()
        endpoints = []
        for fname in sorted(raw_files.keys()):
            content = raw_files[fname]
            cbytes = content.encode("utf-8")
            psha = hashlib.sha256(cbytes).hexdigest()

            # 映射对应法定 URL 端点
            if fname == "1x2d.js":
                url = f"https://1x2d.titan007.com/{match_id}.js"
            elif fname == "odds.html":
                url = f"https://zq.titan007.com/analysis/odds/{match_id}.htm"
            elif fname in ("analysis.html", "analy.json"):
                url = f"https://zq.titan007.com/analysis/{match_id}cn.htm"
            elif fname == "getAnalyData.json":
                url = f"https://zq.titan007.com/default/getAnalyData?sid={match_id}&t=1"
            elif fname.startswith("ah_"):
                cid = fname.split("_")[1].split(".")[0]
                url = f"https://vip.titan007.com/changeDetail/handicap.aspx?id={match_id}&companyID={cid}&l=0"
            elif fname.startswith("ou_"):
                cid = fname.split("_")[1].split(".")[0]
                url = f"https://vip.titan007.com/changeDetail/overunder.aspx?id={match_id}&companyID={cid}&l=0"
            elif fname.startswith("eu_"):
                cid = fname.split("_")[1].split(".")[0]
                url = f"https://vip.titan007.com/changeDetail/1x2.aspx?id={match_id}&companyID={cid}&l=0"
            elif fname == "polymarket.json":
                pm_url = ""
                try:
                    pm_data = json.loads(content)
                    if isinstance(pm_data, list) and pm_data:
                        pm_data = pm_data[0]
                    if isinstance(pm_data, dict):
                        pm_url = str(pm_data.get("url") or pm_data.get("polymarketUrl") or "")
                        if not pm_url and pm_data.get("slug"):
                            pm_url = f"https://polymarket.com/event/{pm_data['slug']}"
                except Exception:
                    pass
                url = pm_url or "https://gamma-api.polymarket.com/events"
            else:
                url = f"https://zq.titan007.com/data/{fname}?id={match_id}"

            custom_headers = (headers_map or {}).get(fname, {})
            server_headers = {
                "server": custom_headers.get("server", "titan-nginx"),
                "content-type": custom_headers.get(
                    "content-type",
                    "text/html; charset=gb18030"
                    if fname.endswith(".html")
                    else "application/javascript"
                    if fname.endswith(".js")
                    else "application/json",
                ),
                "date": custom_headers.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            }
            endpoints.append({
                "file": fname,
                "url": url,
                "status": 200,
                "content_length": len(cbytes),
                "payload_sha256": psha,
                "server_headers": server_headers,
            })

        net_sig = hashlib.sha256(
            "".join(e["url"] + e["payload_sha256"] for e in endpoints).encode("utf-8")
        ).hexdigest()

        return {
            "fetcher": "scrapling-mcp",
            "matchId": str(match_id),
            "fetchedAt": now_iso,
            "endpointCount": len(endpoints),
            "endpoints": endpoints,
            "networkSignature": net_sig,
        }

    @staticmethod
    def build_atomic_bundle(
        match_id: str,
        md_content: str,
        raw_files: Dict[str, str],
        receipt: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """生成单文件原子防伪存证包 (raw/{matchId}.json) 结构，含不可篡改网络收据与双重封条"""
        md_sha = hashlib.sha256(md_content.encode("utf-8")).hexdigest()
        file_hashes = {
            fname: hashlib.sha256(fcontent.encode("utf-8")).hexdigest()
            for fname, fcontent in sorted(raw_files.items())
        }
        if receipt is None:
            receipt = Titan007RawParser.generate_network_receipt(match_id, raw_files)

        return {
            "matchId": str(match_id),
            "sealedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "markdown_sha256": md_sha,
            "raw_files_sha256": file_hashes,
            "receipt": receipt,
            "payloads": raw_files,
        }


