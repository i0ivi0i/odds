# 纯数学算法模块架构说明书 (真 DDD 洋葱整洁乐高架构)

## 一、架构定位与立宪红线

本模块（`算法/`）是足球倍率推演系统的纯数学客观基石。
严格遵循项目最高立宪红线：
1. **绝对禁止业务代码侵入**：严禁在此模块中编写任何与盘口诱阻判定、豪门战意、临场假摔或买彩决策相关的业务推演代码。
2. **纯数学无状态函数**：仅允许客观公理级的数学去水与概率分布算法。
3. **零沉重外部依赖**：仅使用 Python 3 标准库（`math`, `typing`, `json`, `argparse`），坚决杜绝 PyTorch、Transformers、NLTK 等庞大外部依赖。
4. **10/10 纯 DDD 洋葱六边形架构**：严格遵守依赖倒置原则，依赖单向向内，领域内核对外部框架与 I/O 零感知。

---

## 二、目录组织与分层设计

```text
算法/
├── src/                                  # 核心源码
│   ├── domain/                           # 【核心领域层】（内核：数学真理，零外部依赖）
│   │   ├── __init__.py
│   │   ├── model.py                      # 领域模型与值对象：OddsVector, ImpliedProbabilities
│   │   └── calculator.py                 # 领域服务：OoEpcCalculator, MarginCalculatorStrategy 协议
│   │
│   ├── application/                      # 【应用服务层】（中层：用例编排与 DTO 转换）
│   │   ├── __init__.py
│   │   └── use_cases.py                  # 应用用例：ConvertOddsUseCase
│   │
│   └── adapter/                          # 【基础设施与适配器层】（外圈：CLI 终端入站驱动）
│       ├── __init__.py
│       └── cli.py                        # 终端接口：命令行解析、格式化打印、--json 支持
│
├── 测试/                                 # 【镜像测试套件】（与领域模型 1:1 镜像）
│   ├── __init__.py
│   ├── test_domain.py                    # 领域层值对象与模型测试
│   ├── test_use_cases.py                 # 应用用例测试
│   └── test_benchmarks.py                # 学术基准测试（Goto Table 1 对齐，Bit-for-bit 验证）
│
└── 文档/                                 # 【架构与数学契约】
    └── ARCHITECTURE.md                   # 本架构规范文件
```

---

## 三、乐高积木式扩展机制 (Strategy Protocol)

为了确保未来接入新算法（如 Shin 知情交易模型、多项对数 Logit 模型、双变量泊松分布等）时浑然一体，领域层定义了标准的计算策略协议：

```python
class MarginCalculatorStrategy(Protocol):
    @staticmethod
    def calculate(vector: OddsVector, total: float = 1.0) -> ImpliedProbabilities:
        ...
```

### 未来接入新算法的步骤：
1. **新增领域计算器**：在 `算法/src/domain/` 下创建新文件（如 `shin_calculator.py`），实现 `calculate` 静态方法；
2. **注册应用策略**：在 `算法/src/application/use_cases.py` 中注册新策略：
   ```python
   self.register_strategy('shin', ShinCalculator)
   ```
3. **新增镜像单测**：在 `算法/测试/` 下新增 `test_shin.py`；
4. **即插即用**：现有 CLI 即可直接通过 `--strategy shin` 调度新算法，老算法与其他系统模块完全不受影响。

---

## 四、核心算法数学推导：Goto (2026) OO-EPC

- **论文出处**：Shota Goto & Kaito Goto (2026), *Forecasting Sports Outcomes under the Efficient Market Hypothesis: A Universal Framework for Odds-Only Models*, arXiv:2604.17194v1, Algorithm 5.
- **核心逻辑**：
  庄家在长尾冷门（低概率/高赔率）上承担的标准误差远远大于稳胆热门。OO-EPC 基于“各结果对于博彩公司而言盈利确定性（置信度）均等”的原则，将抽水按标准误差（Standard Error）进行差异化扣减：

$$
\pi_i = \frac{1}{\text{odds}_i}
$$

$$
SE_i = \sqrt{\frac{\pi_i - \pi_i^2}{\pi_i}} = \sqrt{1 - \pi_i}
$$

$$
z = \frac{\sum \pi_i - 1.0}{\sum SE_i}
$$

$$
\hat{y}_i = \pi_i - z \cdot SE_i
$$

若任意 $\hat{y}_i \le 0$ 或总倒数和 $\sum \pi_i \le 1.0$，系统自动防御性平滑回退为简单比例归一化：
$$
\hat{y}_i = \frac{\pi_i}{\sum \pi_i}
$$

---

## 五、命令行使用指南

```bash
# 标准三项欧指去水
python 算法/src/adapter/cli.py 2.10 3.40 3.55

# 输出结构化 JSON 数据
python 算法/src/adapter/cli.py 2.10 3.40 3.55 --json

# 两项盘去水 (亚盘 / 大小球)
python 算法/src/adapter/cli.py 1.95 1.95

# 运行完整镜像测试套件
python -m unittest discover -s 算法/测试
```
