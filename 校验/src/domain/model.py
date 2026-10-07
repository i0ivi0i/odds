"""
校验/src/domain/model.py
纯 DDD 领域值对象与实体 (无外部依赖，纯 Python 原生)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class CheckStatus(Enum):
    """检测状态枚举"""
    PASS = "PASS"   # 检验合格，放行
    WARN = "WARN"   # 警告/未核实，允许继续但需强制置顶
    FAIL = "FAIL"   # 严重缺口，物理熔断阻断


class DimensionType(Enum):
    """数据安检黄金维度"""
    BASIC_STATS = "基础战绩与攻防数据"
    EUROPE_1X2 = "欧洲指数(1X2)初即盘"
    ASIAN_HANDICAP = "亚洲让球盘(AH)主流机构"
    OVER_UNDER = "大小球进球数(OU)主流机构"
    TREND_HISTORY = "分钟级变盘流水时序"
    CROWN_CORRECT_SCORE = "Crown皇冠全指数波胆"
    LINEUP_INJURY = "微观阵容与首发伤停"
    POLYMARKET_LIQUIDITY = "Polymarket预测市场真实流动性"


@dataclass(frozen=True)
class DimensionResult:
    """单一维度的检验结果 (不可变值对象)"""
    dimension: DimensionType
    status: CheckStatus
    message: str
    detail: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VerificationReceipt:
    """快照安检法定收据 (不可变值对象)"""
    match_id: str
    results: List[DimensionResult]
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if r.status == CheckStatus.FAIL)

    @property
    def warn_count(self) -> int:
        return sum(1 for r in self.results if r.status == CheckStatus.WARN)

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results if r.status == CheckStatus.PASS)

    @property
    def overall_status(self) -> CheckStatus:
        if self.failed_count > 0:
            return CheckStatus.FAIL
        if self.warn_count > 0:
            return CheckStatus.WARN
        return CheckStatus.PASS

    @property
    def is_valid(self) -> bool:
        """是否通过安检准许推演 (仅当无任何 FAIL 维度时为 True)"""
        return self.failed_count == 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "match_id": self.match_id,
            "overall_status": self.overall_status.value,
            "is_valid": self.is_valid,
            "counts": {
                "pass": self.pass_count,
                "warn": self.warn_count,
                "fail": self.failed_count,
            },
            "dimensions": [
                {
                    "name": r.dimension.value,
                    "status": r.status.value,
                    "message": r.message,
                    "detail": r.detail,
                }
                for r in self.results
            ],
            "metadata": self.metadata,
        }
