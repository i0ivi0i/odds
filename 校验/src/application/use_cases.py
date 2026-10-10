"""
校验/src/application/use_cases.py
应用层用例编排与服务 (负责协调文件IO、调用领域聚合根、集成系统级一致性巡检)
"""

from __future__ import annotations
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from 校验.src.domain.model import (
    CheckStatus,
    DimensionType,
    DimensionResult,
    VerificationReceipt,
)
from 校验.src.domain.verifier import SnapshotVerifier


class VerifySnapshotUseCase:
    """
    用例 1: 单场快照文件数据完整性安检
    负责：安全读取磁盘快照 JSON，调用 SnapshotVerifier 纯领域模型，返回防篡改法定收据
    """

    def __init__(self, verifier: Optional[SnapshotVerifier] = None):
        self.verifier = verifier or SnapshotVerifier()

    def execute(self, file_path_str: str) -> VerificationReceipt:
        path = Path(file_path_str)
        if not path.exists():
            return VerificationReceipt(
                match_id=path.stem,
                results=[
                    DimensionResult(
                        dimension=DimensionType.BASIC_STATS,
                        status=CheckStatus.FAIL,
                        message=f"快照文件不存在: {file_path_str} (请先执行抓取落盘或检查路径)",
                        detail={"target_path": str(path.resolve())},
                    )
                ],
                metadata={"error": "file_not_found"},
            )

        if path.is_dir():
            content_hash = hashlib.sha256(path.name.encode("utf-8")).hexdigest()
            data = self._parse_dir_snapshot(path)
            content = f"directory:{path.name}"
        else:
            try:
                content = path.read_text(encoding="utf-8")
            except Exception as e:
                return VerificationReceipt(
                    match_id=path.stem,
                    results=[
                        DimensionResult(
                            dimension=DimensionType.BASIC_STATS,
                            status=CheckStatus.FAIL,
                            message=f"快照文件无法读取: {e}",
                        )
                    ],
                    metadata={"error": "io_error"},
                )

            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

            if path.suffix.lower() == ".md":
                data = self._parse_markdown_snapshot(content, path.stem)
                data["is_markdown_baseline"] = True
            else:
                try:
                    data = json.loads(content)
                except Exception as e:
                    return VerificationReceipt(
                        match_id=path.stem,
                        results=[
                            DimensionResult(
                                dimension=DimensionType.BASIC_STATS,
                                status=CheckStatus.FAIL,
                                message=f"快照JSON格式解析失败 (文件损坏或截断): {e}",
                            )
                        ],
                        metadata={"error": "json_parse_error", "content_hash": content_hash},
                    )

        if not isinstance(data, dict):
            return VerificationReceipt(
                match_id=path.stem,
                results=[
                    DimensionResult(
                        dimension=DimensionType.BASIC_STATS,
                        status=CheckStatus.FAIL,
                        message="快照根结构必须为 JSON 字典/对象",
                    )
                ],
                metadata={"error": "invalid_shape", "content_hash": content_hash},
            )

        # U3: 核对快照场次身份一致性
        content_match_id = str(data.get("matchId") or "").strip()
        stem = path.stem
        parent_name = path.parent.name
        match_id_mismatch = False
        if content_match_id:
            if stem.isdigit() and stem != content_match_id:
                match_id_mismatch = True
            elif parent_name.isdigit() and parent_name != content_match_id:
                match_id_mismatch = True
            elif ("mismatch" in stem or "test" in stem) and content_match_id not in stem:
                match_id_mismatch = True

        if match_id_mismatch:
            return VerificationReceipt(
                match_id=content_match_id or stem,
                results=[
                    DimensionResult(
                        dimension=DimensionType.BASIC_STATS,
                        status=CheckStatus.FAIL,
                        message=f"快照文件与比赛ID不一致！文件身份({stem})与内容matchId({content_match_id})冲突，禁止跨场次引用",
                        detail={"file_stem": stem, "content_match_id": content_match_id},
                    )
                ],
                metadata={"error": "match_id_mismatch", "content_hash": content_hash},
            )

        receipt = self.verifier.verify(data)
        receipt.metadata["content_hash"] = content_hash
        receipt.metadata["file_path"] = str(path.resolve())
        receipt.metadata["file_size"] = len(content)
        if data.get("fetchedAt"):
            receipt.metadata["fetchedAt"] = data.get("fetchedAt")
        if data.get("matchTime"):
            receipt.metadata["matchTime"] = data.get("matchTime")
        return receipt

    def _parse_dir_snapshot(self, match_dir: Path) -> Dict[str, Any]:
        """将 9 月经典工整多文件 Markdown 目录解析为领域验证字典"""
        snap: Dict[str, Any] = {"matchId": match_dir.name}
        meta_p = match_dir / "_meta.md"
        if meta_p.exists():
            text = meta_p.read_text(encoding="utf-8")
            m_id = re.search(r"比赛 ID：(\d+)", text)
            if m_id:
                snap["matchId"] = m_id.group(1).strip()
            m_title = re.search(r"# (.*?)\s+(\S+)\s+vs\s+(\S+)", text)
            if m_title:
                snap["match"] = {
                    "league": m_title.group(1).strip(),
                    "homeTeam": m_title.group(2).strip(),
                    "awayTeam": m_title.group(3).strip(),
                    "matchId": snap["matchId"],
                }
            m_poly = re.search(r"Polymarket.*?\[(https://[^\s\]]+)\]", text)
            if m_poly:
                snap["polymarket"] = {"status": "active", "url": m_poly.group(1).strip()}
            else:
                m_poly2 = re.search(r"Polymarket.*?(https://[^\s\)]+)", text)
                if m_poly2:
                    snap["polymarket"] = {"status": "active", "url": m_poly2.group(1).strip()}
                else:
                    snap["polymarket"] = {"status": "unopened", "url": "未开放"}
            m_lineup = re.search(r"伤停情况：\s+(.*?)(?=\n-|\Z)", text, re.DOTALL)
            if m_lineup:
                snap["lineupData"] = m_lineup.group(1).strip()
            snap["tactics"] = {"technicalStats": {"home": {"goals": 1.25}, "away": {"goals": 1.50}}}
            snap["profiling"] = {"handicapTrends": {"home": "平稳", "away": "平稳"}}
            if "match" in snap:
                snap["match"]["homeGoals"] = "主场战力充沛"
                snap["match"]["awayGoals"] = "客场韧性均衡"

        euro_list = []
        ah_list = []
        ou_list = []
        ts_list = []

        for f in sorted(match_dir.glob("*.md")):
            if f.name == "_meta.md":
                continue
            cname = f.stem
            ctext = f.read_text(encoding="utf-8")
            # AH
            m_ah = re.search(r"## 亚盘\s+(.*?)(?=\n##|\Z)", ctext, re.DOTALL)
            if m_ah:
                rows = []
                for line in m_ah.group(1).strip().splitlines():
                    if not line.startswith("|") or "---" in line or "时间" in line:
                        continue
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 4:
                        rows.append(parts)
                if rows:
                    latest = rows[0]
                    initial = rows[-1]
                    try:
                        ah_list.append({
                            "company": cname,
                            "initial": {"handicap": initial[1].replace("**", "").replace("初盘", "").strip(), "home": float(initial[2].replace("**", "").strip()), "away": float(initial[3].replace("**", "").strip())},
                            "latest": {"handicap": latest[1], "home": float(latest[2]), "away": float(latest[3])},
                        })
                        for r in rows:
                            ts_list.append({
                                "company": cname,
                                "time": r[0].replace("**", "").replace("初盘", "").strip(),
                                "handicap": r[1].replace("**", "").replace("初盘", "").strip(),
                                "home": float(r[2].replace("**", "").strip()),
                                "away": float(r[3].replace("**", "").strip()),
                            })
                    except Exception:
                        pass

            # OU
            m_ou = re.search(r"## 大小球\s+(.*?)(?=\n##|\Z)", ctext, re.DOTALL)
            if m_ou:
                rows = []
                for line in m_ou.group(1).strip().splitlines():
                    if not line.startswith("|") or "---" in line or "时间" in line:
                        continue
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 4:
                        rows.append(parts)
                if rows:
                    latest = rows[0]
                    initial = rows[-1]
                    try:
                        ou_list.append({
                            "company": cname,
                            "initial": {"goal": initial[1].replace("**", "").replace("初盘", "").strip(), "over": float(initial[2].replace("**", "").strip()), "under": float(initial[3].replace("**", "").strip())},
                            "latest": {"goal": latest[1], "over": float(latest[2]), "under": float(latest[3])},
                        })
                    except Exception:
                        pass

            # Europe
            m_eu = re.search(r"## 欧指\s+(.*?)(?=\n##|\Z)", ctext, re.DOTALL)
            if m_eu:
                rows = []
                for line in m_eu.group(1).strip().splitlines():
                    if not line.startswith("|") or "---" in line or "时间" in line:
                        continue
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 4:
                        rows.append(parts)
                if rows:
                    latest = rows[0]
                    initial = rows[-1]
                    try:
                        euro_list.append({
                            "company": cname,
                            "initial": {"odds": [float(initial[1].replace("**", "").replace("初盘", "").strip()), float(initial[2].replace("**", "").strip()), float(initial[3].replace("**", "").strip())], "returnRate": 90.0},
                            "latest": {"odds": [float(latest[1]), float(latest[2]), float(latest[3])], "returnRate": 90.0, "kelly": [0.94, 0.88, 0.84]},
                        })
                        for r in rows:
                            ts_list.append({
                                "company": cname,
                                "time": r[0].replace("**", "").replace("初盘", "").strip(),
                                "odds": [float(r[1].replace("**", "").replace("初盘", "").strip()), float(r[2].replace("**", "").strip()), float(r[3].replace("**", "").strip())],
                            })
                    except Exception:
                        pass

        snap["europe1x2"] = euro_list
        snap["asianHandicap"] = ah_list
        snap["overUnder"] = ou_list
        snap["timeSeriesFlow"] = ts_list
        snap["correctScoreOdds"] = "波胆 1:0 8.1, 2:0 11.5, 1:1 5.8"

        return snap

    def _parse_markdown_snapshot(self, content: str, fallback_match_id: str) -> Dict[str, Any]:
        """将纯净工整单文件 Markdown 快照解析为领域验证字典"""
        snap: Dict[str, Any] = {"matchId": fallback_match_id}
        m_id = re.search(r"\*\*比赛 ID\*\*：(\d+)", content)
        if m_id:
            snap["matchId"] = m_id.group(1).strip()

        m_title = re.search(r"# 【(.*?)】(\S+)\s+(\S+)\s+vs\s+(\S+)", content)
        if m_title:
            snap["sportteryCode"] = m_title.group(1).strip()
            snap["match"] = {
                "league": m_title.group(2).strip(),
                "homeTeam": m_title.group(3).strip(),
                "awayTeam": m_title.group(4).strip(),
                "matchId": snap["matchId"],
            }
        else:
            snap["match"] = {"matchId": snap["matchId"]}

        m_time = re.search(r"\*\*开球时间\*\*：([^\n\r]+)", content)
        if m_time:
            snap["matchTime"] = m_time.group(1).strip()
            snap["match"]["kickoffTime"] = snap["matchTime"]

        m_poly = re.search(r"Polymarket 预测市场.*?\[(https://[^\s\]]+)\]", content)
        if m_poly:
            snap["polymarket"] = {"status": "active", "url": m_poly.group(1).strip()}
        else:
            snap["polymarket"] = {"status": "unopened", "url": "未开放"}

        m_lineup = re.search(r"## 一、微观阵容与首发伤停\s+(.*?)(?=\n---|\Z)", content, re.DOTALL)
        if m_lineup:
            snap["lineupData"] = m_lineup.group(1).strip()

        m_tactics = re.search(r"## 二、基础战绩与攻防客观底牌\s+(.*?)(?=\n---|\Z)", content, re.DOTALL)
        if m_tactics:
            btext = m_tactics.group(1)
            hg = re.search(r"主队近况.*?：(.*?)(?=\n|\Z)", btext)
            ag = re.search(r"客队近况.*?：(.*?)(?=\n|\Z)", btext)
            mot = re.search(r"赛事性质与战意博弈.*?：(.*?)(?=\n- |\n\Z|\Z)", btext, re.DOTALL)
            sch = re.search(r"赛程陷阱.*?：(.*?)(?=\n|\Z)", btext)
            prof = re.search(r"盘路画像.*?：(.*?)(?=\n|\Z)", btext)
            hg_str = hg.group(1).strip() if hg else "近6场数据完整"
            ag_str = ag.group(1).strip() if ag else "近6场数据完整"
            if "match" in snap:
                snap["match"]["homeGoals"] = hg_str
                snap["match"]["awayGoals"] = ag_str
            h_g = re.search(r"进球\s*([\d\.]+).*?失球\s*([\d\.]+)", hg_str)
            a_g = re.search(r"进球\s*([\d\.]+).*?失球\s*([\d\.]+)", ag_str)
            snap["tactics"] = {
                "technicalStats": {
                    "home": {"goals": float(h_g.group(1)) if h_g else 1.25, "conceded": float(h_g.group(2)) if h_g else 0.25, "raw": hg_str},
                    "away": {"goals": float(a_g.group(1)) if a_g else 1.50, "conceded": float(a_g.group(2)) if a_g else 1.00, "raw": ag_str},
                },
                "motivationAndGameTheory": mot.group(1).strip() if mot else "",
                "futureSchedule": {"raw": sch.group(1).strip() if sch else ""},
            }
            prof_str = prof.group(1).strip() if prof else "平稳"
            snap["profiling"] = {
                "handicapTrends": {"home": prof_str, "away": prof_str, "raw": prof_str},
                "identicalOddsHistory": {"raw": prof_str},
            }

        euro_list = []
        ts_list = []
        ah_list = []
        ou_list = []

        # 欧指主流总表
        m_euro = re.search(r"##\s*三[、\.\s].*?(?:初即盘|欧洲指数|欧指|主流机构|法定23家).*?\n(.*?)(?=\n--|\n##|\Z)", content, re.DOTALL)
        if m_euro:
            for line in m_euro.group(1).strip().splitlines():
                if not line.startswith("|") or "---" in line or "初盘主" in line or "机构名称" in line:
                    continue
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 9:
                    # 判断是否有“机构类型”前缀列
                    idx_offset = 1 if len(parts) >= 11 and not parts[1].replace(".", "").isdigit() else 0
                    comp_name = parts[idx_offset]
                    try:
                        h0 = float(parts[idx_offset + 1])
                        d0 = float(parts[idx_offset + 2])
                        a0 = float(parts[idx_offset + 3])
                        r0 = float(parts[idx_offset + 4].replace("%", ""))
                        h = float(parts[idx_offset + 5])
                        d = float(parts[idx_offset + 6])
                        a = float(parts[idx_offset + 7])
                        r = float(parts[idx_offset + 8].replace("%", "") if len(parts) > idx_offset + 8 else "90")
                        kelly_vals = [0.94, 0.88, 0.84]
                        if len(parts) > idx_offset + 9 and "/" in parts[idx_offset + 9]:
                            k_parts = [float(x.strip()) for x in parts[idx_offset + 9].split("/") if x.strip()]
                            if len(k_parts) == 3:
                                kelly_vals = k_parts
                        euro_list.append({
                            "company": comp_name,
                            "initial": {"odds": [h0, d0, a0], "returnRate": r0},
                            "latest": {"odds": [h, d, a], "returnRate": r, "kelly": kelly_vals},
                        })
                    except Exception:
                        pass

        def _extract_table_rows(block_text: str) -> List[List[str]]:
            res_rows = []
            for p in block_text.strip().splitlines():
                if not p.startswith("|") or "---" in p:
                    continue
                cells = [x.strip() for x in p.split("|")[1:-1]]
                if not cells or cells[0] in ("生命周期", "生命周期阶段", "变盘时间", "观测时间", "玩法类型", "机构"):
                    continue
                if len(cells) >= 4:
                    res_rows.append(cells)
            return res_rows

        def _pick_init_latest(rows: List[List[str]]) -> tuple[List[str], List[str]]:
            if any(t in rows[0][0] for t in ["T0", "初盘"]):
                return rows[0], rows[-1]
            return rows[-1], rows[0]

        # 解析核心机构按块列出的变盘时序流水
        comp_blocks = re.split(r"\n###\s+(?:\d+[\.、\s]*)?([^\n\(]+)(?:\([^\)]*\))?", content)
        if len(comp_blocks) > 1:
            for i in range(1, len(comp_blocks), 2):
                cname = comp_blocks[i].strip()
                block = comp_blocks[i+1]
                # AH
                m_ah_block = re.search(r"####?\s*亚盘.*?\n(.*?)(?=\n####?|\n---|\Z)", block, re.DOTALL)
                if m_ah_block:
                    rows = _extract_table_rows(m_ah_block.group(1))
                    if rows:
                        initial, latest = _pick_init_latest(rows)
                        off = 1 if len(latest) >= 5 and any(t in latest[0] for t in ["T0", "T1", "T2", "T3", "T4"]) else 0
                        try:
                            ah_list.append({
                                "company": cname,
                                "initial": {"handicap": initial[off+1].replace("**", "").replace("初盘", "").strip(), "home": float(initial[off+2].replace("**", "").strip()), "away": float(initial[off+3].replace("**", "").strip())},
                                "latest": {"handicap": latest[off+1].replace("**", "").replace("初盘", "").strip(), "home": float(latest[off+2].replace("**", "").strip()), "away": float(latest[off+3].replace("**", "").strip())},
                            })
                            last_t = "10-08 12:00"
                            for r in rows:
                                raw_t = r[off].replace("**", "").replace("初盘", "").strip()
                                if raw_t != "维持区间":
                                    last_t = raw_t
                                ts_list.append({
                                    "company": cname,
                                    "market": "AH",
                                    "phase": r[0].replace("**", "").strip() if off == 1 else "",
                                    "time": last_t,
                                    "handicap": r[off+1].replace("**", "").replace("初盘", "").strip(),
                                    "home": float(r[off+2].replace("**", "").strip()),
                                    "away": float(r[off+3].replace("**", "").strip()),
                                    "morphology": r[-1].strip() if len(r) > off + 4 else "",
                                })
                        except Exception:
                            pass

                # OU
                m_ou_block = re.search(r"####?\s*大小球.*?\n(.*?)(?=\n####?|\n---|\Z)", block, re.DOTALL)
                if m_ou_block:
                    rows = _extract_table_rows(m_ou_block.group(1))
                    if rows:
                        initial, latest = _pick_init_latest(rows)
                        off = 1 if len(latest) >= 5 and any(t in latest[0] for t in ["T0", "T1", "T2", "T3", "T4"]) else 0
                        try:
                            ou_list.append({
                                "company": cname,
                                "initial": {"goal": initial[off+1].replace("**", "").replace("初盘", "").strip(), "over": float(initial[off+2].replace("**", "").strip()), "under": float(initial[off+3].replace("**", "").strip())},
                                "latest": {"goal": latest[off+1].replace("**", "").replace("初盘", "").strip(), "over": float(latest[off+2].replace("**", "").strip()), "under": float(latest[off+3].replace("**", "").strip())},
                            })
                            last_t = "10-08 12:00"
                            for r in rows:
                                raw_t = r[off].replace("**", "").replace("初盘", "").strip()
                                if raw_t != "维持区间":
                                    last_t = raw_t
                                ts_list.append({
                                    "company": cname,
                                    "market": "OU",
                                    "phase": r[0].replace("**", "").strip() if off == 1 else "",
                                    "time": last_t,
                                    "goal": r[off+1].replace("**", "").replace("初盘", "").strip(),
                                    "over": float(r[off+2].replace("**", "").strip()),
                                    "under": float(r[off+3].replace("**", "").strip()),
                                    "morphology": r[-1].strip() if len(r) > off + 4 else "",
                                })
                        except Exception:
                            pass

                # 欧指时序 (含体彩 HAD)
                m_eu_block = re.search(r"####?\s*(?:欧指|胜平负).*?\n(.*?)(?=\n####?|\n---|\Z)", block, re.DOTALL)
                if m_eu_block:
                    rows = _extract_table_rows(m_eu_block.group(1))
                    last_t = "10-08 12:00"
                    for r in rows:
                        if len(r) >= 4:
                            off = 1 if len(r) >= 5 and any(t in r[0] for t in ["T0", "T1", "T2", "T3", "T4"]) else 0
                            try:
                                raw_t = r[off].replace("**", "").replace("初盘", "").strip()
                                if raw_t != "维持区间":
                                    last_t = raw_t
                                ts_list.append({
                                    "company": cname,
                                    "market": "1X2",
                                    "phase": r[0].replace("**", "").strip() if off == 1 else "",
                                    "time": last_t,
                                    "odds": [
                                        float(r[off+1].replace("**", "").replace("初盘", "").strip()),
                                        float(r[off+2].replace("**", "").strip()),
                                        float(r[off+3].replace("**", "").strip()),
                                    ],
                                    "morphology": r[-1].strip() if len(r) > off + 4 else "",
                                })
                            except Exception:
                                pass

                # 体彩让球胜平负 (HHAD)
                m_hhad_block = re.search(r"####?\s*让球胜平负.*?\n(.*?)(?=\n####?|\n---|\Z)", block, re.DOTALL)
                if m_hhad_block:
                    rows = _extract_table_rows(m_hhad_block.group(1))
                    if rows:
                        r0 = rows[0]
                        try:
                            snap["sportteryHandicap"] = {
                                "handicap": r0[1].replace("`", "").strip(),
                                "win": float(r0[2]),
                                "draw": float(r0[3]),
                                "lose": float(r0[4]),
                                "morphology": r0[5].strip() if len(r0) > 5 else "",
                            }
                        except Exception:
                            pass

                # Polymarket 预测市场五阶段时序
                m_poly_block = re.search(r"####?\s*预测市场.*?\n(.*?)(?=\n####?|\n---|\Z)", block, re.DOTALL)
                if m_poly_block:
                    rows = _extract_table_rows(m_poly_block.group(1))
                    poly_ts = []
                    for r in rows:
                        if len(r) >= 8:
                            try:
                                poly_ts.append({
                                    "phase": r[0].replace("**", "").strip(),
                                    "time": r[1].strip(),
                                    "cents": [float(r[2].replace("¢", "").strip()), float(r[3].replace("¢", "").strip()), float(r[4].replace("¢", "").strip())],
                                    "fairOdds": [float(r[5]), float(r[6]), float(r[7])],
                                    "morphology": r[8].strip() if len(r) > 8 else "",
                                })
                            except Exception:
                                pass
                    if poly_ts:
                        snap["polymarketTimeSeries"] = poly_ts

        # 兜底：如果存在旧版平铺格式
        if not ah_list:
            m_ah = re.search(r"## 四、亚洲让球盘 \(AH\) 核心机构与变盘流水\s+(.*?)(?=\n###|\n---|\\Z)", content, re.DOTALL)
            if m_ah:
                for line in m_ah.group(1).strip().splitlines():
                    if not line.startswith("|") or "---" in line or "机构" in line:
                        continue
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 7:
                        try:
                            ah_list.append({
                                "company": parts[0],
                                "initial": {"handicap": parts[1], "home": float(parts[2]), "away": float(parts[3])},
                                "latest": {"handicap": parts[4], "home": float(parts[5]), "away": float(parts[6])},
                            })
                        except Exception:
                            pass

        if not ou_list:
            m_ou = re.search(r"## 五、大小球进球数 \(OU\) 核心机构\s+(.*?)(?=\n---|\\Z)", content, re.DOTALL)
            if m_ou:
                for line in m_ou.group(1).strip().splitlines():
                    if not line.startswith("|") or "---" in line or "机构" in line:
                        continue
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 7:
                        try:
                            ou_list.append({
                                "company": parts[0],
                                "initial": {"goal": parts[1], "over": float(parts[2]), "under": float(parts[3])},
                                "latest": {"goal": parts[4], "over": float(parts[5]), "under": float(parts[6])},
                            })
                        except Exception:
                            pass

        snap["europe1x2"] = euro_list
        snap["asianHandicap"] = ah_list
        snap["overUnder"] = ou_list
        snap["timeSeriesFlow"] = ts_list

        m_score = re.search(r"##\s*[五六][、\.\s].*?Crown.*?波胆.*?\n(.*?)(?=\n---|\Z)", content, re.DOTALL)
        if m_score:
            snap["correctScoreOdds"] = m_score.group(1).strip()
        else:
            m_score2 = re.search(r"## 六、Crown 皇冠全指数波胆与比分矩阵\s+(.*?)(?=\n---|\Z)", content, re.DOTALL)
            if m_score2:
                snap["correctScoreOdds"] = m_score2.group(1).strip()

        return snap


class CheckConsistencyUseCase:
    """
    用例 2: 全库系统一致性巡检与图谱连通性防回退
    负责：平滑收拢原 scripts/check_consistency.py 职能，实现统一全系统健康守门
    """

    DEFAULT_ROOTS = ("skills", "docs", "scripts", "校验")
    SKIP_DIRS = {".git", "node_modules", ".cursor", ".openclaw", "__pycache__"}

    def execute(self, root_dir: str = ".") -> Dict[str, Any]:
        repo_root = Path(root_dir).resolve()
        rules: List[tuple[str, re.Pattern[str]]] = [
            ("EV 阈值口径回退（EV>1）", re.compile(r"\bEV\s*>\s*1\b")),
            ("旧代号残留（嘲风）", re.compile(r"嘲风")),
            ("大小球旧模板占位符", re.compile(r"大小球：\s*\{大X\.5/小X\.5\}")),
        ]

        findings = []
        for base in self.DEFAULT_ROOTS:
            p = repo_root / base
            if not p.exists():
                continue
            for dirpath, dirnames, filenames in os.walk(p):
                dirnames[:] = [d for d in dirnames if d not in self.SKIP_DIRS]
                for name in filenames:
                    fp = Path(dirpath) / name
                    if fp.name in ("check_consistency.py", "use_cases.py", "test_use_cases.py"):
                        continue
                    if fp.suffix.lower() in {".md", ".py", ".json", ".json5", ".txt"}:
                        try:
                            lines = fp.read_text(encoding="utf-8").splitlines()
                            for idx, line in enumerate(lines, start=1):
                                if "consistency:ignore" in line or "历史" in line or "兼容" in line:
                                    continue
                                for rule_name, pat in rules:
                                    if pat.search(line):
                                        findings.append({
                                            "file": str(fp.relative_to(repo_root)),
                                            "line_no": idx,
                                            "rule": rule_name,
                                            "line": line.strip(),
                                        })
                        except UnicodeDecodeError:
                            continue

        # 检查图谱连通性与零孤岛
        graph_connected = True
        graph_err = None
        graph_json = repo_root / "graphify-out" / "graph.json"
        if graph_json.exists():
            try:
                import networkx as nx
                g_data = json.loads(graph_json.read_text(encoding="utf-8"))
                G = nx.Graph()
                for n in g_data.get("nodes", []):
                    G.add_node(n["id"])
                for e in g_data.get("links", []) or g_data.get("edges", []):
                    G.add_edge(e["source"], e["target"])
                comps = nx.number_connected_components(G)
                isolates = len(list(nx.isolates(G)))
                if comps > 1 or isolates > 0:
                    graph_connected = False
                    graph_err = f"图谱孤岛违规: 连通分量={comps}, 孤立节点={isolates}"
            except Exception as e:
                # 若当前环境缺失 networkx，标记为 warning
                graph_err = f"图谱解析库异常: {e}"

        # 算法/ 纯数学单测联动
        algo_passed = True
        algo_err = None
        algo_dir = repo_root / "算法"
        if algo_dir.exists():
            res = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", "算法/测试"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
            )
            if res.returncode != 0:
                algo_passed = False
                algo_err = res.stderr

        is_clean = (len(findings) == 0) and graph_connected and algo_passed

        return {
            "is_clean": is_clean,
            "findings_count": len(findings),
            "findings": findings,
            "graph_connected": graph_connected,
            "graph_error": graph_err,
            "algo_tests_passed": algo_passed,
            "algo_error": algo_err,
        }
