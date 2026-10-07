"""
校验/src/domain/verifier.py
快照数据完整性纯领域检验引擎 (零外部依赖，纯 Python 原生规则判定)
"""

from __future__ import annotations
import re
from typing import Any, Dict, List

from 校验.src.domain.model import (
    CheckStatus,
    DimensionType,
    DimensionResult,
    VerificationReceipt,
)


class SnapshotVerifier:
    """
    快照数据完整性领域聚合根
    负责对 6 大黄金维度 + 1 阵容容错维度进行纯规则判定
    """

    def verify(self, snapshot: Dict[str, Any]) -> VerificationReceipt:
        match_id = str(snapshot.get("matchId") or snapshot.get("id") or "unknown")
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
                "league": snapshot.get("match", {}).get("league", "unknown"),
                "has_dual_track": has_dual_track,
                "tactics_present": bool(tactics),
                "profiling_present": bool(profiling),
            },
        )

    def _check_basic_stats(self, snapshot: Dict[str, Any]) -> DimensionResult:
        match_info = snapshot.get("match") or {}
        home = match_info.get("homeTeam") or snapshot.get("homeTeam")
        away = match_info.get("awayTeam") or snapshot.get("awayTeam")
        league = match_info.get("league") or snapshot.get("league")

        if not (home and away and league):
            return DimensionResult(
                dimension=DimensionType.BASIC_STATS,
                status=CheckStatus.FAIL,
                message="对阵基本信息残缺 (缺少主队/客队/联赛名称)",
                detail={"home": home, "away": away, "league": league},
            )

        # 检查攻防进失球物理数据 (近6场进失球、主客场进失球等)
        has_goals = False
        home_goals = match_info.get("homeGoals") or snapshot.get("homeGoals")
        away_goals = match_info.get("awayGoals") or snapshot.get("awayGoals")
        basic_text = snapshot.get("basicStatsText") or ""
        goals_stats = snapshot.get("goalsStats") or match_info.get("goalsStats")
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
        companies = markets.get("europeCompanies") or []

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
            for c in companies:
                init_data = c.get("initial") or {}
                latest_data = c.get("latest") or {}
                has_ret = "return_rate" in init_data or "returnRate" in init_data or "return_rate" in latest_data or "returnRate" in latest_data
                has_k = "kelly" in init_data or "kelly" in latest_data
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

        return DimensionResult(
            dimension=DimensionType.EUROPE_1X2,
            status=CheckStatus.PASS,
            message="欧洲指数(1X2)主流机构初即盘与返还率/凯利指数完整",
        )

    def _check_asian_handicap(self, snapshot: Dict[str, Any]) -> DimensionResult:
        text = snapshot.get("asianOddsText") or ""
        markets = snapshot.get("markets") or {}
        histories = markets.get("asianHistories") or []
        profiling = snapshot.get("profiling") or {}
        half_time = markets.get("halfTime") or {}

        has_data = len(text.strip()) > 20 or len(histories) > 0 or bool(profiling)
        if not has_data:
            return DimensionResult(
                dimension=DimensionType.ASIAN_HANDICAP,
                status=CheckStatus.FAIL,
                message="亚洲让球盘(AH)主流机构盘口水位缺失",
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
        text = snapshot.get("overUnderText") or ""
        markets = snapshot.get("markets") or {}
        histories = markets.get("overUnderHistories") or []

        has_data = len(text.strip()) > 20 or len(histories) > 0
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

        ts_count = len(timestamps)
        hist_count = len(histories)
        effective_count = max(ts_count, hist_count)

        # 铁律1: 必须包含时间戳，严禁静态初即两端冒充时序
        if effective_count == 0:
            return DimensionResult(
                dimension=DimensionType.TREND_HISTORY,
                status=CheckStatus.FAIL,
                message="变盘时序流水缺少分秒时间戳，严禁使用静态初即两端冒充时序",
                detail={"timestamps": 0, "histories": hist_count},
            )

        # 铁律2: 有效时间戳流水必须 >= 6 条
        if effective_count < 6:
            return DimensionResult(
                dimension=DimensionType.TREND_HISTORY,
                status=CheckStatus.FAIL,
                message=f"变盘时序流水记录不足 (仅有{effective_count}条时间戳记录，法定最低必须 >= 6行)",
                detail={"timestamps": ts_count, "histories": hist_count},
            )

        return DimensionResult(
            dimension=DimensionType.TREND_HISTORY,
            status=CheckStatus.PASS,
            message=f"变盘时序流水完整 (有效时间戳变盘记录={effective_count}项)",
            detail={"timestamps": ts_count, "histories": hist_count},
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
