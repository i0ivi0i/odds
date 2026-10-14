import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
import tempfile
import shutil

from 校验.src.adapter.cli import (
    run_ingest_match,
    run_graph_affected,
    run_graph_reflect,
    run_graph_query,
)


class TestAssemblyLineAndGraphify(unittest.TestCase):
    """测试现代化装配车间机械臂与 Graphify 官方高阶增智工具链"""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(self.test_dir, ignore_errors=True))

    @patch("校验.src.adapter.cli.run_fetch_match")
    @patch("校验.src.adapter.cli.run_match_verification")
    def test_run_ingest_match_success(self, mock_verify, mock_fetch):
        """测试 --ingest-match 一体化机械臂顺利闭环 (进货 -> 门禁 -> exit 0)"""
        mock_fetch.return_value = 0
        mock_verify.return_value = 0

        target_date = "2026-10-15"
        output_md = str(self.test_dir / "3008269.md")

        ret = run_ingest_match(
            match_id="3008269",
            target_date=target_date,
            output_md=output_md,
            max_age_minutes=30,
        )

        self.assertEqual(ret, 0)
        mock_fetch.assert_called_once_with(
            "3008269", target_date=target_date, output_md=output_md
        )
        mock_verify.assert_called_once_with(
            output_md, as_json=False, max_age_minutes=30
        )

    @patch("校验.src.adapter.cli.run_fetch_match")
    def test_run_ingest_match_fetch_fail(self, mock_fetch):
        """测试 --ingest-match 当抓取装配失败时立即熔断返回 1"""
        mock_fetch.return_value = 1

        ret = run_ingest_match(match_id="3008269")
        self.assertEqual(ret, 1)

    def test_run_graph_affected_node(self):
        """测试官方 graphify.affected 因果涟漪影响传播分析"""
        ret = run_graph_affected("核心心法：足球庄家精算视角与净赔付最小化破译（第一性原理）", depth=2)
        # 只要系统存在 graphify-out/graph.json，应能正常分析并返回 0
        self.assertEqual(ret, 0)

    def test_run_graph_reflect(self):
        """测试官方 graphify.reflect 学习覆盖层与错题反思刷新"""
        ret = run_graph_reflect(if_stale=True)
        self.assertEqual(ret, 0)

    def test_run_graph_query(self):
        """测试官方针对具体盘口特征的靶向穿透检索"""
        ret = run_graph_query("假摔震仓 Winkelmann", mode="bfs", budget=1000)
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main()
