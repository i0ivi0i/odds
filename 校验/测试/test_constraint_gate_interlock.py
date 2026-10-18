import os
import shutil
import tempfile
import unittest
from pathlib import Path
from 校验.src.domain.verifier import verify_memory_cognitive_cards


class TestConstraintGateInterlock(unittest.TestCase):
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

    def test_memory_passes_when_no_block_triggered(self):
        """当源数据未触发任何 block 级探针时，规范的认知契约卡应顺利通过门禁"""
        match_id = "3099001"
        # 构造一份普通的、无脉冲假摔、无欧亚背离、无平博异常的干净源数据
        src_content = f"""# 【周六001】测试联赛 主队 vs 客队
- 比赛 ID：{match_id}
- 开球时间：2026-10-18 20:00

| 核心做市 | 澳彩 | 2.10 | 3.30 | 3.20 | 90% | 2.10 | 3.30 | 3.20 |
| 核心做市 | 平博 | 2.15 | 3.35 | 3.25 | 95% | 2.15 | 3.35 | 3.25 |

## 五、Crown 皇冠全指数波胆
| 1:0 | 6.50 | 0:0 | 8.50 | 0:1 | 7.50 |
"""
        self._create_source_snapshot(match_id, src_content)

        memory_content = f"""# 2026-10-18

| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 周六001 20:00 | 主队 vs 客队 | 主胜 (次选平局) | [-1] 让胜（次选让平） | 45.00% / 28.00% / 27.00% | 平稳控水设防 | [主队 vs 客队（平局 28.0¢ / 3.57倍）](https://polymarket.com/event/test-slug-2026-10-18) |

## 深度分析

### 【周六001】主队 vs 客队 (测试联赛)
- **比赛ID**: {match_id}
- **开球时间**: 2026-10-18 20:00
- **胜负平**: 主胜 (次选平局)
- **让球**: [-1] 让胜（次选让平）
- **胜/平/负点概率 (OO-EPC去水)**: 45.00% / 28.00% / 27.00%
- **【图谱认知基因】**: `Levitt 真实风险闭环` ➔ `Constantinou 均衡做市`
- **【认知契约卡】**:
  - **选择与排除依据**: 排除客胜依据：客胜欧指居高不下；选择主胜依据：主胜赔率低开低走设防。
  - **关键拍板依据**: 澳彩平博主胜稳定在2.10低位。
  - **庄家博弈假说与竞争解释**: 主线假设：庄家控制主胜赔付；竞争假设：防平局。
  - **可推翻反证与改变条件**: 若临盘客胜跌破2.50则假设证伪。
"""
        ok, errors, count = verify_memory_cognitive_cards(
            memory_content,
            expected_matches=1,
            data_dir=self.data_dir
        )
        self.assertTrue(ok, f"无阻断时应通过门禁，但被拦截: {errors}")
        self.assertEqual(count, 1)

    def test_memory_fails_when_block_unresolved(self):
        """当源数据触发 HeadFake_Surge (亚盘脉冲假摔) block 级阻断，但契约卡未开设【机位阻断对质】或未对质该探针时，门禁必须物理拦截"""
        match_id = "3099002"
        # 构造触发脉冲假摔的流水特征：受让半球/一球 1.04 且终盘受让半球
        src_content = f"""# 【周六002】测试联赛 汉堡 vs 斯图加特
- 比赛 ID：{match_id}
- 开球时间：2026-10-18 20:00

| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |
| :--- | :--- | ---: | ---: | :--- |
| 10-17 20:06 | 受让半球 | 1.06 | 0.83 | 即 |
| 10-14 02:13 | 受让半球/一球 | 0.84 | 1.04 | 早 |

| 核心做市 | 澳彩 | 3.43 | 4.35 | 1.68 | 90% | 3.43 | 4.35 | 1.68 |
"""
        self._create_source_snapshot(match_id, src_content)

        # 契约卡缺失【机位阻断对质】
        memory_content = f"""# 2026-10-18

| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 周六002 20:00 | 汉堡 vs 斯图加特 | 客胜 (次选平局) | [+1] 让负（次选让平） | 27.26% / 20.94% / 51.80% | 客让半球低水 | [汉堡 vs 斯图加特（平局 22.5¢ / 4.44倍）](https://polymarket.com/event/test-slug-hsv-stu) |

## 深度分析

### 【周六002】汉堡 vs 斯图加特 (德甲)
- **比赛ID**: {match_id}
- **开球时间**: 2026-10-18 20:00
- **胜负平**: 客胜 (次选平局)
- **让球**: [+1] 让负（次选让平）
- **胜/平/负点概率 (OO-EPC去水)**: 27.26% / 20.94% / 51.80%
- **【图谱认知基因】**: `Levitt 真实风险闭环`
- **【认知契约卡】**:
  - **选择与排除依据**: 排除主胜依据：主胜赔率过高；选择客胜依据：斯图加特实力占优。
  - **关键拍板依据**: 皇冠客水0.83低水。
  - **庄家博弈假说与竞争解释**: 主线假设：庄家正向看好客胜；竞争假设：平局。
  - **可推翻反证与改变条件**: 若客胜升破2.00则证伪。
"""
        ok, errors, count = verify_memory_cognitive_cards(
            memory_content,
            expected_matches=1,
            data_dir=self.data_dir
        )
        self.assertFalse(ok, "触发脉冲假摔阻断但未对质时，门禁必须拦截 (FAIL)")
        self.assertTrue(
            any("MEMORY_CONSTRAINT_BLOCK_UNRESOLVED" in err for err in errors),
            f"错误列表中应包含 MEMORY_CONSTRAINT_BLOCK_UNRESOLVED，实际为: {errors}"
        )

    def test_memory_fails_when_semantic_conflict(self):
        """当触发假摔或脱节阻断，但契约卡出现'深盘共振'或'平稳设防'等严重语义冲突词汇时，门禁必须拦截"""
        match_id = "3099003"
        src_content = f"""# 【周六003】测试联赛 汉堡 vs 斯图加特
- 比赛 ID：{match_id}
- 开球时间：2026-10-18 20:00

| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |
| :--- | :--- | ---: | ---: | :--- |
| 10-17 20:06 | 受让半球 | 1.06 | 0.83 | 即 |
| 10-14 02:13 | 受让半球/一球 | 0.84 | 1.04 | 早 |

| 核心做市 | 澳彩 | 3.43 | 4.35 | 1.68 | 90% | 3.43 | 4.35 | 1.68 |
"""
        self._create_source_snapshot(match_id, src_content)

        # 契约卡虽提到了对质或探针，但出现了违禁的"深盘共振"反向指鹿为马
        memory_content = f"""# 2026-10-18

| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 周六003 20:00 | 汉堡 vs 斯图加特 | 客胜 (次选平局) | [+1] 让负（次选让平） | 27.26% / 20.94% / 51.80% | 客让半球低水 | [汉堡 vs 斯图加特（平局 22.5¢ / 4.44倍）](https://polymarket.com/event/test-slug-hsv-stu) |

## 深度分析

### 【周六003】汉堡 vs 斯图加特 (德甲)
- **比赛ID**: {match_id}
- **开球时间**: 2026-10-18 20:00
- **胜负平**: 客胜 (次选平局)
- **让球**: [+1] 让负（次选让平）
- **胜/平/负点概率 (OO-EPC去水)**: 27.26% / 20.94% / 51.80%
- **【图谱认知基因】**: `Constantinou 欧亚深盘共振`
- **【机位阻断对质】**: 对质 HeadFake_Surge 探针：做市商平稳设防，欧亚深盘共振，客胜无忧。
- **【认知契约卡】**:
  - **选择与排除依据**: 排除主胜；选择客胜。
  - **关键拍板依据**: 皇冠客水0.83。
  - **庄家博弈假说与竞争解释**: 主线假设：客胜打出。
  - **可推翻反证与改变条件**: 若客胜升破2.00则证伪。
"""
        ok, errors, count = verify_memory_cognitive_cards(
            memory_content,
            expected_matches=1,
            data_dir=self.data_dir
        )
        self.assertFalse(ok, "包含语义冲突（深盘共振）时，门禁必须拦截 (FAIL)")
        self.assertTrue(
            any("MEMORY_CONSTRAINT_SEMANTIC_CONFLICT" in err for err in errors),
            f"错误列表中应包含 MEMORY_CONSTRAINT_SEMANTIC_CONFLICT，实际为: {errors}"
        )

    def test_memory_passes_when_block_properly_rebutted(self):
        """当触发假摔阻断，且契约卡如实开设【机位阻断对质】并深刻破译做市商假摔真意图时，门禁顺利放行"""
        match_id = "3099004"
        src_content = f"""# 【周六004】测试联赛 汉堡 vs 斯图加特
- 比赛 ID：{match_id}
- 开球时间：2026-10-18 20:00

| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |
| :--- | :--- | ---: | ---: | :--- |
| 10-17 20:06 | 受让半球 | 1.06 | 0.83 | 即 |
| 10-14 02:13 | 受让半球/一球 | 0.84 | 1.04 | 早 |

| 核心做市 | 澳彩 | 3.43 | 4.35 | 1.68 | 90% | 3.43 | 4.35 | 1.68 |
"""
        self._create_source_snapshot(match_id, src_content)

        memory_content = f"""# 2026-10-18

| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 周六004 20:00 | 汉堡 vs 斯图加特 | 主胜 (次选平局) | [+1] 让胜（次选让平） | 27.26% / 20.94% / 51.80% | 假摔退盘诱客 | [汉堡 vs 斯图加特（平局 22.5¢ / 4.44倍）](https://polymarket.com/event/test-slug-hsv-stu) |

## 深度分析

### 【周六004】汉堡 vs 斯图加特 (德甲)
- **比赛ID**: {match_id}
- **开球时间**: 2026-10-18 20:00
- **胜负平**: 主胜 (次选平局)
- **让球**: [+1] 让胜（次选让平）
- **胜/平/负点概率 (OO-EPC去水)**: 27.26% / 20.94% / 51.80%
- **【图谱认知基因】**: `Winkelmann 假摔退盘诱多` ➔ `Levitt 筹码穿仓通杀`
- **【机位阻断对质】**: 显式对质 HeadFake_Surge (constraint_headfake_rebound)：做市商中盘由半一退至半球，表象降门槛实则诱客出货，判定假摔现行，采纳阻断反审，坚决排除客胜独赢，主推汉堡爆冷不败！
- **【认知契约卡】**:
  - **选择与排除依据**: 排除客胜依据：主流机构临盘从半一全线退盘至半球降门槛诱客出货；选择主胜依据：汉堡主场全力抢分，做市商客胜升赔弃守。
  - **关键拍板依据**: 皇冠平博临盘退盘，对质假摔阻断成功。
  - **庄家博弈假说与竞争解释**: 主线假设：做市商利用豪门声望诱客接盘，实质汉堡爆冷打出；竞争假设：平局防守。
  - **可推翻反证与改变条件**: 若临盘平博强力升盘重回半一低水则证伪。
"""
        ok, errors, count = verify_memory_cognitive_cards(
            memory_content,
            expected_matches=1,
            data_dir=self.data_dir
        )
        self.assertTrue(ok, f"合规对质阻断探针后应放行，实际拦截报错: {errors}")
        self.assertEqual(count, 1)

    def test_memory_fails_when_block_triggered_but_card_claims_no_block(self):
        """当源数据触发假摔阻断，但契约卡谎称'未触发做市阻断探针'时，门禁必须严厉拦截"""
        match_id = "3099005"
        src_content = f"""# 【周六005】测试联赛 汉堡 vs 斯图加特
- 比赛 ID：{match_id}
- 开球时间：2026-10-18 20:00

| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |
| :--- | :--- | ---: | ---: | :--- |
| 10-17 20:06 | 受让半球 | 1.06 | 0.83 | 即 |
| 10-14 02:13 | 受让半球/一球 | 0.84 | 1.04 | 早 |

| 核心做市 | 澳彩 | 3.43 | 4.35 | 1.68 | 90% | 3.43 | 4.35 | 1.68 |
"""
        self._create_source_snapshot(match_id, src_content)

        memory_content = f"""# 2026-10-18

| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 周六005 20:00 | 汉堡 vs 斯图加特 | 客胜 (次选平局) | [+1] 让负（次选让平） | 27.26% / 20.94% / 51.80% | 客让半球低水 | [汉堡 vs 斯图加特（平局 22.5¢ / 4.44倍）](https://polymarket.com/event/test-slug-hsv-stu) |

## 深度分析

### 【周六005】汉堡 vs 斯图加特 (德甲)
- **比赛ID**: {match_id}
- **开球时间**: 2026-10-18 20:00
- **胜负平**: 客胜 (次选平局)
- **让球**: [+1] 让负（次选让平）
- **胜/平/负点概率 (OO-EPC去水)**: 27.26% / 20.94% / 51.80%
- **【图谱认知基因】**: `Levitt 真实风险闭环`
- **【机位阻断对质】**: 未触发做市阻断探针，8大做市机位平稳设防。
- **【认知契约卡】**:
  - **选择与排除依据**: 排除主胜；选择客胜。
  - **关键拍板依据**: 皇冠客水0.83低水。
  - **庄家博弈假说与竞争解释**: 主线假设：客胜打出。
  - **可推翻反证与改变条件**: 若客胜升破2.00则证伪。
"""
        ok, errors, count = verify_memory_cognitive_cards(
            memory_content,
            expected_matches=1,
            data_dir=self.data_dir
        )
        self.assertFalse(ok, "触发阻断却谎称未触发时，门禁必须拦截 (FAIL)")
        self.assertTrue(
            any("MEMORY_CONSTRAINT_SEMANTIC_CONFLICT" in err for err in errors),
            f"应报告 MEMORY_CONSTRAINT_SEMANTIC_CONFLICT，实际为: {errors}"
        )


if __name__ == "__main__":
    unittest.main()
