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
from 校验.src.domain.verifier import SnapshotVerifier, get_match_property


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
    parser.add_argument("--match", type=str, help="从快照文件提取战术技统与波胆赔率并执行泊松对账")

    parsed = parser.parse_args(args)

    # 1. 快照分析或泊松进球期望值计算分支
    if parsed.match or parsed.poisson:
        snapshot = None
        l1, l2 = (None, None)

        if parsed.match:
            try:
                with open(parsed.match, "r", encoding="utf-8") as f:
                    snapshot = json.load(f)
                SnapshotVerifier().verify(snapshot)
            except Exception as e:
                sys.stderr.write(f"读取快照失败: {e}\n")
                return 1

            # 从战术技统推导基准期望 λ
            tech_items = snapshot.get("tactics", {}).get("technicalStats", {}).get("items", [])
            if len(tech_items) >= 2:
                t1, t2 = tech_items[0], tech_items[1]
                t1_att = t1.get("home_away_avg_goals") or t1.get("avg_goals") or 1.10
                t2_att = t2.get("home_away_avg_goals") or t2.get("avg_goals") or 0.90
                t1_def = (t1.get("conceded", 14) / 28.0) if t1.get("conceded") else 1.0
                t2_def = (t2.get("conceded", 14) / 28.0) if t2.get("conceded") else 1.0
                l1 = round((t1_att + t2_def) / 2.0, 2)
                l2 = round((t2_att + t1_def) / 2.0, 2)
            else:
                l1, l2 = (1.20, 1.00)

        if parsed.poisson:
            l1, l2 = parsed.poisson

        l1 = max(0.40, float(l1 or 1.20))
        l2 = max(0.40, float(l2 or 1.00))

        use_case = CalculatePoissonUseCase()
        try:
            result = use_case.execute(lambda_home=l1, lambda_away=l2, top_n=parsed.top)
        except Exception as e:
            sys.stderr.write(f"泊松计算失败: {e}\n")
            return 1

        # 若有快照，丰富队名与 Crown 波胆交叉对账
        if snapshot:
            home_team = get_match_property(snapshot, "homeTeam", "主队")
            away_team = get_match_property(snapshot, "awayTeam", "客队")
            result["home_team"] = home_team
            result["away_team"] = away_team

            crown_scores = snapshot.get("markets", {}).get("crowFullIndex", {}).get("correctScores", {}).get("flat", {})
            for s in result["top_scores"]:
                score_str = s["score"]
                if score_str in crown_scores:
                    c_odds = crown_scores[score_str]
                    s["crown_odds"] = c_odds
                    c_prob = round(1.0 / c_odds, 4)
                    s["crown_implied_prob"] = c_prob
                    s["crown_implied_percentage"] = f"{c_prob * 100:.2f}%"
                    diff = round(s["probability"] - c_prob, 4)
                    s["discrepancy_percentage"] = f"{diff * 100:+.2f}%"

        if parsed.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            title = f"[快照战术技统与 Crown 波胆泊松对账: {result.get('home_team', '主队')} vs {result.get('away_team', '客队')}]" if snapshot else f"[纯物理泊松进球期望值推演: 主队λ={l1:.2f}, 客队λ={l2:.2f}]"
            print(title)
            print(f"期望进球: 主队λ={l1:.2f}, 客队λ={l2:.2f} | 期望总进球: {result['expected_total_goals']}")
            dist = result['distribution_1x2']
            print(f"胜平负物理基准: 主胜={dist['home_win']} | 平局={dist['draw']} | 客胜={dist['away_win']}")
            print("Top 预测比分与 Crown 市场波胆对账:")
            for s in result['top_scores']:
                c_str = f" | Crown波胆: {s['crown_odds']:.2f} (市场隐含: {s.get('crown_implied_percentage')}, 物理偏差: {s.get('discrepancy_percentage')})" if "crown_odds" in s else ""
                print(f"  {s['score']} -> 泊松概率: {s['percentage']} (公允倍率: {s['fair_odds']:.2f}){c_str}")
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
