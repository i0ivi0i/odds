"""适配器层 CLI 命令行入站驱动 (Adapter Layer CLI)

负责命令行入参解析、用例调用与标准格式化输出。
"""

import sys
import os
import json
import argparse
from typing import List, Optional

# 确保包根路径在 sys.path 中，支持直接命令行运行
_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from 算法.src.application.use_cases import ConvertOddsUseCase, CalculatePoissonUseCase


def main(args: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="纯数学算法工具箱 (Goto OO-EPC 去水算法 & 独立泊松进球期望值引擎)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python 算法/src/adapter/cli.py 2.10 3.40 3.55\n  python 算法/src/adapter/cli.py --poisson 1.50 1.20 --json"
    )
    parser.add_argument("odds", nargs="*", type=float, help="待去水的赔率列表 (如 2.10 3.40 3.55)")
    parser.add_argument("--strategy", default="goto", choices=["goto", "oo-epc"], help="去水算法策略 (默认: goto)")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")
    parser.add_argument("--decimals", type=int, default=2, help="百分比小数保留位数 (默认: 2)")
    parser.add_argument("--poisson", nargs=2, type=float, metavar=("L1", "L2"), help="计算双队泊松进球期望值 (主队λ 客队λ)")
    parser.add_argument("--top", type=int, default=6, help="输出 Top 比分个数 (默认: 6)")

    parsed = parser.parse_args(args)

    # 1. 泊松进球期望值计算分支
    if parsed.poisson:
        l1, l2 = parsed.poisson
        use_case = CalculatePoissonUseCase()
        try:
            result = use_case.execute(lambda_home=l1, lambda_away=l2, top_n=parsed.top)
        except Exception as e:
            sys.stderr.write(f"泊松计算失败: {e}\n")
            return 1

        if parsed.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"[纯物理泊松进球期望值推演: 主队λ={l1:.2f}, 客队λ={l2:.2f}]")
            print(f"期望总进球: {result['expected_total_goals']}")
            dist = result['distribution_1x2']
            print(f"胜平负物理基准: 主胜={dist['home_win']} | 平局={dist['draw']} | 客胜={dist['away_win']}")
            print("Top 预测比分分布:")
            for s in result['top_scores']:
                print(f"  {s['score']} -> 概率: {s['percentage']} (公允倍率: {s['fair_odds']:.2f})")
        return 0

    # 2. 赔率去水计算分支
    if not parsed.odds:
        parser.print_help()
        return 1

    use_case = ConvertOddsUseCase()
    try:
        result = use_case.execute(parsed.odds, strategy=parsed.strategy)
    except Exception as e:
        sys.stderr.write(f"去水计算失败: {e}\n")
        return 1

    if parsed.json:
        data = result.to_dict()
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        odds_str = "/".join(f"{x:.2f}" for x in result.odds)
        pct_str = "/".join(result.percentages)
        margin_pct = f"{result.margin * 100:.2f}%"
        print(f"[{result.algorithm} 纯数学去水计算]")
        print(f"输入赔率: {odds_str} (抽水水钱: {margin_pct})")
        print(f"无偏概率: {pct_str} (总概率: {result.total_probability * 100:.2f}%)")
        float_str = ", ".join(f"{p:.6f}" for p in result.probabilities)
        print(f"高精浮点: [{float_str}]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
