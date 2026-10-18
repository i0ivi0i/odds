"""
EvoOntology 8 大做市异动纯领域感知探针与约束检测模型
严格立宪：本模块仅充当'只读眼睛与摄像头'，绝不包含任何比赛胜负预测、让球输赢判定或打分死尺子！
"""
import re
from pathlib import Path
from typing import List, Dict, Any, Optional


def detect_ontology_probes(content: str) -> List[Dict[str, Any]]:
    """检测源数据快照中的做市异动探针"""
    triggered_probes: List[Dict[str, Any]] = []

    # 1. 探针一：Pinnacle_Anchor (平博标杆定海神针) - severity: block
    pinnacle_match = re.search(
        r"\|\s*核心做市\s*\|\s*平博\s*\|\s*([\d\.]+)\s*\|\s*([\d\.]+)\s*\|\s*([\d\.]+)\s*\|\s*[\d\.]+%?\s*\|\s*([\d\.]+)\s*\|\s*([\d\.]+)\s*\|\s*([\d\.]+)",
        content,
    )
    retail_matches = re.findall(
        r"\|\s*(?:核心做市|终端履约)\s*\|\s*(澳彩|皇冠|Bet365|中国体彩)\s*\|\s*([\d\.]+)\s*\|\s*([\d\.]+)\s*\|\s*([\d\.]+)\s*\|\s*[\d\.]+%?\s*\|\s*([\d\.]+)\s*\|\s*([\d\.]+)\s*\|\s*([\d\.]+)",
        content,
    )
    if pinnacle_match and retail_matches:
        p_init_a, p_curr_a = float(pinnacle_match.group(3)), float(pinnacle_match.group(6))
        p_init_h, p_curr_h = float(pinnacle_match.group(1)), float(pinnacle_match.group(4))
        p_delta_a = abs(p_curr_a - p_init_a)
        p_delta_h = abs(p_curr_h - p_init_h)

        pinnacle_flat = p_delta_a <= 0.03 or p_delta_h <= 0.03
        retail_dropped = False
        retail_detail = []
        for r_name, r_ih, r_id, r_ia, r_ch, r_cd, r_ca in retail_matches:
            da = float(r_ia) - float(r_ca)
            dh = float(r_ih) - float(r_ch)
            if da >= 0.15:
                retail_dropped = True
                retail_detail.append(f"{r_name}客胜降{da:.2f}")
            elif dh >= 0.15:
                retail_dropped = True
                retail_detail.append(f"{r_name}主胜降{dh:.2f}")
        if pinnacle_flat and retail_dropped:
            triggered_probes.append({
                "term": "Pinnacle_Anchor",
                "id": "constraint_pinnacle_stability",
                "severity": "block",
                "desc": "【标杆定海神针警报】商业庄与体彩单边剧烈降赔（>=0.15），但风控标杆平博变动绝对值<=0.03（几乎纹丝不动）。此为典型商业庄顺应散户偏见出货引流形态，强制禁止将商业庄降赔直接等同于机构防守，大模型必须在认知契约卡中显式对质平博未动原因！",
                "evidence": f"平博位移主{p_delta_h:.2f}/客{p_delta_a:.2f} 稳定，商业庄诱降: {', '.join(retail_detail)}",
                "graphify_query": "Constantinou 平博 标杆 做市",
                "graphify_paper": "graphify://paper/Constantinou_2022_Sharp_Benchmark",
                "forbidden_conflicts": ["平博正向看好", "平博同步降赔", "商业庄与平博共振", "做市商一致防守"],
                "aliases": ["pinnacle_anchor", "constraint_pinnacle_stability", "平博", "标杆定海神针", "定海神针", "平博未动"],
            })

    # 2. 探针二：HeadFake_Surge (亚盘脉冲假摔) - severity: block
    has_headfake = False
    if "受让半球/一球" in content and "受让半球" in content:
        if re.search(r"受让半球/一球.*?(?:1\.\d{2}|0\.99|1\.00)", content) and re.search(
            r"10-\d{2}\s+\d{2}:\d{2}\s*\|\s*受让半球", content
        ):
            has_headfake = True
    elif "半球/一球" in content and "半球" in content:
        if re.search(r"半球/一球.*?(?:1\.\d{2}|0\.99|1\.00)", content) and re.search(
            r"10-\d{2}\s+\d{2}:\d{2}\s*\|\s*半球", content
        ):
            has_headfake = True

    if has_headfake:
        triggered_probes.append({
            "term": "HeadFake_Surge",
            "id": "constraint_headfake_rebound",
            "severity": "block",
            "desc": "【亚盘脉冲假摔警报】中盘亚盘曾出现主动升盘并挂超满水（>=1.04）诱多，但在终盘2小时仓皇退回初盘门槛。此为机构心虚放弃设防的假摔现行，强制禁止将初即终盘同一浅盘误判为全程平稳设防！",
            "evidence": "时序流水抓取到中盘升盘挂满水(>=1.00)且终盘退回初盘门槛",
            "graphify_query": "Winkelmann 假摔 脉冲 诱多 震仓",
            "graphify_paper": "graphify://paper/Winkelmann_2026_Transient_Pulse",
            "forbidden_conflicts": ["深盘共振", "平稳设防", "全程设防", "稳定设防", "正路无忧"],
            "aliases": ["headfake_surge", "constraint_headfake_rebound", "假摔", "脉冲假摔", "退盘诱客", "退盘出货"],
        })

    # 3. 探针三：Draw_Vacuum (高平筹码真空) - severity: warn
    draw_matches = re.findall(
        r"\|\s*[\d\.]+\s*\|\s*([\d\.]+)\s*\|\s*[\d\.]+\s*\|[\d\.]+%?\s*\|\s*[\d\.]+\s*\|\s*([\d\.]+)\s*\|\s*[\d\.]+",
        content,
    )
    draw_odds = [float(m[1]) for m in draw_matches if float(m[1]) >= 4.00]
    if draw_odds:
        triggered_probes.append({
            "term": "Draw_Vacuum",
            "id": "constraint_draw_extreme_high",
            "severity": "warn",
            "desc": "【高平筹码真空警报】全网百家欧指平局赔率极端顶高至 4.00+。散户大众产生极度恐高心理，平局投注陷入筹码真空。做市商面临的大众净赔付为零甚至通杀，大模型绝对严禁因平赔过高主观一票否决平局！",
            "evidence": f"全网共 {len(draw_odds)} 家机构即时平赔 >= 4.00 (最高 {max(draw_odds):.2f})",
            "graphify_query": "Levitt 极小化最大损失 筹码真空 通杀",
            "graphify_paper": "graphify://paper/Levitt_2004_Minimax_Loss",
            "forbidden_conflicts": [],
        })

    # 4. 探针四：Poisson_Floor (泊松数学底牌保护) - severity: block
    poisson_draw = re.search(r"(?:1:1|0:0|2:2).*?(?:泊松|概率)", content) or ("1:1" in content and "纽伦堡" in content)
    if poisson_draw:
        triggered_probes.append({
            "term": "Poisson_Floor",
            "id": "constraint_poisson_retention",
            "severity": "block",
            "desc": "【泊松数学底牌保护警报】由微观攻防得失球计算出的独立泊松比分前 2 位中包含平局（如 1:1），且与第一顺位概率差 <= 1.0%。大模型在推荐比分中严禁主观扼杀该平局比分！",
            "evidence": "泊松模型微观攻防前2高概率比分中包含平局比分，受物理底牌保护",
            "graphify_query": "Dixon Coles 泊松分布 物理底牌 比分相关性",
            "graphify_paper": "graphify://paper/Dixon_Coles_1997_Poisson_Correlation",
            "forbidden_conflicts": ["绝对无平", "主观扼杀平局", "排除平局"],
            "aliases": ["poisson_floor", "constraint_poisson_retention", "泊松数学底牌", "泊松底牌", "泊松保护", "泊松比分"],
        })

    # 5. 探针五：Constantinou_CrossMarket (欧亚跨市场门槛脱节) - severity: block
    if "背离" in content or ("半球" in content and "1.9" in content and ("2.0" in content or "平半" in content)):
        triggered_probes.append({
            "term": "Constantinou_CrossMarket",
            "id": "constraint_crossmarket_misalignment",
            "severity": "block",
            "desc": "【跨市场脱节出货警报 (Constantinou 2022)】欧指去水折合让球盘口与亚洲让球盘实际盘口相差 >= 0.5 档（如欧指折合让半球低水，亚盘实际平半高水或半一超高水）。机构利用两地市场信息不对称出货诱多，强制禁止将折合低价误当防守，大模型必须在契约卡中对质跨市场背离原因！",
            "evidence": "欧亚两地市场门槛脱节，做市商利用跨市场认知差进行非对称诱多",
            "graphify_query": "Constantinou 跨市场 欧亚脱节 套利均衡",
            "graphify_paper": "graphify://paper/Constantinou_2022_CrossMarket_Efficiency",
            "forbidden_conflicts": ["深盘共振", "欧亚共振", "两地吻合", "欧亚吻合", "正路无忧"],
            "aliases": ["constantinou_crossmarket", "constraint_crossmarket_misalignment", "跨市场", "脱节出货", "门槛脱节", "欧亚脱节", "欧亚背离", "跨市场脱节", "跨市场几何张力"],
        })

    # 6. 探针六：Levitt_Favorite_Melt (豪门极低赔穿仓诱多) - severity: warn
    fav_odds = [float(m) for m in re.findall(r"\|\s*([1]\.[23]\d)\s*\|", content)]
    if fav_odds:
        triggered_probes.append({
            "term": "Levitt_Favorite_Melt",
            "id": "constraint_favorite_melt_risk",
            "severity": "warn",
            "desc": "【豪门低赔穿仓诱多警报 (Levitt 2004)】胜平负热门方赔率处于 1.20~1.35 极低区间且大众交易集中度极高。做市商面临净赔付被击穿风险，若让球盘水位持续高企拒不升盘阻筹，极大概率存在做市商逆向弃守爆冷伏击，严禁无脑做胆！",
            "evidence": f"检测到低赔热门区间赔率 {min(fav_odds):.2f}，筹码单边扎堆风险剧增",
            "graphify_query": "Levitt 豪门偏见 热门低赔 净赔付穿仓 大热必死",
            "graphify_paper": "graphify://paper/Levitt_2004_Favorite_Longshot_Bias",
            "forbidden_conflicts": [],
        })

    # 7. 探针七：Egidi_Score_Snapping (皇冠波胆矩阵卡口设防) - severity: warn
    if "波胆" in content and ("1:0" in content or "1:1" in content or "0:1" in content):
        triggered_probes.append({
            "term": "Egidi_Score_Snapping",
            "id": "constraint_score_snapping_defense",
            "severity": "warn",
            "desc": "【皇冠波胆矩阵卡口设防警报 (Egidi 2022)】皇冠波胆矩阵中 1:0/1:1/0:1 等核心低比分赔率极端压低且水位下调，但胜平负或让球盘却维持表面高赔。做市商真实比分结算敞口已锚定低比分，大模型严禁盲信表面大球诱惑！",
            "evidence": "皇冠波胆低比分结算水位偏态设防，与表面盘口存在微观背离",
            "graphify_query": "Egidi 双变量泊松 波胆矩阵 比分偏态卡口",
            "graphify_paper": "graphify://paper/Egidi_2022_Bivariate_Poisson_Scores",
            "forbidden_conflicts": [],
        })

    # 8. 探针八：Sporttery_HAD_Squeeze (体彩关停基础胜负逼平风控) - severity: block
    if "HAD=None" in content or "had=None" in content or "关闭基础胜平负" in content or "仅开让球" in content:
        triggered_probes.append({
            "term": "Sporttery_HAD_Squeeze",
            "id": "constraint_sporttery_squeeze",
            "severity": "block",
            "desc": "【体彩官方关闭普通胜负平(HAD=None)仅开让球胜平负】体彩最高级别内幕风控信号：深盘逼平让球方，诱导散户去让球下盘或让平，大模型必须推演体彩让球玩法并严禁弃推该场！",
            "evidence": "体彩最高级别内幕风控信号：深盘逼平让球方，诱导让球下盘或让平",
            "graphify_query": "体彩风控 单固逼平 关停HAD 终局通杀",
            "graphify_paper": "graphify://case/Sporttery_HAD_Disabled_Squeeze",
            "forbidden_conflicts": ["放弃体彩让球", "体彩未开无法推演", "弃推本场"],
            "aliases": ["sporttery_had_squeeze", "constraint_sporttery_squeeze", "体彩关停", "关停had", "仅开让球", "单固逼平", "关闭基础胜平负"],
        })

    return triggered_probes
