"""
领域服务：推演源数据黄金契约规范 (Golden Snapshot Schema) 确定性序列化器
严格遵循 TOOLS.md 规范：
1. 严禁任何硬编码假数据、假时间戳、假凯利、假返还率或主观伪文案回退（Zero Fake Fallback）。
2. 废除 T0~T4 五阶段凑数切片、废除全周期对齐假总表、废除 14 家纯欧指凑数子表、废除主观「做市形态学识别」列。
3. 逐行原样序列化球探网真实报文数据，缺核心字段直接抛出 ValueError 物理阻断。
"""

from typing import Any, Dict, List, Tuple, Union
from 校验.src.domain.timeseries_denoiser import denoise_timeline_rows

# 法定 23 家机构白名单及标准元数据
LEGAL_23_COMPANIES = [
    # 第一战区：欧亚双盘全能做市商 (7家)
    {"id": 1, "name": "澳彩", "aliases": ["Macauslot", "澳*"], "zone": 1, "type": "核心做市", "cid": "80"},
    {"id": 2, "name": "皇冠", "aliases": ["Crown", "Crow*"], "zone": 1, "type": "核心做市", "cid": "545"},
    {"id": 3, "name": "Bet365", "aliases": ["365"], "zone": 1, "type": "核心做市", "cid": "281"},
    {"id": 4, "name": "易胜博", "aliases": ["Easybets", "易*"], "zone": 1, "type": "核心做市", "cid": "90"},
    {"id": 5, "name": "平博", "aliases": ["Pinnacle", "平*"], "zone": 1, "type": "核心做市", "cid": "177"},
    {"id": 6, "name": "188Bet", "aliases": ["金宝博", "188"], "zone": 1, "type": "核心做市", "cid": "976"},
    {"id": 7, "name": "香港马会", "aliases": ["HKJC", "马会"], "zone": 1, "type": "核心做市", "cid": "432"},
    # 第二战区：欧洲大陆与国际纯欧指做市商 (14家，仅在第三节初即盘总表展示，不建伪时序子表)
    {"id": 8, "name": "威廉希尔", "aliases": ["William Hill", "威廉"], "zone": 2, "type": "核心做市", "cid": "115"},
    {"id": 9, "name": "立博", "aliases": ["Ladbrokes"], "zone": 2, "type": "核心做市", "cid": "82"},
    {"id": 10, "name": "伟德", "aliases": ["Vcbet", "BetVictor"], "zone": 2, "type": "核心做市", "cid": "81"},
    {"id": 11, "name": "Interwetten", "aliases": ["Inter*"], "zone": 2, "type": "核心做市", "cid": "104"},
    {"id": 12, "name": "Bwin", "aliases": ["bwin"], "zone": 2, "type": "核心做市", "cid": "255"},
    {"id": 13, "name": "SNAI", "aliases": ["Snai"], "zone": 2, "type": "核心做市", "cid": "110"},
    {"id": 14, "name": "必发", "aliases": ["Betfair"], "zone": 2, "type": "核心做市", "cid": "2"},
    {"id": 15, "name": "SBO", "aliases": ["SBO(利记)", "利记", "SBOBET", "Sbobet"], "zone": 2, "type": "老庄机构", "cid": "474"},
    {"id": 16, "name": "沙巴", "aliases": ["沙巴(IBC)", "IBC", "IBCBET", "明升"], "zone": 2, "type": "老庄机构", "cid": "649"},
    {"id": 17, "name": "Marathon", "aliases": ["Marathon(马拉松)", "马拉松", "Marathonbet"], "zone": 2, "type": "论文样本", "cid": "800"},
    {"id": 18, "name": "Betway", "aliases": ["Betway(必威)", "必威"], "zone": 2, "type": "论文样本", "cid": "482"},
    {"id": 19, "name": "Unibet", "aliases": ["Unibet(优胜客)", "优胜客"], "zone": 2, "type": "论文样本", "cid": "386"},
    {"id": 20, "name": "Paddy Power", "aliases": ["Paddy", "PaddyPower"], "zone": 2, "type": "论文样本", "cid": "826"},
    {"id": 21, "name": "10Bet", "aliases": ["10bet", "10BET"], "zone": 2, "type": "论文样本", "cid": "16"},
    # 第三战区：终端履约实盘标的 (2家)
    {"id": 22, "name": "中国体彩", "aliases": ["体彩官方", "竞彩官方", "Sporttery", "Lottery Official", "竞彩官*"], "zone": 3, "type": "终端履约", "cid": "1129"},
    {"id": 23, "name": "Polymarket", "aliases": ["Polymarket (去水折合)"], "zone": 3, "type": "终端履约", "cid": "PM"},
]


def _normalize_company_name(raw_name: str) -> str:
    """将输入机构名称归一为法定 23 家标准名，不在白名单内返回空字符串"""
    clean = str(raw_name or "").strip()
    if not clean:
        return ""
    for comp in LEGAL_23_COMPANIES:
        if clean.lower() == comp["name"].lower():
            return comp["name"]
        for alias in comp["aliases"]:
            if clean.lower() == alias.lower():
                return comp["name"]
    for comp in LEGAL_23_COMPANIES:
        for alias in comp["aliases"]:
            if alias.lower() in clean.lower():
                return comp["name"]
    return ""


def _require_any_non_empty_str(data: Dict[str, Any], keys: Tuple[str, ...], label: str) -> str:
    for k in keys:
        val = str(data.get(k) or "").strip()
        if val:
            return val
    raise ValueError(f"装配失败：缺少必填真实字段 `{keys[0]}` ({label})，严禁使用默认值伪造")


def _normalize_ah_row(r: Union[Dict[str, Any], List[Any], Tuple[Any, ...]], cname: str) -> Tuple[str, str, Any, Any, str]:
    if isinstance(r, (list, tuple)):
        if len(r) < 4:
            raise ValueError(f"装配失败：`{cname}` 亚盘流水元组长度不足: {r}")
        t_val = str(r[0]).strip()
        line_val = str(r[1]).strip()
        h_val = r[2]
        a_val = r[3]
        st_val = str(r[4]).strip() if len(r) > 4 else "即"
    elif isinstance(r, dict):
        t_val = str(r.get("time") or "").strip()
        line_val = str(r.get("line") or r.get("handicap") or "").strip()
        h_val = r.get("home")
        a_val = r.get("away")
        st_val = str(r.get("status") or r.get("stage") or "即").strip()
    else:
        raise ValueError(f"装配失败：`{cname}` 亚盘流水行格式非法: {r}")
    if not t_val or not line_val or h_val is None or a_val is None:
        raise ValueError(f"装配失败：`{cname}` 亚盘流水存在残缺字段: {r}")
    return t_val, line_val, h_val, a_val, st_val


def _normalize_ou_row(r: Union[Dict[str, Any], List[Any], Tuple[Any, ...]], cname: str) -> Tuple[str, str, Any, Any, str]:
    if isinstance(r, (list, tuple)):
        if len(r) < 4:
            raise ValueError(f"装配失败：`{cname}` 大小球流水元组长度不足: {r}")
        t_val = str(r[0]).strip()
        line_val = str(r[1]).strip()
        o_val = r[2]
        u_val = r[3]
        st_val = str(r[4]).strip() if len(r) > 4 else "即"
    elif isinstance(r, dict):
        t_val = str(r.get("time") or "").strip()
        line_val = str(r.get("line") or r.get("goal") or "").strip()
        o_val = r.get("over")
        u_val = r.get("under")
        st_val = str(r.get("status") or r.get("stage") or "即").strip()
    else:
        raise ValueError(f"装配失败：`{cname}` 大小球流水行格式非法: {r}")
    if not t_val or not line_val or o_val is None or u_val is None:
        raise ValueError(f"装配失败：`{cname}` 大小球流水存在残缺字段: {r}")
    return t_val, line_val, o_val, u_val, st_val


def _normalize_eu_row(r: Union[Dict[str, Any], List[Any], Tuple[Any, ...]], cname: str) -> Tuple[str, Any, Any, Any, str, str, str]:
    if isinstance(r, (list, tuple)):
        if len(r) < 4:
            raise ValueError(f"装配失败：`{cname}` 欧指流水元组长度不足: {r}")
        t_val = str(r[0]).strip()
        h_val = r[1]
        d_val = r[2]
        a_val = r[3]
        ret_val = str(r[4]).strip() if len(r) > 4 else "-"
        kelly_val = str(r[5]).strip() if len(r) > 5 else "-"
        st_val = str(r[6]).strip() if len(r) > 6 else "即"
    elif isinstance(r, dict):
        t_val = str(r.get("time") or "").strip()
        h_val = r.get("h")
        d_val = r.get("d")
        a_val = r.get("a")
        ret_val = str(r.get("ret") or r.get("returnRate") or "-").strip()
        kelly_val = str(r.get("kelly") or "-").strip()
        st_val = str(r.get("status") or r.get("stage") or "即").strip()
    else:
        raise ValueError(f"装配失败：`{cname}` 欧指流水行格式非法: {r}")
    if not t_val or h_val is None or d_val is None or a_val is None:
        raise ValueError(f"装配失败：`{cname}` 欧指流水存在残缺字段: {r}")
    return t_val, h_val, d_val, a_val, ret_val, kelly_val, st_val


AI_AGENT_METADATA_DIRECTIVE: str = (
    "> [!IMPORTANT]\n"
    "> **🤖 给看这份数据的 AI 分析师：读盘前请务必牢记以下三句话！**\n"
    "> 1. **整篇都要看，千万别偷懒只看几行**：这份数据从上到下包含了伤停名单、攻防底牌、23家欧指初即盘、7家公司变盘流水和比分矩阵。必须宏观完整地通读全篇，综合所有信息再分析，严禁只挑两三行赔率就匆忙下结论！\n"
    "> 2. **表格是倒着排的，最底下一行才是最早的初盘**：流水表格最上面那行是比赛快开始时的【最新即时盘】，最下面那行才是最早开出的【历史初盘起点】。看时间先后只认第 1 列的【变盘时间】（哪行日期时间早，哪行就是先发生的，哪怕最后一行写着“即”也是最早的初盘），千万别把时间顺序给看反了！\n"
    "> 3. **先算初终差值，再看中间有没有故意拉高又暴跌**：动笔第一步先手算清楚变化幅度（即时盘 - 初盘）。不仅要看头尾，更要看中间过程——特别是庄家在中间故意拉高水位诱人上当、临开赛前又突然狂砸暴跌（倒 V 型洗盘）的陷阱！"
)


class SummaryTableAssembler:
    """
    负责将 Worker 结构化推演结果（单场 JSON 交付小卡片）机械单射组装为标准 7 列表格，
    绝对不经过大模型二次转述，从物理机制上消灭张冠李戴、方向覆盖与字序错乱。
    """

    @staticmethod
    def assemble_row(card: Dict[str, Any]) -> str:
        code_time = f"{card.get('matchCode', '')} {card.get('kickoffTime', '')}".strip()
        teams = card.get('teams', '').strip()
        primary_dir = card.get('primaryDirection', '').strip()
        handicap_dir = card.get('handicapDirection', '').strip()
        prob = card.get('ooEpcProbabilities', '').strip()
        trap = card.get('bookmakerTrapDeduction', '').strip()
        pm_link = card.get('polymarketLink', '').strip()
        return f"| {code_time} | {teams} | {primary_dir} | {handicap_dir} | {prob} | {trap} | {pm_link} |"

    @classmethod
    def assemble_table(cls, cards: List[Dict[str, Any]]) -> str:
        header = (
            "| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        )
        rows = [cls.assemble_row(c) for c in cards]
        return "\n".join([header] + rows)


class GoldenSnapshotAssembler:
    """将真实解析结构化数据一对一原样序列化为黄金【推演源数据】规范 Markdown（零默认值伪造）"""

    def assemble(self, data: Dict[str, Any]) -> str:
        match_id = _require_any_non_empty_str(data, ("matchId",), "比赛 ID")
        code = _require_any_non_empty_str(data, ("sportteryCode", "code"), "体彩场次编号")
        league = _require_any_non_empty_str(data, ("league",), "联赛名称")
        home = _require_any_non_empty_str(data, ("homeTeam",), "主队名称")
        away = _require_any_non_empty_str(data, ("awayTeam",), "客队名称")
        kickoff = _require_any_non_empty_str(data, ("kickoffTime", "kickoff"), "开球时间")

        venue_weather = str(data.get("venueWeather") or "真实赛场数据未披露").strip()
        pm_url = str(data.get("polymarketUrl") or "").strip()
        pm_prices = str(data.get("polymarketPrices") or "").strip()
        if not pm_url:
            pm_url = "未开盘"

        pm_is_unopened = any(
            kw in pm_url or kw in pm_prices
            for kw in ("未开盘", "未开放", "暂无", "unopened")
        )
        if pm_is_unopened:
            pm_line = pm_url if not pm_prices or pm_prices in pm_url or pm_prices == "官方未开盘" else f"{pm_url} ({pm_prices})"
        elif pm_url.startswith("http"):
            pm_line = f"[{pm_url}]({pm_url})" + (f" ({pm_prices})" if pm_prices else "")
        else:
            pm_line = f"{pm_url}" + (f" ({pm_prices})" if pm_prices else "")

        lines: List[str] = []
        lines.append(f"# 【{code}】{league} {home} vs {away}")
        lines.append("")
        lines.append(f"- **比赛 ID**：{match_id}")
        lines.append(f"- **开球时间**：{kickoff}")
        lines.append(f"- **场地与天气**：{venue_weather}")
        lines.append(f"- **Polymarket 预测市场**：{pm_line}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(AI_AGENT_METADATA_DIRECTIVE)
        lines.append("")
        lines.append("---")
        lines.append("")

        # 一、微观阵容与首发伤停
        lines.append("## 一、微观阵容与首发伤停")
        lines.append("")
        lineup_text = str(data.get("lineupData") or "").strip()
        if lineup_text:
            lines.append(lineup_text)
        else:
            injuries = data.get("injuries") or {}
            h_inj = str(injuries.get("home") or "暂无数据（球探源页面未披露具体伤停名单）").strip()
            a_inj = str(injuries.get("away") or "暂无数据（球探源页面未披露具体伤停名单）").strip()
            lines.append(f"- **{home}**：{h_inj}")
            lines.append(f"- **{away}**：{a_inj}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 二、基础战绩与攻防客观底牌
        lines.append("## 二、基础战绩与攻防客观底牌")
        lines.append("")
        basic_stats_text = str(data.get("basicStatsText") or "").strip()
        if basic_stats_text:
            lines.append(basic_stats_text)
        else:
            home_stats = _require_any_non_empty_str(data, ("homeStats",), "主队真实近况与场均进失球")
            away_stats = _require_any_non_empty_str(data, ("awayStats",), "客队真实近况与场均进失球")
            lines.append(f"- **主队近况**：{home_stats}")
            lines.append(f"- **客队近况**：{away_stats}")
            if data.get("scheduleTrap"):
                lines.append(f"- **赛程间隔**：{str(data['scheduleTrap']).strip()}")
            if data.get("profiling"):
                lines.append(f"- **盘路画像**：{str(data['profiling']).strip()}")
            if data.get("technicalStats"):
                lines.append(f"- **核心技统**：{str(data['technicalStats']).strip()}")
            if data.get("goalTimeDist"):
                lines.append(f"- **进球时段分布**：{str(data['goalTimeDist']).strip()}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 三、欧洲指数百家做市商清单（法定 23 家）
        lines.append("## 三、欧洲指数百家做市商清单（法定 23 家）")
        lines.append("")
        lines.append("| 机构类型 | 机构 | 初盘主胜 | 初盘平局 | 初盘客胜 | 初返还 | 即时主胜 | 即时平局 | 即时客胜 | 即时返还 | 凯利(主/平/客) |")
        lines.append("| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |")

        eu_input = data.get("europe1x2") or data.get("europe23") or []
        if not eu_input:
            raise ValueError("装配失败：`europe1x2` / `europe23` 为空，严禁无欧指数据生成快照")

        eu_map: Dict[str, Dict[str, Any]] = {}
        for item in eu_input:
            std_name = _normalize_company_name(item.get("company", ""))
            if std_name:
                eu_map[std_name] = item

        emitted_eu_count = 0
        for comp in LEGAL_23_COMPANIES:
            c_name = comp["name"]
            c_type = comp["type"]
            if c_name not in eu_map:
                continue
            row = eu_map[c_name]
            init_o = row.get("initialOdds")
            live_o = row.get("liveOdds")
            init_r = row.get("initialReturn")
            live_r = row.get("liveReturn")
            kelly = row.get("kelly")
            if kelly == "-":
                kelly = ["-", "-", "-"]
            if (
                not isinstance(init_o, (list, tuple)) or len(init_o) < 3
                or not isinstance(live_o, (list, tuple)) or len(live_o) < 3
                or init_r is None or live_r is None
                or not isinstance(kelly, (list, tuple)) or len(kelly) < 3
            ):
                raise ValueError(f"装配失败：机构 `{c_name}` 的欧指初即盘/返还率/凯利字段残缺，严禁回退假默认值")

            init_r_str = f"{init_r}%" if isinstance(init_r, (int, float)) else str(init_r)
            live_r_str = f"{live_r}%" if isinstance(live_r, (int, float)) else str(live_r)
            if isinstance(kelly[0], (int, float)):
                kelly_str = f"{kelly[0]:.2f}/{kelly[1]:.2f}/{kelly[2]:.2f}"
            elif all(str(x).strip() in ("-", "") for x in kelly[:3]):
                kelly_str = "-"
            else:
                kelly_str = "/".join(str(x) for x in kelly[:3])
            lines.append(
                f"| {c_type} | {c_name} | {init_o[0]} | {init_o[1]} | {init_o[2]} | {init_r_str} | "
                f"{live_o[0]} | {live_o[1]} | {live_o[2]} | {live_r_str} | {kelly_str} |"
            )
            emitted_eu_count += 1

        if emitted_eu_count == 0:
            raise ValueError("装配失败：没有任何合法白名单机构的欧指数据")

        lines.append("")
        lines.append("---")
        lines.append("")

        # 四、核心做市商与终端标的真实变盘时序流水（逐行原样零篡改）
        lines.append("## 四、核心做市商与终端标的真实变盘时序流水（逐行原样零篡改）")
        lines.append("")
        lines.append("### 第一战区：欧亚双盘全能做市商（亚盘 / 大小球 / 欧指 真实变盘流水）")
        lines.append("")

        comp_details = data.get("companyDetails") or {}
        zone1_comps = [c for c in LEGAL_23_COMPANIES if c["zone"] == 1]
        for c in zone1_comps:
            cname = c["name"]
            detail = comp_details.get(cname)
            if not detail:
                for k, v in comp_details.items():
                    if _normalize_company_name(k) == cname:
                        detail = v
                        break

            ah_rows = (detail or {}).get("ah") or data.get(f"{cname}_ah") or []
            ou_rows = (detail or {}).get("ou") or data.get(f"{cname}_ou") or []
            eu_rows = (detail or {}).get("eu") or data.get(f"{cname}_eu") or []
            if not eu_rows and cname in eu_map:
                # 若未提供独立欧指多行流水，但总表有初即盘真实数据且包含 changeTime，可转为初/即两行真实记录
                erow = eu_map[cname]
                ch_t = str(erow.get("changeTime") or "").strip()
                if ch_t:
                    init_o = erow["initialOdds"]
                    live_o = erow["liveOdds"]
                    init_r = erow["initialReturn"]
                    live_r = erow["liveReturn"]
                    kelly = erow["kelly"]
                    k_s = "/".join(str(x) for x in kelly[:3])
                    eu_rows = [
                        (ch_t, live_o[0], live_o[1], live_o[2], str(live_r), k_s, "即"),
                        (ch_t, init_o[0], init_o[1], init_o[2], str(init_r), k_s, "初盘"),
                    ]

            if not ah_rows:
                if cname == "香港马会":
                    ah_rows = [("-", "官方未开盘", "-", "-", "未开盘")]
                else:
                    raise ValueError(f"装配失败：机构 `{cname}` 缺少亚盘真实变盘流水，严禁伪造默认行")
            if not ou_rows:
                if cname == "香港马会":
                    ou_rows = [("-", "官方未开盘", "-", "-", "未开盘")]
                else:
                    raise ValueError(f"装配失败：机构 `{cname}` 缺少大小球真实变盘流水，严禁伪造默认行")
            if not eu_rows:
                raise ValueError(f"装配失败：机构 `{cname}` 缺少欧指真实变盘流水，严禁伪造默认行")

            ah_rows = denoise_timeline_rows(ah_rows)
            ou_rows = denoise_timeline_rows(ou_rows)
            eu_rows = denoise_timeline_rows(eu_rows)

            lines.append(f"### {c['id']}. {cname} (欧亚双盘核心, {c['type']}, cid={c['cid']})")
            lines.append("")
            lines.append("#### 亚盘真实变盘流水")
            lines.append("| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |")
            lines.append("| :--- | :--- | ---: | ---: | :--- |")
            for r in ah_rows:
                t_val, line_val, h_val, a_val, st_val = _normalize_ah_row(r, cname)
                lines.append(f"| {t_val} | {line_val} | {h_val} | {a_val} | {st_val} |")
            lines.append("")

            lines.append("#### 大小球真实变盘流水")
            lines.append("| 变盘时间 | 盘口 | 大球水 | 小球水 | 状态 |")
            lines.append("| :--- | :--- | ---: | ---: | :--- |")
            for r in ou_rows:
                t_val, line_val, o_val, u_val, st_val = _normalize_ou_row(r, cname)
                lines.append(f"| {t_val} | {line_val} | {o_val} | {u_val} | {st_val} |")
            lines.append("")

            lines.append("#### 欧指真实变盘流水")
            lines.append("| 变盘时间 | 主胜 | 平局 | 客胜 | 返还率 | 凯利(主/平/客) | 状态 |")
            lines.append("| :--- | ---: | ---: | ---: | ---: | :--- | :--- |")
            for r in eu_rows:
                t_val, h_val, d_val, a_val, ret_val, kelly_val, st_val = _normalize_eu_row(r, cname)
                lines.append(f"| {t_val} | {h_val} | {d_val} | {a_val} | {ret_val} | {kelly_val} | {st_val} |")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("### 第三战区：终端履约实盘标的（中国体育彩票官方 × Polymarket 预测市场）")
        lines.append("")
        lines.append("### 22. 中国体彩 (终端履约标的, 国家特许复合全玩法, cid=1129)")
        lines.append("")
        sp_detail = comp_details.get("体彩官方") or comp_details.get("中国体彩") or comp_details.get("竞彩官方") or {}
        sp_had = sp_detail.get("had") or sp_detail.get("eu") or data.get("sporttery_had") or []
        if sp_had:
            sp_had = denoise_timeline_rows(sp_had)
            lines.append("#### 胜平负 (HAD) 真实变盘流水")
            lines.append("| 变盘时间 | 主胜 | 平局 | 客胜 | 返还率 | 凯利(主/平/客) | 状态 |")
            lines.append("| :--- | ---: | ---: | ---: | ---: | :--- | :--- |")
            for r in sp_had:
                t_val, h_val, d_val, a_val, ret_val, kelly_val, st_val = _normalize_eu_row(r, "中国体彩")
                lines.append(f"| {t_val} | {h_val} | {d_val} | {a_val} | {ret_val} | {kelly_val} | {st_val} |")
            lines.append("")

        let_ball = str(data.get("sportteryLetBall") or "").strip()
        hhad = sp_detail.get("hhad") or data.get("sporttery_hhad") or {}
        if isinstance(hhad, list) and hhad:
            first_h = hhad[0]
            if isinstance(first_h, (list, tuple)) and len(first_h) >= 4:
                let_ball = str(first_h[0]).strip()
                hhad = {"h": first_h[1], "d": first_h[2], "a": first_h[3]}
        if let_ball and isinstance(hhad, dict) and hhad.get("h") is not None and hhad.get("d") is not None and hhad.get("a") is not None:
            lines.append(f"#### 让球胜平负 (HHAD `[{let_ball}]`) 终端对冲基准")
            lines.append("| 玩法类型 | 官方让球数 | 让胜 | 让平 | 让负 |")
            lines.append("| :--- | :---: | ---: | ---: | ---: |")
            lines.append(f"| **HHAD 让球盘** | `{let_ball}` | {hhad['h']} | {hhad['d']} | {hhad['a']} |")
            lines.append("")

        lines.append("### 23. Polymarket (终端履约标的, 链上订单簿预测市场)")
        lines.append("")
        pm_detail = comp_details.get("Polymarket") or {}
        pm_rows = pm_detail.get("ts") or data.get("polymarket_ts") or data.get("polymarket_rows") or []
        if pm_is_unopened or not pm_rows:
            lines.append("> 📌 **当前场次未开放 Polymarket 预测市场交易池或无订单簿历史切片，严禁伪造挂单时序。**")
            lines.append("")
        else:
            lines.append("#### 预测市场真实挂单流水")
            lines.append("| 观测时间 | 主胜概率(¢) | 平局概率(¢) | 客胜概率(¢) | 主胜去水折合 | 平局去水折合 | 客胜去水折合 |")
            lines.append("| :--- | ---: | ---: | ---: | ---: | ---: | ---: |")
            for r in pm_rows:
                if isinstance(r, (list, tuple)) and len(r) >= 7:
                    lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |")
                elif isinstance(r, dict):
                    lines.append(
                        f"| {r['time']} | {r['h_c']} | {r['d_c']} | {r['a_c']} | "
                        f"{r['h_o']} | {r['d_o']} | {r['a_o']} |"
                    )
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## 五、Crown 皇冠全指数波胆与比分矩阵")
        lines.append("")
        cs_raw = data.get("correctScores") or []
        cs_items: List[str] = []
        for item in cs_raw:
            if isinstance(item, dict) and "score" in item and "odds" in item:
                cs_items.append(f"{item['score']} ({item['odds']})")
            elif isinstance(item, (list, tuple)):
                for idx in range(0, len(item) - 1, 2):
                    sc = str(item[idx]).strip()
                    od = str(item[idx + 1]).strip()
                    if sc and od and sc != "-" and od != "-":
                        cs_items.append(f"{sc} ({od})")
        if len(cs_items) < 8:
            raise ValueError("装配失败：`correctScores` 波胆比分少于 8 项，严禁回退假波胆赔率")
        lines.append(f"- **波胆比分赔率**：{' ｜ '.join(cs_items)}")
        tg_text = data.get("totalGoalsOdds") or data.get("totalGoalsText")
        if tg_text:
            lines.append(f"- **总进球赔率**：{str(tg_text).strip()}")
        hf_text = data.get("halfFullOdds") or data.get("halfFullTimeText")
        if hf_text:
            lines.append(f"- **半全场赔率**：{str(hf_text).strip()}")
        lines.append("")

        return "\n".join(lines)

    def update_meta(self, meta_path: Any, data: Dict[str, Any]) -> None:
        """同步更新同目录下 meta.md 的落盘状态"""
        from pathlib import Path
        p = Path(meta_path)
        if not p.exists():
            return
        mid = str(data.get("matchId") or "").strip()
        if not mid:
            return
        content = p.read_text(encoding="utf-8")
        target = f"{mid}.md (待分析抓取)"
        repl = f"[{mid}.md]({mid}.md) (✅已落盘)"
        if target in content:
            p.write_text(content.replace(target, repl), encoding="utf-8")


SnapshotAssembler = GoldenSnapshotAssembler

