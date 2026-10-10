"""
校验/src/domain/verifier.py
快照数据完整性纯领域检验引擎 (零外部依赖，纯 Python 原生规则判定)
"""

from __future__ import annotations
from datetime import datetime, timedelta
import json
import re
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
    """清洗从 Chromium AXTree / BrowserOS 页面快照中残留的无障碍树标记杂质"""
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
    快照数据完整性领域聚合根
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

        if (home_goals and away_goals) or goals_stats or tech_stats:
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
                                    message=f"变盘时序流水与快照抓取时点冲突！快照抓取时点({fetched_at_str})早于内部变盘时序时间戳({ts_s})，存在混批次时点倒挂风险",
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

        return DimensionResult(
            dimension=DimensionType.TREND_HISTORY,
            status=CheckStatus.PASS,
            message=f"变盘时序流水完整 (有效时间戳变盘记录={effective_count}项，涵盖核心做市商={', '.join(sorted(matched_core_companies))})",
            detail={"timestamps": ts_count, "histories": hist_records_count, "companies": list(matched_core_companies)},
        )

    def _check_crown_correct_score(self, snapshot: Dict[str, Any]) -> DimensionResult:
        score_text = snapshot.get("correctScoreOdds") or ""
        markets = snapshot.get("markets") or {}
        crow_full = markets.get("crowFullIndex") or {}

        has_score = (
            len(score_text.strip()) > 15
            and ("波胆" in score_text or "1:0" in score_text or "0:0" in score_text)
        ) or bool(crow_full)

        if not has_score:
            return DimensionResult(
                dimension=DimensionType.CROWN_CORRECT_SCORE,
                status=CheckStatus.FAIL,
                message="Crown皇冠全指数波胆缺失或残缺 (未检测到 0:0~4:4 比分赔率矩阵)",
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
        status_val = pm.get("status") or ""

        # 如果没有填写任何 polymarket 字段，或者标明未开放/无流动性
        is_unopened = (
            not url
            or "未开放" in url
            or "暂无流动性" in url
            or "未开盘" in url
            or status_val == "unopened"
        )
        if is_unopened:
            return DimensionResult(
                dimension=DimensionType.POLYMARKET_LIQUIDITY,
                status=CheckStatus.WARN,
                message="Polymarket 当前未开放独立交易池或暂无流动性 (实事求是标注，允许推演)",
                detail={"url": url or "未开放", "status": "unopened"},
            )

        # 检查是否包含虚构的模板占位符 (例如 {league}, {slug}, fake 等)
        if "{" in url or "}" in url or "fake" in url.lower():
            return DimensionResult(
                dimension=DimensionType.POLYMARKET_LIQUIDITY,
                status=CheckStatus.FAIL,
                message=f"Polymarket 检测到包含模板占位符的伪造链接 ({url})，严禁编造链接！未开盘必须实事求是标注",
                detail={"url": url},
            )

        # 正常真实 URL
        return DimensionResult(
            dimension=DimensionType.POLYMARKET_LIQUIDITY,
            status=CheckStatus.PASS,
            message=f"Polymarket 真实交易市场链接已配置: {url}",
            detail={"url": url, "slug": slug},
        )
