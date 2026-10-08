"""
校验/src/domain/profiling_parser.py
操盘画像纯领域结构化解析服务 (Profiling Parser)

负责将球探分析页中的 raw 制表符文本安全解析为结构化列表与指标字典，
支持大模型精确研判与下游纯数学算法消费。
"""

from __future__ import annotations
import re
from typing import Any, Dict, List, Optional


class ProfilingParser:
    """操盘画像纯领域解析器"""

    def parse_identical_odds(self, raw_text: Optional[str]) -> List[Dict[str, Any]]:
        """
        解析相同初盘历史走势
        """
        if not raw_text or not isinstance(raw_text, str):
            return []

        # 清洗多余回车并分行
        lines = [line.strip() for line in raw_text.replace('\r\n', '\n').split('\n') if line.strip()]
        if not lines:
            return []

        results: List[Dict[str, Any]] = []
        current_team: Optional[str] = None
        current_handicap: Optional[str] = None
        current_stats: Dict[str, Dict[str, Any]] = {}
        current_recent6: List[str] = []

        def flush_current():
            if current_team and (current_handicap or current_stats or current_recent6):
                results.append({
                    "team": current_team,
                    "initialHandicap": current_handicap or "",
                    "stats": dict(current_stats),
                    "recent6": list(current_recent6)
                })

        i = 0
        while i < len(lines):
            line = lines[i]

            # 匹配初盘: xxx
            handicap_match = re.search(r"初盘[:：]\s*([^\s\t]+)", line)
            if handicap_match:
                current_handicap = handicap_match.group(1).strip()
                i += 1
                continue

            # 匹配近6场盘路走势: ...
            if "近6场盘路走势" in line:
                tokens = re.split(r"[:：\s\t\xa0]+", line)
                recent_tokens = [t for t in tokens if t in ("赢", "输", "走")]
                current_recent6 = recent_tokens
                i += 1
                continue

            # 匹配表格行: 总/主/客 \t 赢 \t 走 \t 输 \t 赢盘率
            parts = [p.strip() for p in re.split(r"[\t\s]+", line) if p.strip()]
            if parts and parts[0] in ("总", "主", "客"):
                row_key = "total" if parts[0] == "总" else ("home" if parts[0] == "主" else "away")
                # parts 格式通常为: ['总', '87', '0', '124', '41.2%']
                if len(parts) >= 5:
                    try:
                        win = int(parts[1])
                        push = int(parts[2])
                        loss = int(parts[3])
                        win_rate = parts[4]
                        current_stats[row_key] = {
                            "win": win,
                            "push": push,
                            "loss": loss,
                            "winRate": win_rate
                        }
                    except ValueError:
                        pass
                i += 1
                continue

            # 遇到可能是队名的新行 (非表头，非关键字)
            if not any(k in line for k in ("赢盘率", "盘路走势", "全场", "半场", "查看", "亚让盘")):
                if current_team and (current_stats or current_handicap):
                    flush_current()
                    current_handicap = None
                    current_stats = {}
                    current_recent6 = []
                current_team = line
                i += 1
                continue

            i += 1

        flush_current()
        return results

    def parse_handicap_trends(self, raw_text: Optional[str]) -> List[Dict[str, Any]]:
        """
        解析近期让球与大小球盘路趋势 (全场/半场)
        """
        if not raw_text or not isinstance(raw_text, str):
            return []

        lines = [line.strip() for line in raw_text.replace('\r\n', '\n').split('\n') if line.strip()]
        if not lines:
            return []

        results: List[Dict[str, Any]] = []
        current_team: Optional[str] = None
        current_scope: str = "全场"
        current_stats: Dict[str, Dict[str, Any]] = {}
        recent6_handicap: List[str] = []
        recent6_overunder: List[str] = []

        def flush_current():
            if current_team and current_stats:
                results.append({
                    "team": current_team,
                    "scope": current_scope,
                    "stats": dict(current_stats),
                    "recent6_handicap": list(recent6_handicap),
                    "recent6_overunder": list(recent6_overunder)
                })

        i = 0
        while i < len(lines):
            line = lines[i]

            # 作用域识别: 全场 / 半场
            if line.startswith("全场") or "\t全场" in line:
                current_scope = "全场"
                i += 1
                continue
            elif line.startswith("半场") or "\t半场" in line:
                if current_team and current_stats:
                    flush_current()
                    current_stats = {}
                    recent6_handicap = []
                    recent6_overunder = []
                current_scope = "半场"
                i += 1
                continue

            # 匹配近6场让球与大小走势
            if "近6场" in line:
                tokens = [t.strip() for t in re.split(r"[\t\s\xa0]+", line) if t.strip()]
                # 寻找输赢走列表与大小走列表
                h_list = []
                ou_list = []
                for tok in tokens:
                    if tok in ("赢", "输", "走"):
                        h_list.append(tok)
                    elif tok in ("大", "小"):
                        ou_list.append(tok)
                if h_list:
                    recent6_handicap = h_list
                if ou_list:
                    recent6_overunder = ou_list
                i += 1
                continue

            # 匹配统计行: 总/主场/客场
            parts = [p.strip() for p in re.split(r"[\t\s]+", line) if p.strip()]
            if parts and parts[0] in ("总", "主场", "客场"):
                row_key = "total" if parts[0] == "总" else ("home" if parts[0] == "主场" else "away")
                # parts 格式常见: ['总', '28', '10', '2', '16', '35.7%', '查看', '11', '39.3%', '16', '57.1%', '查看']
                # 过滤掉 '查看'
                clean_parts = [p for p in parts if p != "查看"]
                if len(clean_parts) >= 6:
                    try:
                        played = int(clean_parts[1])
                        win = int(clean_parts[2])
                        push = int(clean_parts[3])
                        loss = int(clean_parts[4])
                        win_rate = clean_parts[5]
                        over = int(clean_parts[6]) if len(clean_parts) > 6 and clean_parts[6].isdigit() else 0
                        over_rate = clean_parts[7] if len(clean_parts) > 7 else ""
                        under = int(clean_parts[8]) if len(clean_parts) > 8 and clean_parts[8].isdigit() else 0
                        under_rate = clean_parts[9] if len(clean_parts) > 9 else ""

                        current_stats[row_key] = {
                            "played": played,
                            "win": win,
                            "push": push,
                            "loss": loss,
                            "winRate": win_rate,
                            "over": over,
                            "overRate": over_rate,
                            "under": under,
                            "underRate": under_rate
                        }
                    except (ValueError, IndexError):
                        pass
                i += 1
                continue

            # 遇到队名
            if not any(k in line for k in ("亚让盘", "进球数", "赢盘率", "大球率", "小球率", "赛", "走水")):
                if current_team and current_stats:
                    flush_current()
                    current_stats = {}
                    recent6_handicap = []
                    recent6_overunder = []
                current_team = line
                i += 1
                continue

            i += 1

        flush_current()
        return results

    def enrich_profiling(self, profiling: Dict[str, Any]) -> Dict[str, Any]:
        """
        结构化增强操盘画像字典，添加 items 字段
        """
        if not profiling or not isinstance(profiling, dict):
            return profiling

        if "identicalOddsHistory" in profiling and isinstance(profiling["identicalOddsHistory"], dict):
            raw = profiling["identicalOddsHistory"].get("raw")
            if raw:
                profiling["identicalOddsHistory"]["items"] = self.parse_identical_odds(raw)

        if "handicapTrends" in profiling and isinstance(profiling["handicapTrends"], dict):
            raw = profiling["handicapTrends"].get("raw")
            if raw:
                profiling["handicapTrends"]["items"] = self.parse_handicap_trends(raw)

        return profiling
