import unittest
import os
import json

class TestOntologyLens(unittest.TestCase):
    def setUp(self):
        self.workspace_dir = os.path.abspath(".evoontology")
        self.v0_dir = os.path.join(self.workspace_dir, "versions", "ontology_v0")

    def test_workspace_and_active_version(self):
        """测试工作区与当前激活版本文件存在"""
        self.assertTrue(os.path.exists(self.workspace_dir), "EvoOntology 工作区目录不存在")
        active_json_path = os.path.join(self.workspace_dir, "active.json")
        self.assertTrue(os.path.exists(active_json_path), "active.json 不存在")
        with open(active_json_path, "r", encoding="utf-8") as f:
            active_data = json.load(f)
        self.assertIn("active_version", active_data)
        self.assertEqual(active_data["active_version"], "ontology_v0")

    def test_core_ontology_assets_exist(self):
        """测试 ontology_v0 5 大核心定义文件存在"""
        required_files = ["terms.json", "mappings.json", "relations.json", "constraints.json", "evidence.json"]
        for fname in required_files:
            fpath = os.path.join(self.v0_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"缺少本体核心文件: {fname}")

    def test_core_constraints_definitions(self):
        """测试 4 大核心关注探针（平博基准、亚盘假摔、高平真空、泊松底牌）正确注册"""
        constraints_path = os.path.join(self.v0_dir, "constraints.json")
        with open(constraints_path, "r", encoding="utf-8") as f:
            constraints_data = json.load(f)

        constraint_ids = [c["id"] for c in constraints_data]
        self.assertIn("constraint_pinnacle_stability", constraint_ids, "缺少平博定海神针探针")
        self.assertIn("constraint_headfake_rebound", constraint_ids, "缺少亚盘脉冲假摔探针")
        self.assertIn("constraint_draw_extreme_high", constraint_ids, "缺少高平筹码真空探针")
        self.assertIn("constraint_poisson_retention", constraint_ids, "缺少泊松底牌保护探针")

    def test_strict_non_deduction_boundary(self):
        """最高立宪测试：扫描本体层所有 JSON，确保绝无胜负预测、让球输赢判定或赔率死尺子逻辑"""
        forbidden_keywords = ["predict_outcome", "calc_handicap_winner", "home_win_rule", "win_rate_score", "定负", "必胜"]
        for root, _, files in os.walk(self.workspace_dir):
            for file in files:
                if file.endswith(".json"):
                    fpath = os.path.join(root, file)
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    for kw in forbidden_keywords:
                        self.assertNotIn(kw, content, f"本体资产文件 {file} 违规包含硬编码推演词汇: {kw}")

    def test_native_runtime_semantic_resolution(self):
        """测试 EvoOntology 原生 SemanticLayer 能够正常加载工作区并成功解析探针"""
        try:
            from evoontology.runtime.runtime import SemanticLayer
        except ImportError:
            self.skipTest("未安装 evoontology 包，跳过原生 runtime 测试")

        layer = SemanticLayer.load(self.workspace_dir)
        self.assertEqual(layer.version, "ontology_v0")
        
        # 测试 browse_semantics 检索平博
        browse_res = layer.execute("browse_semantics", {"query": "平博"})
        self.assertEqual(browse_res.get("status"), "ok")
        self.assertGreaterEqual(browse_res.get("matched_total", 0), 1)

        # 测试 resolve_semantics 解析假摔与平博探针
        resolve_res = layer.execute("resolve_semantics", {"mentions": ["平博", "假摔"]})
        self.assertEqual(resolve_res.get("status"), "ok")
        results = resolve_res.get("results", [])
        self.assertEqual(len(results), 2)
        
        # 验证探针约束被成功提取
        resolved_constraints = []
        for r in results:
            resolved_constraints.extend([c["id"] for c in r.get("constraints", [])])
        self.assertIn("constraint_pinnacle_stability", resolved_constraints)
        self.assertIn("constraint_headfake_rebound", resolved_constraints)

if __name__ == "__main__":
    unittest.main()
