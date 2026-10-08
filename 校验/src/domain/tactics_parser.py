"""
校验/src/domain/tactics_parser.py
战术技统与攻防压制力领域解析服务 (TacticsParser)

负责将球探快照中 tactics 的原始文本（技术统计、进球时段分布、未来赛程）
解析为强类型结构化字典与指标列表，供大模型精准研判与泊松期望值参数修正。
"""

from __future__ import annotations
import re
from typing import Any, Dict, List, Optional


class TacticsParser:
    """战术技统纯领域解析器"""

    def parse_technical_stats(self, raw_text: Optional[str]) -> List[Dict[str, Any]]:
        """
        解析技术统计表格 (胜平负%, 进球, 失球, 净胜球, 场均进球, 场均角球, 场均黄牌...)
        """
        if not raw_text or not isinstance(raw_text, str):
            return []

        lines = [line.strip() for line in raw_text.replace('\r\n', '\n').split('\n') if line.strip()]
        if len(lines) < 3:
            return []

        results: List[Dict[str, Any]] = []

        # 遍历数据行（跳过前两行表头）
        for line in lines[2:]:
            parts = [p.strip() for p in re.split(r"[\t\s]+", line) if p.strip()]
            if len(parts) >= 10:
                team_name = parts[0]
                try:
                    # parts: [队名, 胜%, 平%, 负%, 进球, 失球, 净胜球, 场均进球, 场均角球, 场均黄牌, 同进, 同失, 同净, 同场均, 同胜%, 同平%, 同负%]
                    goals = int(parts[4])
                    conceded = int(parts[5])
                    net_goals = int(parts[6])
                    avg_goals = float(parts[7])
                    avg_corners = float(parts[8])
                    avg_yellow_cards = float(parts[9])
                    
                    home_away_avg_goals = float(parts[13]) if len(parts) > 13 else avg_goals

                    results.append({
                        "team": team_name,
                        "win_rate": parts[1],
                        "draw_rate": parts[2],
                        "loss_rate": parts[3],
                        "goals": goals,
                        "conceded": conceded,
                        "net_goals": net_goals,
                        "avg_goals": avg_goals,
                        "avg_corners": avg_corners,
                        "avg_yellow_cards": avg_yellow_cards,
                        "home_away_avg_goals": home_away_avg_goals
                    })
                except (ValueError, IndexError):
                    pass

        return results

    def parse_future_schedule(self, raw_text: Optional[str]) -> List[Dict[str, Any]]:
        """
        解析未来赛程列表 (时间, 赛事, 对阵, 相隔天数)
        """
        if not raw_text or not isinstance(raw_text, str):
            return []

        lines = [line.strip() for line in raw_text.replace('\r\n', '\n').split('\n') if line.strip()]
        results: List[Dict[str, Any]] = []
        current_team: Optional[str] = None
        current_matches: List[Dict[str, Any]] = []

        def flush_current():
            if current_team and current_matches:
                results.append({
                    "team": current_team,
                    "matches": list(current_matches)
                })

        for line in lines:
            if "时间\t赛事" in line or line.startswith("时间"):
                continue

            # 匹配对阵行: 日期 \t 赛事 \t 对阵 \t 分析 ... \t X 天
            parts = [p.strip() for p in re.split(r"[\t]+", line) if p.strip()]
            if len(parts) >= 3 and any(char.isdigit() for char in parts[0]) and "-" in parts[0]:
                date_str = parts[0]
                league_str = parts[1]
                match_str = parts[2]
                days = 0
                for part in parts:
                    day_match = re.search(r"(\d+)\s*天", part)
                    if day_match:
                        days = int(day_match.group(1))
                        break
                current_matches.append({
                    "date": date_str,
                    "league": league_str,
                    "opponent_match": match_str,
                    "days_interval": days
                })
            else:
                # 可能是队名
                if not any(k in line for k in ("相隔", "分析", "直播", "赛事")):
                    if current_team and current_matches:
                        flush_current()
                        current_matches = []
                    current_team = line

        flush_current()
        return results

    def parse_goal_time_distribution(self, raw_text: Optional[str]) -> Dict[str, Any]:
        """
        解析进球时段分布与首球时段统计
        """
        if not raw_text or not isinstance(raw_text, str):
            return {"distribution": {}, "first_goal": {}}

        lines = [line.strip() for line in raw_text.replace('\r\n', '\n').split('\n') if line.strip()]
        intervals = ["1-10", "11-20", "21-30", "31-40", "41-45", "46-50", "51-60", "61-70", "71-80", "81-90+"]

        dist_dict: Dict[str, Dict[str, int]] = {}
        first_goal_dict: Dict[str, Dict[str, int]] = {}
        target = dist_dict

        for line in lines:
            if "第一个进球的时间统计" in line:
                target = first_goal_dict
                continue

            parts = [p.strip() for p in re.split(r"[\t\s]+", line) if p.strip()]
            if parts and parts[0] in ("总", "主", "客"):
                row_key = "total" if parts[0] == "总" else ("home" if parts[0] == "主" else "away")
                values = parts[1:]
                row_map: Dict[str, int] = {}
                for idx, intv in enumerate(intervals):
                    if idx < len(values):
                        try:
                            row_map[intv] = int(values[idx])
                        except ValueError:
                            row_map[intv] = 0
                target[row_key] = row_map

        return {
            "distribution": dist_dict,
            "first_goal": first_goal_dict
        }

    def enrich_tactics(self, tactics: Dict[str, Any]) -> Dict[str, Any]:
        """
        结构化增强战术技统字典
        """
        if not tactics or not isinstance(tactics, dict):
            return tactics

        if "technicalStats" in tactics and isinstance(tactics["technicalStats"], dict):
            raw = tactics["technicalStats"].get("raw")
            if raw:
                tactics["technicalStats"]["items"] = self.parse_technical_stats(raw)

        if "futureSchedule" in tactics and isinstance(tactics["futureSchedule"], dict):
            raw = tactics["futureSchedule"].get("raw")
            if raw:
                tactics["futureSchedule"]["items"] = self.parse_future_schedule(raw)

        if "goalTimeDistribution" in tactics and isinstance(tactics["goalTimeDistribution"], dict):
            raw = tactics["goalTimeDistribution"].get("raw")
            if raw:
                tactics["goalTimeDistribution"]["structured"] = self.parse_goal_time_distribution(raw)

        return tactics
