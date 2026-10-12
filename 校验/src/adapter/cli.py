"""
校验/src/adapter/cli.py
适配器层: 统一质量守门人命令行入口 (CLI)
支持：
  1. 单场比赛【推演源数据】完整性 6 维度穿透扫描与硬熔断: --match <md_path> [--json]
  2. 全库系统规范与图谱健康一致性巡检: --system [--print-ok]
"""

from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Optional

# 彻底免疫 Windows 控制台 GBK 编码异常 (防止 UnicodeEncodeError)
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 确保项目根目录在 sys.path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from 校验.src.application.use_cases import (
    VerifySnapshotUseCase,
    CheckConsistencyUseCase,
)
from 校验.src.domain.model import CheckStatus
from 校验.src.domain.assembler import SnapshotAssembler


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
        if receipt.overall_status == CheckStatus.PASS:
            msg = f"🎉 状态: 验收全部通过 (PASS) - 允许启动 10 步深度推演！"
        else:
            msg = f"⚠️ 状态: 验收存在警告 ({receipt.overall_status.value}) - 允许启动 10 步深度推演（请注意置顶未核实项）"
        if receipt.metadata.get("has_dual_track"):
            msg += "\n🔥 进阶: 已装载【物理客观底牌】与【散户偏见镜像】双轨实战数据，支持站在庄家视角反向破译！"
        lines.append(msg)
    else:
        lines.append(f"🚫 状态: 验收失败 ({receipt.overall_status.value}) - 存在核心数据缺口，物理熔断禁止推演！")
    lines.append(f"============================================================")
    return "\n".join(lines)


def run_match_verify(match_path: str, output_json: bool, max_age_minutes: Optional[int] = None) -> int:
    uc = VerifySnapshotUseCase()
    receipt = uc.execute(match_path, max_age_minutes=max_age_minutes)

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


def run_batch_verify(dir_path: str, max_age_minutes: Optional[int] = None, isolate_failed: bool = False) -> int:
    p = Path(dir_path)
    if not p.is_dir():
        print(f"❌ 批量安检失败: 目录不存在 ({dir_path})", file=sys.stderr)
        return 1
    md_files = [f for f in p.glob("*.md") if f.stem.isdigit()]
    if not md_files:
        print(f"❌ 批量安检失败: 目录下无比赛 ID 命名的 .md 【推演源数据】文件 ({dir_path})", file=sys.stderr)
        return 1

    uc = VerifySnapshotUseCase()
    failed = []
    failed_files = set()
    seen_ts = {}

    for f in md_files:
        receipt = uc.execute(str(f), max_age_minutes=max_age_minutes)
        if not receipt.is_valid:
            fail_msgs = [r.message for r in receipt.results if r.status == CheckStatus.FAIL]
            failed.append(f"{f.name}: 门禁安检未通过 ({receipt.overall_status.value}) - {'; '.join(fail_msgs)}")
            failed_files.add(f)
            continue

        # 跨场次时序去重防作弊核验 (同一批次不同比赛的时间戳不得完全碰撞)
        content = f.read_text(encoding="utf-8")
        timestamps = tuple(re.findall(r"\b\d{2}-\d{2}\s+\d{2}:\d{2}\b", content)[:10])
        if timestamps and len(timestamps) >= 3:
            if timestamps in seen_ts:
                failed.append(f"{f.name}: 与 {seen_ts[timestamps]} 变盘时间戳完全相同，判定为跨场次克隆作弊！")
                failed_files.add(f)
            else:
                seen_ts[timestamps] = f.name

        # 跨场次张冠李戴核验 (文件名 ID 与正文比赛 ID 必须一致)
        body_id = re.search(r"-\s*\*\*比赛\s*ID\*\*[：:]\s*(\d+)", content)
        if not body_id:
            failed.append(f"{f.name}: 正文缺少明确的比赛 ID 声明 (格式: - **比赛 ID**：xxx)！")
            failed_files.add(f)
        elif body_id.group(1) != f.stem:
            failed.append(f"{f.name}: 文件名 ID ({f.stem}) 与正文声明 ID ({body_id.group(1)}) 冲突，判定为冒名顶替！")
            failed_files.add(f)

        # 跨场次对阵重复核验
        title_m = re.search(r"#\s*【(.*?)】\S+\s+(\S+)\s+vs\s+(\S+)", content)
        if title_m:
            teams = f"{title_m.group(2)} vs {title_m.group(3)}"
            if teams in seen_ts.get("_teams", {}):
                failed.append(f"{f.name}: 对阵双方 ({teams}) 与 {seen_ts['_teams'][teams]} 完全相同，判定为跨场次文件复制造假！")
                failed_files.add(f)
            else:
                if "_teams" not in seen_ts:
                    seen_ts["_teams"] = {}
                seen_ts["_teams"][teams] = f.name

    if failed:
        if isolate_failed:
            quarantine_dir = p / ".quarantine"
            quarantine_dir.mkdir(parents=True, exist_ok=True)
            isolated_names = []
            for ff in failed_files:
                target = quarantine_dir / ff.name
                if target.exists():
                    target.unlink()
                ff.rename(target)
                isolated_names.append(ff.name)

            valid_files = [f for f in md_files if f not in failed_files]
            print(f"⚠️ 故障隔离触发: 已自动隔离 {len(isolated_names)} 场违规快照至 {quarantine_dir}: {', '.join(isolated_names)}")
            for err in failed:
                print(f"  ❌ [已隔离] {err}", file=sys.stderr)

            if valid_files:
                valid_ids = [f.stem for f in valid_files]
                print(f"✅ 批量安检通过 (故障隔离放行): 剩余 {len(valid_files)} 场【推演源数据】合法且无跨场克隆")
                print(f"📋 放行合格场次列表: {', '.join(valid_ids)}")
                return 0
            else:
                print(f"🚫 批量安检失败: 隔离后无有效【推演源数据】文件！", file=sys.stderr)
                return 1

        print(f"🚫 批量安检失败 ({len(failed)} 项违规):", file=sys.stderr)
        for err in failed:
            print(f"  ❌ {err}", file=sys.stderr)
        return 1

    print(f"✅ 批量安检通过: 全部 {len(md_files)} 场【推演源数据】合法且无跨场克隆")
    return 0


def run_assemble(input_json_path: str, output_md_path: Optional[str]) -> int:
    assembler = SnapshotAssembler()
    p = Path(input_json_path)
    if not p.exists():
        print(f"❌ 原始数据文件不存在: {input_json_path}", file=sys.stderr)
        return 1
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        md_content = assembler.assemble(data)
    except Exception as e:
        print(f"❌ 【推演源数据】装配失败: {e}", file=sys.stderr)
        return 1

    if output_md_path:
        out_p = Path(output_md_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(md_content, encoding="utf-8")
        st = out_p.stat()
        file_sha256 = hashlib.sha256(md_content.encode("utf-8")).hexdigest()
        mtime_str = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"🧾 [PHYSICAL_RECEIPT] 黄金【推演源数据】装配落盘完成: path={out_p.resolve()}, sha256={file_sha256}, mtime={mtime_str}, size={st.st_size}B")
        meta_p = out_p.parent / "meta.md"
        if meta_p.exists():
            assembler.update_meta(meta_p, data)
            print(f"✅ 自动同步赛程总览索引: {meta_p}")
    else:
        print(md_content)
    return 0


def run_sync_meta(dir_path: str) -> int:
    p = Path(dir_path)
    meta_p = p / "meta.md"
    if not meta_p.exists():
        print(f"❌ 同步失败: 目录下未找到 meta.md ({dir_path})", file=sys.stderr)
        return 1
    md_files = [f for f in p.glob("*.md") if f.stem.isdigit()]
    content = meta_p.read_text(encoding="utf-8")
    updated = 0
    for f in md_files:
        mid = f.stem
        target = f"{mid}.md (待分析抓取)"
        repl = f"[{mid}.md]({mid}.md) (✅已落盘)"
        if target in content:
            content = content.replace(target, repl)
            updated += 1
    meta_p.write_text(content, encoding="utf-8")
    print(f"✅ 赛程总览 meta.md 同步完成: 状态已对齐 {len(md_files)} 场落盘【推演源数据】 (更新了 {updated} 处状态)")
    return 0


def run_verify_memory(memory_path: str, expected_matches: Optional[int] = None) -> int:
    path = Path(memory_path)
    if not path.exists():
        print(f"❌ 门禁拦截: 每日记忆文件不存在: {memory_path}", file=sys.stderr)
        return 1

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ 门禁拦截: 每日记忆文件读取失败: {e}", file=sys.stderr)
        return 1

    from 校验.src.domain.verifier import verify_memory_cognitive_cards

    ok, errors, count = verify_memory_cognitive_cards(content, expected_matches=expected_matches)

    print("============================================================")
    print(f" 🛡️ 足球系统认知契约卡与图谱自愈前置门禁收据 ({path.name})")
    print("============================================================")
    if ok:
        print(f"🎉 状态: 验收全部通过 (PASS) - 共成功验证 {count} 场四维认知契约卡与图谱认知基因！")
        print("💡 结论: 赛前博弈假说与反证条件已 100% 冻结，学术论文审计链完整，放行对外交付与复盘！")
        print("============================================================")
        return 0
    else:
        print(f"❌ 状态: 验收拦截失败 (FAIL) - 发现 {len(errors)} 项契约违规：", file=sys.stderr)
        for err in errors:
            print(f"  - 🚫 {err}", file=sys.stderr)
        print("============================================================", file=sys.stderr)
        print("🛑 熔断警告: 认知契约卡未规范落盘前，严禁向前台发送任何表格，严禁汇报完成！", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="pansuan 校验守门人：单场【推演源数据】安检与全系统一致性巡检",
    )
    parser.add_argument(
        "--match",
        help="指定待检测的比赛【推演源数据】路径 (如 data/2026-10-10/3000480.md)",
    )
    parser.add_argument(
        "--batch",
        help="指定待批量检测的目录 (如 data/2026-10-10)，执行整批合法性与跨场次防克隆安检",
    )
    parser.add_argument(
        "--assemble",
        help="指定待装配的原始结构化 JSON 路径，自动组装为黄金 Markdown 【推演源数据】",
    )
    parser.add_argument(
        "--output",
        help="【推演源数据】装配输出路径 (如 data/2026-10-10/3000480.md)",
    )
    parser.add_argument(
        "--sync-meta",
        help="指定日期目录 (如 data/2026-10-10)，将所有已落盘【推演源数据】状态同步至 meta.md",
    )
    parser.add_argument(
        "--verify-memory",
        help="指定待核验的每日记忆文件路径 (如 memory/2026-10-12.md)，对【认知契约卡】与【图谱认知基因】执行硬门禁核验",
    )
    parser.add_argument(
        "--expected-matches",
        type=int,
        default=None,
        help="核验每日记忆时指定的期望深度分析场次数量 (如 10)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出【推演源数据】安检法定收据",
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
    parser.add_argument(
        "--max-age-minutes",
        type=int,
        default=None,
        help="【推演源数据】文件物理新鲜度最大允许分钟数 (如 30)，超期直接判定 STALE_SNAPSHOT 熔断",
    )
    parser.add_argument(
        "--isolate-failed",
        action="store_true",
        help="批量安检模式下启用故障隔离：将违规快照自动移入 .quarantine，若剩余快照有效则放行 (返回 0)",
    )

    args = parser.parse_args()

    # 门禁安全硬上限：严禁篡改 --max-age-minutes 传入超大数值逃避新鲜度熔断
    MAX_ALLOWABLE_FRESHNESS = 45
    if (args.batch or args.match) and args.max_age_minutes is not None:
        if args.max_age_minutes > MAX_ALLOWABLE_FRESHNESS or args.max_age_minutes <= 0:
            print(f"❌ 门禁安全违规: --max-age-minutes ({args.max_age_minutes}) 超过系统法定允许最大值 ({MAX_ALLOWABLE_FRESHNESS} 分钟)！严禁篡改参数绕过新鲜度核验！", file=sys.stderr)
            return 1

    # 优先级 0: 每日记忆认知契约卡门禁
    if args.verify_memory:
        return run_verify_memory(args.verify_memory, expected_matches=args.expected_matches)

    # 优先级 1: 【推演源数据】装配
    if args.assemble:
        return run_assemble(args.assemble, args.output)

    # 优先级 2: 同步 meta.md
    if args.sync_meta:
        return run_sync_meta(args.sync_meta)

    # 优先级 3: 批量安检
    if args.batch:
        return run_batch_verify(args.batch, max_age_minutes=args.max_age_minutes, isolate_failed=args.isolate_failed)

    # 优先级 4: 指定了单场比赛【推演源数据】进行安检
    if args.match:
        return run_match_verify(args.match, args.json, max_age_minutes=args.max_age_minutes)

    # 优先级 5: 系统巡检 (传了 --system 或默认行为)
    return run_system_check(args.root, args.print_ok or args.system)


if __name__ == "__main__":
    sys.exit(main())
