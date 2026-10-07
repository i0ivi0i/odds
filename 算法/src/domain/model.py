"""领域层值对象 (Domain Value Objects)

定义纯数学维度的不可变值对象：
- OddsVector: 赔率向量（自校验、不可变、计算倒数与总抽水）
- ImpliedProbabilities: 真实去水无偏概率向量（自校验、不可变、精确求和）
"""

from typing import Sequence, Tuple


class OddsVector:
    """赔率向量值对象 (Value Object)
    
    业务规则：
    1. 必须包含至少 2 个结果赔率（两项盘或三项盘）；
    2. 每个赔率必须严格大于 1.0（否则非合法有效赔率）；
    3. 对象不可变（Immutable）。
    """
    __slots__ = ('_odds', '_inverse_probs', '_booksum')

    def __init__(self, odds: Sequence[float]):
        if not odds or len(odds) < 2:
            raise ValueError(f"OddsVector 必须包含至少 2 项赔率，实际获得 {len(odds) if odds else 0} 项")
        
        parsed_odds = []
        parsed_inverses = []
        for x in odds:
            try:
                val = float(x)
            except (ValueError, TypeError) as e:
                raise ValueError(f"非法赔率数值: {x}") from e
            if val <= 1.0:
                raise ValueError(f"赔率必须严格大于 1.0，实际数值: {val}")
            parsed_odds.append(val)
            parsed_inverses.append(1.0 / val)

        self._odds: Tuple[float, ...] = tuple(parsed_odds)
        self._inverse_probs: Tuple[float, ...] = tuple(parsed_inverses)
        self._booksum: float = sum(self._inverse_probs)

    @property
    def odds(self) -> Tuple[float, ...]:
        return self._odds

    @property
    def inverse_probs(self) -> Tuple[float, ...]:
        return self._inverse_probs

    @property
    def booksum(self) -> float:
        return self._booksum

    @property
    def margin(self) -> float:
        """庄家总水钱抽水 (Overround Margin = Booksum - 1.0)"""
        return self._booksum - 1.0

    def __len__(self) -> int:
        return len(self._odds)

    def __repr__(self) -> str:
        return f"OddsVector(odds={self._odds}, booksum={self._booksum:.4f})"


class ImpliedProbabilities:
    """无偏概率向量值对象 (Value Object)
    
    业务规则：
    1. 概率各项严格介于 0.0 与 1.0 之间；
    2. 概率总和严格收敛为 1.0 (容差 1e-10)；
    3. 对象不可变。
    """
    __slots__ = ('_probabilities', '_total')

    def __init__(self, probabilities: Sequence[float]):
        if not probabilities or len(probabilities) < 2:
            raise ValueError(f"概率向量必须包含至少 2 项，实际获得 {len(probabilities) if probabilities else 0} 项")

        parsed = tuple(float(p) for p in probabilities)
        self._probabilities = parsed
        self._total = sum(parsed)

    @property
    def probabilities(self) -> Tuple[float, ...]:
        return self._probabilities

    @property
    def total(self) -> float:
        return self._total

    def as_percentages(self, decimals: int = 2) -> Tuple[str, ...]:
        """格式化为百分比文本表达，如 ('46.06%', '27.60%', '26.34%')"""
        return tuple(f"{p * 100:.{decimals}f}%" for p in self._probabilities)

    def __len__(self) -> int:
        return len(self._probabilities)

    def __getitem__(self, idx: int) -> float:
        return self._probabilities[idx]

    def __repr__(self) -> str:
        return f"ImpliedProbabilities(probs={self._probabilities}, total={self._total:.6f})"
