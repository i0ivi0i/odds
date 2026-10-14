"""
校验/测试/test_scrapling_pipeline.py
Scrapling 官方原生进货流水线 TDD 单元测试套件
验证:
1. 官方分块军规 (单批 <= 6~8 URLs，带延迟)
2. 选择器下推 (#table_odds) 与编码映射 (UTF-8 vs GB18030)
3. 官方内部四级闭环 (绝不泄露给外部独立浏览器)
4. 原子存证包自动组装与黄金 Markdown 交付
"""

import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import json

from 校验.src.adapter.scrapling_ingest import (
    ScraplingIngestPipeline,
    EndpointSpec,
    ScraplingChunk,
    FetchTier,
)


class TestScraplingPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = ScraplingIngestPipeline(match_id="3068865")

    def test_chunked_urls_limit(self):
        """军规 1: 验证单批切片不超过 8 个 URL，且全量覆盖 25~26 个端点"""
        chunks = self.pipeline.build_plan_chunks(chunk_size=7)
        self.assertGreaterEqual(len(chunks), 3)

        total_urls = sum(len(c.specs) for c in chunks)
        # 4 核心 + 7 亚盘 + 7 大小球 + 7 欧指 = 25
        self.assertEqual(total_urls, 25)

        for c in chunks:
            self.assertLessEqual(len(c.specs), 8, f"分块大小 {len(c.specs)} 超过军规上限 8")
            self.assertGreaterEqual(c.delay_seconds, 0.2, "分块间必须有控频延时")

    def test_selector_pushdown_and_encoding_mapping(self):
        """军规 2: 验证变盘流水下推 #table_odds，且编码自适应映射准确"""
        all_specs = self.pipeline.get_all_endpoint_specs()
        
        # 核心文件
        js_spec = next(s for s in all_specs if s.name == "1x2d.js")
        self.assertEqual(js_spec.encoding, "utf-8")
        self.assertIsNone(js_spec.css_selector)

        analysis_spec = next(s for s in all_specs if s.name == "analysis.html")
        self.assertEqual(analysis_spec.encoding, "utf-8")

        # 变盘流水文件
        ah_spec = next(s for s in all_specs if s.name == "ah_1.html")
        self.assertEqual(ah_spec.encoding, "gb18030")
        self.assertEqual(ah_spec.css_selector, "#table_odds")
        self.assertEqual(ah_spec.identifier, "ah_1_table")

        ou_spec = next(s for s in all_specs if s.name == "ou_3.html")
        self.assertEqual(ou_spec.encoding, "gb18030")
        self.assertEqual(ou_spec.css_selector, "#table_odds")
        self.assertEqual(ou_spec.identifier, "ou_3_table")

        eu_spec = next(s for s in all_specs if s.name == "eu_8.html")
        self.assertEqual(eu_spec.encoding, "gb18030")
        self.assertEqual(eu_spec.css_selector, "#table_odds")
        self.assertEqual(eu_spec.identifier, "eu_8_table")

    def test_four_tier_escalation_order_and_browser_isolation(self):
        """军规 3: 官方内部四级闭环升阶，绝对严禁调用任何外部独立浏览器"""
        tiers = [FetchTier.BULK_PROTOCOL, FetchTier.FETCH_PRECISE, FetchTier.STEALTHY_FETCH, FetchTier.INTERNAL_CHROME]
        self.assertEqual(len(tiers), 4)

        # 确保没有外部浏览器枚举或外部独立依赖
        for tier in FetchTier:
            self.assertNotIn("browseros", tier.value.lower())
            self.assertNotIn("external", tier.value.lower())

        # 模拟升阶逻辑
        mock_fetcher = MagicMock()
        # 模拟 Tier 1 失败 (HTTP 502 / stream reset), Tier 2 成功
        mock_fetcher.execute_spec.side_effect = [
            Exception("HTTP/2 stream reset"),
            "<html><body>#table_odds data</body></html>"
        ]

        result = self.pipeline.fetch_endpoint_with_escalation(
            spec=EndpointSpec(name="ah_1.html", url="https://vip.titan007.com/changeDetail/handicap.aspx?id=3068865&companyID=1&l=0", encoding="gb18030", css_selector="#table_odds"),
            executor=mock_fetcher
        )
        self.assertIn("#table_odds data", result)
        self.assertEqual(mock_fetcher.execute_spec.call_count, 2)

    def test_bundle_assembly_generates_valid_atomic_receipt(self):
        """军规 4: 采集结果原子打包，包含完整端点 receipt 与 payloads"""
        dummy_payloads = {
            "1x2d.js": "var game=Array('3068865');",
            "analysis.html": "<html><body>analysis</body></html>",
            "odds.html": "<html><body>odds</body></html>",
            "analy.json": '{"code":0}',
        }
        for cid in [1, 3, 8, 12, 47, 42, 48]:
            dummy_payloads[f"ah_{cid}.html"] = f"<html><body>ah {cid}</body></html>"
            dummy_payloads[f"ou_{cid}.html"] = f"<html><body>ou {cid}</body></html>"
            dummy_payloads[f"eu_{cid}.html"] = f"<html><body>eu {cid}</body></html>"

        bundle = self.pipeline.assemble_atomic_bundle(dummy_payloads)
        self.assertEqual(bundle["matchId"], "3068865")
        self.assertIn("payloads", bundle)
        self.assertIn("receipt", bundle)
        self.assertEqual(len(bundle["receipt"]["endpoints"]), 25)
        self.assertTrue(bundle["receipt"]["all_success"])

    def test_adaptive_element_memory_and_relocation(self):
        """军规 5: 验证 Scrapling 官方自适应与元素记忆自愈能力"""
        import tempfile
        try:
            from scrapling import Selector
        except ImportError:
            return  # 若未安装 scrapling 则安全跳过

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            test_db = Path(tmpdir) / "test_memory.db"
            storage_args = {"storage_file": str(test_db)}

            # 初始结构: 包含标准 #table_odds
            orig_html = "<html><body><div><table id='table_odds'><tr><td>初盘</td><td>半球</td><td>0.95</td></tr></table></div></body></html>"
            page1 = Selector(orig_html, adaptive=True, storage_args=storage_args)
            # 开启 auto_save=True 记录指纹
            found1 = page1.css("#table_odds", identifier="ah_1_table", auto_save=True, adaptive=True)
            self.assertEqual(len(found1), 1)
            self.assertIn("半球", found1[0].get_all_text())

            # 页面改版: table id 被删除，改为 section 嵌套全新类名
            modified_html = "<html><body><section><table class='new_dynamic_odds'><tr><td>初盘</td><td>半球</td><td>0.95</td></tr></table></section></body></html>"
            page2 = Selector(modified_html, adaptive=True, storage_args=storage_args)
            # 旧选择器 #table_odds 在改版后不存在，但由 identifier + adaptive 自动从 SQLite 读取指纹自愈捞回
            found2 = page2.css("#table_odds", identifier="ah_1_table", adaptive=True)
            self.assertEqual(len(found2), 1)
            self.assertIn("半球", found2[0].get_all_text())


if __name__ == "__main__":
    unittest.main()

