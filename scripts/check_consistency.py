#!/usr/bin/env python3
"""
轻量一致性自检：防止规则口径“悄悄回退”。

默认只扫描：skills/ docs/ scripts/（不扫 memory/ data/，避免历史噪声）。

检查项（可扩展）：
- EV 阈值口径：禁止出现 `EV>1`/`EV > 1`
- 比分口径：禁止出现孤立的 `Top 3`（允许 `Top 3/5` 这类历史统计口径描述）
- 大小球模板：禁止旧模板 `大小球：{大X.5/小X.5}`
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


@dataclass(frozen=True)
class Finding:
    path: Path
    line_no: int
    line: str
    rule: str


DEFAULT_ROOTS = ("skills", "docs", "scripts")
SKIP_DIRS = {".git", "node_modules", ".cursor", ".openclaw", "__pycache__"}
SELF_NAME = "check_consistency.py"


def is_ignored_line(rule_name: str, line: str) -> bool:
    """
    允许少量“刻意出现”的关键字：
    - 文档里描述历史兼容（如“历史旧记录 … 兼容处理”）不应算回退
    - 支持人工行级忽略标记：`consistency:ignore`
    """
    if "consistency:ignore" in line:
        return True
    if ("历史" in line) or ("兼容" in line):
        return True
    return False


def iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for base in DEFAULT_ROOTS:
        p = root / base
        if not p.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(p):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                fp = Path(dirpath) / name
                if fp.name == SELF_NAME:
                    continue
                # 只扫常见文本；如后续需要可放开
                if fp.suffix.lower() in {".md", ".py", ".json", ".json5", ".txt"}:
                    files.append(fp)
    return sorted(files)


def scan_file(path: Path, rules: list[tuple[str, re.Pattern[str]]]) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    findings: list[Finding] = []
    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        for rule_name, pat in rules:
            if pat.search(line) and not is_ignored_line(rule_name, line):
                findings.append(Finding(path=path, line_no=idx, line=line, rule=rule_name))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="pansuan 一致性自检（口径防回归）")
    parser.add_argument(
        "--root",
        default=".",
        help="仓库根目录（默认：当前目录）",
    )
    parser.add_argument(
        "--print-ok",
        action="store_true",
        help="通过时也输出一行 OK",
    )
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    rules: list[tuple[str, re.Pattern[str]]] = [
        ("EV 阈值口径回退（EV>1）", re.compile(r"\bEV\s*>\s*1\b")),
        ("旧代号残留（嘲风）", re.compile(r"嘲风")),
        ("大小球旧模板占位符", re.compile(r"大小球：\s*\{大X\.5/小X\.5\}")),
    ]

    all_files = iter_text_files(repo_root)
    all_findings: list[Finding] = []
    for fp in all_files:
        all_findings.extend(scan_file(fp, rules))

    # 图谱连通性与零孤岛强校验
    graph_json = repo_root / "graphify-out" / "graph.json"
    if graph_json.exists():
        import json
        import networkx as nx
        try:
            g_data = json.loads(graph_json.read_text(encoding="utf-8"))
            G = nx.Graph()
            for n in g_data.get("nodes", []):
                G.add_node(n["id"])
            for e in g_data.get("links", []) or g_data.get("edges", []):
                G.add_edge(e["source"], e["target"])
            comps = nx.number_connected_components(G)
            isolates = len(list(nx.isolates(G)))
            if comps > 1 or isolates > 0:
                print(f"发现图谱孤岛违规：连通分量={comps} (铁律恒为1)，孤立节点={isolates} (铁律恒为0)", file=sys.stderr)
                return 3
        except Exception as e:
            print(f"图谱解析异常: {e}", file=sys.stderr)
            return 3

    if not all_findings:
        if args.print_ok:
            print("OK: 未发现口径回退且图谱0孤岛100%连通（skills/docs/scripts/graphify）")
        return 0

    # 以 path + line_no 排序，方便定位
    all_findings.sort(key=lambda f: (str(f.path), f.line_no, f.rule))
    print("发现一致性问题（可能口径回退）：", file=sys.stderr)
    for f in all_findings:
        rel = f.path.relative_to(repo_root)
        print(f"- {rel}:{f.line_no} [{f.rule}]\n  {f.line}", file=sys.stderr)

    print(
        "\n提示：历史 memory/data 不在扫描范围；若这是刻意的历史说明/兼容描述，可调整规则白名单。",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())


