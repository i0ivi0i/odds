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


def probe_remote_provenance(match_id: str, timeout: float = 3.0) -> Tuple[bool, str]:
    """对源站轻量 1x2d.js 端点发起子秒级物理探针，核实真实物理服务器响应与场次存活状态"""
    import urllib.request
    url = f"https://1x2d.titan007.com/{match_id}.js"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Referer": "https://titan007.com/",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            if status != 200:
                return False, f"源站返回非 200 状态码: {status}"
            content = resp.read()
            if len(content) < 20:
                return False, f"源站返回报文过短 ({len(content)} 字节)，疑似空盘"
            if match_id.encode("utf-8") not in content:
                return False, f"源站 1x2d.js 报文未包含比赛 ID {match_id}"
            return True, f"源站物理核验通过 (HTTP 200, length={len(content)}B)"
    except Exception as e:
        return False, f"源站网络探针连接失败: {e}"


def run_match_verify(
    match_path: str,
    output_json: bool,
    max_age_minutes: Optional[int] = None,
    verify_network: bool = False,
) -> int:
    uc = VerifySnapshotUseCase()
    receipt = uc.execute(match_path, max_age_minutes=max_age_minutes)

    if receipt.is_valid and verify_network:
        ok, msg = probe_remote_provenance(receipt.match_id)
        if not ok:
            print(f"❌ NETWORK_PROVENANCE_DESYNC: 源站网络物理抽验失败 ({msg})！判定为伪造或断网快照！", file=sys.stderr)
            return 1
        if not output_json:
            print(f"🌐 [NETWORK_PROVENANCE_PASS] {msg}")

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


def run_match_verification(
    match_path: str,
    as_json: bool = False,
    max_age_minutes: Optional[int] = None,
    verify_network: bool = False,
) -> int:
    """单场门禁检验统一方法 (兼容单测与内部调用)"""
    return run_match_verify(
        match_path=match_path,
        output_json=as_json,
        max_age_minutes=max_age_minutes,
        verify_network=verify_network,
    )


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


def run_batch_verify(
    dir_path: str,
    max_age_minutes: Optional[int] = None,
    isolate_failed: bool = False,
    verify_network: bool = False,
) -> int:
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

        # 联网物理探针抽验 (若启用)
        if verify_network:
            ok, msg = probe_remote_provenance(f.stem)
            if not ok:
                failed.append(f"{f.name}: 源站网络物理抽验失败 ({msg})！")
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
    from 校验.src.domain.raw_parser import Titan007RawParser
    from 校验.src.domain.assembler import _normalize_company_name

    assembler = SnapshotAssembler()
    p = Path(input_json_path)
    if not p.exists():
        print(f"❌ 原始数据文件不存在: {input_json_path}", file=sys.stderr)
        return 1
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        raw_files_dict = data.get("rawFiles") or {}
        if isinstance(raw_files_dict, dict) and raw_files_dict.get("1x2d.js"):
            parsed_wire = Titan007RawParser().parse_1x2d_js(str(raw_files_dict["1x2d.js"]))
            wire_by_comp = parsed_wire.get("byCompany") or {}
            euro_entries = (data.get("markets") or {}).get("europeCompanies") or data.get("europe1x2") or []
            for row in euro_entries:
                if not isinstance(row, dict):
                    continue
                std_c = _normalize_company_name(str(row.get("company") or ""))
                if std_c in wire_by_comp:
                    w_entry = wire_by_comp[std_c]
                    w_init = [float(x) for x in w_entry["initialOdds"]]
                    w_live = [float(x) for x in w_entry["liveOdds"]]
                    init_raw = row.get("initialOdds") or (row.get("initial") or {}).get("odds") or []
                    live_raw = row.get("liveOdds") or (row.get("latest") or {}).get("odds") or []
                    if len(init_raw) == 3 and len(live_raw) == 3:
                        r_init = [float(x) for x in init_raw]
                        r_live = [float(x) for x in live_raw]
                        if max(abs(r_init[i] - w_init[i]) for i in range(3)) > 0.015 or max(abs(r_live[i] - w_live[i]) for i in range(3)) > 0.015:
                            raise ValueError(
                                f"RAW_PROVENANCE_MISMATCH: 机构【{std_c}】输入欧指 ({r_init}->{r_live}) "
                                f"与 rawFiles['1x2d.js'] 原始报文 ({w_init}->{w_live}) 不符，拒绝装配！"
                            )
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

        # U3: 自动写入 raw/{matchId}.json 单文件原子存证包与 SHA-256 封条，清理旧碎文件目录
        mid = str(data.get("matchId") or out_p.stem).strip()
        raw_parent = out_p.parent / "raw"
        raw_parent.mkdir(parents=True, exist_ok=True)
        raw_files_dict = data.get("rawFiles") or {}
        existing_raw: dict[str, str] = {}
        if isinstance(raw_files_dict, dict):
            existing_raw = dict(raw_files_dict)

        target_atomic_json = raw_parent / f"{mid}.json"
        manifest_obj = Titan007RawParser.build_atomic_bundle(mid, md_content, existing_raw)
        target_atomic_json.write_text(
            json.dumps(manifest_obj, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # 彻底清理旧的 28 个碎文件目录 (如果存在)
        legacy_loose_dir = raw_parent / mid
        if legacy_loose_dir.exists() and legacy_loose_dir.is_dir():
            import shutil
            shutil.rmtree(legacy_loose_dir, ignore_errors=True)

        print(f"🧾 [PHYSICAL_RECEIPT] 黄金【推演源数据】装配落盘完成: path={out_p.resolve()}, sha256={file_sha256}, mtime={mtime_str}, size={st.st_size}B, atomic_bundle={target_atomic_json.resolve()}")
        meta_p = out_p.parent / "meta.md"
        if meta_p.exists():
            assembler.update_meta(meta_p, data)
            print(f"✅ 自动同步赛程总览索引: {meta_p}")
    else:
        print(md_content)
    return 0


def run_assemble_bundle(bundle_json_path: str, output_md_path: Optional[str]) -> int:
    """从单文件原子存证包 raw/{matchId}.json (或输入 bundle) 离线装配黄金 Markdown 并清理旧碎文件目录"""
    import shutil
    from 校验.src.domain.raw_parser import Titan007RawParser

    parser = Titan007RawParser()
    assembler = SnapshotAssembler()
    p = Path(bundle_json_path)
    if not p.exists() or not p.is_file():
        print(f"❌ 单文件原子包不存在: {bundle_json_path}", file=sys.stderr)
        return 1

    try:
        bundle_obj = json.loads(p.read_text(encoding="utf-8"))
        raw_files = bundle_obj.get("payloads") or bundle_obj.get("rawFiles") or {}
        match_id_str = str(bundle_obj.get("matchId") or p.stem).strip()

        # 官方 Discover Markets 探针: 若缺少或未解析出有效 polymarket.json，自动尝试官方双向检索发现
        pm_content = str(raw_files.get("polymarket.json") or "").strip()
        if not pm_content or len(pm_content) < 5 or '"slug"' not in pm_content:
            from 校验.src.domain.polymarket_official_resolver import PolymarketOfficialResolver
            pm_resolver = PolymarketOfficialResolver()
            resolved, pm_info = pm_resolver.resolve_raw_bundle(bundle_obj)
            if resolved:
                print(f"🎯 [OFFICIAL_POLYMARKET] 官方 Discover Markets 自动命中链上标的: {pm_info}")
                raw_files = bundle_obj.get("payloads") or bundle_obj.get("rawFiles") or {}
                p.write_text(json.dumps(bundle_obj, ensure_ascii=False, indent=2), encoding="utf-8")

        meta_md_txt = ""
        meta_md_path = p.parent.parent / "meta.md"
        if meta_md_path.exists():
            try:
                meta_md_txt = meta_md_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass

        data, extracted_raw = parser.parse_raw_payloads(match_id_str, raw_files, meta_md_txt)
        md_content = assembler.assemble(data)
    except Exception as e:
        print(f"❌ 单文件原子包装配失败: {e}", file=sys.stderr)
        return 1

    if output_md_path:
        out_p = Path(output_md_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(md_content, encoding="utf-8")
        st = out_p.stat()
        file_sha256 = hashlib.sha256(md_content.encode("utf-8")).hexdigest()
        mtime_str = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        mid = str(data.get("matchId") or out_p.stem).strip()
        raw_parent = out_p.parent / "raw"
        raw_parent.mkdir(parents=True, exist_ok=True)
        target_atomic_json = raw_parent / f"{mid}.json"

        # 生成并落盘单文件原子存证包
        atomic_bundle = Titan007RawParser.build_atomic_bundle(mid, md_content, extracted_raw)
        target_atomic_json.write_text(
            json.dumps(atomic_bundle, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # 彻底清理旧的 28 个碎文件目录 (如果存在)
        legacy_loose_dir = raw_parent / mid
        if legacy_loose_dir.exists() and legacy_loose_dir.is_dir():
            shutil.rmtree(legacy_loose_dir, ignore_errors=True)

        print(f"🧾 [PHYSICAL_RECEIPT] 单文件原子【推演源数据】装配落盘完成: path={out_p.resolve()}, sha256={file_sha256}, mtime={mtime_str}, size={st.st_size}B, atomic_bundle={target_atomic_json.resolve()}")
        meta_p = out_p.parent / "meta.md"
        if meta_p.exists():
            assembler.update_meta(meta_p, data)
            print(f"✅ 自动同步赛程总览索引: {meta_p}")
    else:
        print(md_content)
    return 0


def run_resolve_polymarket(path_or_id: str) -> int:
    """按 Polymarket 官方 Discover Markets API 检索并补齐单文件原子存证包"""
    p = Path(path_or_id)
    if not p.exists() or not p.is_file():
        # 尝试查找 data/*/{path_or_id}.json
        matches = list(Path("data").glob(f"*/raw/{path_or_id}.json"))
        if matches:
            p = matches[0]
        else:
            print(f"❌ 找不到原子存证包文件: {path_or_id}", file=sys.stderr)
            return 1

    from 校验.src.domain.polymarket_official_resolver import PolymarketOfficialResolver
    resolver = PolymarketOfficialResolver()
    try:
        bundle_obj = json.loads(p.read_text(encoding="utf-8"))
        ok, msg = resolver.resolve_raw_bundle(bundle_obj)
        if ok:
            p.write_text(json.dumps(bundle_obj, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ [OFFICIAL_POLYMARKET] 成功解析并回填 Polymarket 官方标的: {msg}")
            return 0
        else:
            print(f"⚠️ [OFFICIAL_POLYMARKET] 检索结果: {msg}")
            return 1
    except Exception as e:
        print(f"❌ 解析失败: {e}", file=sys.stderr)
        return 1


def run_plan_scrapling_chunks(match_id: str, chunk_size: int = 7, as_json: bool = False) -> int:
    """输出某场比赛 Scrapling 原生分块规划矩阵 (遵循官方 <= 6~8 URLs 军规与选择器下推)"""
    from 校验.src.adapter.scrapling_ingest import ScraplingIngestPipeline
    pipeline = ScraplingIngestPipeline(match_id=match_id)
    chunks = pipeline.build_plan_chunks(chunk_size=chunk_size)
    if as_json:
        out = []
        for c in chunks:
            out.append({
                "chunk_index": c.chunk_index,
                "delay_seconds": c.delay_seconds,
                "specs": [
                    {
                        "name": s.name,
                        "url": s.url,
                        "encoding": s.encoding,
                        "css_selector": s.css_selector,
                        "category": s.category,
                    }
                    for s in c.specs
                ]
            })
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"📦 Scrapling 原生分块矩阵规划 (Match ID: {match_id}): 共 {len(chunks)} 批次")
        for c in chunks:
            print(f"  - 批次 {c.chunk_index}: {len(c.specs)} URLs (延时 {c.delay_seconds}s)")
            for s in c.specs:
                sel = f" [selector: {s.css_selector}]" if s.css_selector else ""
                print(f"    * {s.name} ({s.encoding}){sel} -> {s.url}")
    return 0


def run_fetch_match(match_id: str, target_date: Optional[str] = None, output_md: Optional[str] = None) -> int:
    """通过 Scrapling 原生流水线执行单场进货与原子组装"""
    import time
    from 校验.src.adapter.scrapling_ingest import ScraplingIngestPipeline
    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")

    pipeline = ScraplingIngestPipeline(match_id=match_id)
    specs = pipeline.get_all_endpoint_specs()
    chunks = pipeline.build_plan_chunks()

    print(f"⚡ [SCRAPLING_INGEST_START] 启动比赛 {match_id} 进货 (共 {len(specs)} 端点, {len(chunks)} 分块)")
    payloads = {}
    for chunk in chunks:
        for spec in chunk.specs:
            try:
                content = pipeline.fetch_endpoint_with_escalation(spec)
                payloads[spec.name] = content
            except Exception as e:
                print(f"⚠️ 端点抓取异常: {spec.name}: {e}", file=sys.stderr)
                payloads[spec.name] = ""
        import random
        # 拟人随机抖动 (Jitter: 0.3s ~ 0.65s)，粉碎等间隔机械节拍特征
        time.sleep(chunk.delay_seconds + random.uniform(0.1, 0.35))

    bundle = pipeline.assemble_atomic_bundle(payloads)
    raw_dir = Path("data") / target_date / "raw"
    raw_json_path = raw_dir / f"{match_id}.json"
    pipeline.save_bundle(bundle, raw_json_path)
    print(f"✅ 原子存证包已生成: {raw_json_path.resolve()}")

    if not output_md:
        output_md = str(Path("data") / target_date / f"{match_id}.md")

    return run_assemble_bundle(str(raw_json_path), output_md)


def run_ingest_match(
    match_id: str,
    target_date: Optional[str] = None,
    output_md: Optional[str] = None,
    max_age_minutes: Optional[int] = 30,
) -> int:
    """专职搬运工一体化进货与门禁机械臂: 进货抓取 -> 原子装配 -> 门禁验证 (单命令闭环)"""
    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")
    if not output_md:
        output_md = str(Path("data") / target_date / f"{match_id}.md")

    print(f"🚀 [INGEST_MATCH_START] 启动单场一体化进货: match_id={match_id}, date={target_date}")
    fetch_ret = run_fetch_match(match_id, target_date=target_date, output_md=output_md)
    if fetch_ret != 0:
        print(f"🚫 [INGEST_MATCH_FAILED] 抓取装配失败 (exit {fetch_ret})，物理熔断禁止推演！", file=sys.stderr)
        return fetch_ret

    print(f"🔍 [INGEST_MATCH_VERIFY] 启动单场门禁安检: {output_md}")
    verify_ret = run_match_verification(output_md, as_json=False, max_age_minutes=max_age_minutes)
    if verify_ret == 0:
        print(f"🎉 [INGEST_MATCH_SUCCESS] 比赛 {match_id} 进货与门禁检验双合格 (PASS)！")
    else:
        print(f"🚫 [INGEST_MATCH_REJECTED] 比赛 {match_id} 门禁检验未通过 (exit {verify_ret})！", file=sys.stderr)
    return verify_ret


def run_graph_affected(node_name: str, depth: int = 2) -> int:
    """调用官方 graphify.affected 执行因果涟漪影响传播分析"""
    graph_path = Path("graphify-out/graph.json")
    if not graph_path.exists():
        print(f"❌ 知识图谱文件不存在: {graph_path}", file=sys.stderr)
        return 1

    try:
        import graphify.affected as aff
        G = aff.load_graph(graph_path)
        formatted = aff.format_affected(G, node_name, depth=depth)
        print(f"🕸️ [GRAPHIFY_AFFECTED] 种子节点【{node_name}】因果涟漪影响分析 (深度={depth}):")
        print(formatted)
        return 0
    except Exception as e:
        print(f"❌ 因果涟漪影响分析异常: {e}", file=sys.stderr)
        return 1


def run_graph_reflect(if_stale: bool = True) -> int:
    """调用官方 graphify.reflect 刷新 Learning Overlay 与 LESSONS.md 错题反思"""
    mem_dir = Path("graphify-out/memory")
    if not mem_dir.exists() or not list(mem_dir.glob("*.md")):
        mem_dir = Path("memory")
    out_path = Path("graphify-out/reflections/LESSONS.md")
    graph_path = Path("graphify-out/graph.json")
    analysis_path = Path("graphify-out/.graphify_analysis.json")
    labels_path = Path("graphify-out/.graphify_labels.json")

    try:
        import graphify.reflect as ref
        if if_stale:
            is_fresh = ref.lessons_fresh(
                out_path=out_path,
                memory_dir=mem_dir,
                graph_path=graph_path if graph_path.exists() else None,
                analysis_path=analysis_path if analysis_path.exists() else None,
                labels_path=labels_path if labels_path.exists() else None,
            )
            if is_fresh and out_path.exists():
                print(f"⚡ [GRAPHIFY_REFLECT] 反思导览仍然新鲜 (Fresh)，跳过重复计算")
                return 0

        res_path, summary = ref.reflect(
            memory_dir=mem_dir,
            out_path=out_path,
            graph_path=graph_path if graph_path.exists() else None,
            analysis_path=analysis_path if analysis_path.exists() else None,
            labels_path=labels_path if labels_path.exists() else None,
        )
        print(f"💡 [GRAPHIFY_REFLECT] 错题反思与学习覆盖层刷新完成: {res_path} (提取了 {len(summary)} 条反思经验)")
        return 0
    except Exception as e:
        print(f"❌ 错题反思刷新异常: {e}", file=sys.stderr)
        return 1


def run_graph_query(query: str, mode: str = "bfs", budget: int = 1000) -> int:
    """针对当场盘口具体特征对 5.6MB 知识图谱进行靶向穿透检索 (基于 NetworkX)"""
    graph_path = Path("graphify-out/graph.json")
    if not graph_path.exists():
        print(f"❌ 知识图谱文件不存在: {graph_path}", file=sys.stderr)
        return 1

    try:
        from networkx.readwrite import json_graph
        import networkx as nx
        data = json.loads(graph_path.read_text(encoding="utf-8"))
        G = json_graph.node_link_graph(data, edges="links")

        terms = [t.lower() for t in re.split(r"[\s,;，；]+", query) if len(t) >= 2]
        scored = []
        for nid, ndata in G.nodes(data=True):
            label = str(ndata.get("label", "")).lower()
            desc = str(ndata.get("description", "")).lower()
            score = sum(2 for t in terms if t in label) + sum(1 for t in terms if t in desc)
            if score > 0:
                scored.append((score, nid, ndata.get("label", nid), ndata.get("community", 0)))
        scored.sort(reverse=True)

        if not scored:
            print(f"🔍 [GRAPHIFY_QUERY] 未在图谱中直接匹配到关键词: {query} (建议换词或查阅 graphify-out/wiki/)")
            return 0

        start_nodes = [nid for _, nid, _, _ in scored[:3]]
        visited = set()
        subgraph_nodes = []

        for sn in start_nodes:
            if sn in visited:
                continue
            if mode.lower() == "dfs":
                path_nodes = list(nx.dfs_preorder_nodes(G, source=sn, depth_limit=2))
            else:
                path_nodes = list(nx.bfs_tree(G, source=sn, depth_limit=2).nodes())
            for n in path_nodes:
                if n not in visited:
                    visited.add(n)
                    subgraph_nodes.append(n)

        print(f"🧠 [GRAPHIFY_QUERY] 盘口疑难靶向穿透检索: 【{query}】 (模式={mode.upper()}, 命中起点={len(start_nodes)}, 展开节点={len(subgraph_nodes)})")
        total_tokens = 0
        for nid in subgraph_nodes:
            ndata = G.nodes[nid]
            label = ndata.get("label", nid)
            desc = ndata.get("description", "")
            source_loc = ndata.get("source_location", "")
            comm = ndata.get("community", "")
            node_text = f"• [{comm}] {label}"
            if source_loc:
                node_text += f" ({source_loc})"
            if desc:
                node_text += f"\n  {desc[:120]}"
            print(node_text)
            total_tokens += len(node_text) // 2
            if total_tokens >= budget:
                print(f"  ... (达到 budget 预算上限 {budget} 字符，截断保护上下文)")
                break

        return 0
    except Exception as e:
        print(f"❌ 靶向图谱检索异常: {e}", file=sys.stderr)
        return 1


def run_assemble_raw_dir(raw_dir_path: str, output_md_path: Optional[str]) -> int:
    """从 raw/{matchId}/ 目录或单文件 raw/{matchId}.json 直接读取全量原始报文，直出 .md 与原子存证包"""
    from 校验.src.domain.raw_parser import Titan007RawParser

    parser = Titan007RawParser()
    assembler = SnapshotAssembler()
    raw_path = Path(raw_dir_path)
    if not raw_path.exists():
        print(f"❌ 原始报文路径不存在: {raw_dir_path}", file=sys.stderr)
        return 1

    try:
        data, raw_files = parser.parse_raw_directory(raw_path)
        md_content = assembler.assemble(data)
    except Exception as e:
        print(f"❌ 【推演源数据】原始报文直装失败: {e}", file=sys.stderr)
        return 1

    if output_md_path:
        out_p = Path(output_md_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(md_content, encoding="utf-8")
        st = out_p.stat()
        file_sha256 = hashlib.sha256(md_content.encode("utf-8")).hexdigest()
        mtime_str = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        mid = str(data.get("matchId") or out_p.stem).strip()
        raw_parent = out_p.parent / "raw"
        raw_parent.mkdir(parents=True, exist_ok=True)

        # 写入单一原子存证包
        target_atomic_json = raw_parent / f"{mid}.json"
        atomic_bundle = Titan007RawParser.build_atomic_bundle(mid, md_content, raw_files)
        target_atomic_json.write_text(
            json.dumps(atomic_bundle, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # 彻底清理旧的 28 个碎文件目录 (如果存在)
        legacy_loose_dir = raw_parent / mid
        if legacy_loose_dir.exists() and legacy_loose_dir.is_dir():
            import shutil
            shutil.rmtree(legacy_loose_dir, ignore_errors=True)

        print(f"🧾 [PHYSICAL_RECEIPT] 零转录原生【推演源数据】装配落盘完成: path={out_p.resolve()}, sha256={file_sha256}, mtime={mtime_str}, size={st.st_size}B, atomic_bundle={target_atomic_json.resolve()}")
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


def run_verify_memory(
    memory_path: str,
    expected_matches: Optional[int] = None,
    data_dir: Optional[str] = None,
) -> int:
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

    ok, errors, count = verify_memory_cognitive_cards(
        content,
        expected_matches=expected_matches,
        data_dir=data_dir,
    )

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


def run_audit_integrity(target_path: str) -> int:
    """执行五重轮番数据纯净度、极值数学零丢失与单调子序列穿透质检"""
    from 校验.src.domain.integrity_auditor import IntegrityAuditor, AuditStatus

    auditor = IntegrityAuditor()
    p = Path(target_path)
    if not p.exists():
        print(f"❌ 质检失败: 路径不存在 ({target_path})", file=sys.stderr)
        return 1

    md_files = []
    if p.is_file() and p.suffix == ".md":
        md_files = [p]
    elif p.is_dir():
        md_files = sorted([f for f in p.glob("*.md") if f.stem.isdigit()])
    else:
        print(f"❌ 质检失败: 无效的目标路径 ({target_path})", file=sys.stderr)
        return 1

    if not md_files:
        print(f"❌ 质检失败: 目录下未找到任何以比赛 ID 命名的 .md 文件 ({target_path})", file=sys.stderr)
        return 1

    print("============================================================")
    print(" 🛡️ 足球系统全链路数据纯净度与五重轮番穿透质检报告")
    print("============================================================")

    all_passed = True
    total_extrema_lost = 0
    total_inversions = 0
    total_fabricated = 0
    summary_rows = []

    for md_f in md_files:
        mid = md_f.stem
        raw_f = md_f.parent / "raw" / f"{mid}.json"
        if not raw_f.exists():
            print(f"❌ [Match {mid}] 缺少原始存证包 raw/{mid}.json！", file=sys.stderr)
            all_passed = False
            continue

        report = auditor.audit_match(str(raw_f), str(md_f))
        status_icon = "✅ [PASS]" if report.is_valid else "❌ [FAIL]"
        print(f"{status_icon} 比赛 {mid}:")
        for res in report.results:
            icon = "  ✓" if res.status == AuditStatus.PASS else "  ✗"
            print(f"{icon} {res.dimension.value}: {res.message}")

        if not report.is_valid:
            all_passed = False

        total_extrema_lost += report.extremum_lost_count
        total_inversions += report.temporal_inversions_count
        total_fabricated += report.fabricated_rows_count
        summary_rows.append((mid, report.is_valid, report.extremum_coverage_rate, report.total_raw_rows, report.total_md_rows))

    print("------------------------------------------------------------")
    print(f"📊 汇总结算卡 (共全量穿透质检 {len(md_files)} 场比赛):")
    for mid, ok, ext_rate, r_rows, m_rows in summary_rows:
        sym = "✅" if ok else "❌"
        pct = f"{ext_rate * 100:.1f}%"
        ratio = ((1 - m_rows / r_rows) * 100) if r_rows else 0
        print(f"  {sym} 比赛 {mid}: 极值保留率 {pct} | 原始流水 {r_rows}行 -> 提纯 {m_rows}行 (瘦身 {ratio:.1f}%)")

    print("============================================================")
    if all_passed and total_extrema_lost == 0 and total_inversions == 0 and total_fabricated == 0:
        print("🎉 最终裁定: 100% 纯净保真 (PASS)！零极值丢失、零时序倒置、零伪造插值！")
        return 0
    else:
        print(f"❌ 最终裁定: 发现数据失真或偏差 (FAIL)！极值丢失={total_extrema_lost}, 时序倒置={total_inversions}, 伪造插值={total_fabricated}", file=sys.stderr)
def run_diagnose_gate(file_path: str) -> int:
    """深度剖析单场文件的门禁健康状况，打印各做市商时序、封条状态与静默判定"""
    p = Path(file_path)
    if not p.exists():
        print(f"❌ 文件不存在: {file_path}", file=sys.stderr)
        return 1

    content = p.read_text(encoding="utf-8")
    st = p.stat()
    mtime_dt = datetime.fromtimestamp(st.st_mtime)
    age_min = (datetime.now() - mtime_dt).total_seconds() / 60.0

    print("=" * 60)
    print(f" 🔍 足球系统门禁深度自诊断报告: {p.name}")
    print("=" * 60)
    print(f"📁 文件路径: {p.resolve()}")
    print(f"🕒 物理修改时间: {mtime_dt.strftime('%Y-%m-%d %H:%M:%S')} (距今 {age_min:.1f} 分钟)")

    # 提取各做市商时间戳
    core_companies = {
        "澳彩": ["澳彩", "澳"],
        "Crown": ["皇冠", "Crown", "crown"],
        "Bet365": ["Bet365", "bet365", "365"],
        "易胜博": ["易胜博"],
        "平博": ["平博", "Pinnacle", "pinnacle"],
        "香港马会": ["香港马会", "马会", "HKJC"],
        "188": ["188", "188bet", "金宝博"],
    }
    company_latest_dts = {}
    year = mtime_dt.year
    for cname, aliases in core_companies.items():
        c_pat = rf"(?:###\s*(?:\d+[\.、\s]*)?(?:{'|'.join(aliases)})).*?(?=(?:\n###\s+[^\#]|\Z))"
        m_block = re.search(c_pat, content, re.DOTALL | re.IGNORECASE)
        if m_block:
            c_ts = re.findall(r"\b(\d{2}-\d{2}\s+\d{2}:\d{2})\b", m_block.group(0))
            if c_ts:
                c_max_s = max(c_ts)
                company_latest_dts[cname] = c_max_s

    print("\n📊 核心机构最新时序水位:")
    if company_latest_dts:
        for cname, ts_str in company_latest_dts.items():
            print(f"  - {cname:8s}: {ts_str}")
        overall_max = max(company_latest_dts.values())
        print(f"\n⚡ 全盘最新时序标记: {overall_max}")
    else:
        print("  ⚠️ 未提取到核心机构时间戳")

    # 封条与原子存证状态
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    target_mid = p.stem
    atomic_bundle_p = p.parent / "raw" / f"{target_mid}.json"
    if not atomic_bundle_p.exists() and p.parent.name == ".quarantine":
        atomic_bundle_p = p.parent.parent / "raw" / f"{target_mid}.json"

    print(f"\n🔐 SHA-256 内容哈希: {content_hash}")
    if atomic_bundle_p.exists():
        try:
            b_obj = json.loads(atomic_bundle_p.read_text(encoding="utf-8"))
            exp_sha = b_obj.get("markdown_sha256")
            print(f"📦 对应原子存证包: {atomic_bundle_p.name} (已封存)")
            print(f"🛡️ 封条匹配核验: {'✅ 吻合 (PASS)' if exp_sha == content_hash else '❌ 篡改 (TAMPERED)'}")
        except Exception as e:
            print(f"⚠️ 读取原子存证异常: {e}")
    else:
        print("⚠️ 未发现对应的 raw/*.json 原子存证包")
    print("=" * 60)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="pansuan 校验守门人：单场【推演源数据】安检与全系统一致性巡检",
    )
    parser.add_argument(
        "--diagnose-gate",
        help="指定待诊断的【推演源数据】路径，深度自查各做市商时间戳、时序水位、封条匹配与静默状态",
    )
    parser.add_argument(
        "--audit-integrity",
        help="指定待穿透质检的【推演源数据】文件或日期目录 (如 data/2026-10-13)，执行五重轮番数据纯净度与极值零丢失对账",
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
        "--assemble-bundle",
        help="指定待装配的单文件原子防伪包 (如 data/2026-10-13/raw/3068865.json)，离线装配黄金 Markdown 与单一原子包",
    )
    parser.add_argument(
        "--assemble-raw-dir",
        help="指定待装配的原始报文目录或单文件原子包 (如 data/2026-10-13/raw/3068865)，零大模型转录直出黄金 Markdown 与原子存证包",
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
        "--data-dir",
        default=None,
        help="核验每日记忆时交叉比对的物理源数据目录 (如 data/2026-10-12)",
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
    parser.add_argument(
        "--verify-network",
        action="store_true",
        help="启用源站物理网络抽验 (子秒级探针核验 1x2d.js 源站存活与响应状态，杜绝离线伪造 raw.json)",
    )
    parser.add_argument(
        "--plan-scrapling-chunks",
        metavar="MATCH_ID",
        help="输出官方 Scrapling 分块规划矩阵 (用于并发搬运工分批抓取)",
    )
    parser.add_argument(
        "--fetch-match",
        metavar="MATCH_ID",
        help="通过 Scrapling 原生流水线执行单场进货与原子组装",
    )
    parser.add_argument(
        "--resolve-polymarket",
        metavar="PATH_OR_ID",
        help="通过 Polymarket 官方 Discover Markets API 检索并自动补齐 raw/{matchId}.json 中的 polymarket.json 报文",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="进货或核验的目标销售日 (如 2026-10-14，默认当天)",
    )
    parser.add_argument(
        "--ingest-match",
        metavar="MATCH_ID",
        help="专职搬运工一体化进货与门禁机械臂 (进货拉取 -> 原子组装 -> 门禁验证单命令闭环)",
    )
    parser.add_argument(
        "--graph-affected",
        metavar="NODE_NAME",
        help="调用官方 graphify.affected 执行因果涟漪影响传播分析",
    )
    parser.add_argument(
        "--graph-reflect",
        action="store_true",
        help="调用官方 graphify.reflect 刷新 Learning Overlay 与 LESSONS.md 错题反思",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制刷新反思覆盖层 (忽略新鲜度检查)",
    )
    parser.add_argument(
        "--graph-query",
        metavar="QUERY",
        help="针对当场盘口具体特征对 5.6MB 知识图谱进行靶向穿透检索",
    )
    parser.add_argument(
        "--mode",
        default="bfs",
        choices=["bfs", "dfs"],
        help="知识图谱检索遍历模式 (默认 bfs, 可选 dfs)",
    )
    parser.add_argument(
        "--dfs",
        action="store_true",
        help="知识图谱深度优先遍历模式 (等同于 --mode dfs)",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        help="因果涟漪影响传播分析遍历深度 (默认 2)",
    )
    parser.add_argument(
        "--budget",
        type=int,
        default=1000,
        help="知识图谱检索上下文保护预算字符数 (默认 1000)",
    )

    args = parser.parse_args()

    # 门禁安全硬上限：严禁篡改 --max-age-minutes 传入超大数值逃避新鲜度熔断
    MAX_ALLOWABLE_FRESHNESS = 45
    if (args.batch or args.match or args.ingest_match) and args.max_age_minutes is not None:
        if args.max_age_minutes > MAX_ALLOWABLE_FRESHNESS or args.max_age_minutes <= 0:
            print(f"❌ 门禁安全违规: --max-age-minutes ({args.max_age_minutes}) 超过系统法定允许最大值 ({MAX_ALLOWABLE_FRESHNESS} 分钟)！严禁篡改参数绕过新鲜度核验！", file=sys.stderr)
            return 1

    # 优先级 -3: Graphify 官方高阶增智工具链
    if args.graph_affected:
        return run_graph_affected(args.graph_affected, depth=args.depth)
    if args.graph_reflect:
        return run_graph_reflect(if_stale=not args.force)
    if args.graph_query:
        query_mode = "dfs" if args.dfs else args.mode
        return run_graph_query(args.graph_query, mode=query_mode, budget=args.budget)

    # 优先级 -2.5: 一体化单场进货与门禁机械臂
    if args.ingest_match:
        return run_ingest_match(
            args.ingest_match,
            target_date=args.date,
            output_md=args.output,
            max_age_minutes=args.max_age_minutes if args.max_age_minutes is not None else 30,
        )

    # 优先级 -2: Scrapling 分块规划与原生进货
    if args.plan_scrapling_chunks:
        return run_plan_scrapling_chunks(args.plan_scrapling_chunks, as_json=args.json)
    if args.fetch_match:
        return run_fetch_match(args.fetch_match, target_date=args.date, output_md=args.output)
    if args.resolve_polymarket:
        return run_resolve_polymarket(args.resolve_polymarket)

    # 优先级 -1.5: 门禁自诊断深度排查
    if args.diagnose_gate:
        return run_diagnose_gate(args.diagnose_gate)

    # 优先级 -1: 数据纯净度五重轮番穿透质检
    if args.audit_integrity:
        return run_audit_integrity(args.audit_integrity)

    # 优先级 0: 每日记忆认知契约卡门禁
    if args.verify_memory:
        return run_verify_memory(args.verify_memory, expected_matches=args.expected_matches, data_dir=args.data_dir)

    # 优先级 1: 【推演源数据】装配
    if args.assemble_bundle:
        return run_assemble_bundle(args.assemble_bundle, args.output)
    if args.assemble_raw_dir:
        return run_assemble_raw_dir(args.assemble_raw_dir, args.output)
    if args.assemble:
        return run_assemble(args.assemble, args.output)

    # 优先级 2: 同步 meta.md
    if args.sync_meta:
        return run_sync_meta(args.sync_meta)

    # 优先级 3: 批量安检
    if args.batch:
        return run_batch_verify(
            args.batch,
            max_age_minutes=args.max_age_minutes,
            isolate_failed=args.isolate_failed,
            verify_network=args.verify_network,
        )

    # 优先级 4: 指定了单场比赛【推演源数据】进行安检
    if args.match:
        return run_match_verify(
            args.match,
            args.json,
            max_age_minutes=args.max_age_minutes,
            verify_network=args.verify_network,
        )

    # 优先级 5: 系统巡检 (传了 --system 或默认行为)
    return run_system_check(args.root, args.print_ok or args.system)


if __name__ == "__main__":
    sys.exit(main())
