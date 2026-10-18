import os
import shutil
import tempfile
import unittest
from pathlib import Path

from 校验.src.domain.ontology_probes import detect_ontology_probes
from 校验.src.domain.verifier import verify_memory_cognitive_cards


class TestSentinelDefenseAndArbitration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.temp_dir, "data_dir")
        os.makedirs(self.data_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_source_snapshot(self, match_id: str, content: str):
        path = os.path.join(self.data_dir, f"{match_id}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_sentinel_defense_triggers_on_sporttery_drop(self):
        """中国体彩单边降赔 >= 0.10 (如 1.92 -> 1.79 降 0.13) 时，必须触发 Sentinel_Defense (block)"""
        src = """# 【周日006】西乙 奥萨苏纳 vs 桑坦德竞技
- 比赛 ID：3013728
- 开球时间：2026-10-18 20:00

| 机构分层 | 机构名称 | 初盘主胜 | 初盘平局 | 初盘客胜 | 初盘返还率 | 即时主胜 | 即时平局 | 即时客胜 | 即时返还率 | 相对初盘位移 (主/平/客) |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 核心做市 | 澳彩 | 1.95 | 3.3 | 3.4 | 90.0% | 1.95 | 3.3 | 3.4 | 90.0% | 0.00/0.00/0.00 |
| 终端履约 | 中国体彩 | 1.92 | 3.5 | 3.1 | 88.56% | 1.79 | 3.55 | 3.46 | 88.55% | 0.86/0.92/0.90 |
"""
        probes = detect_ontology_probes(src)
        sentinel_probe = next((p for p in probes if p["term"] == "Sentinel_Defense"), None)
        self.assertIsNotNone(sentinel_probe, "体彩降赔 >= 0.10 必须触发 Sentinel_Defense")
        self.assertEqual(sentinel_probe["severity"], "block")
        self.assertIn("中国体彩", sentinel_probe["evidence"])

    def test_sentinel_defense_triggers_on_hkjc_drop_and_low_water(self):
        """香港马会降赔 >= 0.08 且亚盘低水 (<= 0.75) 拒赔时，必须触发 Sentinel_Defense"""
        src = """# 【周日006】西乙 测试比赛
- 比赛 ID：3013729
- 开球时间：2026-10-18 20:00

| 机构分层 | 机构名称 | 初盘主胜 | 初盘平局 | 初盘客胜 | 初盘返还率 | 即时主胜 | 即时平局 | 即时客胜 | 即时返还率 | 相对初盘位移 (主/平/客) |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 核心做市 | 香港马会 | 1.90 | 3.5 | 3.1 | 88.14% | 1.82 | 3.55 | 3.25 | 88.04% | 0.88/0.92/0.84 |

### 7. 香港马会 (欧亚双盘核心, 核心做市, cid=432)
#### 亚盘真实变盘流水
| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |
| :--- | :--- | ---: | ---: | :--- |
| 10-18 18:50 | 平手/半球 | 0.70 | 1.13 | 即 |
"""
        probes = detect_ontology_probes(src)
        sentinel_probe = next((p for p in probes if p["term"] == "Sentinel_Defense"), None)
        self.assertIsNotNone(sentinel_probe, "香港马会降水防守必须触发 Sentinel_Defense")
        self.assertEqual(sentinel_probe["severity"], "block")

    def test_headfake_ignores_monotonic_drop_and_cross_bookmaker_noise(self):
        """006 真实形态：皇冠全程半球死守未升盘，188Bet 开盘半一随后单向降至半球，绝不触发 HeadFake_Surge 误报"""
        src = """# 【周日006】西乙 奥萨苏纳 vs 桑坦德竞技
- 比赛 ID：3013728
- 开球时间：2026-10-18 20:00

### 2. 皇冠 (欧亚双盘核心, 核心做市, cid=281)
#### 亚盘真实变盘流水
| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |
| :--- | :--- | ---: | ---: | :--- |
| 10-18 18:58 | 半球 | 0.98 | 0.88 | 即 |
| 10-18 17:28 | 半球 | 1.01 | 0.85 | 即 |
| 10-18 14:14 | 半球 | 0.96 | 0.90 | 即 |
| 10-16 22:15 | 半球 | 0.97 | 0.89 | 早 |
| 09-21 16:42 | 半球 | 0.88 | 0.98 | 初盘 |

### 6. 188Bet (欧亚双盘核心, 核心做市, cid=976)
#### 亚盘真实变盘流水
| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |
| :--- | :--- | ---: | ---: | :--- |
| 10-18 18:58 | 半球 | 0.97 | 0.85 | 即 |
| 10-05 12:08 | 半球/一球 | 1.14 | 0.68 | 早 |
| 09-21 15:09 | 半球/一球 | 0.83 | 0.94 | 早 |
"""
        probes = detect_ontology_probes(src)
        headfake_probe = next((p for p in probes if p["term"] == "HeadFake_Surge"), None)
        self.assertIsNone(headfake_probe, "单向降盘及跨机构不应误报 HeadFake_Surge 假摔")

    def test_headfake_triggers_on_true_rebound_sequence(self):
        """单机构内部存在真实折返序列：初盘半球 -> 升半一挂 1.04 满水 -> 退回半球，必须精准触发 HeadFake_Surge"""
        src = """# 【周六002】测试联赛 汉堡 vs 斯图加特
- 比赛 ID：3099002
- 开球时间：2026-10-18 20:00

### 2. 皇冠 (欧亚双盘核心, 核心做市, cid=281)
#### 亚盘真实变盘流水
| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |
| :--- | :--- | ---: | ---: | :--- |
| 10-18 18:58 | 半球 | 0.98 | 0.88 | 即 |
| 10-18 12:00 | 半球/一球 | 1.06 | 0.82 | 即 |
| 10-17 10:00 | 半球 | 0.85 | 1.01 | 早 |
"""
        probes = detect_ontology_probes(src)
        headfake_probe = next((p for p in probes if p["term"] == "HeadFake_Surge"), None)
        self.assertIsNotNone(headfake_probe, "单机构内部存在先升后退闭环时必须触发 HeadFake_Surge")
        self.assertEqual(headfake_probe["severity"], "block")

    def test_cross_probe_arbitration_allows_sentinel_defense_rebuttal(self):
        """当同时触发外盘异动与 Sentinel_Defense 时，契约卡援引哨兵防守论证可使用平稳设防词汇顺利通过门禁"""
        match_id = "3013728"
        # 构造包含体彩大幅降水 (Sentinel_Defense) 的快照
        src_content = f"""# 【周日006】西乙 奥萨苏纳 vs 桑坦德竞技
- 比赛 ID：{match_id}
- 开球时间：2026-10-18 20:00

| 机构分层 | 机构名称 | 初盘主胜 | 初盘平局 | 初盘客胜 | 初盘返还率 | 即时主胜 | 即时平局 | 即时客胜 | 即时返还率 | 相对初盘位移 (主/平/客) |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 核心做市 | 澳彩 | 1.95 | 3.3 | 3.4 | 90.0% | 1.95 | 3.3 | 3.4 | 90.0% | 0.00/0.00/0.00 |
| 核心做市 | 香港马会 | 1.90 | 3.5 | 3.1 | 88.14% | 1.82 | 3.55 | 3.25 | 88.04% | 0.88/0.92/0.84 |
| 终端履约 | 中国体彩 | 1.92 | 3.5 | 3.1 | 88.56% | 1.79 | 3.55 | 3.46 | 88.55% | 0.86/0.92/0.90 |

### 2. 皇冠 (欧亚双盘核心, 核心做市, cid=281)
#### 亚盘真实变盘流水
| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |
| :--- | :--- | ---: | ---: | :--- |
| 10-18 18:58 | 半球 | 0.98 | 0.88 | 即 |
| 10-18 12:00 | 半球/一球 | 1.06 | 0.82 | 即 |
| 10-17 10:00 | 半球 | 0.85 | 1.01 | 早 |
"""
        self._create_source_snapshot(match_id, src_content)

        # 契约卡对质：指出虽然皇冠有波动假摔，但体彩与马会作为法定哨兵大幅降赔平稳设防，采纳哨兵防守为主线
        memory_content = f"""# 2026-10-18

| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 周日006 20:00 | 奥萨苏纳 vs 桑坦德竞技 | 主胜 (次选平局) | [-1] 让平（次选让胜） | 48.26% / 23.69% / 28.05% | 体彩哨兵断崖设防 | [奥萨苏纳 vs 桑坦德（平局 23.5¢ / 4.25倍）](https://polymarket.com/event/test-slug-osa-rac) |

## 深度分析

### 【周日006】奥萨苏纳 vs 桑坦德竞技 (西乙)
- **比赛ID**: {match_id}
- **开球时间**: 2026-10-18 20:00
- **胜负平**: 主胜 (次选平局)
- **让球**: [-1] 让平（次选让胜）
- **胜/平/负点概率 (OO-EPC去水)**: 48.26% / 23.69% / 28.05%
- **【图谱认知基因】**: `Sentinel_Defense 本土风控底牌` ➔ `Constantinou 市场分层`
- **【机位阻断对质】**: 显式对质 HeadFake_Surge 与 Sentinel_Defense (constraint_sentinel_defense)：虽然皇冠中盘由半一退回半球，但中国体彩主胜从 1.92 断崖砸至 1.79，香港马会降至 1.82 且平半 0.70 水拒赔客队。本土哨兵真金白银平稳设防，外盘退盘属于散户筹码平衡而非弃守，双向冲抵后采纳哨兵真实防守，主胜打出。
- **【认知契约卡】**:
  - **选择与排除依据**: 排除客胜依据：客队客战4连败0分；选择主胜依据：体彩与马会本土哨兵强力设防。
  - **关键拍板依据**: 体彩 1.79 极端防范。
  - **庄家博弈假说与竞争解释**: 主线假设：哨兵机构控制主胜赔付；竞争假设：防平。
  - **可推翻反证与改变条件**: 若体彩客胜跌破 2.80 则假设证伪。
"""
        ok, errors, count = verify_memory_cognitive_cards(
            memory_content,
            expected_matches=1,
            data_dir=self.data_dir
        )
        self.assertTrue(ok, f"双向机位冲抵后应顺利通过门禁，但被拦截: {errors}")
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
