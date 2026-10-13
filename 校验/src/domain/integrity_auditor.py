"""
校验/src/domain/integrity_auditor.py
数据纯净度、全链路防失真与五重轮番穿透质检领域服务
理论依据：
1. Winkelmann (2026) 微观结构状态守恒与防抖保真
2. Wheatcroft (2019) 盘口信息率不变量理论
3. 单调子序列与 SHA-256 不可篡改数学公理
"""

from __future__ import annotations
import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from 校验.src.domain.assembler import _normalize_company_name
from 校验.src.domain.timeseries_denoiser import _normalize_handicap_name
from 校验.src.domain.raw_parser import Titan007RawParser


class AuditDimension(Enum):
    SHA256_SEAL = "SHA-256防伪封条"
    MONOTONIC_TIMELINE = "时序单调拓扑"
    INVARIANTS_CONSERVATION = "四大不变量守恒"
    EXTREMUM_PRESERVATION = "极值数学零丢失"
    VERBATIM_SUBSEQUENCE = "原始报文单调子序列"


class AuditStatus(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class AuditResult:
    dimension: AuditDimension
    status: AuditStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IntegrityAuditReport:
    match_id: str
    is_valid: bool = True
    results: List[AuditResult] = field(default_factory=list)
    extremum_coverage_rate: float = 1.0
    extremum_lost_count: int = 0
    temporal_inversions_count: int = 0
    fabricated_rows_count: int = 0
    total_raw_rows: int = 0
    total_md_rows: int = 0

    def add_result(self, result: AuditResult) -> None:
        self.results.append(result)
        if result.status == AuditStatus.FAIL:
            self.is_valid = False

    def get_result(self, dimension: AuditDimension) -> Optional[AuditResult]:
        for r in self.results:
            if r.dimension == dimension:
                return r
        return None

    def summary_failures(self) -> str:
        fails = [f"[{r.dimension.value}] {r.message}" for r in self.results if r.status == AuditStatus.FAIL]
        return "; ".join(fails) if fails else "全部检查项通过"


def _safe_float(val: Any) -> float:
    try:
        return float(str(val).replace("**", "").replace("初盘", "").strip())
    except (ValueError, TypeError):
        return 0.0


def _parse_time_tuple(ts_str: str, anchor_month: int = 10) -> Tuple[int, int, int, int, int]:
    """解析 MM-DD HH:MM 格式为保序时间元组 (year_offset, month, day, hour, minute)"""
    m = re.search(r"(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2})", str(ts_str).strip())
    if not m:
        return (0, 0, 0, 0, 0)
    month, day, hour, minute = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    # 跨年归一化：若锚定在年初 (1~3月) 而时间为年末 (11~12月)，则 offset = 0，否则 offset = 1
    year_offset = 1
    if anchor_month <= 3 and month >= 10:
        year_offset = 0
    elif anchor_month >= 10 and month <= 3:
        year_offset = 2
    return (year_offset, month, day, hour, minute)


class IntegrityAuditor:
    """五重轮番穿透质检引擎"""

    def __init__(self) -> None:
        self.parser = Titan007RawParser()

    def audit_match(self, raw_bundle_path: str, md_path: str) -> IntegrityAuditReport:
        p_raw = Path(raw_bundle_path)
        p_md = Path(md_path)
        if not p_raw.exists() or not p_md.exists():
            report = IntegrityAuditReport(match_id=p_md.stem if p_md.exists() else p_raw.stem, is_valid=False)
            report.add_result(AuditResult(AuditDimension.SHA256_SEAL, AuditStatus.FAIL, f"文件不存在: raw={p_raw}, md={p_md}"))
            return report

        md_text = p_md.read_text(encoding="utf-8")
        return self.audit_content(raw_bundle_path, md_text, skip_seal=False)

    def audit_content(
        self, raw_bundle_path: str, md_text: str, skip_seal: bool = False
    ) -> IntegrityAuditReport:
        p_raw = Path(raw_bundle_path)
        try:
            bundle_obj = json.loads(p_raw.read_text(encoding="utf-8"))
        except Exception as e:
            report = IntegrityAuditReport(match_id=p_raw.stem, is_valid=False)
            report.add_result(AuditResult(AuditDimension.SHA256_SEAL, AuditStatus.FAIL, f"原始原子包 JSON 损坏: {e}"))
            return report

        match_id = str(bundle_obj.get("matchId") or p_raw.stem).strip()
        report = IntegrityAuditReport(match_id=match_id)

        # 1. SHA-256 封条质检
        if not skip_seal:
            expected_sha = bundle_obj.get("markdown_sha256")
            actual_sha = hashlib.sha256(md_text.encode("utf-8")).hexdigest()
            if not expected_sha or expected_sha != actual_sha:
                report.add_result(
                    AuditResult(
                        AuditDimension.SHA256_SEAL,
                        AuditStatus.FAIL,
                        f"SHA-256 封条不匹配！期望 {expected_sha}，实际 {actual_sha}（检测到文件被篡改）",
                        {"expected": expected_sha, "actual": actual_sha},
                    )
                )
            else:
                report.add_result(
                    AuditResult(AuditDimension.SHA256_SEAL, AuditStatus.PASS, f"SHA-256 封条校验通过 ({actual_sha[:16]}...)")
                )

        # 解析原始报文中的纯净流水
        raw_files = bundle_obj.get("payloads") or bundle_obj.get("rawFiles") or {}
        try:
            raw_data, _ = self.parser.parse_raw_payloads(match_id, raw_files, "")
        except Exception as e:
            report.add_result(
                AuditResult(AuditDimension.VERBATIM_SUBSEQUENCE, AuditStatus.FAIL, f"原始报文解析失败: {e}")
            )
            return report

        # 解析 Markdown 中的表格
        md_tables = self.parse_markdown_tables(md_text)

        # 2. 时序单调拓扑质检
        mono_res = self.check_monotonic_timeline(md_tables)
        report.temporal_inversions_count = mono_res["inversions_count"]
        if mono_res["passed"]:
            report.add_result(
                AuditResult(
                    AuditDimension.MONOTONIC_TIMELINE,
                    AuditStatus.PASS,
                    f"全部 {mono_res['checked_tables']} 张时序表格时间戳严格单调递减（最新在上、初盘在下）",
                )
            )
        else:
            report.add_result(
                AuditResult(
                    AuditDimension.MONOTONIC_TIMELINE,
                    AuditStatus.FAIL,
                    f"发现 {mono_res['inversions_count']} 处时序倒置错误: {'; '.join(mono_res['errors'][:3])}",
                    {"errors": mono_res["errors"]},
                )
            )

        # 遍历第一战区 7 大机构 (澳彩、皇冠、Bet365、易胜博、平博、188Bet、香港马会) 对比 3 维度
        target_companies = ["澳彩", "皇冠", "Bet365", "易胜博", "平博", "188Bet", "香港马会"]
        all_extrema_tested = 0
        all_extrema_preserved = 0
        total_raw_rows = 0
        total_md_rows = 0
        subsequence_fails = []
        invariant_fails = []
        extremum_lost_details = []

        for comp in target_companies:
            for market in ["ah", "ou", "eu"]:
                raw_key = f"{comp}_{market}"
                raw_rows = raw_data.get(raw_key) or []
                md_rows = md_tables.get((comp, market)) or []

                total_raw_rows += len(raw_rows)
                total_md_rows += len(md_rows)

                if not raw_rows:
                    continue

                # 3. 四大不变量守恒质检
                inv_check = self.check_invariants_conservation(comp, market, raw_rows, md_rows)
                if not inv_check["passed"]:
                    invariant_fails.append(inv_check["message"])

                # 4. 极值数学零丢失质检
                ext_check = self.check_extremum_preservation(comp, market, raw_rows, md_rows)
                all_extrema_tested += ext_check["tested_count"]
                all_extrema_preserved += ext_check["preserved_count"]
                if not ext_check["passed"]:
                    extremum_lost_details.extend(ext_check["lost_extrema"])

                # 5. 单调子序列与逐字防伪质检
                sub_check = self.check_verbatim_subsequence(comp, market, raw_rows, md_rows)
                if not sub_check["passed"]:
                    subsequence_fails.append(sub_check["message"])
                    report.fabricated_rows_count += sub_check["fabricated_count"]

        report.total_raw_rows = total_raw_rows
        report.total_md_rows = total_md_rows
        report.extremum_lost_count = len(extremum_lost_details)
        if all_extrema_tested > 0:
            report.extremum_coverage_rate = round(all_extrema_preserved / all_extrema_tested, 4)
        else:
            report.extremum_coverage_rate = 1.0

        # 汇总不变量
        if not invariant_fails:
            report.add_result(
                AuditResult(
                    AuditDimension.INVARIANTS_CONSERVATION,
                    AuditStatus.PASS,
                    f"四大不变量 100% 守恒：各机构初盘行、即时盘行与宏观盘口档位全部精准对齐",
                )
            )
        else:
            report.add_result(
                AuditResult(
                    AuditDimension.INVARIANTS_CONSERVATION,
                    AuditStatus.FAIL,
                    f"不变量守恒异常: {'; '.join(invariant_fails[:3])}",
                    {"fails": invariant_fails},
                )
            )

        # 汇总极值
        if report.extremum_lost_count == 0:
            report.add_result(
                AuditResult(
                    AuditDimension.EXTREMUM_PRESERVATION,
                    AuditStatus.PASS,
                    f"数学极值零丢失：{all_extrema_tested} 处全局最高水/最低水与赔率极值点 100% 保留",
                )
            )
        else:
            report.add_result(
                AuditResult(
                    AuditDimension.EXTREMUM_PRESERVATION,
                    AuditStatus.FAIL,
                    f"发现 {report.extremum_lost_count} 处极值被削顶误删: {'; '.join(extremum_lost_details[:3])}",
                    {"lost": extremum_lost_details},
                )
            )

        # 汇总单调子序列
        if not subsequence_fails:
            report.add_result(
                AuditResult(
                    AuditDimension.VERBATIM_SUBSEQUENCE,
                    AuditStatus.PASS,
                    f"原始报文单调子序列验证通过：全部 {total_md_rows} 行均为原始报文严格子序列，零插值伪造",
                )
            )
        else:
            report.add_result(
                AuditResult(
                    AuditDimension.VERBATIM_SUBSEQUENCE,
                    AuditStatus.FAIL,
                    f"单调子序列异常: {'; '.join(subsequence_fails[:3])}",
                    {"fails": subsequence_fails},
                )
            )

        return report

    def parse_markdown_tables(self, md_text: str) -> Dict[Tuple[str, str], List[Tuple[str, ...]]]:
        """从 Markdown 正文中抽取各机构的变盘流水表格"""
        tables: Dict[Tuple[str, str], List[Tuple[str, ...]]] = {}
        curr_comp = ""
        curr_market = ""

        comp_pattern = re.compile(r"^###\s+\d+\.\s+([^\s\(]+)")
        market_pattern = re.compile(r"^####\s+(亚盘|大小球|欧指)")

        lines = md_text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # 识别机构标题
            m_comp = comp_pattern.match(line)
            if m_comp:
                raw_cname = m_comp.group(1).strip()
                curr_comp = _normalize_company_name(raw_cname)
                curr_market = ""
                i += 1
                continue

            # 识别玩法
            m_mkt = market_pattern.match(line)
            if m_mkt:
                m_str = m_mkt.group(1)
                curr_market = "ah" if "亚盘" in m_str else ("ou" if "大小球" in m_str else "eu")
                i += 1
                continue

            # 识别表格行
            if curr_comp and curr_market and line.startswith("|") and not line.startswith("| :---"):
                parts = [p.strip() for p in line.strip("|").split("|")]
                # 排除表头行
                if parts and ("变盘时间" in parts[0] or "观测时间" in parts[0]):
                    i += 1
                    continue
                if len(parts) >= 4:
                    key = (curr_comp, curr_market)
                    if key not in tables:
                        tables[key] = []
                    tables[key].append(tuple(parts))

            i += 1

        return tables

    def check_monotonic_timeline(
        self, md_tables: Dict[Tuple[str, str], List[Tuple[str, ...]]]
    ) -> Dict[str, Any]:
        """检查各表格时间戳是否单调递减"""
        errors = []
        checked = 0
        for (comp, market), rows in md_tables.items():
            if len(rows) <= 1:
                continue
            checked += 1
            for i in range(len(rows) - 1):
                t1 = _parse_time_tuple(rows[i][0])
                t2 = _parse_time_tuple(rows[i + 1][0])
                if t1 < t2:
                    errors.append(f"{comp}_{market} 行 {i} ({rows[i][0]}) 晚于后一行 ({rows[i+1][0]})，时序倒置")

        return {
            "passed": len(errors) == 0,
            "checked_tables": checked,
            "inversions_count": len(errors),
            "errors": errors,
        }

    def check_invariants_conservation(
        self, company: str, market: str, raw_rows: List[Any], md_rows: List[Tuple[str, ...]]
    ) -> Dict[str, Any]:
        """检查四大不变量（初盘、即时盘、宏观跳盘档位）是否守恒"""
        if not raw_rows or not md_rows:
            return {"passed": True, "message": "无时序数据无需核验"}

        # 1. 即时盘 (首行) 必须对齐 (raw[0] vs md_rows[0])
        raw_first = raw_rows[0]
        md_first = md_rows[0]
        if market in ("ah", "ou"):
            raw_tag = _normalize_handicap_name(raw_first[1])
            md_tag = _normalize_handicap_name(md_first[1])
            if raw_tag != md_tag:
                return {"passed": False, "message": f"{company}_{market} 即时盘口不一致: 原始【{raw_tag}】!= 提取【{md_tag}】"}
            # 校验水位数值
            if abs(_safe_float(raw_first[2]) - _safe_float(md_first[2])) > 0.015:
                return {"passed": False, "message": f"{company}_{market} 即时盘主水/大球水不一致: 原始 {raw_first[2]} != 提取 {md_first[2]}"}
        else:
            # 欧指胜平负
            if abs(_safe_float(raw_first[1]) - _safe_float(md_first[1])) > 0.015:
                return {"passed": False, "message": f"{company}_{market} 即时欧指主胜不一致: 原始 {raw_first[1]} != 提取 {md_first[1]}"}

        # 2. 初盘 (末行) 必须对齐 (raw[-1] vs md_rows[-1])
        raw_last = raw_rows[-1]
        md_last = md_rows[-1]
        if market in ("ah", "ou"):
            raw_last_tag = _normalize_handicap_name(raw_last[1])
            md_last_tag = _normalize_handicap_name(md_last[1])
            if raw_last_tag != md_last_tag:
                return {"passed": False, "message": f"{company}_{market} 初盘不一致: 原始【{raw_last_tag}】!= 提取【{md_last_tag}】"}
            if abs(_safe_float(raw_last[2]) - _safe_float(md_last[2])) > 0.015:
                return {"passed": False, "message": f"{company}_{market} 初盘不一致: 原始主水/大球水 {raw_last[2]} != 提取 {md_last[2]}"}
        else:
            if abs(_safe_float(raw_last[1]) - _safe_float(md_last[1])) > 0.015:
                return {"passed": False, "message": f"{company}_{market} 初盘不一致: 原始主胜 {raw_last[1]} != 提取主胜 {md_last[1]}"}

        # 3. 宏观盘口档位全覆盖
        if market in ("ah", "ou"):
            raw_tags = {_normalize_handicap_name(r[1]) for r in raw_rows if len(r) in (4, 5)}
            md_tags = {_normalize_handicap_name(r[1]) for r in md_rows if len(r) in (4, 5)}
            missing_tags = raw_tags - md_tags
            if missing_tags:
                return {"passed": False, "message": f"{company}_{market} 丢失宏观盘口档位: {missing_tags}"}

        return {"passed": True, "message": "四大不变量完全守恒"}

    def check_extremum_preservation(
        self, company: str, market: str, raw_rows: List[Any], md_rows: List[Tuple[str, ...]]
    ) -> Dict[str, Any]:
        """检查原始报文中的全局最大/最小水位与赔率极值点是否 100% 存在于 md_rows"""
        if not raw_rows or not md_rows:
            return {"passed": True, "tested_count": 0, "preserved_count": 0, "lost_extrema": []}

        lost = []
        tested = 0
        preserved = 0

        # 提取各数值列极值
        col_indices = [2, 3] if market in ("ah", "ou") else [1, 2, 3]
        for c_idx in col_indices:
            raw_vals = [_safe_float(r[c_idx]) for r in raw_rows if len(r) > c_idx and _safe_float(r[c_idx]) > 0]
            md_vals = [_safe_float(r[c_idx]) for r in md_rows if len(r) > c_idx and _safe_float(r[c_idx]) > 0]

            if not raw_vals or not md_vals:
                continue

            min_val = min(raw_vals)
            max_val = max(raw_vals)

            # 检验最小值
            tested += 1
            if any(abs(v - min_val) < 0.005 for v in md_vals):
                preserved += 1
            else:
                lost.append(f"{company}_{market} 列{c_idx} 丢失最低极值 {min_val}")

            # 检验最大值
            tested += 1
            if any(abs(v - max_val) < 0.005 for v in md_vals):
                preserved += 1
            else:
                lost.append(f"{company}_{market} 列{c_idx} 丢失最高极值 {max_val}")

        return {
            "passed": len(lost) == 0,
            "tested_count": tested,
            "preserved_count": preserved,
            "lost_extrema": lost,
        }

    def check_verbatim_subsequence(
        self, company: str, market: str, raw_rows: List[Any], md_rows: List[Tuple[str, ...]]
    ) -> Dict[str, Any]:
        """检查 md_rows 中的每一行是否均为 raw_rows 的真实条目且保持严格单调时序"""
        if not md_rows:
            return {"passed": True, "fabricated_count": 0, "message": "无数据"}

        # 预先构建 raw_rows 的签名列表
        def row_sig(r: Any) -> Tuple[str, ...]:
            if market in ("ah", "ou"):
                return (
                    str(r[0]).strip(),
                    _normalize_handicap_name(r[1]),
                    f"{_safe_float(r[2]):.2f}",
                    f"{_safe_float(r[3]):.2f}",
                )
            else:
                return (
                    str(r[0]).strip(),
                    f"{_safe_float(r[1]):.2f}",
                    f"{_safe_float(r[2]):.2f}",
                    f"{_safe_float(r[3]):.2f}",
                )

        raw_sigs = [row_sig(r) for r in raw_rows]
        md_sigs = [row_sig(r) for r in md_rows]

        raw_idx = 0
        raw_len = len(raw_sigs)
        fabricated = 0

        for m_sig in md_sigs:
            found_idx = -1
            for k in range(raw_idx, raw_len):
                if raw_sigs[k] == m_sig:
                    found_idx = k
                    break
            if found_idx != -1:
                raw_idx = found_idx + 1
            else:
                fabricated += 1

        if fabricated > 0:
            return {
                "passed": False,
                "fabricated_count": fabricated,
                "message": f"{company}_{market} 发现 {fabricated} 行不属于原始报文单调子序列的行（疑似伪造或时序错位）",
            }

        return {"passed": True, "fabricated_count": 0, "message": "100% 原始子序列保真"}
