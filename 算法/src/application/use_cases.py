"""应用层用例服务 (Application Use Cases)

负责应用用例编排与跨层数据传输 (DTO)：
- ConvertOddsUseCase: 赔率去水计算用例
- OddsConversionResult: 纯数据传输对象 (DTO)
"""

from typing import Sequence, Dict, Any, Type, Tuple, Optional
from ..domain.model import OddsVector, ImpliedProbabilities
from ..domain.calculator import OoEpcCalculator, MarginCalculatorStrategy
from ..domain.poisson import PoissonEngine, PoissonParams, PoissonResult


class OddsConversionResult:
    """去水转换结果数据传输对象 (DTO)"""
    __slots__ = ('_odds', '_probabilities', '_percentages', '_total', '_booksum', '_margin', '_algorithm')

    def __init__(
        self,
        odds: Tuple[float, ...],
        probabilities: Tuple[float, ...],
        percentages: Tuple[str, ...],
        total: float,
        booksum: float,
        margin: float,
        algorithm: str
    ):
        self._odds = odds
        self._probabilities = probabilities
        self._percentages = percentages
        self._total = total
        self._booksum = booksum
        self._margin = margin
        self._algorithm = algorithm

    @property
    def odds(self) -> Tuple[float, ...]:
        return self._odds

    @property
    def probabilities(self) -> Tuple[float, ...]:
        return self._probabilities

    @property
    def percentages(self) -> Tuple[str, ...]:
        return self._percentages

    @property
    def total_probability(self) -> float:
        return self._total

    @property
    def booksum(self) -> float:
        return self._booksum

    @property
    def margin(self) -> float:
        return self._margin

    @property
    def algorithm(self) -> str:
        return self._algorithm

    def to_dict(self) -> Dict[str, Any]:
        return {
            "algorithm": self._algorithm,
            "odds": list(self._odds),
            "probabilities": [round(p, 6) for p in self._probabilities],
            "percentages": list(self._percentages),
            "total_probability": round(self._total, 6),
            "booksum": round(self._booksum, 4),
            "margin": round(self._margin, 4)
        }


class ConvertOddsUseCase:
    """赔率去水应用用例 (Application Service)
    
    采用乐高策略注册表，默认绑定 Goto-OO-EPC，支持未来无缝扩展其他算法。
    """

    def __init__(self):
        self._strategies: Dict[str, Type[MarginCalculatorStrategy]] = {
            'goto': OoEpcCalculator,
            'oo-epc': OoEpcCalculator
        }

    def register_strategy(self, name: str, strategy: Type[MarginCalculatorStrategy]) -> None:
        """乐高卡扣：注册新的去水纯数学算法策略"""
        self._strategies[name.lower()] = strategy

    def execute(self, odds: Sequence[float], strategy: str = 'goto') -> OddsConversionResult:
        key = strategy.lower()
        if key not in self._strategies:
            supported = list(self._strategies.keys())
            raise ValueError(f"不支持的去水算法策略: '{strategy}', 支持的策略为: {supported}")

        # 1. 组装领域值对象并进行自校验
        odds_vector = OddsVector(odds)

        # 2. 调度领域纯数学计算服务
        calculator = self._strategies[key]
        implied: ImpliedProbabilities = calculator.calculate(odds_vector)

        # 3. 封装为不可变应用 DTO 返回
        algo_name = "Goto-OO-EPC" if key in ('goto', 'oo-epc') else key.upper()
        return OddsConversionResult(
            odds=odds_vector.odds,
            probabilities=implied.probabilities,
            percentages=implied.as_percentages(decimals=2),
            total=implied.total,
            booksum=odds_vector.booksum,
            margin=odds_vector.margin,
            algorithm=algo_name
        )


class CalculatePoissonUseCase:
    """泊松进球期望值与比分概率计算用例 (Application Service)"""

    def __init__(self, engine: Optional[PoissonEngine] = None):
        self._engine = engine or PoissonEngine()

    def execute(
        self,
        lambda_home: float,
        lambda_away: float,
        top_n: int = 6,
        apply_low_score_factors: bool = True,
    ) -> Dict[str, Any]:
        result: PoissonResult = self._engine.calculate(
            lambda_home=lambda_home,
            lambda_away=lambda_away,
            apply_low_score_factors=apply_low_score_factors,
        )
        return result.to_dict(top_n=top_n)
