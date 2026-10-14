"""
校验/src/domain/verifier.py
【推演源数据】完整性纯领域检验引擎 (零外部依赖，纯 Python 原生规则判定)

【架构铁律与只读契约】
1. 本模块为绝对只读检验员 (Read-Only Verifier)，严禁在此类中添加任何写文件、改文件、创建文件逻辑！
2. 任何比赛预测、推演算法、让球定性严禁在此编写，本模块仅负责数据真实性、完整性与时序合法性质检。
3. 一旦发现数据缺失、非法时间戳 (如分钟>59) 或时序造假，直接返回 FAIL 触发物理熔断。
"""

from __future__ import annotations
from datetime import datetime, timedelta
import json
import re
import time
from typing import Any, Dict, List, Optional

from 校验.src.domain.model import (
    CheckStatus,
    DimensionType,
    DimensionResult,
    VerificationReceipt,
)
from 校验.src.domain.profiling_parser import ProfilingParser
from 校验.src.domain.correct_score_parser import CorrectScoreParser
from 校验.src.domain.tactics_parser import TacticsParser


def _is_valid_rate(val: Any) -> bool:
    """校验返还率/赔率是否为有效非空正数值"""
    if val is None or val is False or val == "":
        return False
    if isinstance(val, (int, float)):
        return val > 0
    if isinstance(val, str):
        try:
            return float(val.rstrip("%").strip()) > 0
        except ValueError:
            return False
    return False


def _is_valid_kelly(val: Any) -> bool:
    """校验凯利指数是否为有效非空数值或数值列表"""
    if val is None or val is False or val == "":
        return False
    if isinstance(val, (list, tuple)):
        return len(val) >= 3 and any(_is_valid_rate(x) for x in val)
    return _is_valid_rate(val)


def convert_a11y_table_to_tsv(text: str) -> str:
    """若文本包含 LayoutTableRow / LayoutTableCell 无障碍树表格，转换为制表符 TSV 文本"""
    if not text or "LayoutTableCell" not in text:
        return text
    rows = []
    current_cells = []
    for line in text.splitlines():
        line = line.strip()
        if "LayoutTableRow" in line and not "LayoutTableCell" in line:
            if current_cells:
                rows.append("\t".join(current_cells))
                current_cells = []
        m = re.search(r'LayoutTableCell\s+"([^"]*)"', line)
        if m:
            current_cells.append(m.group(1))
    if current_cells:
        rows.append("\t".join(current_cells))
    return "\n".join(rows)


def clean_a11y_noise(text: Optional[str]) -> str:
    """清洗从 Chromium AXTree / BrowserOS 页面无障碍文本中残留的标记杂质"""
    if not text or not isinstance(text, str):
        return ""
    # 优先转换可能存在的 LayoutTable 无障碍树表格
    text = convert_a11y_table_to_tsv(text)
    # 替换 - cell "xxx" [ref=yyy] 或 - link "xxx" [ref=yyy] 等标记为纯文本 xxx
    cleaned = re.sub(r'-\s*(?:cell|row|table|heading|link|listitem|image)\s+"([^"]*)"\s*\[ref=[^\]]+\]', r'\1', text)
    # 替换剩余的独立 [ref=xxx] 标签
    cleaned = re.sub(r'\[ref=[^\]]+\]', '', cleaned)
    # 替换 - listitem [level=\d+]
    cleaned = re.sub(r'-\s*listitem\s*\[level=\d+\]', '', cleaned)
    # 替换 - list
    cleaned = re.sub(r'-\s*list\b', '', cleaned)
    # 替换残留的 [cursor=pointer] 等属性
    cleaned = re.sub(r'\[cursor=[^\]]+\]', '', cleaned)
    return cleaned.strip()


def get_match_property(snapshot: Dict[str, Any], key: str, default: Any = None) -> Any:
    """平铺标准访问器：优先读取根层级，其次读取 d["match"] 嵌套层级"""
    if not snapshot or not isinstance(snapshot, dict):
        return default
    if key in snapshot and snapshot[key] is not None:
        return snapshot[key]
    match_dict = snapshot.get("match")
    if isinstance(match_dict, dict) and key in match_dict and match_dict[key] is not None:
        return match_dict[key]
    return default


class SnapshotVerifier:
    """
    【推演源数据】完整性领域聚合根
    负责对 6 大黄金维度 + 1 阵容容错维度进行纯规则判定
    """

    def verify(self, snapshot: Dict[str, Any]) -> VerificationReceipt:
        match_id = str(get_match_property(snapshot, "matchId") or snapshot.get("id") or "unknown")

        # 0. 自动清洗可能残余的 AXTree 标记
        for field in ("european1x2Text", "asianOddsText", "overUnderOddsText", "basicStatsText", "lineupData", "correctScoreOdds"):
            if field in snapshot and isinstance(snapshot[field], str):
                snapshot[field] = clean_a11y_noise(snapshot[field])

        # 0.1 结构化增强操盘画像
        if "profiling" in snapshot and isinstance(snapshot["profiling"], dict):
            ProfilingParser().enrich_profiling(snapshot["profiling"])

        # 0.2 结构化增强波胆赔率与半全场
        if "correctScoreOdds" in snapshot and snapshot["correctScoreOdds"]:
            CorrectScoreParser().enrich_snapshot(snapshot)

        # 0.3 结构化增强战术技统与攻防压制力
        if "tactics" in snapshot and isinstance(snapshot["tactics"], dict):
            TacticsParser().enrich_tactics(snapshot["tactics"])

        results: List[DimensionResult] = []

        # 1. 基础战绩与攻防数据
        results.append(self._check_basic_stats(snapshot))

        # 2. 欧洲指数 (1X2)
        results.append(self._check_europe_1x2(snapshot))

        # 3. 亚洲让球盘 (AH)
        results.append(self._check_asian_handicap(snapshot))

        # 4. 大小球进球数 (OU)
        results.append(self._check_over_under(snapshot))

        # 5. 分钟级变盘流水时序 (>= 3行)
        results.append(self._check_trend_history(snapshot))

        # 6. Crown 皇冠全指数波胆
        results.append(self._check_crown_correct_score(snapshot))

        # 7. 微观阵容与首发伤停 (容错维度，暂无数据为 WARN，不阻断)
        results.append(self._check_lineup_injury(snapshot))

        # 8. Polymarket 真实流动性与链接真实性核验
        results.append(self._check_polymarket(snapshot))

        # 9. 真实性与防克隆核验 (严禁跨场次克隆与模板伪造)
        results.append(self._check_authenticity(snapshot))

        tactics = snapshot.get("tactics") or {}
        profiling = snapshot.get("profiling") or {}
        has_dual_track = bool(
            tactics.get("technicalStats")
            and (profiling.get("identicalOddsHistory") or profiling.get("handicapTrends"))
        )

        return VerificationReceipt(
            match_id=match_id,
            results=results,
            metadata={
                "source": snapshot.get("source", "unknown"),
                "fetchedAt": snapshot.get("fetchedAt", "unknown"),
                "league": get_match_property(snapshot, "league", "unknown"),
                "has_dual_track": has_dual_track,
                "tactics_present": bool(tactics),
                "profiling_present": bool(profiling),
            },
        )

    def _check_basic_stats(self, snapshot: Dict[str, Any]) -> DimensionResult:
        home = get_match_property(snapshot, "homeTeam")
        away = get_match_property(snapshot, "awayTeam")
        league = get_match_property(snapshot, "league")

        if not (home and away and league):
            return DimensionResult(
                dimension=DimensionType.BASIC_STATS,
                status=CheckStatus.FAIL,
                message="对阵基本信息残缺 (缺少主队/客队/联赛名称)",
                detail={"home": home, "away": away, "league": league},
            )

        # 检查攻防进失球物理数据 (近6场进失球、主客场进失球等)
        has_goals = False
        home_goals = get_match_property(snapshot, "homeGoals")
        away_goals = get_match_property(snapshot, "awayGoals")
        basic_text = snapshot.get("basicStatsText") or ""
        # 负面清单: 严禁包含 HTML 骨架或导航栏垃圾
        if re.search(r"<!DOCTYPE|<html\b|<body\b", basic_text, re.I):
            return DimensionResult(
                dimension=DimensionType.BASIC_STATS,
                status=CheckStatus.FAIL,
                message="基础战绩数据未解析: 包含未清洗的 HTML 空骨架标签，严禁保存空骨架",
            )
        if re.search(r"首页\s*\n\s*足球直播|分析师\s*\n\s*新\s*\n\s*V计划", basic_text):
            return DimensionResult(
                dimension=DimensionType.BASIC_STATS,
                status=CheckStatus.FAIL,
                message="基础战绩包含整页导航栏垃圾文本，必须使用精准 CSS 容器提取",
            )

        goals_stats = get_match_property(snapshot, "goalsStats")
        correct_score = snapshot.get("correctScoreOdds") or ""
        tactics = snapshot.get("tactics") or {}
        tech_stats = tactics.get("technicalStats") or {}

        has_num_in_goals = bool(
            home_goals and away_goals
            and re.search(r"\d+", str(home_goals))
            and re.search(r"\d+", str(away_goals))
        )

        if has_num_in_goals or goals_stats or tech_stats:
            has_goals = True
        elif basic_text:
            if re.search(r"(?:进|失|得)\s*\d+", basic_text):
                has_goals = True
        elif "联赛积分排名" in correct_score and "得" in correct_score and "失" in correct_score:
            has_goals = True
        elif tactics and re.search(r"(?:进|失|得)\s*\d+|avgGoals", json.dumps(tactics, ensure_ascii=False)):
            has_goals = True

        if not has_goals:
            return DimensionResult(
                dimension=DimensionType.BASIC_STATS,
                status=CheckStatus.FAIL,
                message="对阵基础战绩残缺: 缺少攻防进失球物理统计数字 (近6场/主客场进失球或真实战术技统)",
                detail={"home": home, "away": away, "league": league},
            )

        detail_data: Dict[str, Any] = {"home": home, "away": away, "league": league}
        msg = "对阵基础战绩与攻防进失球信息完整"
        if tactics:
            detail_data["tactics"] = tactics
            msg += " (含真实场上压制力技统与时段赛程)"

        return DimensionResult(
            dimension=DimensionType.BASIC_STATS,
            status=CheckStatus.PASS,
            message=msg,
            detail=detail_data,
        )

    def _check_europe_1x2(self, snapshot: Dict[str, Any]) -> DimensionResult:
        text = snapshot.get("european1x2Text") or ""
        markets = snapshot.get("markets") or {}
        histories = markets.get("europeHistories") or []
        companies = markets.get("europeCompanies") or snapshot.get("europe1x2") or []

        # 0. 严禁算术平均伪数据
        if "marketConsensus" in snapshot or "marketConsensus" in markets or "百家平均" in text:
            return DimensionResult(
                dimension=DimensionType.EUROPE_1X2,
                status=CheckStatus.FAIL,
                message="严禁百家赔率算术平均伪数据！不同机构抽水率各异，必须遵循单家去水(OO-EPC)后聚合",
            )

        # 负面清单: 严禁包含 HTML 骨架或导航栏垃圾
        if re.search(r"<!DOCTYPE|<html\b|<body\b", text, re.I):
            return DimensionResult(
                dimension=DimensionType.EUROPE_1X2,
                status=CheckStatus.FAIL,
                message="欧洲指数数据未解析: 包含未清洗的 HTML 空骨架标签，严禁保存空骨架",
            )
        if re.search(r"首页\s*\n\s*足球直播|分析师\s*\n\s*新\s*\n\s*V计划", text):
            return DimensionResult(
                dimension=DimensionType.EUROPE_1X2,
                status=CheckStatus.FAIL,
                message="欧洲指数包含整页导航栏垃圾文本，必须使用精准 CSS 容器提取",
            )

        has_data = len(text.strip()) > 20 or len(histories) > 0 or len(companies) > 0
        if not has_data:
            return DimensionResult(
                dimension=DimensionType.EUROPE_1X2,
                status=CheckStatus.FAIL,
                message="欧洲指数(1X2)数据缺失，未检测到百家欧指初即盘文本或历史",
            )

        # 强化质检: 必须包含机构已算好的返还率与凯利指数，严禁偷懒只抄3项主平客静态赔率
        has_kelly_and_return = False

        # 1. 结构化 europeCompanies 校验
        if companies:
            core_keywords = [
                "macau", "crown", "bet 365", "bet365", "easybet", "pinnacle", "william", "ladbroke",
                "interwetten", "bwin", "snai", "betfair", "jockey club", "188bet",
                "澳门", "澳彩", "皇冠", "易胜博", "平博", "威廉", "立博", "伟德", "马会", "必发"
            ]
            matched_core = [
                c for c in companies
                if any(k in str(c.get("company") or c.get("name") or "").lower() for k in core_keywords)
            ]
            if len(companies) >= 3 and len(matched_core) < 2:
                return DimensionResult(
                    dimension=DimensionType.EUROPE_1X2,
                    status=CheckStatus.FAIL,
                    message=f"核心做市商覆盖不足: 法定核心机构仅匹配到 {len(matched_core)} 家 (至少需 2 家主流做市商)",
                )

            for c in companies:
                init_data = c.get("initial") or {}
                latest_data = c.get("latest") or {}
                has_ret = (
                    _is_valid_rate(init_data.get("return_rate"))
                    or _is_valid_rate(init_data.get("returnRate"))
                    or _is_valid_rate(latest_data.get("return_rate"))
                    or _is_valid_rate(latest_data.get("returnRate"))
                )
                has_k = _is_valid_kelly(init_data.get("kelly")) or _is_valid_kelly(latest_data.get("kelly"))
                if has_ret and has_k:
                    has_kelly_and_return = True
                    break

        # 2. 文本表格校验 (匹配返还率与凯利指数关键词或百分比)
        if not has_kelly_and_return and text:
            has_ret_word = bool(re.search(r"(?:返还|返还率|\b\d{2}(?:\.\d+)?%)", text, re.I))
            has_kelly_word = bool(re.search(r"(?:凯利|kelly)", text, re.I))
            if has_ret_word and has_kelly_word:
                has_kelly_and_return = True

        if not has_kelly_and_return:
            return DimensionResult(
                dimension=DimensionType.EUROPE_1X2,
                status=CheckStatus.FAIL,
                message="欧洲指数(1X2)残缺: 缺少主流机构返还率与凯利指数数据 (平台已算好，严禁偷懒漏抄)",
            )

        # 3. 欧指连续变盘时序流水校验：严禁仅有初即盘两点切片偷懒 (至少需包含竞彩官方或主流做市商带时间戳变盘记录)
        europe_histories = markets.get("europeHistories") or snapshot.get("europeHistories") or []
        trend_text = snapshot.get("trendComparison") or ""

        timeline_count = sum(len(h.get("records") or h.get("timeline") or []) for h in europe_histories if isinstance(h, dict))
        if timeline_count == 0:
            timeline_count += sum(len(c.get("records") or c.get("timeline") or []) for c in companies if isinstance(c, dict))
        if timeline_count == 0:
            time_series = snapshot.get("timeSeriesFlow") or snapshot.get("timeSeries") or []
            if isinstance(time_series, list):
                timeline_count += sum(1 for item in time_series if isinstance(item, dict) and ("odds" in item or "1x2" in item or "europe" in str(item).lower()))
        if timeline_count == 0:
            timeline_count = len(re.findall(r"(?:\(欧\)|欧指|1X2|标准走势).*?\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}", trend_text))

        if timeline_count < 4:
            return DimensionResult(
                dimension=DimensionType.EUROPE_1X2,
                status=CheckStatus.FAIL,
                message=f"欧洲指数(1X2)缺少连续变盘时序流水！严禁仅用初即盘切片偷懒 (有效欧指变盘记录={timeline_count}项，至少需4项带时间戳流水)",
            )

        if snapshot.get("is_markdown_baseline"):
            euro_list = snapshot.get("europe1x2") or []
            cnames = {str(x.get("company") or "").strip().lower() for x in euro_list}
            pm = snapshot.get("polymarket") or {}
            pm_url = (pm.get("url") or "").strip()
            pm_status = str(pm.get("status") or "")
            is_pm_unopened = not pm_url or "未开放" in pm_url or "未开盘" in pm_url or pm_status == "unopened" or "polymarket" not in cnames
            is_sporttery_unopened = not any("体彩" in c or "竞彩" in c for c in cnames)
            required_count = 23 - (1 if is_pm_unopened else 0) - (1 if is_sporttery_unopened else 0)
            if len(euro_list) < required_count:
                return DimensionResult(
                    dimension=DimensionType.EUROPE_1X2,
                    status=CheckStatus.FAIL,
                    message=f"欧洲指数(1X2)法定机构数量不足 (当前仅{len(euro_list)}家，法定必须满{required_count}家，严禁漏项！)",
                    detail={"count": len(euro_list), "required": required_count},
                )

        return DimensionResult(
            dimension=DimensionType.EUROPE_1X2,
            status=CheckStatus.PASS,
            message="欧洲指数(1X2)主流机构初即盘、返还率/凯利指数与分钟级时序完整",
        )

    def _check_asian_handicap(self, snapshot: Dict[str, Any]) -> DimensionResult:
        text = snapshot.get("asianOddsText") or ""
        markets = snapshot.get("markets") or {}
        histories = markets.get("asianHistories") or []
        profiling = snapshot.get("profiling") or {}
        half_time = markets.get("halfTime") or {}

        # 负面清单: 严禁包含 HTML 骨架或导航栏垃圾
        if re.search(r"<!DOCTYPE|<html\b|<body\b", text, re.I):
            return DimensionResult(
                dimension=DimensionType.ASIAN_HANDICAP,
                status=CheckStatus.FAIL,
                message="亚洲让球盘数据未解析: 包含未清洗的 HTML 空骨架标签，严禁保存空骨架",
            )
        if re.search(r"首页\s*\n\s*足球直播|分析师\s*\n\s*新\s*\n\s*V计划", text):
            return DimensionResult(
                dimension=DimensionType.ASIAN_HANDICAP,
                status=CheckStatus.FAIL,
                message="亚洲让球盘包含整页导航栏垃圾文本，必须使用精准 CSS 容器提取",
            )

        valid_histories = [
            h for h in histories
            if isinstance(h, dict) and len(h.get("records") or h.get("timeline") or []) > 0
        ]
        ah_list = snapshot.get("asianHandicap") or markets.get("asianHandicap") or []
        valid_ah = [
            x for x in ah_list
            if isinstance(x, dict) and (x.get("company") or x.get("initial") or x.get("latest"))
        ]
        has_text_data = len(text.strip()) > 20
        has_real_ah = has_text_data or len(valid_histories) > 0 or len(valid_ah) > 0

        if not has_real_ah:
            return DimensionResult(
                dimension=DimensionType.ASIAN_HANDICAP,
                status=CheckStatus.FAIL,
                message="亚洲让球盘(AH)主流机构盘口水位缺失 (严禁仅用 profiling 叙述或空容器替代真实盘口)",
            )

        if snapshot.get("is_markdown_baseline"):
            statutory_7 = {"澳彩", "皇冠", "Bet365", "易胜博", "平博", "188Bet", "香港马会"}
            def _norm_c(c):
                c = str(c).strip()
                if c in ("365", "bet365"): return "Bet365"
                if c in ("188", "188bet"): return "188Bet"
                if c in ("马会", "HKJC"): return "香港马会"
                if c in ("Crown", "冠"): return "皇冠"
                return c
            present_ah = {_norm_c(x.get("company")) for x in valid_ah}
            missing_ah = statutory_7 - present_ah
            if missing_ah:
                return DimensionResult(
                    dimension=DimensionType.ASIAN_HANDICAP,
                    status=CheckStatus.FAIL,
                    message=f"亚洲让球盘(AH)第一战区核心做市商缺失: {sorted(list(missing_ah))} (法定7家必须全齐，严禁漏项！)",
                    detail={"missing": list(missing_ah), "present": list(present_ah)},
                )

        detail_data: Dict[str, Any] = {}
        msg = "亚洲让球盘主流机构盘口与水位完整"
        if profiling:
            detail_data["profiling"] = profiling
            msg += " (含相同初盘画像与盘路形态)"
        if half_time:
            detail_data["halfTime"] = half_time
            msg += " (含半场双盘联动)"

        return DimensionResult(
            dimension=DimensionType.ASIAN_HANDICAP,
            status=CheckStatus.PASS,
            message=msg,
            detail=detail_data,
        )

    def _check_over_under(self, snapshot: Dict[str, Any]) -> DimensionResult:
        text = snapshot.get("overUnderOddsText") or snapshot.get("overUnderText") or ""
        markets = snapshot.get("markets") or {}
        histories = markets.get("overUnderHistories") or []

        # 负面清单: 严禁包含 HTML 骨架或导航栏垃圾
        if re.search(r"<!DOCTYPE|<html\b|<body\b", text, re.I):
            return DimensionResult(
                dimension=DimensionType.OVER_UNDER,
                status=CheckStatus.FAIL,
                message="大小球数据未解析: 包含未清洗的 HTML 空骨架标签，严禁保存空骨架",
            )
        if re.search(r"首页\s*\n\s*足球直播|分析师\s*\n\s*新\s*\n\s*V计划", text):
            return DimensionResult(
                dimension=DimensionType.OVER_UNDER,
                status=CheckStatus.FAIL,
                message="大小球包含整页导航栏垃圾文本，必须使用精准 CSS 容器提取",
            )

        valid_histories = [
            h for h in histories
            if isinstance(h, dict) and len(h.get("records") or h.get("timeline") or []) > 0
        ]
        ou_list = snapshot.get("overUnder") or snapshot.get("overUnderOdds") or markets.get("overUnder") or []
        valid_ou = [
            x for x in ou_list
            if isinstance(x, dict) and (x.get("company") or x.get("initial") or x.get("latest"))
        ]
        has_text_data = len(text.strip()) > 20
        has_data = has_text_data or len(valid_histories) > 0 or len(valid_ou) > 0
        if not has_data:
            return DimensionResult(
                dimension=DimensionType.OVER_UNDER,
                status=CheckStatus.FAIL,
                message="大小球进球数(OU)主流机构盘口水位缺失",
            )

        if snapshot.get("is_markdown_baseline"):
            statutory_7 = {"澳彩", "皇冠", "Bet365", "易胜博", "平博", "188Bet", "香港马会"}
            def _norm_c(c):
                c = str(c).strip()
                if c in ("365", "bet365"): return "Bet365"
                if c in ("188", "188bet"): return "188Bet"
                if c in ("马会", "HKJC"): return "香港马会"
                if c in ("Crown", "冠"): return "皇冠"
                return c
            present_ou = {_norm_c(x.get("company")) for x in valid_ou}
            missing_ou = statutory_7 - present_ou
            if missing_ou:
                return DimensionResult(
                    dimension=DimensionType.OVER_UNDER,
                    status=CheckStatus.FAIL,
                    message=f"大小球进球数(OU)第一战区核心做市商缺失: {sorted(list(missing_ou))} (法定7家必须全齐，包含香港马会，严禁漏项！)",
                    detail={"missing": list(missing_ou), "present": list(present_ou)},
                )

        return DimensionResult(
            dimension=DimensionType.OVER_UNDER,
            status=CheckStatus.PASS,
            message="大小球进球数主流机构盘口与水位完整",
        )

    def _check_trend_history(self, snapshot: Dict[str, Any]) -> DimensionResult:
        trend = snapshot.get("trendComparison") or ""
        if isinstance(trend, list):
            trend = "\n".join(str(x) for x in trend)
        asian_text = snapshot.get("asianOddsText") or ""
        markets = snapshot.get("markets") or {}
        histories = (
            markets.get("asianHistories")
            or markets.get("europeHistories")
            or []
        )

        combined_text = trend + "\n" + asian_text
        # 匹配时间戳，例如: "10-07 21:33", "10-7 21:09", "10-06 19:37"
        timestamps = re.findall(r"\b\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}\b", combined_text)
        if not timestamps:
            # 兼容时分格式，如 "21:33"
            timestamps = re.findall(r"\b\d{1,2}:\d{2}\b", trend)

        # 兼容原生结构化 timeSeriesFlow 列表
        time_series = snapshot.get("timeSeriesFlow") or snapshot.get("timeSeries") or []
        ts_flow_count = 0
        if isinstance(time_series, list) and time_series:
            ts_flow_count = len(time_series)
            for item in time_series:
                if isinstance(item, dict):
                    t_val = str(item.get("time") or item.get("timestamp") or "")
                    if t_val:
                        found_ts = re.findall(r"\b\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}\b", t_val)
                        if found_ts:
                            timestamps.extend(found_ts)
                        else:
                            timestamps.append(t_val)

        # 铁律0: 校验提取到的全部时间戳合法性 (杜绝 18:62 伪造时间，小时 0-23，分钟 0-59)
        for ts_raw in timestamps:
            m_time = re.search(r"(\d{1,2}):(\d{2})", ts_raw)
            if m_time:
                hh = int(m_time.group(1))
                mm = int(m_time.group(2))
                if hh < 0 or hh > 23 or mm < 0 or mm > 59:
                    return DimensionResult(
                        dimension=DimensionType.TREND_HISTORY,
                        status=CheckStatus.FAIL,
                        message=f"变盘时序流水包含非法时间戳 '{ts_raw}' (小时必须在0~23，分钟必须在0~59)！严禁公式粗制伪造时间！",
                        detail={"invalid_timestamp": ts_raw, "hour": hh, "minute": mm},
                    )

        ts_count = len(timestamps)
        # 仅统计包含真实 records/timeline 的记录条数，空容器不能伪充记录行数
        hist_records_count = sum(
            len(h.get("records") or h.get("timeline") or [])
            for h in (markets.get("asianHistories") or []) + (markets.get("europeHistories") or [])
            if isinstance(h, dict)
        )
        effective_count = max(ts_count, hist_records_count, ts_flow_count)

        # 铁律1: 必须包含时间戳，严禁静态初即两端冒充时序
        if effective_count == 0:
            return DimensionResult(
                dimension=DimensionType.TREND_HISTORY,
                status=CheckStatus.FAIL,
                message="变盘时序流水缺少分秒时间戳，严禁使用静态初即两端冒充时序",
                detail={"timestamps": 0, "histories": hist_records_count},
            )

        # 铁律2: 有效时间戳流水必须 >= 6 条
        if effective_count < 6:
            return DimensionResult(
                dimension=DimensionType.TREND_HISTORY,
                status=CheckStatus.FAIL,
                message=f"变盘时序流水记录不足 (仅有{effective_count}条时间戳记录，法定最低必须 >= 6行)",
                detail={"timestamps": ts_count, "histories": hist_records_count},
            )

        # 铁律3 (负面清单): 严禁混入赛后“滚”球时序数据（必须是赛前赔率）
        if re.search(r"\t滚\b|\s+滚\s+|\t滚$", trend):
            return DimensionResult(
                dimension=DimensionType.TREND_HISTORY,
                status=CheckStatus.FAIL,
                message="变盘时序流水混入赛中‘滚’球盘口！系统法定只准使用赛前赔率时序",
                detail={"trend": trend[:100]},
            )

        # 铁律4 (时点一致性与防混批次): 抓取时间 fetchedAt 不得早于时序流水时间戳 (时点倒挂/混批次检测)
        fetched_at_str = str(snapshot.get("fetchedAt") or "").strip()
        if fetched_at_str and timestamps:
            m_fetch = re.search(r"(\d{4})?-?(\d{1,2})-(\d{1,2})[T\s]+(\d{1,2}):(\d{2})", fetched_at_str)
            if m_fetch:
                f_year = int(m_fetch.group(1)) if m_fetch.group(1) else datetime.now().year
                f_month = int(m_fetch.group(2))
                f_day = int(m_fetch.group(3))
                f_hour = int(m_fetch.group(4))
                f_min = int(m_fetch.group(5))
                try:
                    dt_fetch = datetime(f_year, f_month, f_day, f_hour, f_min)
                    for ts_s in timestamps:
                        m_ts = re.search(r"(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})", ts_s)
                        if m_ts:
                            t_month = int(m_ts.group(1))
                            t_day = int(m_ts.group(2))
                            t_hour = int(m_ts.group(3))
                            t_min = int(m_ts.group(4))
                            t_year = f_year
                            if f_month == 12 and t_month == 1:
                                t_year = f_year + 1
                            elif f_month == 1 and t_month == 12:
                                t_year = f_year - 1
                            dt_ts = datetime(t_year, t_month, t_day, t_hour, t_min)
                            if dt_ts > dt_fetch + timedelta(minutes=10):
                                return DimensionResult(
                                    dimension=DimensionType.TREND_HISTORY,
                                    status=CheckStatus.FAIL,
                                    message=f"变盘时序流水与【推演源数据】抓取时点冲突！【推演源数据】抓取时点({fetched_at_str})早于内部变盘时序时间戳({ts_s})，存在混批次时点倒挂风险",
                                    detail={"fetchedAt": fetched_at_str, "conflictTimestamp": ts_s},
                                )
                except Exception:
                    pass

        # 铁律4 (防偷懒硬门禁): 变盘时序流水核心做市商覆盖必须 >= 3 家 (覆盖范围：澳彩/皇冠/365/易胜博/平博/188/香港马会)
        matched_core_companies = set()
        core_keys = {
            "澳彩": ["澳彩", "澳门", "澳*"],
            "Crown": ["皇冠", "crown", "crow*"],
            "Bet365": ["bet365", "365", "36*"],
            "易胜博": ["易胜博", "易*"],
            "平博": ["平博", "pinnacle"],
            "188": ["188", "188bet"],
            "香港马会": ["香港马会", "马会", "hkjc"],
        }
        for cname, aliases in core_keys.items():
            for a in aliases:
                pattern = rf"{re.escape(a)}[^\n]*?(\d{{1,2}}-\d{{1,2}}\s+\d{{1,2}}:\d{{2}}|\d{{1,2}}:\d{{2}})"
                if re.search(pattern, combined_text, re.I):
                    matched_core_companies.add(cname)
                    break
        for h in (markets.get("asianHistories") or []) + (markets.get("europeHistories") or []):
            c_name = str(h.get("company") or h.get("companyId") or "")
            for cname, aliases in core_keys.items():
                if any(a.lower() in c_name.lower() for a in aliases):
                    if len(h.get("records") or h.get("timeline") or []) > 0:
                        matched_core_companies.add(cname)
        if isinstance(time_series, list) and time_series:
            for item in time_series:
                if isinstance(item, dict):
                    c_name = str(item.get("company") or "")
                    for cname, aliases in core_keys.items():
                        if any(a.lower() in c_name.lower() for a in aliases):
                            matched_core_companies.add(cname)

        if len(matched_core_companies) < 5:
            return DimensionResult(
                dimension=DimensionType.TREND_HISTORY,
                status=CheckStatus.FAIL,
                message=f"变盘时序流水核心做市商覆盖不足！至少需包含 5 家核心做市商时序流水（澳彩/Crown/Bet365/易胜博/平博/188/香港马会），严禁偷懒漏抓做市商 (当前仅匹配到: {', '.join(sorted(matched_core_companies)) if matched_core_companies else '0家'})",
                detail={"matched_companies": list(matched_core_companies)},
            )

        if snapshot.get("is_markdown_baseline"):
            raw_c = snapshot.get("_raw_content", "")
            if "### 第一战区：" not in raw_c or "### 第三战区：" not in raw_c:
                return DimensionResult(
                    dimension=DimensionType.TREND_HISTORY,
                    status=CheckStatus.FAIL,
                    message="变盘时序核心战区不完整！必须包含第一战区(7家欧亚双盘核心)与第三战区(终端履约标的)，严禁截断漏项！",
                )


        return DimensionResult(
            dimension=DimensionType.TREND_HISTORY,
            status=CheckStatus.PASS,
            message=f"变盘时序流水完整 (有效时间戳变盘记录={effective_count}项，涵盖核心做市商={', '.join(sorted(matched_core_companies))})",
            detail={"timestamps": ts_count, "histories": hist_records_count, "companies": list(matched_core_companies)},
        )

    def _check_crown_correct_score(self, snapshot: Dict[str, Any]) -> DimensionResult:
        score_text = str(snapshot.get("correctScoreOdds") or "")
        markets = snapshot.get("markets") or {}
        crow_full = markets.get("crowFullIndex") or {}

        # 检查是否包含占位符
        if any(ph in score_text for ph in ["TODO", "占位", "暂无数据", "待填", "待补充"]):
            return DimensionResult(
                dimension=DimensionType.CROWN_CORRECT_SCORE,
                status=CheckStatus.FAIL,
                message="Crown皇冠全指数波胆包含占位符或未填充提示，禁止使用半成品！",
                detail={"score_text_preview": score_text[:100]},
            )

        # 解析实际提取到的比分赔率项
        parsed = snapshot.get("parsedScores")
        if not parsed or not isinstance(parsed, dict) or not parsed.get("correctScores"):
            parsed = CorrectScoreParser().parse(score_text)

        flat_scores = parsed.get("correctScores", {}).get("flat", {}) if parsed else {}

        # 必须至少包含 8 项常规有效比分赔率 (如 1:0, 2:0, 1:1, 0:1 等)
        if len(flat_scores) < 8 and not crow_full:
            explicit_score_matches = re.findall(r"\b([0-4]:[0-4])\b\s*\|\s*(\d+\.\d+)", score_text)
            total_detected = max(len(flat_scores), len(explicit_score_matches))
            if total_detected < 8:
                return DimensionResult(
                    dimension=DimensionType.CROWN_CORRECT_SCORE,
                    status=CheckStatus.FAIL,
                    message=f"Crown皇冠全指数波胆缺失或残缺：有效比分赔率少于 8 项 (仅检测到 {total_detected} 项)，严禁在无数据时强行推演！",
                    detail={"valid_score_count": total_detected},
                )

        return DimensionResult(
            dimension=DimensionType.CROWN_CORRECT_SCORE,
            status=CheckStatus.PASS,
            message="Crown皇冠全指数波胆比分赔率矩阵完整",
        )

    def _check_lineup_injury(self, snapshot: Dict[str, Any]) -> DimensionResult:
        lineup = (snapshot.get("lineupData") or "").strip()

        # 负面清单: 严禁全页导航栏垃圾与 HTML 骨架标签
        if re.search(r"首页\s*\n\s*足球直播|分析师\s*\n\s*新\s*\n\s*V计划", lineup):
            return DimensionResult(
                dimension=DimensionType.LINEUP_INJURY,
                status=CheckStatus.FAIL,
                message="阵容数据污染: 包含全页导航栏垃圾文本，必须使用精准 CSS 容器选择器提取！",
                detail={"raw_preview": lineup[:80]},
            )
        if re.search(r"<!DOCTYPE|<html\b|<body\b", lineup, re.I):
            return DimensionResult(
                dimension=DimensionType.LINEUP_INJURY,
                status=CheckStatus.FAIL,
                message="阵容数据未解析: 包含未清洗的 HTML 骨架标签",
                detail={"raw_preview": lineup[:80]},
            )

        if not lineup or "暂无数据" in lineup:
            return DimensionResult(
                dimension=DimensionType.LINEUP_INJURY,
                status=CheckStatus.WARN,
                message="微观伤停为【暂无数据】(未核实状态，允许继续十步但严禁脑补无人缺阵)",
                detail={"raw_preview": lineup[:50]},
            )

        # 识别主观概括性套话 (例如：主力阵容齐整、战意强烈、无重大伤病、全员健康等)
        boilerplate_patterns = [
            r"主力(?:阵容)?(?:基本)?(?:齐整|整齐)",
            r"战意强烈",
            r"无重大伤病",
            r"全员健康",
            r"框架完整",
            r"影响较小",
            r"健康出战",
            r"体能充沛",
            r"伤病困扰较小",
        ]
        has_boilerplate = any(re.search(p, lineup) for p in boilerplate_patterns)

        # 识别真实结构化伤停特征
        injury_keywords = [
            r"缺阵原因", r"伤病", r"停赛", r"受伤", r"拉伤", r"扭伤", r"骨折",
            r"韧带", r"膝盖", r"红牌", r"黄牌", r"禁赛", r"出场评分", r"首发",
            r"守门员", r"门将", r"中卫", r"后卫", r"后腰", r"中场", r"前锋", r"边锋", r"前腰",
            r"球员", r"号码", r"评分",
        ]
        has_injury_structure = any(re.search(k, lineup) for k in injury_keywords)

        if has_boilerplate or not has_injury_structure:
            return DimensionResult(
                dimension=DimensionType.LINEUP_INJURY,
                status=CheckStatus.FAIL,
                message="微观伤停检测到概括性套话或缺乏结构化球员名单 (严禁以自然语言脑补冒充真实伤停)",
                detail={"raw_preview": lineup[:80]},
            )

        return DimensionResult(
            dimension=DimensionType.LINEUP_INJURY,
            status=CheckStatus.PASS,
            message="微观伤停阵容名单已有效提取",
            detail={"raw_preview": lineup[:50]},
        )

    def _check_polymarket(self, snapshot: Dict[str, Any]) -> DimensionResult:
        pm = snapshot.get("polymarket") or {}
        url = (pm.get("url") or "").strip()
        slug = (pm.get("slug") or "").strip()
        status_val = str(pm.get("status") or "")
        league = str(get_match_property(snapshot, "league") or "").strip()
        raw_content = str(snapshot.get("_raw_content") or "")

        # 核心主流活跃联赛白名单 (预测市场常态化开设标的，严禁任何形式的未开盘声明)
        core_leagues = {
            "英超", "英冠", "英格兰冠军联赛", "EFL", "ELC", "CHAMPIONSHIP",
            "意甲", "西甲", "德甲", "法甲", "法乙",
            "德乙", "意乙", "西乙",
            "欧冠", "欧洲冠军联赛", "欧联杯", "欧联", "欧协联",
            "葡超", "巴西甲", "巴甲", "亚冠", "亚冠精英",
            "瑞典超", "挪超", "荷甲", "美职联", "MLS",
            "EPL", "SERIE A", "LA LIGA", "BUNDESLIGA", "LIGUE 1"
        }
        is_core_league = any(c.lower() in league.lower() for c in core_leagues) if league else False

        # 如果没有填写任何 polymarket 字段，或者标明未开放/无流动性
        is_unopened = (
            not url
            or "未开放" in url
            or "暂无流动性" in url
            or "未开盘" in url
            or status_val == "unopened"
        )

        # 1. 快照内部自洽性检查：顶部标明未开盘/未开放，但正文或欧指表格中又编造了 Polymarket 挂单数据
        if is_unopened:
            has_fabricated_odds = False
            if re.search(r"\|\s*(?:\*\*\d+\*\*|\d+)\s*\|\s*[\*]*Polymarket[\*]*.*?\|\s*\d+¢", raw_content, re.I):
                has_fabricated_odds = True
            euro_list = snapshot.get("europe1x2") or []
            for row in euro_list:
                if isinstance(row, dict) and "polymarket" in str(row.get("company", "")).lower():
                    init = row.get("initial") or {}
                    latest = row.get("latest") or {}
                    if (init.get("odds") and any(init.get("odds"))) or (latest.get("odds") and any(latest.get("odds"))):
                        has_fabricated_odds = True
                        break
            if has_fabricated_odds:
                return DimensionResult(
                    dimension=DimensionType.POLYMARKET_LIQUIDITY,
                    status=CheckStatus.FAIL,
                    message="快照内部逻辑矛盾：顶部标明 Polymarket 未开盘/未开放，但正文表格中又编造了 Polymarket 挂单赔率！严禁自相矛盾伪造数据！",
                    detail={"url": url, "league": league},
                )

            # 主流核心联赛常态化开盘撮合，绝对严禁标记未开盘逃避过验
            if is_core_league:
                return DimensionResult(
                    dimension=DimensionType.POLYMARKET_LIQUIDITY,
                    status=CheckStatus.FAIL,
                    message=f"Polymarket 门禁拦截：当前赛事联赛为【{league}】，属于主流核心联赛，预测市场常态化开盘撮合，严禁偷懒标记未开盘逃避过验！必须提供真实链上事件链接 (当前为: {url or '未开盘'})",
                    detail={"league": league, "url": url},
                )

            # 2. 真实双向检索与未开盘存证核验（仅对非核心主流次级联赛放行真实双向检索存证）
            has_dual_proof = bool(
                re.search(r"(?:双向|双向核验|双向检索|q_home.*q_away|q=.*(?:与|and|及).*q=|经Gamma.*(?:双向)?核验)", url, re.I)
                and (len(url) >= 15 or "核验" in url)
            )
            if not has_dual_proof:
                return DimensionResult(
                    dimension=DimensionType.POLYMARKET_LIQUIDITY,
                    status=CheckStatus.FAIL,
                    message=f"Polymarket 未开盘存证不足：未开盘声明必须附带真实双向检索凭据（如『官方未开盘（经Gamma双向核验q=Home与q=Away均无活跃标的）』），严禁口头空头逃逸！(当前为: {url})",
                    detail={"url": url, "league": league},
                )

            return DimensionResult(
                dimension=DimensionType.POLYMARKET_LIQUIDITY,
                status=CheckStatus.WARN,
                message="Polymarket 当前未开放独立交易池或暂无流动性 (已具备真实双向核验凭据，允许推演)",
                detail={"url": url or "官方未开盘", "status": "unopened", "league": league},
            )

        # 检查是否包含虚构的模板占位符或假规则 (例如 {league}, {slug}, fake, match-, 包含中文字符等)
        if "{" in url or "}" in url or "fake" in url.lower() or "match-" in url.lower() or any("\u4e00" <= c <= "\u9fff" for c in url):
            return DimensionResult(
                dimension=DimensionType.POLYMARKET_LIQUIDITY,
                status=CheckStatus.FAIL,
                message=f"Polymarket 检测到包含模板占位符、伪造前缀或汉字的虚构链接 ({url})，严禁编造假链接！未开盘必须实事求是标注",
                detail={"url": url},
            )

        # 检查 URL 域名与格式规范 (必须只包含合法英文字符与数字，严禁夹带汉字或非标准字符)
        if not re.search(r"^https?://(?:www\.)?polymarket\.com/(?:event|zh/sports|sports)/[a-zA-Z0-9_\-/]+$", url.strip()):
            return DimensionResult(
                dimension=DimensionType.POLYMARKET_LIQUIDITY,
                status=CheckStatus.FAIL,
                message=f"Polymarket 链接格式不合规 ({url})，必须为形如 https://polymarket.com/event/{{slug}} 的纯英文字符有效事件链接！",
                detail={"url": url},
            )

        # 正常真实 URL
        return DimensionResult(
            dimension=DimensionType.POLYMARKET_LIQUIDITY,
            status=CheckStatus.PASS,
            message=f"Polymarket 真实交易市场链接已配置: {url}",
            detail={"url": url, "slug": slug},
        )

    def _check_authenticity(self, snapshot: Dict[str, Any]) -> DimensionResult:
        """真实性与防克隆核验：杜绝跨场次复制、模板克隆与未替换占位符"""
        match_id = str(get_match_property(snapshot, "matchId") or snapshot.get("id") or "unknown")
        home = str(get_match_property(snapshot, "homeTeam") or "")
        away = str(get_match_property(snapshot, "awayTeam") or "")

        raw_content = str(snapshot.get("_raw_content") or "")
        full_text = raw_content if raw_content else str(snapshot)

        # 1. 占位符检测
        for ph in ["{homeTeam}", "{awayTeam}", "{league}", "{matchId}", "TODO", "xxx", "待填", "待补充"]:
            if ph in full_text:
                return DimensionResult(
                    dimension=DimensionType.AUTHENTICITY,
                    status=CheckStatus.FAIL,
                    message=f"真实性核验失败：【推演源数据】中存在未填充的模板占位符 '{ph}'，禁止使用半成品模板！",
                    detail={"match_id": match_id, "placeholder": ph},
                )

        # 1.1 主客队伍名非空核验
        if not home or not away:
            return DimensionResult(
                dimension=DimensionType.AUTHENTICITY,
                status=CheckStatus.FAIL,
                message=f"真实性核验失败：未能提取到明确的主客对阵队名 (home='{home}', away='{away}')，【推演源数据】格式不合规！",
                detail={"match_id": match_id, "home": home, "away": away},
            )

        # 2. 队伍名称与比赛 ID 自洽性断言 (杜绝拿 002 的内容分析 004 或冒名顶替)
        if home and home not in full_text:
            return DimensionResult(
                dimension=DimensionType.AUTHENTICITY,
                status=CheckStatus.FAIL,
                message=f"真实性核验失败：主队名称 '{home}' 未出现在【推演源数据】正文中，存在张冠李戴冒名顶替！",
                detail={"match_id": match_id, "missing_home": home},
            )
        if away and away not in full_text:
            return DimensionResult(
                dimension=DimensionType.AUTHENTICITY,
                status=CheckStatus.FAIL,
                message=f"真实性核验失败：客队名称 '{away}' 未出现在【推演源数据】正文中，存在张冠李戴冒名顶替！",
                detail={"match_id": match_id, "missing_away": away},
            )

        # 2.1 与 meta.md 登记信息交叉核验 (若存在)
        meta_info = snapshot.get("_meta_info")
        if meta_info and isinstance(meta_info, dict):
            meta_home = meta_info.get("home", "")
            meta_away = meta_info.get("away", "")
            if meta_home and meta_away:
                if home != meta_home or away != meta_away:
                    return DimensionResult(
                        dimension=DimensionType.AUTHENTICITY,
                        status=CheckStatus.FAIL,
                        message=f"真实性与场次一致性核验失败：【推演源数据】对阵 ({home} vs {away}) 与 meta.md 登记对阵 ({meta_home} vs {meta_away}) 冲突，判定为严重张冠李戴！",
                        detail={"match_id": match_id, "snapshot_teams": f"{home} vs {away}", "meta_teams": f"{meta_home} vs {meta_away}"},
                    )

        # 正文声明的比赛 ID 必须与【推演源数据】文件名 match_id 严格一致
        body_id_match = re.search(r"-\s*\*\*比赛\s*ID\*\*[：:]\s*(\d+)", full_text)
        if body_id_match and match_id.isdigit() and body_id_match.group(1) != match_id:
            return DimensionResult(
                dimension=DimensionType.AUTHENTICITY,
                status=CheckStatus.FAIL,
                message=f"真实性核验失败：正文声明的比赛 ID ({body_id_match.group(1)}) 与文件名 ID ({match_id}) 冲突，判定为跨场次文件冒名顶替！",
                detail={"match_id": match_id, "body_id": body_id_match.group(1)},
            )

        # 2. 检查跨场次对阵泄漏 (通用检测正文中是否包含了与本场完全无关的第三方比赛对阵)
        generic_terms = {"主队", "客队", "全场", "半场", "独赢", "让球", "走水", "平手", "胜平负"}
        vs_matches = re.findall(
            r"([\u4e00-\u9fa5a-zA-Z0-9·]{2,12})\s*(?:vs|VS|Vs|对阵)\s*([\u4e00-\u9fa5a-zA-Z0-9·]{2,12})",
            full_text,
        )
        for t1, t2 in vs_matches:
            t1_s, t2_s = t1.strip(), t2.strip()
            if t1_s in generic_terms or t2_s in generic_terms:
                continue
            # 若两支队伍均非本场主客队，判定为跨场次对阵泄漏或模板夹具残留克隆
            if (t1_s not in home and home not in t1_s and t1_s not in away and away not in t1_s) and \
               (t2_s not in home and home not in t2_s and t2_s not in away and away not in t2_s):
                return DimensionResult(
                    dimension=DimensionType.AUTHENTICITY,
                    status=CheckStatus.FAIL,
                    message=f"真实性核验失败：当前比赛 ({home} vs {away}, ID: {match_id}) 正文包含与本场不符的第三方比赛对阵 ({t1_s} vs {t2_s})，判定为测试夹具专属特征或跨场克隆造假！",
                    detail={"match_id": match_id, "home": home, "away": away, "alien_match": f"{t1_s} vs {t2_s}", "violation": "fixture_team_leak"},
                )

        # 3. 检查【推演源数据】内各 URL 中的 matchId 与文件实际 match_id 是否匹配 (严禁引用任何其他比赛 ID)
        url_matches = re.findall(r"(?:id|sid)=(\d{6,8})\b", full_text)
        conflicts = [uid for uid in url_matches if uid != match_id]
        if conflicts and match_id.isdigit():
            first_conflict = conflicts[0]
            return DimensionResult(
                dimension=DimensionType.AUTHENTICITY,
                status=CheckStatus.FAIL,
                message=f"真实性核验失败：【推演源数据】内数据源链接引用了其他场次比赛 ID ({first_conflict})，与当前场次 ({match_id}) 冲突，判定为跨场次张冠李戴！",
                detail={"match_id": match_id, "conflicting_url_id": first_conflict, "all_conflicts": list(set(conflicts))},
            )

        # 4. 【推演源数据】物理新鲜度核验 (防止跳过抓取偷懒使用历史旧【推演源数据】蒙混过关)
        max_age = snapshot.get("_max_age_minutes")
        file_mtime = snapshot.get("_file_mtime")
        if max_age is not None and file_mtime is not None:
            try:
                age_sec = time.time() - float(file_mtime)
                age_min = age_sec / 60.0
                if age_min > float(max_age):
                    mtime_str = datetime.fromtimestamp(float(file_mtime)).strftime("%Y-%m-%d %H:%M:%S")
                    return DimensionResult(
                        dimension=DimensionType.AUTHENTICITY,
                        status=CheckStatus.FAIL,
                        message=f"STALE_SNAPSHOT: 【推演源数据】物理修改时间已过期 (最后修改于 {mtime_str}，距今 {age_min:.1f} 分钟 > 允许阈值 {max_age} 分钟)！严禁跳过真实抓取使用历史旧【推演源数据】炒冷饭！",
                        detail={"match_id": match_id, "mtime": mtime_str, "age_minutes": round(age_min, 1), "max_age_minutes": max_age},
                    )
            except Exception:
                pass

        # 5. 【变盘流水时间戳水印与反打补丁作弊核验】
        if max_age is not None and file_mtime is not None:
            raw_content = snapshot.get("_raw_content") or ""
            ts_matches = re.findall(r"\b(\d{2}-\d{2}\s+\d{2}:\d{2})\b", raw_content)
            if ts_matches:
                try:
                    file_dt = datetime.fromtimestamp(float(file_mtime))
                    year = file_dt.year

                    # 提取各大核心做市商在正文中的最新变盘时序时间戳
                    core_companies = {
                        "澳彩": ["澳彩", "澳门"],
                        "Crown": ["皇冠", "Crown", "crown"],
                        "Bet365": ["Bet365", "bet365", "365"],
                        "易胜博": ["易胜博"],
                        "平博": ["平博", "Pinnacle", "pinnacle"],
                    }
                    company_latest_dts = {}
                    for cname, aliases in core_companies.items():
                        c_pat = rf"(?:###\s*(?:\d+[\.、\s]*)?(?:{'|'.join(aliases)})).*?(?=(?:\n###\s+[^\#]|\Z))"
                        m_block = re.search(c_pat, raw_content, re.DOTALL | re.I)
                        if m_block:
                            c_ts = re.findall(r"\b(\d{2}-\d{2}\s+\d{2}:\d{2})\b", m_block.group(0))
                            if c_ts:
                                c_max_s = max(c_ts)
                                company_latest_dts[cname] = datetime.strptime(f"{year}-{c_max_s}", "%Y-%m-%d %H:%M")

                    # 提取开球时间，比赛已开球时以开球时间为活水基准
                    kickoff_raw = snapshot.get("kickoffTime") or snapshot.get("kickoff") or ""
                    ref_dt = file_dt
                    if kickoff_raw:
                        km = re.search(r"(?:(\d{4})-)?(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})", str(kickoff_raw))
                        if km:
                            ky = int(km.group(1)) if km.group(1) else year
                            kdt = datetime(ky, int(km.group(2)), int(km.group(3)), int(km.group(4)), int(km.group(5)))
                            if file_dt > kdt:
                                ref_dt = kdt

                    if len(company_latest_dts) >= 3:
                        overall_latest_dt = max(company_latest_dts.values())

                        # 5.1 最新时序不能落后基准时间超过 120 分钟 (若比赛已开球，基准时间锁定为开球时间)
                        overall_lag = (ref_dt - overall_latest_dt).total_seconds() / 60.0
                        if overall_lag > 120.0:
                            return DimensionResult(
                                dimension=DimensionType.AUTHENTICITY,
                                status=CheckStatus.FAIL,
                                message=f"STALE_TIMELINE_WATERMARK: 正文核心机构最新变盘时间戳停滞于 {overall_latest_dt.strftime('%m-%d %H:%M')}，落后基准时间 {overall_lag:.1f} 分钟 (> 120 分钟)！判定为未拉取最新活水行情的假刷新！",
                                detail={"match_id": match_id, "latest_timeline": overall_latest_dt.strftime('%m-%d %H:%M'), "file_mtime": file_dt.strftime("%Y-%m-%d %H:%M:%S"), "lag_minutes": round(overall_lag, 1)},
                            )

                        # 5.2 反局部打补丁作弊核验 (SUSPECTED_PATCH_CHEAT)
                        sync_count = sum(
                            1 for dt in company_latest_dts.values()
                            if (overall_latest_dt - dt).total_seconds() / 60.0 <= 60.0
                        )
                        lagging_count = sum(
                            1 for dt in company_latest_dts.values()
                            if (overall_latest_dt - dt).total_seconds() / 60.0 > 90.0
                        )
                        if sync_count < 3 and lagging_count >= 2:
                            # 5.2.1 鉴伪防护：检查是否为合法做市商盘口静默 (Market Quiescence)
                            # 若文件具备有效加密封条与原始报文存证且未被手动篡改，则证明各机构时序与源站一致，属于晚盘合理静默期
                            is_genuine_quiescence = False
                            raw_wire_obj = snapshot.get("_raw_wire")
                            if isinstance(raw_wire_obj, dict):
                                manifest_obj = raw_wire_obj.get("manifest")
                                if isinstance(manifest_obj, dict) and manifest_obj.get("markdown_sha256"):
                                    import hashlib
                                    act_sha = snapshot.get("_markdown_sha256") or hashlib.sha256(raw_content.encode("utf-8")).hexdigest()
                                    if act_sha == manifest_obj.get("markdown_sha256"):
                                        is_genuine_quiescence = True

                            if not is_genuine_quiescence:
                                return DimensionResult(
                                    dimension=DimensionType.AUTHENTICITY,
                                    status=CheckStatus.FAIL,
                                    message=f"SUSPECTED_PATCH_CHEAT: 疑似局部打补丁作弊！核心做市商时序严重不同步 (仅 {sync_count} 家机构更新至最新区间，而有 {lagging_count} 家机构严重滞后超 90 分钟)！重跑推演必须全量并发重抓所有核心机构！",
                                    detail={"match_id": match_id, "sync_count": sync_count, "lagging_count": lagging_count, "company_timestamps": {k: v.strftime('%m-%d %H:%M') for k, v in company_latest_dts.items()}},
                                )
                    else:
                        latest_ts_str = max(ts_matches)
                        latest_ts_dt = datetime.strptime(f"{year}-{latest_ts_str}", "%Y-%m-%d %H:%M")
                        lag_minutes = (ref_dt - latest_ts_dt).total_seconds() / 60.0
                        if lag_minutes > 120.0:
                            return DimensionResult(
                                dimension=DimensionType.AUTHENTICITY,
                                status=CheckStatus.FAIL,
                                message=f"STALE_TIMELINE_WATERMARK: 正文变盘时序时间戳停滞于 {latest_ts_str}，落后基准时间 {lag_minutes:.1f} 分钟 (> 120 分钟)！判定为未拉取最新活水行情的假刷新！",
                                detail={"match_id": match_id, "latest_timeline_time": latest_ts_str, "file_mtime": file_dt.strftime("%Y-%m-%d %H:%M:%S"), "lag_minutes": round(lag_minutes, 1)},
                            )
                except Exception:
                    pass

        # 6. U3: 防凑数伪造时序、原始报文加密哈希封条 (TAMPERED_MARKDOWN_SEAL / MISSING_CRYPTOGRAPHIC_SEAL) 与原文子串交叉校验 (RAW_PROVENANCE_MISMATCH)
        if snapshot.get("is_markdown_baseline") and raw_content:
            for forbidden_pad in ("维持区间", "T0 初盘骨架", "T1 早盘试探", "T2 中盘假摔", "T3 临盘洗盘", "做市形态学识别", "10-08 12:00"):
                if forbidden_pad in raw_content:
                    return DimensionResult(
                        dimension=DimensionType.AUTHENTICITY,
                        status=CheckStatus.FAIL,
                        message=(
                            f"FABRICATED_TIMELINE_PADDING: 检测到已废除的伪造时序凑数标记 '{forbidden_pad}'！"
                            "严禁凑满 T0~T4 五阶段、伪造『维持区间』或填写『做市形态学识别』脑补散文！"
                        ),
                        detail={"match_id": match_id, "forbidden_token": forbidden_pad},
                    )

        raw_wire = snapshot.get("_raw_wire")
        if snapshot.get("is_markdown_baseline") and max_age is not None:
            if not isinstance(raw_wire, dict) or not isinstance(raw_wire.get("manifest"), dict) or not raw_wire["manifest"].get("markdown_sha256"):
                return DimensionResult(
                    dimension=DimensionType.AUTHENTICITY,
                    status=CheckStatus.FAIL,
                    message=(
                        f"MISSING_CRYPTOGRAPHIC_SEAL: 实时门禁模式下比赛【{match_id}】缺失 raw/{match_id}/manifest.json 加密封条！"
                        "严禁大模型调用 write_to_file 手写 .md，必须通过 cli.py --assemble 确定性装配落盘！"
                    ),
                    detail={"match_id": match_id},
                )

        if isinstance(raw_wire, dict):
            import hashlib
            from 校验.src.domain.raw_parser import Titan007RawParser
            from 校验.src.domain.assembler import _normalize_company_name

            manifest = raw_wire.get("manifest")
            if isinstance(manifest, dict):
                expected_sha = str(manifest.get("markdown_sha256") or "").strip()
                actual_sha = str(snapshot.get("_markdown_sha256") or "").strip()
                if not actual_sha and raw_content:
                    actual_sha = hashlib.sha256(raw_content.encode("utf-8")).hexdigest()
                if expected_sha and actual_sha and expected_sha != actual_sha:
                    return DimensionResult(
                        dimension=DimensionType.AUTHENTICITY,
                        status=CheckStatus.FAIL,
                        message=(
                            f"TAMPERED_MARKDOWN_SEAL: 【推演源数据】.md 文件哈希 ({actual_sha[:12]}...) "
                            f"与 raw/manifest.json 原始加密封条 ({expected_sha[:12]}...) 不符！"
                            "严禁对源数据做任何手动修改、增删标点符号或篡改时间戳！"
                        ),
                        detail={"match_id": match_id, "expected_sha256": expected_sha, "actual_sha256": actual_sha},
                    )

                raw_files_sha = manifest.get("raw_files_sha256")
                disk_files_sha = raw_wire.get("files_sha256")
                if isinstance(raw_files_sha, dict) and isinstance(disk_files_sha, dict) and disk_files_sha:
                    for fname, exp_fsha in raw_files_sha.items():
                        act_fsha = disk_files_sha.get(fname)
                        if not act_fsha or str(exp_fsha).strip() != str(act_fsha).strip():
                            return DimensionResult(
                                dimension=DimensionType.AUTHENTICITY,
                                status=CheckStatus.FAIL,
                                message=(
                                    f"TAMPERED_RAW_WIRE_SEAL: raw/{match_id}/{fname} 原始报文哈希 ({str(act_fsha)[:12]}...) "
                                    f"与 manifest.json 封条 ({str(exp_fsha)[:12]}...) 不符或缺失！"
                                ),
                                detail={"match_id": match_id, "file": fname},
                            )

            # 6.1 U2: 真实网络收据防伪核验 (RECEIPT_PAYLOAD_MISMATCH)
            receipt = raw_wire.get("receipt")
            if isinstance(receipt, dict):
                endpoints = receipt.get("endpoints") or []
                disk_files_sha = raw_wire.get("files_sha256") or {}
                manifest_files_sha = (raw_wire.get("manifest") or {}).get("raw_files_sha256") or {}
                raw_files_temp = raw_wire.get("files") if isinstance(raw_wire.get("files"), dict) else {}
                for ep in endpoints:
                    if not isinstance(ep, dict):
                        continue
                    fname = ep.get("file") or ""
                    ep_status = ep.get("status")
                    if ep_status is not None and int(ep_status) != 200:
                        return DimensionResult(
                            dimension=DimensionType.AUTHENTICITY,
                            status=CheckStatus.FAIL,
                            message=f"INVALID_RECEIPT_STATUS: 网络收据端点 {fname} ({ep.get('url')}) 响应状态码为 {ep_status} (!= 200)！",
                            detail={"match_id": match_id, "file": fname, "status": ep_status},
                        )
                    ep_sha = str(ep.get("payload_sha256") or "").strip()
                    if fname and ep_sha:
                        act_sha = disk_files_sha.get(fname) or manifest_files_sha.get(fname)
                        if not act_sha and fname in raw_files_temp:
                            act_sha = hashlib.sha256(str(raw_files_temp[fname]).encode("utf-8")).hexdigest()
                        if act_sha and str(act_sha).strip() != ep_sha:
                            return DimensionResult(
                                dimension=DimensionType.AUTHENTICITY,
                                status=CheckStatus.FAIL,
                                message=(
                                    f"RECEIPT_PAYLOAD_MISMATCH: 网络收据记录的 {fname} 报文哈希 ({ep_sha[:12]}...) "
                                    f"与实际磁盘报文哈希 ({str(act_sha)[:12]}...) 不一致！判定为伪造收据或篡改报文！"
                                ),
                                detail={"match_id": match_id, "file": fname, "receipt_sha": ep_sha, "actual_sha": str(act_sha)},
                            )

            raw_files_map = raw_wire.get("files") if isinstance(raw_wire.get("files"), dict) else {}
            raw_1x2_js = raw_wire.get("1x2d.js") or raw_files_map.get("1x2d.js")
            if raw_1x2_js:
                parsed_wire = Titan007RawParser().parse_1x2d_js(str(raw_1x2_js))
                wire_home = parsed_wire.get("homeTeam") or ""
                wire_away = parsed_wire.get("awayTeam") or ""
                if wire_home and wire_away:
                    if (wire_home not in home and home not in wire_home) or (wire_away not in away and away not in wire_away):
                        return DimensionResult(
                            dimension=DimensionType.AUTHENTICITY,
                            status=CheckStatus.FAIL,
                            message=(
                                f"RAW_PROVENANCE_MISMATCH: .md 对阵 ({home} vs {away}) 与 raw/1x2d.js "
                                f"原始报文对阵 ({wire_home} vs {wire_away}) 不符！"
                            ),
                            detail={"match_id": match_id, "md_teams": f"{home} vs {away}", "wire_teams": f"{wire_home} vs {wire_away}"},
                        )

                wire_by_comp = parsed_wire.get("byCompany") or {}
                euro_list = snapshot.get("europe1x2") or []
                for row in euro_list:
                    if not isinstance(row, dict):
                        continue
                    std_c = _normalize_company_name(str(row.get("company") or ""))
                    if not std_c or std_c == "Polymarket":
                        continue
                    if std_c in wire_by_comp:
                        w_entry = wire_by_comp[std_c]
                        w_init = [float(x) for x in w_entry["initialOdds"]]
                        w_live = [float(x) for x in w_entry["liveOdds"]]
                        md_init = [float(x) for x in (row.get("initial") or {}).get("odds", [])]
                        md_live = [float(x) for x in (row.get("latest") or {}).get("odds", [])]
                        if len(md_init) == 3 and len(md_live) == 3:
                            init_diff = max(abs(md_init[i] - w_init[i]) for i in range(3))
                            live_diff = max(abs(md_live[i] - w_live[i]) for i in range(3))
                            if init_diff > 0.015 or live_diff > 0.015:
                                return DimensionResult(
                                    dimension=DimensionType.AUTHENTICITY,
                                    status=CheckStatus.FAIL,
                                    message=(
                                        f"RAW_PROVENANCE_MISMATCH: 机构【{std_c}】在 .md 中的欧指 "
                                        f"({md_init} -> {md_live}) 与 raw/1x2d.js 原始报文 "
                                        f"({w_init} -> {w_live}) 严重不符！严禁篡改或捏造赔率！"
                                    ),
                                    detail={
                                        "match_id": match_id,
                                        "company": std_c,
                                        "md_initial": md_init,
                                        "md_latest": md_live,
                                        "wire_initial": w_init,
                                        "wire_latest": w_live,
                                    },
                                )

                if "中国体彩" in wire_by_comp and "eu_1129.html" not in raw_files_map:
                    sp_entry = wire_by_comp["中国体彩"]
                    sp_wire_time = str(sp_entry.get("changeTime") or "-").strip()
                    valid_sp_times = {sp_wire_time}
                    for gd_r in (sp_entry.get("detailRows") or []):
                        if gd_r and gd_r[0]:
                            valid_sp_times.add(str(gd_r[0]).strip())
                    for sp_row in (snapshot.get("sportteryHadRows") or []):
                        if isinstance(sp_row, (list, tuple)) and len(sp_row) >= 5:
                            row_time = str(sp_row[0]).strip()
                            if row_time and row_time != "-" and row_time not in valid_sp_times:
                                return DimensionResult(
                                    dimension=DimensionType.AUTHENTICITY,
                                    status=CheckStatus.FAIL,
                                    message=(
                                        f"RAW_PROVENANCE_MISMATCH: 第4/5节中国体彩变盘时间 ({row_time}) "
                                        f"在 raw/1x2d.js 中并不存在（原始报文仅记录 {sorted(valid_sp_times)}）！严禁脑补捏造初盘时间戳！"
                                    ),
                                    detail={"match_id": match_id, "fabricated_time": row_time, "wire_time": sp_wire_time},
                                )

            if "odds.html" in raw_files_map:
                cs_wire = Titan007RawParser().parse_correct_score_html(str(raw_files_map["odds.html"]))
                wire_scores = cs_wire.get("flatScores") or {}
                md_scores = snapshot.get("correctScore") or {}
                if not md_scores and snapshot.get("correctScoreOdds"):
                    md_parsed = CorrectScoreParser().parse(str(snapshot.get("correctScoreOdds") or ""))
                    md_scores = (md_parsed.get("correctScores") or {}).get("flat") or {}
                if wire_scores and md_scores:
                    for sc_key, md_val in md_scores.items():
                        if sc_key in wire_scores and abs(float(md_val) - float(wire_scores[sc_key])) > 0.015:
                            return DimensionResult(
                                dimension=DimensionType.AUTHENTICITY,
                                status=CheckStatus.FAIL,
                                message=(
                                    f"RAW_PROVENANCE_MISMATCH: 第5节 Crown 波胆比分【{sc_key}】在 .md 中的赔率 ({md_val}) "
                                    f"与 raw/odds.html 原始报文 ({wire_scores[sc_key]}) 不符！严禁用体彩 jcOdds 冒充皇冠波胆！"
                                ),
                                detail={"match_id": match_id, "score": sc_key, "md_odds": md_val, "wire_odds": wire_scores[sc_key]},
                            )

            comp_timelines = snapshot.get("companyTimelines")
            if raw_files_map and isinstance(comp_timelines, dict):
                from 校验.src.domain.raw_parser import ZONE1_COMPANY_FILE_KEYS
                parser_inst = Titan007RawParser()

                def _norm_tl_row(r: Any) -> Tuple[str, str, str, str, str]:
                    if isinstance(r, dict):
                        return (
                            str(r.get("timestamp", "")).strip(),
                            str(r.get("col1", r.get("home", ""))).strip(),
                            str(r.get("col2", r.get("draw", ""))).strip(),
                            str(r.get("col3", r.get("away", ""))).strip(),
                            str(r.get("status", "")).strip(),
                        )
                    if isinstance(r, (list, tuple)) and len(r) >= 5:
                        return (str(r[0]).strip(), str(r[1]).strip(), str(r[2]).strip(), str(r[3]).strip(), str(r[4]).strip())
                    return ("", "", "", "", "")

                def _cells_match(a: str, b: str) -> bool:
                    if a == b:
                        return True
                    try:
                        return abs(float(a) - float(b)) <= 1e-4
                    except ValueError:
                        return False

                for cname, fkeys in ZONE1_COMPANY_FILE_KEYS.items():
                    md_comp = comp_timelines.get(cname) or {}
                    for kind, prefix, label in (("ah", "ah", "亚盘"), ("ou", "ou", "大小球"), ("eu", "eu", "欧指")):
                        raw_html = None
                        used_fname = ""
                        for fk in fkeys:
                            cand = f"{prefix}_{fk}.html"
                            if cand in raw_files_map:
                                raw_html = str(raw_files_map[cand])
                                used_fname = cand
                                break
                        if not raw_html:
                            continue
                        raw_parsed = (
                            parser_inst.parse_1x2_detail_rows(
                                raw_html,
                                company_entry=(parsed_wire.get("byCompany") or {}).get(cname) if raw_1x2_js else None,
                            )
                            if kind == "eu"
                            else parser_inst.parse_change_detail_rows(raw_html)
                        )
                        if not raw_parsed:
                            continue
                        md_rows_norm = [_norm_tl_row(x) for x in (md_comp.get(kind) or [])]
                        raw_rows_norm = [_norm_tl_row(x) for x in raw_parsed]
                        from 校验.src.domain.timeseries_denoiser import denoise_timeline_rows
                        denoised_rows_norm = [_norm_tl_row(x) for x in denoise_timeline_rows(raw_parsed)]
                        expected_rows = denoised_rows_norm if len(md_rows_norm) == len(denoised_rows_norm) else raw_rows_norm

                        if len(md_rows_norm) != len(expected_rows):
                            return DimensionResult(
                                dimension=DimensionType.AUTHENTICITY,
                                status=CheckStatus.FAIL,
                                message=(
                                    f"RAW_PROVENANCE_MISMATCH: 机构【{cname}】第4节{label}变盘流水行数 ({len(md_rows_norm)} 行) "
                                    f"与降噪规范行数 ({len(denoised_rows_norm)} 行) 及原始报文行数 ({len(raw_rows_norm)} 行) 均不符！严禁篡改或捏造流水！"
                                ),
                                detail={
                                    "match_id": match_id,
                                    "company": cname,
                                    "market": kind,
                                    "md_row_count": len(md_rows_norm),
                                    "expected_count": len(expected_rows),
                                    "raw_row_count": len(raw_rows_norm),
                                },
                            )
                        for r_idx, (m_row, w_row) in enumerate(zip(md_rows_norm, expected_rows)):
                            if (
                                m_row[0] != w_row[0]
                                or m_row[4] != w_row[4]
                                or not _cells_match(m_row[1], w_row[1])
                                or not _cells_match(m_row[2], w_row[2])
                                or not _cells_match(m_row[3], w_row[3])
                            ):
                                return DimensionResult(
                                    dimension=DimensionType.AUTHENTICITY,
                                    status=CheckStatus.FAIL,
                                    message=(
                                        f"RAW_PROVENANCE_MISMATCH: 机构【{cname}】第4节{label}第 {r_idx + 1} 行 "
                                        f"{m_row} 与期望报文 {used_fname} {w_row} 不符！严禁篡改时间、水位或状态词（早/即/初盘）！"
                                    ),
                                    detail={
                                        "match_id": match_id,
                                        "company": cname,
                                        "market": kind,
                                        "row_index": r_idx + 1,
                                        "md_row": m_row,
                                        "raw_row": w_row,
                                    },
                                )

        return DimensionResult(
            dimension=DimensionType.AUTHENTICITY,
            status=CheckStatus.PASS,
            message="数据真实性与防克隆指纹核验通过 (无模板造假、无测试夹具克隆)",
            detail={"match_id": match_id},
        )


def _normalize_primary_direction(text: str) -> str:
    """从胜负平单元格或卡片首选文本中提取第一顺位方向（主胜 / 平局 / 客胜）"""
    clean = re.sub(r"\*\*|首选|次选|[:：]", " ", str(text or "")).strip()
    first_part = re.split(r"[/｜|、,，\s]+", clean)[0].strip() if clean else ""
    if first_part in ("主胜", "胜"):
        return "主胜"
    if first_part in ("平局", "平"):
        return "平局"
    if first_part in ("客胜", "负"):
        return "客胜"
    m = re.search(r"(主胜|平局|客胜)", clean)
    return m.group(1) if m else ""


def verify_memory_cognitive_cards(
    content: str,
    expected_matches: Optional[int] = None,
    data_dir: Optional[str] = None,
) -> tuple[bool, list[str], int]:
    """
    纯领域检验函数：验证每日记忆 (memory/YYYY-MM-DD.md) 中的【认知契约卡】、【图谱认知基因】、
    7列汇总表内部一致性 (MEMORY_INTERNAL_DIRECTION_CONFLICT) 以及与源数据快照交叉核对 (MEMORY_SOURCE_DRIFT)。
    """
    from pathlib import Path

    errors: list[str] = []
    if not content or not content.strip():
        return False, ["每日记忆文本为空，无法核验认知契约卡"], 0

    # 提取 7 列推荐汇总表中的场次首选方向映射 (按场次编号或对阵名索引)
    table_directions_by_code: Dict[str, str] = {}
    table_directions_by_teams: Dict[str, str] = {}
    table_pm_by_code: Dict[str, str] = {}
    table_pm_by_teams: Dict[str, str] = {}
    for line in content.splitlines():
        sline = line.strip()
        if not sline.startswith("|") or "---" in sline or "场次/时间" in sline or "对阵双方" in sline:
            continue
        cells = [c.strip() for c in sline.split("|")[1:-1]]
        if len(cells) >= 7 and "vs" in cells[1].lower():
            code_m = re.search(r"(周[一二三四五六日]\d{3})", cells[0])
            code_str = code_m.group(1) if code_m else ""
            teams_key = re.sub(r"\s+", "", cells[1])
            pm_cell = cells[6]
            if code_str:
                table_pm_by_code[code_str] = pm_cell
            table_pm_by_teams[teams_key] = pm_cell

            p_dir = _normalize_primary_direction(cells[2])
            if p_dir:
                if code_str:
                    table_directions_by_code[code_str] = p_dir
                table_directions_by_teams[teams_key] = p_dir

            # 严格核验第7列 Polymarket 真实性与防伪 (杜绝虚构链接流向交付)
            pm_cell = cells[6]
            if "{" in pm_cell or "}" in pm_cell or "fake" in pm_cell.lower() or "match-" in pm_cell.lower():
                errors.append(f"7列推荐汇总表第7列包含模板占位符或伪造链接 ({cells[0]} {pm_cell})！未开盘必须标明『官方未开盘（经Gamma双向核验）』")
            elif "http" in pm_cell:
                url_m = re.search(r"\((https?://[^\)]+)\)", pm_cell)
                url_to_check = url_m.group(1) if url_m else pm_cell
                if any("\u4e00" <= c <= "\u9fff" for c in url_to_check):
                    errors.append(f"7列推荐汇总表第7列 Polymarket 链接夹带汉字 ({cells[0]} {url_to_check})，严禁编造假链接！未开盘必须实事求是标注")
                elif not re.search(r"^https?://(?:www\.)?polymarket\.com/(?:event|zh/sports|sports)/[a-zA-Z0-9_\-/]+$", url_to_check.strip()):
                    errors.append(f"7列推荐汇总表第7列 Polymarket 链接格式不合规 ({cells[0]} {url_to_check})，必须为纯英文事件有效链接！")
            elif not any(kw in pm_cell for kw in ("未开盘", "未开放", "暂无")):
                errors.append(f"7列推荐汇总表第7列缺少有效 Polymarket 真实链接或未开盘声明 ({cells[0]} {pm_cell})！")

    # 1. 检查是否存在 ## 深度分析 (或带有时间的 ## 深度分析)
    section_pattern = r"(?m)^##\s+深度分析.*$"
    match_section = re.search(section_pattern, content)
    if not match_section:
        return False, ["缺失 '## 深度分析' 章节，未见赛前冻结深度分析与认知契约卡底账"], 0

    start_pos = match_section.end()
    next_section = re.search(r"(?m)^##\s+(?!深度分析).*$", content[start_pos:])
    if next_section:
        analysis_block = content[start_pos : start_pos + next_section.start()]
    else:
        analysis_block = content[start_pos:]

    # 2. 切分各场子块 (以 ### 为界)
    match_blocks = re.split(r"(?m)^###\s+", analysis_block)
    actual_blocks = [b.strip() for b in match_blocks[1:] if b.strip()]

    if not actual_blocks:
        return False, ["'## 深度分析' 章节下未解析出任何单场比赛分析块 (缺少 '### {场次}' 标题)"], 0

    valid_matches_count = 0
    mandatory_dimensions = [
        "选择与排除依据",
        "关键拍板依据",
        "庄家博弈假说与竞争解释",
        "可推翻反证与改变条件",
    ]

    for idx, block in enumerate(actual_blocks, start=1):
        header_line = block.splitlines()[0] if block.splitlines() else f"第 {idx} 场"

        # 提取 matchId
        id_match = re.search(r"(?:比赛ID|matchId)\s*[:：]\s*(\d+)", block, re.IGNORECASE)
        match_id_str = id_match.group(1) if id_match else f"未知ID({header_line})"

        block_errors = []

        # 检查图谱认知基因
        if "【图谱认知基因】" not in block and "图谱认知基因" not in block:
            block_errors.append(f"【{match_id_str}】缺少【图谱认知基因】，未关联 Graphify 知识图谱节点与演绎链")

        # 检查认知契约卡标题
        if "【认知契约卡】" not in block and "认知契约卡" not in block:
            block_errors.append(f"【{match_id_str}】缺少【认知契约卡】主体")
        else:
            for dim in mandatory_dimensions:
                if dim not in block:
                    block_errors.append(f"【{match_id_str}】认知契约卡缺少核心维度：'{dim}'")

        # 检查去水点概率
        prob_match = re.search(r"(?:点概率|OO-EPC|胜/平/负|概率)\s*.*?\d+(\.\d+)?%", block)
        if not prob_match and "胜/平/负点概率" not in block:
            block_errors.append(f"【{match_id_str}】缺少去水点概率数值（必须保留 OO-EPC 去水概率，Wheatcroft 2019 铁律）")

        # U4.1: 检查 7 列汇总表与卡片内部首选方向是否矛盾 (MEMORY_INTERNAL_DIRECTION_CONFLICT)
        card_dir_m = re.search(r"胜平负\s*[:：]\s*([^\n\r]+)", block)
        if card_dir_m:
            card_primary = _normalize_primary_direction(card_dir_m.group(1))
            code_m = re.search(r"(周[一二三四五六日]\d{3})", header_line)
            teams_m = re.search(r"([^\s（(]+)\s*vs\s*([^\s（(]+)", header_line, re.I)
            table_primary = ""
            if code_m and code_m.group(1) in table_directions_by_code:
                table_primary = table_directions_by_code[code_m.group(1)]
            elif teams_m:
                tkey = f"{teams_m.group(1)}vs{teams_m.group(2)}"
                table_primary = table_directions_by_teams.get(tkey, "")
            if card_primary and table_primary and card_primary != table_primary:
                block_errors.append(
                    f"MEMORY_INTERNAL_DIRECTION_CONFLICT: 【{match_id_str}】7列推荐汇总表首选方向 ({table_primary}) "
                    f"与深度分析卡片首选方向 ({card_primary}) 前后矛盾！"
                )

        # U4.1b: 严格核验主流核心联赛在第 7 列表格中必须具备真实链接，严禁标记未开盘逃避过验
        if table_pm_by_code or table_pm_by_teams:
            core_leagues = {
                "英超", "英冠", "英格兰冠军联赛", "EFL", "ELC", "CHAMPIONSHIP",
                "意甲", "西甲", "德甲", "法甲", "法乙",
                "德乙", "意乙", "西乙",
                "欧冠", "欧洲冠军联赛", "欧联杯", "欧联", "欧协联",
                "葡超", "巴西甲", "巴甲", "亚冠", "亚冠精英",
                "瑞典超", "挪超", "荷甲", "美职联", "MLS",
                "EPL", "SERIE A", "LA LIGA", "BUNDESLIGA", "LIGUE 1"
            }
            if any(c.lower() in header_line.lower() for c in core_leagues):
                code_m = re.search(r"(周[一二三四五六日]\d{3})", header_line)
                code_key = code_m.group(1) if code_m else ""
                matched_pm = table_pm_by_code.get(code_key, "")
                if not matched_pm:
                    for tkey, pval in table_pm_by_teams.items():
                        if tkey in header_line.replace(" ", ""):
                            matched_pm = pval
                            break
                if matched_pm and any(kw in matched_pm for kw in ("未开盘", "未开放", "暂无")):
                    block_errors.append(
                        f"【{match_id_str} {code_key}】属于主流核心联赛，Polymarket 预测市场常态化开设标的，推荐总表第 7 列必须具备真实链上事件链接，严禁标注未开盘逃避过验！(当前为: {matched_pm})"
                    )

        # U4.2: 若提供了 data_dir，交叉核验 memory 卡片与源数据 data/{销售日}/{matchId}.md
        if data_dir and id_match:
            src_md_path = Path(data_dir) / f"{match_id_str}.md"
            if not src_md_path.exists():
                block_errors.append(
                    f"MEMORY_SOURCE_DRIFT: 【{match_id_str}】在源数据目录 {data_dir} 中不存在对应的 {match_id_str}.md 物理文件！"
                )
            else:
                try:
                    src_text = src_md_path.read_text(encoding="utf-8")
                    # 提取源数据中的欧指 (主胜, 平局, 客胜) 赔率集合
                    src_home_odds: List[float] = []
                    for sline in src_text.splitlines():
                        if sline.startswith("|") and "%" in sline and "/" in sline:
                            sparts = [p.strip() for p in sline.split("|")[1:-1]]
                            if len(sparts) >= 10:
                                try:
                                    src_home_odds.append(float(sparts[2]))
                                    src_home_odds.append(float(sparts[6]))
                                except ValueError:
                                    pass
                    cited_odds_m = re.search(r"主胜\s*([\d\.]+)\s*[/｜|]\s*平(?:局)?\s*([\d\.]+)\s*[/｜|]\s*客胜\s*([\d\.]+)", block)
                    if cited_odds_m and src_home_odds:
                        cited_h = float(cited_odds_m.group(1))
                        min_diff = min(abs(cited_h - sh) for sh in src_home_odds)
                        if min_diff > 0.05:
                            block_errors.append(
                                f"MEMORY_SOURCE_DRIFT: 【{match_id_str}】记忆卡片引用的主胜赔率 ({cited_h}) "
                                f"与源数据 {match_id_str}.md 真实赔率区间 ({min(src_home_odds):.2f}~{max(src_home_odds):.2f}) 偏差 > 0.05 (实为 {min_diff:.2f})！"
                            )
                except Exception as e:
                    block_errors.append(f"MEMORY_SOURCE_DRIFT: 【{match_id_str}】读取源数据快照核对失败: {e}")

        if block_errors:
            errors.extend(block_errors)
        else:
            valid_matches_count += 1

    # 3. 检查场次数量
    if expected_matches is not None and valid_matches_count < expected_matches:
        errors.append(
            f"实际合格深度分析场次 ({valid_matches_count}) 低于预期场次 ({expected_matches})！严禁部分场次缺卡发布"
        )

    is_ok = len(errors) == 0 and valid_matches_count > 0
    return is_ok, errors, valid_matches_count


