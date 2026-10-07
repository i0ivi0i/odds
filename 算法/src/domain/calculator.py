"""领域层计算服务与策略接口 (Domain Service & Strategy Protocol)

纯数学领域核心算子，实现乐高积木式可插拔策略。
包含：
- MarginCalculatorStrategy: 抽水去水计算策略抽象基类/协议
- OoEpcCalculator: 东京大学 Shota Goto (2026) 等置信标准误差去水核心算法 (Algorithm 5)
"""

import math
from typing import Protocol, List
from .model import OddsVector, ImpliedProbabilities


class MarginCalculatorStrategy(Protocol):
    """乐高积木卡扣：纯数学去水计算器抽象协议
    
    所有未来的新算法（如 Shin知情交易模型、Logit凸组合模型等）只需实现此协议，
    即可无缝插入领域服务中，实现零破坏扩展。
    """
    @staticmethod
    def calculate(vector: OddsVector, total: float = 1.0) -> ImpliedProbabilities:
        ...


class OoEpcCalculator:
    """东京大学 Goto (2026) OO-EPC 官方原版纯数学去水核心引擎
    
    算法来源：
    Shota Goto & Kaito Goto (2026), arXiv:2604.17194v1, Algorithm 5.
    官方开源包：goto-conversion v4.0.3 原生纯 Python 分支实现。
    
    数学推导：
    1. 倒数概率：pi_i = 1.0 / odds_i
    2. 标准误差：SE_i = sqrt((pi_i - pi_i^2) / pi_i) = sqrt(1.0 - pi_i)
    3. 等置信步长：step = (sum(pi) - total) / sum(SE)
    4. 无偏概率：p_i = pi_i - step * SE_i
    5. 防御性回退：若任意 p_i <= 0 或总水钱 sum(pi) <= 1.0，优雅回退为简单比例归一化 pi_i / sum(pi)
    """

    @staticmethod
    def calculate(vector: OddsVector, total: float = 1.0) -> ImpliedProbabilities:
        inverses: List[float] = list(vector.inverse_probs)
        booksum: float = vector.booksum

        # 标准误差 SE = sqrt((p - p^2) / p) = sqrt(1 - p)
        ses: List[float] = [math.sqrt(max(0.0, 1.0 - p)) for p in inverses]
        sum_se: float = sum(ses)

        if sum_se > 0.0 and booksum > total:
            step: float = (booksum - total) / sum_se
            output_probs: List[float] = [p - (s * step) for p, s in zip(inverses, ses)]
        else:
            output_probs = [0.0] * len(inverses)

        # 官方防御性回退检查 (Imprudent Odds Fallback)
        if any(p <= 0.0 for p in output_probs) or (booksum <= total):
            normalizer = booksum / total
            output_probs = [p / normalizer for p in inverses]

        return ImpliedProbabilities(output_probs)
