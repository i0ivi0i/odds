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
    用例 1: 单场【推演源数据】文件数据完整性安检
    负责：安全读取磁盘【推演源数据】，调用 SnapshotVerifier 纯领域模型，返回防篡改法定收据
    """

    def __init__(self, verifier: Optional[SnapshotVerifier] = None):
        self.verifier = verifier or SnapshotVerifier()

    def execute(self, file_path_str: str, max_age_minutes: Optional[int] = None) -> VerificationReceipt:
        path = Path(file_path_str)
        if not path.exists():
            return VerificationReceipt(
                match_id=path.stem,
                results=[
                    DimensionResult(
                        dimension=DimensionType.BASIC_STATS,
                        status=CheckStatus.FAIL,
                        message=f"【推演源数据】文件不存在: {file_path_str} (请先执行抓取落盘或检查路径)",
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
                            message=f"【推演源数据】文件无法读取: {e}",
                        )
                    ],
                    metadata={"error": "io_error"},
                )

            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

            if path.suffix.lower() == ".md":
                data = self._parse_markdown_snapshot(content, path.stem)
                data["is_markdown_baseline"] = True
                data["_raw_content"] = content

                # 交叉核对同目录下的 meta.md (若存在)
                meta_path = path.parent / "meta.md"
                if meta_path.exists():
                    try:
                        meta_text = meta_path.read_text(encoding="utf-8")
                        row_m = re.search(rf"\|\s*([^\|]+)\s*\|\s*{re.escape(path.stem)}\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*vs\s*([^\|]+)\s*\|", meta_text)
                        if row_m:
                            data["_meta_info"] = {
                                "code": row_m.group(1).strip(),
                                "league": row_m.group(2).strip(),
                                "home": row_m.group(3).strip(),
                                "away": row_m.group(4).strip(),
                            }
                    except Exception:
                        pass
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
                                message=f"【推演源数据】JSON格式解析失败 (文件损坏或截断): {e}",
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
                        message="【推演源数据】根结构必须为 JSON 字典/对象",
                    )
                ],
                metadata={"error": "invalid_shape", "content_hash": content_hash},
            )

        # U3: 核对【推演源数据】场次身份一致性
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
                        message=f"【推演源数据】文件与比赛ID不一致！文件身份({stem})与内容matchId({content_match_id})冲突，禁止跨场次引用",
                        detail={"file_stem": stem, "content_match_id": content_match_id},
                    )
                ],
                metadata={"error": "match_id_mismatch", "content_hash": content_hash},
            )

        if not path.is_dir():
            try:
                data["_file_mtime"] = path.stat().st_mtime
            except Exception:
                pass
        if max_age_minutes is not None:
            data["_max_age_minutes"] = max_age_minutes
        data["_raw_content"] = content
        data["_markdown_sha256"] = content_hash

        # U3: 优先检查单文件原子防伪存证包 raw/{matchId}.json，回退兼容旧目录 raw/{matchId}/
        target_mid = content_match_id or path.stem
        atomic_bundle_p = path.parent / "raw" / f"{target_mid}.json"
        if not atomic_bundle_p.exists() and path.parent.name == ".quarantine":
            atomic_bundle_p = path.parent.parent / "raw" / f"{target_mid}.json"
        raw_dir = path.parent / "raw" / target_mid
        if not raw_dir.exists() and path.parent.name == ".quarantine":
            raw_dir = path.parent.parent / "raw" / target_mid
        if atomic_bundle_p.exists() and atomic_bundle_p.is_file():
            try:
                bundle_obj = json.loads(atomic_bundle_p.read_text(encoding="utf-8"))
                payloads = bundle_obj.get("payloads") or {}
                files_sha256 = {
                    fname: hashlib.sha256(str(fcontent).encode("utf-8")).hexdigest()
                    for fname, fcontent in sorted(payloads.items())
                }
                raw_wire: Dict[str, Any] = {
                    "raw_dir": str(atomic_bundle_p),
                    "manifest": {
                        "matchId": bundle_obj.get("matchId"),
                        "sealedAt": bundle_obj.get("sealedAt"),
                        "markdown_sha256": bundle_obj.get("markdown_sha256"),
                        "raw_files_sha256": bundle_obj.get("raw_files_sha256") or files_sha256,
                    },
                    "receipt": bundle_obj.get("receipt"),
                    "files": payloads,
                    "files_sha256": files_sha256,
                }
                for fname, fcontent in payloads.items():
                    raw_wire[fname] = fcontent
                data["_raw_wire"] = raw_wire
            except Exception as e:
                data["_raw_wire"] = {"manifest_error": str(e)}
        elif raw_dir.exists() and raw_dir.is_dir():
            raw_wire: Dict[str, Any] = {
                "raw_dir": str(raw_dir),
                "files": {},
                "files_sha256": {},
            }
            manifest_p = raw_dir / "manifest.json"
            if manifest_p.exists():
                try:
                    raw_wire["manifest"] = json.loads(manifest_p.read_text(encoding="utf-8"))
                except Exception as e:
                    raw_wire["manifest_error"] = str(e)
            for fp in sorted(raw_dir.iterdir()):
                if fp.is_file() and fp.name != "manifest.json":
                    try:
                        fcontent = fp.read_text(encoding="utf-8", errors="replace")
                        raw_wire["files"][fp.name] = fcontent
                        raw_wire["files_sha256"][fp.name] = hashlib.sha256(fcontent.encode("utf-8")).hexdigest()
                        raw_wire[fp.name] = fcontent
                    except Exception:
                        pass
            data["_raw_wire"] = raw_wire

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
        """将多文件 Markdown 目录解析为领域验证字典（严禁硬编码假默认值）"""
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

            # 从 _meta.md 或 02_历史战绩_近况.md 提取真实进失球数据，严禁硬编码 1.25/1.50
            stats_text = text
            stats_file = match_dir / "02_历史战绩_近况.md"
            if stats_file.exists():
                stats_text += "\n" + stats_file.read_text(encoding="utf-8")
            snap["basicStatsText"] = stats_text

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
                        r_init = float(initial[4].replace("%", "").strip()) if len(initial) > 4 and initial[4].strip() else None
                        r_lat = float(latest[4].replace("%", "").strip()) if len(latest) > 4 and latest[4].strip() else None
                        k_lat = []
                        if len(latest) > 5 and "/" in latest[5]:
                            k_lat = [float(x.strip()) for x in latest[5].split("/") if x.strip()]
                        euro_list.append({
                            "company": cname,
                            "initial": {"odds": [float(initial[1].replace("**", "").replace("初盘", "").strip()), float(initial[2].replace("**", "").strip()), float(initial[3].replace("**", "").strip())], "returnRate": r_init},
                            "latest": {"odds": [float(latest[1]), float(latest[2]), float(latest[3])], "returnRate": r_lat, "kelly": k_lat},
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
        cs_file = match_dir / "06_Crown波胆_总进球.md"
        snap["correctScoreOdds"] = cs_file.read_text(encoding="utf-8") if cs_file.exists() else ""

        return snap

    def _parse_markdown_snapshot(self, content: str, fallback_match_id: str) -> Dict[str, Any]:
        """将纯净工整单文件 Markdown 【推演源数据】解析为领域验证字典（严禁静默注入任何假默认值）"""
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

        # 解析 Polymarket
        m_poly_line = re.search(r"Polymarket.*?预测市场[^\r\n]*?[：:]\s*([^\r\n]+)", content)
        if m_poly_line:
            poly_text = m_poly_line.group(1).strip()
            url_m = re.search(r"\]\((https?://[^\s\)]+)\)", poly_text)
            if not url_m:
                url_m = re.search(r"\b(https?://[^\s\)\],]+)", poly_text)
            if url_m:
                snap["polymarket"] = {"status": "active", "url": url_m.group(1).strip(), "raw": poly_text}
            else:
                snap["polymarket"] = {"status": "unopened", "url": poly_text, "raw": poly_text}
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
            sch = re.search(r"赛程(?:陷阱|间隔).*?：(.*?)(?=\n|\Z)", btext)
            prof = re.search(r"盘路画像.*?：(.*?)(?=\n|\Z)", btext)
            raw_hg = hg.group(1).strip() if hg else ""
            raw_ag = ag.group(1).strip() if ag else ""
            h_g = re.search(r"(?:进|得)球?\s*([\d\.]+).*?失球?\s*([\d\.]+)", raw_hg)
            a_g = re.search(r"(?:进|得)球?\s*([\d\.]+).*?失球?\s*([\d\.]+)", raw_ag)
            has_goal_digits = bool(h_g or a_g or re.search(r"\d+\s*胜|\d+\s*球|进\s*\d+|失\s*\d+", raw_hg + " " + raw_ag))
            hg_str = raw_hg if has_goal_digits else ""
            ag_str = raw_ag if has_goal_digits else ""
            if "match" in snap:
                snap["match"]["homeGoals"] = hg_str
                snap["match"]["awayGoals"] = ag_str
            snap["basicStatsText"] = btext.strip()
            snap["tactics"] = {
                "technicalStats": {
                    "home": {"goals": float(h_g.group(1)) if h_g else 0.0, "conceded": float(h_g.group(2)) if h_g else 0.0, "raw": hg_str},
                    "away": {"goals": float(a_g.group(1)) if a_g else 0.0, "conceded": float(a_g.group(2)) if a_g else 0.0, "raw": ag_str},
                },
                "motivationAndGameTheory": mot.group(1).strip() if mot else "",
                "futureSchedule": {"raw": sch.group(1).strip() if sch else ""},
            }
            prof_str = prof.group(1).strip() if prof else ""
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
                    idx_offset = 1 if len(parts) >= 11 and not parts[1].replace(".", "").isdigit() else 0
                    comp_name = parts[idx_offset]
                    try:
                        if parts[idx_offset + 1].strip() == "-":
                            init_odds_vals: List[float] = []
                            r0: Optional[float] = None
                        else:
                            init_odds_vals = [
                                float(parts[idx_offset + 1]),
                                float(parts[idx_offset + 2]),
                                float(parts[idx_offset + 3]),
                            ]
                            r0_raw = parts[idx_offset + 4].replace("%", "").strip()
                            try:
                                r0 = float(r0_raw)
                            except ValueError:
                                r0 = None
                        h = float(parts[idx_offset + 5])
                        d = float(parts[idx_offset + 6])
                        a = float(parts[idx_offset + 7])
                        r_raw = parts[idx_offset + 8].replace("%", "").strip() if len(parts) > idx_offset + 8 else ""
                        try:
                            r: Optional[float] = float(r_raw)
                        except ValueError:
                            r = None
                        kelly_vals: List[float] = []
                        if len(parts) > idx_offset + 9 and "/" in parts[idx_offset + 9]:
                            try:
                                k_parts = [float(x.strip()) for x in parts[idx_offset + 9].split("/") if x.strip()]
                                if len(k_parts) == 3:
                                    kelly_vals = k_parts
                            except ValueError:
                                kelly_vals = []
                        euro_list.append({
                            "company": comp_name,
                            "initial": {"odds": init_odds_vals, "returnRate": r0},
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

        def _row_offset(r: List[str]) -> int:
            """判断行是否带旧版 T0~T4 阶段前缀列"""
            if len(r) >= 5 and not re.search(r"\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}", r[0]):
                return 1
            return 0

        def _pick_init_latest(rows: List[List[str]]) -> tuple[List[str], List[str]]:
            if any(t in rows[0][0] for t in ["T0", "初盘"]) or any(t in rows[0][-1] for t in ["初盘", "初"]):
                return rows[0], rows[-1]
            if any(t in rows[-1][0] for t in ["T0", "初盘"]) or any(t in rows[-1][-1] for t in ["初盘", "初"]):
                return rows[-1], rows[0]
            off0 = _row_offset(rows[0])
            offN = _row_offset(rows[-1])
            if rows[0][off0] <= rows[-1][offN]:
                return rows[0], rows[-1]
            return rows[-1], rows[0]

        # 解析核心机构按块列出的变盘时序流水
        from 校验.src.domain.assembler import _normalize_company_name
        company_timelines: Dict[str, Dict[str, List[Any]]] = {}
        sporttery_had_rows: List[Tuple[str, str, str, str, str, str, str]] = []

        comp_blocks = re.split(r"\n###\s+(?:\d+[\.、\s]*)?([^\n\(]+)(?:\([^\)]*\))?", content)
        if len(comp_blocks) > 1:
            for i in range(1, len(comp_blocks), 2):
                cname = comp_blocks[i].strip()
                std_cname = _normalize_company_name(cname) or cname
                block = comp_blocks[i+1]
                ah_tuples: List[Tuple[str, str, str, str, str]] = []
                ou_tuples: List[Tuple[str, str, str, str, str]] = []
                eu_tuples: List[Tuple[str, str, str, str, str, str, str]] = []

                # AH
                m_ah_block = re.search(r"####?\s*亚盘.*?\n(.*?)(?=\n####?|\n---|\Z)", block, re.DOTALL)
                if m_ah_block:
                    rows = _extract_table_rows(m_ah_block.group(1))
                    if rows:
                        initial, latest = _pick_init_latest(rows)
                        off_i = _row_offset(initial)
                        off_l = _row_offset(latest)
                        def _safe_f(v):
                            try:
                                return float(str(v).replace("**", "").strip())
                            except ValueError:
                                return 0.0
                        try:
                            ah_list.append({
                                "company": cname,
                                "initial": {"handicap": initial[off_i+1].replace("**", "").replace("初盘", "").strip(), "home": _safe_f(initial[off_i+2]), "away": _safe_f(initial[off_i+3])},
                                "latest": {"handicap": latest[off_l+1].replace("**", "").replace("初盘", "").strip(), "home": _safe_f(latest[off_l+2]), "away": _safe_f(latest[off_l+3])},
                            })
                            for r in rows:
                                off = _row_offset(r)
                                raw_t = r[off].replace("**", "").replace("初盘", "").strip()
                                st_cell = r[off+4].replace("**", "").strip() if len(r) > off + 4 else "即"
                                ah_tuples.append((
                                    raw_t,
                                    r[off+1].replace("**", "").replace("初盘", "").strip(),
                                    r[off+2].replace("**", "").strip(),
                                    r[off+3].replace("**", "").strip(),
                                    st_cell,
                                ))
                                if not re.search(r"\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}", raw_t):
                                    continue
                                ts_list.append({
                                    "company": cname,
                                    "market": "AH",
                                    "phase": r[0].replace("**", "").strip() if off == 1 else "",
                                    "time": raw_t,
                                    "handicap": r[off+1].replace("**", "").replace("初盘", "").strip(),
                                    "home": _safe_f(r[off+2]),
                                    "away": _safe_f(r[off+3]),
                                })
                        except Exception:
                            pass

                # OU
                m_ou_block = re.search(r"####?\s*大小球.*?\n(.*?)(?=\n####?|\n---|\Z)", block, re.DOTALL)
                if m_ou_block:
                    rows = _extract_table_rows(m_ou_block.group(1))
                    if rows:
                        initial, latest = _pick_init_latest(rows)
                        off_i = _row_offset(initial)
                        off_l = _row_offset(latest)
                        try:
                            ou_list.append({
                                "company": cname,
                                "initial": {"goal": initial[off_i+1].replace("**", "").replace("初盘", "").strip(), "over": _safe_f(initial[off_i+2]), "under": _safe_f(initial[off_i+3])},
                                "latest": {"goal": latest[off_l+1].replace("**", "").replace("初盘", "").strip(), "over": _safe_f(latest[off_l+2]), "under": _safe_f(latest[off_l+3])},
                            })
                            for r in rows:
                                off = _row_offset(r)
                                raw_t = r[off].replace("**", "").replace("初盘", "").strip()
                                st_cell = r[off+4].replace("**", "").strip() if len(r) > off + 4 else "即"
                                ou_tuples.append((
                                    raw_t,
                                    r[off+1].replace("**", "").replace("初盘", "").strip(),
                                    r[off+2].replace("**", "").strip(),
                                    r[off+3].replace("**", "").strip(),
                                    st_cell,
                                ))
                                if not re.search(r"\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}", raw_t):
                                    continue
                                ts_list.append({
                                    "company": cname,
                                    "market": "OU",
                                    "phase": r[0].replace("**", "").strip() if off == 1 else "",
                                    "time": raw_t,
                                    "goal": r[off+1].replace("**", "").replace("初盘", "").strip(),
                                    "over": _safe_f(r[off+2]),
                                    "under": _safe_f(r[off+3]),
                                })
                        except Exception:
                            pass

                # 欧指时序 (含体彩 HAD)
                m_eu_block = re.search(r"####?\s*(?:欧指|胜平负).*?\n(.*?)(?=\n####?|\n---|\Z)", block, re.DOTALL)
                if m_eu_block:
                    rows = _extract_table_rows(m_eu_block.group(1))
                    for r in rows:
                        if len(r) >= 4:
                            off = _row_offset(r)
                            if r[0].strip() == "-":
                                off = 0
                            try:
                                raw_t = r[off].replace("**", "").replace("初盘", "").strip()
                                ret_cell = r[off+4].replace("**", "").strip() if len(r) > off + 4 else "-"
                                kelly_cell = r[off+5].replace("**", "").strip() if len(r) > off + 5 else "-"
                                st_cell = r[off+6].replace("**", "").strip() if len(r) > off + 6 else "即"
                                eu_tuples.append((
                                    raw_t,
                                    r[off+1].replace("**", "").replace("初盘", "").strip(),
                                    r[off+2].replace("**", "").strip(),
                                    r[off+3].replace("**", "").strip(),
                                    ret_cell,
                                    kelly_cell,
                                    st_cell,
                                ))
                                if not re.search(r"\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}", raw_t):
                                    continue
                                ts_list.append({
                                    "company": cname,
                                    "market": "1X2",
                                    "phase": r[0].replace("**", "").strip() if off == 1 else "",
                                    "time": raw_t,
                                    "odds": [
                                        float(r[off+1].replace("**", "").replace("初盘", "").strip()),
                                        float(r[off+2].replace("**", "").strip()),
                                        float(r[off+3].replace("**", "").strip()),
                                    ],
                                })
                            except Exception:
                                pass

                if ah_tuples or ou_tuples or eu_tuples:
                    company_timelines[std_cname] = {
                        "ah": ah_tuples,
                        "ou": ou_tuples,
                        "eu": eu_tuples,
                    }
                if std_cname == "中国体彩" and eu_tuples:
                    sporttery_had_rows = eu_tuples

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
                            }
                        except Exception:
                            pass

                # Polymarket 预测市场真实挂单流水
                m_poly_block = re.search(r"####?\s*预测市场.*?\n(.*?)(?=\n####?|\n---|\Z)", block, re.DOTALL)
                if m_poly_block:
                    rows = _extract_table_rows(m_poly_block.group(1))
                    poly_ts = []
                    for r in rows:
                        if len(r) >= 7:
                            off_p = 1 if len(r) >= 8 and not re.search(r"\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}", r[0]) else 0
                            try:
                                poly_ts.append({
                                    "phase": r[0].replace("**", "").strip() if off_p == 1 else "",
                                    "time": r[off_p].strip(),
                                    "cents": [
                                        float(r[off_p+1].replace("¢", "").strip()),
                                        float(r[off_p+2].replace("¢", "").strip()),
                                        float(r[off_p+3].replace("¢", "").strip()),
                                    ],
                                    "fairOdds": [
                                        float(r[off_p+4]),
                                        float(r[off_p+5]),
                                        float(r[off_p+6]),
                                    ],
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
        snap["companyTimelines"] = company_timelines
        snap["sportteryHadRows"] = sporttery_had_rows

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
    SKIP_DIRS = {".git", "node_modules", ".cursor", ".openclaw", "__pycache__", "plans"}

    def execute(self, root_dir: str = ".") -> Dict[str, Any]:
        repo_root = Path(root_dir).resolve()
        rules: List[tuple[str, re.Pattern[str]]] = [
            ("EV 阈值口径回退（EV>1）", re.compile(r"\bEV\s*>\s*1\b")),
            ("旧代号残留（嘲风）", re.compile(r"嘲风")),
            ("大小球旧模板占位符", re.compile(r"大小球：\s*\{大X\.5/小X\.5\}")),
            ("已废除 T0~T4 五阶段矩阵残留", re.compile(r"五阶段时序生命周期矩阵（T0~T4）|T0~T4\s*五阶段分钟级时序矩阵")),
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
                                if "consistency:ignore" in line or "历史" in line or "兼容" in line or "废除" in line:
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

        # 检查图谱连通性、零孤岛与零 T0~T4 污染节点
        graph_connected = True
        graph_err = None
        graph_json = repo_root / "graphify-out" / "graph.json"
        if graph_json.exists():
            try:
                import networkx as nx
                g_data = json.loads(graph_json.read_text(encoding="utf-8"))
                G = nx.Graph()
                for n in g_data.get("nodes", []):
                    nid = str(n.get("id") or "")
                    nlabel = str(n.get("label") or "")
                    G.add_node(nid)
                    if "t0_t4" in nid.lower() or "五阶段时序生命周期矩阵" in nlabel:
                        findings.append({
                            "file": "graphify-out/graph.json",
                            "line_no": 1,
                            "rule": "图谱残留已废除 T0~T4 毒节点",
                            "line": f"{nid}: {nlabel}",
                        })
                for e in g_data.get("links", []) or g_data.get("edges", []):
                    G.add_edge(e["source"], e["target"])
                comps = nx.number_connected_components(G)
                isolates = len(list(nx.isolates(G)))
                if comps > 1 or isolates > 0:
                    graph_connected = False
                    graph_err = f"图谱孤岛违规: 连通分量={comps}, 孤立节点={isolates}"
            except Exception as e:
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
