"""
校验/src/adapter/cli.py
适配器层: 统一质量守门人命令行入口 (CLI)
支持：
  1. 单场比赛快照数据完整性 6 维度穿透扫描与硬熔断: --match <json_path> [--json]
  2. 全库系统规范与图谱健康一致性巡检: --system [--print-ok]
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

# 确保项目根目录在 sys.path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from 校验.src.application.use_cases import (
    VerifySnapshotUseCase,
    CheckConsistencyUseCase,
)
from 校验.src.domain.model import CheckStatus


def format_receipt_console(receipt) -> str:
    lines = [
        f"============================================================",
        f" 🛡️ 足球系统数据完整性安检报告 (Match ID: {receipt.match_id})",
        f"============================================================",
    ]
    for r in receipt.results:
        symbol = "✅ [PASS]" if r.status == CheckStatus.PASS else (
            "⚠️ [WARN]" if r.status == CheckStatus.WARN else "❌ [FAIL]"
        )
        lines.append(f"{symbol} {r.dimension.value}: {r.message}")

    lines.append(f"------------------------------------------------------------")
    if receipt.is_valid:
        lines.append(f"🎉 状态: 验收全部通过 ({receipt.overall_status.value}) - 允许启动 10 步深度推演！")
    else:
        lines.append(f"🚫 状态: 验收失败 ({receipt.overall_status.value}) - 存在核心数据缺口，物理熔断禁止推演！")
    lines.append(f"============================================================")
    return "\n".join(lines)


def run_match_verify(match_path: str, output_json: bool) -> int:
    uc = VerifySnapshotUseCase()
    receipt = uc.execute(match_path)

    if output_json:
        print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2))
    else:
        output_text = format_receipt_console(receipt)
        if receipt.is_valid:
            print(output_text)
        else:
            print(output_text, file=sys.stderr)

    # 物理硬卡死法则：只要不是 valid，直接 exit 1
    return 0 if receipt.is_valid else 1


def run_system_check(root_dir: str, print_ok: bool) -> int:
    uc = CheckConsistencyUseCase()
    res = uc.execute(root_dir=root_dir)

    if not res["is_clean"]:
        print("❌ 发现系统一致性或健康异常：", file=sys.stderr)
        for f in res["findings"]:
            print(f"- {f['file']}:{f['line_no']} [{f['rule']}] {f['line']}", file=sys.stderr)
        if not res["graph_connected"]:
            print(f"- 图谱连通性异常: {res['graph_error']}", file=sys.stderr)
        if not res["algo_tests_passed"]:
            print(f"- 算法单测未通过: {res['algo_error']}", file=sys.stderr)
        return 2

    if print_ok:
        print("OK: 全库一致性与图谱连通性正常，算法单测全部通过。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="pansuan 校验守门人：单场数据快照安检与全系统一致性巡检",
    )
    parser.add_argument(
        "--match",
        help="指定待检测的比赛数据快照路径 (如 data/2026-10-07/2981506.json)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出快照安检法定收据",
    )
    parser.add_argument(
        "--system",
        action="store_true",
        help="执行全库一致性与图谱健康自检",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="系统巡检根目录 (默认当前目录)",
    )
    parser.add_argument(
        "--print-ok",
        action="store_true",
        help="系统巡检通过时输出 OK 提示",
    )

    args = parser.parse_args()

    # 优先级 1: 指定了比赛快照
    if args.match:
        return run_match_verify(args.match, args.json)

    # 优先级 2: 系统巡检 (传了 --system 或默认行为)
    return run_system_check(args.root, args.print_ok or args.system)


if __name__ == "__main__":
    sys.exit(main())
