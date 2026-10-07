"""
算法/src/domain/poisson.py
纯 DDD 泊松进球期望值与比分概率领域模型 (Zero-Drift 100% 零偏差对齐)
无任何外部重量级依赖，纯 Python 原生数学实现
"""

from __future__ import annotations
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ScoreItem:
    """单一比分及其概率值对象 (Immutable Value Object)"""
    home_goals: int
    away_goals: int
    score: str
    probability: float
    fair_odds: float

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "probability": round(self.probability, 6),
            "percentage": f"{self.probability * 100:.2f}%",
            "fair_odds": round(self.fair_odds, 2),
        }


@dataclass(frozen=True)
class PoissonParams:
    """泊松计算参数 (Dixon-Coles 修正与边界配置)"""
    low_score_factors: Dict[Tuple[int, int], float]
    max_goals: int = 8
    lambda_min: float = 0.4
    lambda_max: float = 3.5

    @classmethod
    def default(cls, config_path: Optional[str] = "config/poisson_params.json") -> PoissonParams:
        """从配置文件加载参数，带健壮回退"""
        factors = {
            (0, 0): 1.10,
            (1, 0): 1.05,
            (0, 1): 1.05,
            (1, 1): 1.10,
        }
        max_g = 8
        l_min = 0.4
        l_max = 3.5

        if config_path and Path(config_path).exists():
            try:
                raw = json.loads(Path(config_path).read_text(encoding="utf-8"))
                low_raw = raw.get("low_score_factors", {})
                factors = {}
                for k, v in low_raw.items():
                    a, b = k.split(":")
                    factors[(int(a), int(b))] = float(v)
                max_g = int(raw.get("max_goals", 8))
                lb = raw.get("lambda_bounds", {})
                l_min = float(lb.get("min", 0.4))
                l_max = float(lb.get("max", 3.5))
            except Exception:
                pass

        return cls(
            low_score_factors=factors,
            max_goals=max_g,
            lambda_min=l_min,
            lambda_max=l_max,
        )


@dataclass(frozen=True)
class PoissonResult:
    """泊松比分推演结果聚合"""
    lambda_home: float
    lambda_away: float
    all_scores: List[ScoreItem]
    home_win_prob: float
    draw_prob: float
    away_win_prob: float

    def top_scores(self, n: int = 6) -> List[ScoreItem]:
        return self.all_scores[:n]

    def to_dict(self, top_n: int = 6) -> dict:
        return {
            "lambda_home": self.lambda_home,
            "lambda_away": self.lambda_away,
            "expected_total_goals": round(self.lambda_home + self.lambda_away, 2),
            "distribution_1x2": {
                "home_win": f"{self.home_win_prob * 100:.2f}%",
                "draw": f"{self.draw_prob * 100:.2f}%",
                "away_win": f"{self.away_win_prob * 100:.2f}%",
            },
            "top_scores": [item.to_dict() for item in self.top_scores(top_n)],
        }


class PoissonEngine:
    """泊松分布纯领域计算引擎 (Domain Service)"""
    def __init__(self, params: Optional[PoissonParams] = None):
        self._params = params or PoissonParams.default()

    @staticmethod
    def _pmf(lamb: float, k: int) -> float:
        """纯标准库单变量泊松概率质量函数"""
        return math.exp(-lamb) * (lamb ** k) / math.factorial(k)

    def calculate(
        self,
        lambda_home: float,
        lambda_away: float,
        apply_low_score_factors: bool = True,
    ) -> PoissonResult:
        """计算双队进球联合泊松分布与全量比分矩阵"""
        l1 = max(self._params.lambda_min, min(self._params.lambda_max, float(lambda_home)))
        l2 = max(self._params.lambda_min, min(self._params.lambda_max, float(lambda_away)))
        max_g = self._params.max_goals
        low_factors = self._params.low_score_factors if apply_low_score_factors else {}

        raw_scores: List[Tuple[int, int, float]] = []
        for i in range(max_g):
            for j in range(max_g):
                p = self._pmf(l1, i) * self._pmf(l2, j)
                p *= float(low_factors.get((i, j), 1.0))
                raw_scores.append((i, j, p))

        total_p = sum(p for _, _, p in raw_scores)
        if total_p <= 0:
            raise ValueError(f"泊松总概率异常 (total_p={total_p})，请检查输入参数")

        # 归一化并排序
        score_items: List[ScoreItem] = []
        p_home_win = 0.0
        p_draw = 0.0
        p_away_win = 0.0

        for i, j, p in raw_scores:
            norm_p = p / total_p
            odds = 1.0 / norm_p if norm_p > 0 else 999.0
            score_items.append(ScoreItem(
                home_goals=i,
                away_goals=j,
                score=f"{i}:{j}",
                probability=norm_p,
                fair_odds=odds,
            ))
            if i > j:
                p_home_win += norm_p
            elif i == j:
                p_draw += norm_p
            else:
                p_away_win += norm_p

        score_items.sort(key=lambda x: -x.probability)

        return PoissonResult(
            lambda_home=l1,
            lambda_away=l2,
            all_scores=score_items,
            home_win_prob=p_home_win,
            draw_prob=p_draw,
            away_win_prob=p_away_win,
        )
