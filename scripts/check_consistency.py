#!/usr/bin/env python3
"""
scripts/check_consistency.py
兼容垫片 (Shim Adapter)
本文件作为历史遗产向后兼容垫片，底层全面委托给全新 10/10 纯 DDD 洋葱六边形架构的 `校验/` 模块。
随着 `scripts/` 目录的逐步弱化与淘汰，未来命令请统一迁移至：
    python 校验/src/adapter/cli.py --system
    python 校验/src/adapter/cli.py --match <json_path>
"""

from __future__ import annotations
import sys
from pathlib import Path

# 将项目根目录置入 sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from 校验.src.adapter.cli import main as verifier_main

if __name__ == "__main__":
    raise SystemExit(verifier_main())



