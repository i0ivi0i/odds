# 预测与复盘论文（本项目）

比赛战报仍在 `data/`。这里放赔率推演、模型交叉验证与复盘研究的原文和按页转写，不另建案例答案书。**各种足球倍率及其时序推演胜平负仍是预测核心**；研究方法融入原有五技能和完整十步，不替代当场三端比较。

用法就三句：先遮比分审当时理由；看整份胜/平/负概率，不当对错本；改规矩必须用后面没见过的球检验。论文指导方法，不证明本项目能赚钱。

| 文件 | 一句话 | 原文 |
| --- | --- | --- |
| `2023_Aiyer_结果偏见与决策评价.pdf` | 知道结果后会高估/低估当时决定，复盘要先审过程 | https://doi.org/10.5334/irsp.751 |
| `2019_Wheatcroft_足球概率预测评分.pdf` | 足球预测用概率评分，不当猜中/没猜中 | https://arxiv.org/abs/1908.08980 |
| `2023_Hewamalage_预测评估陷阱与最佳实践.pdf` | 防偷看、防事后切数据找假规律 | https://doi.org/10.1007/s10618-022-00894-5 |
| `2021_Dimitriadis_稳定可靠性图_CORP.pdf` | 概率说 30% 平，七成分胜负仍正常；要看大样本校准 | https://doi.org/10.1073/pnas.2016191118 |
| `2006_Giacomini_条件预测能力检验.pdf` | 改方法前先冻结假设，再用后面的球检验 | https://doi.org/10.1111/j.1468-0262.2006.00718.x |
| `2023_Choe_序贯预测者比较_arXiv_v6.pdf` | 长期跟踪两套方法谁更好，少被单日情绪带跑 | https://arxiv.org/abs/2110.00115 |
| `2025_Macri_足球贝叶斯加权动态模型_arXiv.pdf` | 稳定时借用历史，核实重大变化时允许快速调整 | https://arxiv.org/abs/2508.05891 |
| `2026_Wilkens_德甲预测与滚动验证.pdf` | 简单模型 + 按赛季滚动检验，别叠例外条款 | https://doi.org/10.1177/22150218261416681 |
| `2004_Levitt_NBER_w9422.pdf` | 美式NFL定价可利用偏见，不证明足球当场底牌 | https://www.nber.org/papers/w9422 |
| `2017_Kaunitz_用庄家赔率寻找足球错价_arXiv_v2.pdf` | 多公司共识与报价偏离，须区分看板报价和实际可成交价 | https://arxiv.org/abs/1710.02824 |
| `2023_Hegarty_Whelan_足球赔率预测_双市场_MPRA工作论文.pdf` | 比较1X2与AH校准；两项AH水位不独自识别退款概率 | https://mpra.ub.uni-muenchen.de/116925/1/MPRA_paper_116925.pdf |
| `2011_Andrikogiannopoulou_博彩市场效率与行为偏差_工作论文.pdf` | 长赔平局也可能被高估；公开价格不能唯一分辨偏差机制 | 同名校准版保留来源及版本 |
| `2017_Feng_英超赔率与动态进球分布_arXiv_v5.pdf` | 用比分赔率估进球分布；动态研究含滚球，不偷用赛中事件 | 同名校准版保留来源及版本 |
| `2022_Constantinou_亚洲让球与胜平负市场效率_arXiv_v2.pdf` | 跨市场预测与收益比较；BN验证部分可能使用未来资料 | 同名校准版保留来源及版本 |
| `2025_德甲赔率能否预感进球_arXiv_v1.pdf` | 单家公司德甲首球前研究未发现明显预感进球行为 | 同名校准版保留来源及版本 |
| `2604.17194_Forecast_Sports_Outcomes_under_EMH_Odds_Only_Models.pdf` | 9万场实证纯赔率转化与庄家各端等置信收益目标 (OO-EPC) | https://arxiv.org/abs/2604.17194 |
| `2403.16282_足球博彩演进_机器学习预测与庄家赔率估算.pdf` | 机器学习预测足球赛果与做市商赔率估算演进路径 | https://arxiv.org/abs/2403.16282 |
| `1802.08848_结合历史数据与庄家赔率预测足球比分.pdf` | 泊松双重攻防建模与庄家欧亚赔率综合预测 | https://arxiv.org/abs/1802.08848 |
| `2605.30209_识别异常赔率波动与市场动态.pdf` | 状态空间模型与微观异常赔率波动、假球市场动态识别 | https://arxiv.org/abs/2605.30209 |

Shin（1993）期刊原文需订阅，未放入。隔壁 `足球预测/温故而知新学习资料` 另有笔记，此处不重复拷贝。

同目录 `*.calibrated.md` 是按页对齐的文字层转写（工具检查已通过）。引用论文时优先打开对应 calibrated 文件的 `## Page NN`，不要用本表「一句话」代替原文。公式若在文字层里已经乱，以 PDF 原页为准，不许猜。

## 十九篇的执行落点与原文锚点

下表页码都是 **PDF物理页**，对应同名 `*.calibrated.md` 的 `## Page NN`。短句为原文片段，不是另造规则。研究动作已写入各技能，索引只导航；公式需原页核实，不推测转写乱码。

**当前执行：paper-application-v2。** 以主人撤回后版本为基线，只嵌入研究动作与记录。以各市场全维度原始初盘（欧指、亚盘、让球、大小球、波胆等初盘）为基准坐标系，紧密结合各盘口在变动过程中的时序轨迹与资金流向动态交叉验证，诱阻、RLM与三端裁决继续作为胜平负推演主线，绝不搞任何死板一刀切；无实际注额仍能推演有方向的资金假设，不把“不能证明唯一机制”误当“不能推演”。论文不替代三端落槌，也不凭缺项增加观望门槛。下表的动作分别落实在四个现有分析技能，赛程抓取职责不变。

| 论文／页 | 可回查原文短句 | 现有流程中实际怎么用 | 适用边界／尚不能做什么 |
| --- | --- | --- | --- |
| Kaunitz，p7、14–16 | “Sometimes bookmakers offer odds above fair value either to compete to attract clients or to maintain a balanced book to avoid getting overly exposed to risk.” | 初筛阶段5、深度第4/8步比较同口径同时间的多公司基准、单家离群及持续变化；推荐标报价时点，成交另记 | 跨公司错价不是单家升降必出。本文 `1/平均赔率` 不等于本项目逐家比例去水再均值；本地方法单独标识、不称复现。延迟、限额、有限实盘及正文／表格疑误保留，不搬α或收益 |
| Hegarty/Whelan，p18（短句）、4、20 | “This is a system of three linear equations in four unknowns (the three probabilities and the expected return) so there is no unique solution.” | 深度第5/7步先区分AH退本、四分盘拆半与竞彩三项；核对净胜球事件再比较欧亚 | AH平均校准较好不授权一票优先。退款率主估计用全样本，但脚注9也报告用过去赛季取得同样结果，不能说整篇无时序检验；未来参数须冻结 |
| Andrikogiannopoulou，p8、13 | “it is impossible to disentangle between the above explanations.” | 初筛和深度第4/7/9步分主、平、客及赔率区间记录偏差疑点；公开报价、热度代理和真实注额分开 | 单庄家、100客户样本；长赔平局额外效应部分证据弱。高平不排除平，不固定只推冷，不从报价唯一识别庄家意图 |
| Feng，p1 | “Given a matrix of market odds on all possible score outcomes, we estimate the expected scoring rates for each team.” | 深度第3/5/6/7步把独立泊松与市场进球分布分开；核对胜者、净胜球、总进球的相容性 | 包含滚球动态研究。无完整比分市场与拟合条件不编Skellam参数；小球不等于平、三项胜平负不唯一确定让球 |
| Constantinou，p11 | “the BN model assumes no temporal relationships.” | 深度第7步跨市场核验、复盘方法比较分清样本设计，所有新训练、调参只用预测时以前资料 | 评级有时间顺序，BN部分LOOCV可含未来资料；作者以关系不变解释，不将所报收益全称严格滚动实盘，不照搬模型 |
| 德甲首球研究，p1 | “Our results indicate that neither side of the market anticipates goals by significantly adjusting their behaviour.” | 深度第8步区分微动事实与消息、跟价、风控等解释，复盘不以赛果倒证预知 | 单公司、单赛季、1Hz滚球首球前，负面结果不推广成所有赛前赔率无信息；赛中数据不进赛前预测 |
| Aiyer，p2 | “the judge processes only the information available to the decision-maker at the time of a decision.” | 推荐保存赛前发布版；复盘先核当时可知依据，过程与结果分开，已知答案如实标注 | 医疗决定研究迁移的是评价方法，不是足球准确率证据 |
| Wheatcroft，p2 | “A score is proper if, in expectation, it favours a forecast that consists of the distribution from which the outcome is drawn” | 保存三个赛前点概率；复盘三项布莱尔平方和及可选对数损失，市场／独立泊松／综合判断分源比较 | 本文偏好ignorance，非证明布莱尔最好；无点概率不得用区间中点补造 |
| Hewamalage，p17 | “Data leakage refers to the inadvertent use of data from the test set” | 分析时点、消息时点、推荐版本留存；逐场取开球前最终有效版，不偷看、事后选规则 | 通用时间序列方法，赛后核事实不等于偷看；识别新假设的旧案例不作为验证样本 |
| Dimitriadis，p1 | “the predicted probabilities are matched by ex post observed frequencies” | 复盘按胜／平／客分别检查累计概率与实际频率，报告样本与不确定性；不凭单败否定30%预测 | 不能用少量样本宣称已校准；分项校准后还要验证概率合计1，校准与评价窗口分开 |
| Giacomini，p2 | “what data to use for estimation.” | 待验证保存整套旧／新方法、数据、版本和失败条件，同场后续配对比较；锚定前后并列 | 正式条件检验需实际满足条件；启用组／未启用组差异不是因果效果，8场不是统计证实 |
| Choe，p1 | “valid at arbitrary data-dependent stopping times” | 复盘连续记录同场预测损失差，按事先窗口评价，不因某天领先换规则 | 本文实例棒球／天气；没实际构造置信序列不称任意时点显著，对数损失不能直接套有界定理 |
| Macri，p1 | “allows rapid adjustments when teams experience substantial changes” | 深度第3步稳定时借用历史，核实换帅、转会、伤停变化才调整并留时点；复盘检查长期λ残差 | 足球动态模型不是固定慢衰减；不复制未核公式，不因单场Top6不中就重设模型 |
| Wilkens，p7 | “all results and reliability plots are strictly out-of-sample with respect to their calibration window” | 推荐优先胜平负证据；复盘用旧窗拟合后窗评价，新增复杂条款须有后续配对改善 | 德甲模型／模拟研究不能外推实盘收益；两季、裁剪区间等是研究设定，不作本项目门禁 |
| Levitt，p2 | “choosing prices that deviate from the market clearing price.” | 深度第7/8步保留主动定价与偏见解释，同时核对竞争解释；复盘不从赛果倒证账本 | NFL不是足球，原研究有价格与注额。本项目没有真实注额／已接受赔率／对冲，净赔付只能声明假设，不能识别唯一赛果 |
| Goto (2026)，p1、3 | “we propose an odds-only model based on equal profit for confidence (OO-EPC)... achieving state-of-the-art predictive performance” | 深度第4/9步提取无偏胜平负客观发生率，首选遵从无偏胜率最高项 (argmax P) 死磕命中率 | 纯赔率模型依赖做市商定价有效性；不保证单场必中，9万场实证胜在长期校准与Log-Loss最优 |
| Winkelmann (2026)，p1、12 | “identifying abnormal betting patterns... distinguishing between transient liquidity shocks and persistent information shifts” | 深度第4/8步识别微观做市假摔 (Head-Fake)，区分中途瞬态跳水与临盘持久性大资金位移 | 状态空间模型侧重盘口异动识别，不能证明当场踢出特定比分；需与三盘几何交叉验证 |
| Egidi (2018)，p1、7 | “the scoring rates of the teams are convex combinations of parameters estimated from historical data and the additional source of the betting odds.” | 深度第3步泊松进球期望建模，将历史攻防均值与盘口隐含期望做凸组合融合 (Convex Combination) | 凸组合权重取决于赛事样本与盘口成熟度；杯赛或阵容巨变时需提高即时盘口权重 |
| Mandadapu (2024)，p1、6 | “A Machine Learning Approach to Match Outcome Forecasting and Bookmaker Odds Estimation... investigating the significance of various features” | 深度第7/8步结合多维动态特征检验庄家开盘合理性，破译做市商风险对冲与引流杠杆 | 机器学习特征工程不能替代当场临盘资金博弈；模型特征需赛前冻结 |

## 预测 → 推荐 → 复盘的实际闭环

1. **初筛**：离群和矛盾表示值得深挖，不直接表示冷门或能赚；保留公司、市场、真实时点及缺失。
2. **十步分析**：先独立泊松，再各公司逐项去水及三市场时序；区分胜者、净胜球、总进球，复核消息与结算；第9步三端比较落首选，替代解释与可推翻条件一并保留。报价同步不自动扣分，固定数值不一票裁决。
3. **推荐留存**：`paper-application-v2`、matchId、发布时点、引用分析版本、赔率截至时点、公司／方法、最终主平客点概率与独立基准、首选／次选、精选／候补／观望。已发布版不覆盖。Polymarket地址按现有教程核验，研究价不等于成交价。
4. **逐场复盘**：新研究记录按比赛取最终有效赛前版，另列首选命中与备选覆盖、只评分赛前点概率，按场次／版本／指标去重。现有历史累计口径不改、不混入新研究账，不把覆盖提升当首选能力提升。
5. **滚动学习**：新假设与旧方法在相同后续比赛和资料时点留预测，比较配对概率损失、首选及观望变化；按类别检查校准。无正式检验只称观察改善／恶化，不用单场、八场或引用数量证明准确率提升。

完整技能入口：`skills/match-screening/SKILL.md` 阶段5、`skills/deep-analysis/SKILL.md` 研究应用入口及第4–9步、`skills/recommendation/SKILL.md` 推荐留存、`skills/post-review/SKILL.md` 概率评分／方法比较。不新增技能，不改抓取脚本；本次落实的是可执行分析和记录方法，不声称已训练或验证十九套模型。

图谱检索先 `graphify query`，再回当前原文核对；`source_location` 带文件页码／行号。旧图谱节点不替代当前正文。不要求每场十九篇打卡，不能把论文一句话变成新门禁。旧九篇的转写图表核查覆盖以各文件头部和 `核对记录.md` 为准，本次原句回检不是重新完整校准。
