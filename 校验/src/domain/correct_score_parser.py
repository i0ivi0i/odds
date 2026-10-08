"""
校验/src/domain/correct_score_parser.py
波胆比分与半全场赔率领域解析服务 (CorrectScoreParser)

将球探快照中 correctScoreOdds 的原始文本安全解析为结构化波胆赔率字典 (homeWin, draw, awayWin, flat)
以及半全场赔率字典 (halfFullTime)，并按 SKILL.md 要求挂载到 snapshot["markets"]["crowFullIndex"]["correctScores"]。
"""

from __future__ import annotations
import re
from typing import Any, Dict, Optional


class CorrectScoreParser:
    """皇冠 Crown 波胆与半全场赔率纯领域解析器"""

    def parse(self, raw_text: Optional[str]) -> Dict[str, Any]:
        """
        解析波胆比分及半全场赔率文本
        """
        if not raw_text or not isinstance(raw_text, str):
            return {
                "correctScores": {"homeWin": {}, "draw": {}, "awayWin": {}, "flat": {}},
                "halfFullTime": {}
            }

        lines = [line.strip() for line in raw_text.replace('\r\n', '\n').split('\n') if line.strip()]
        
        home_win: Dict[str, float] = {}
        draw: Dict[str, float] = {}
        away_win: Dict[str, float] = {}
        flat: Dict[str, float] = {}
        half_full_time: Dict[str, float] = {}

        i = 0
        while i < len(lines):
            line = lines[i]

            # 1. 匹配 胜比分
            if line.startswith("胜\t") or line == "胜":
                # 表头可能同在第 i 行，如 胜\t1:0\t2:0...
                headers = [p.strip() for p in re.split(r"[\t\s]+", line) if p.strip()]
                score_names = [h for h in headers if h != "胜"]
                # 赔率行在下一行 i+1
                if i + 1 < len(lines):
                    odds_tokens = [p.strip() for p in re.split(r"[\t\s]+", lines[i + 1]) if p.strip()]
                    for score, val_str in zip(score_names, odds_tokens):
                        try:
                            val = float(val_str)
                            home_win[score] = val
                            flat[score] = val
                        except ValueError:
                            pass
                    i += 2
                    continue

            # 2. 匹配 平比分
            elif line.startswith("平\t") or line == "平":
                headers = [p.strip() for p in re.split(r"[\t\s]+", line) if p.strip()]
                score_names = [h for h in headers if h != "平"]
                if i + 1 < len(lines):
                    odds_tokens = [p.strip() for p in re.split(r"[\t\s]+", lines[i + 1]) if p.strip()]
                    for score, val_str in zip(score_names, odds_tokens):
                        try:
                            val = float(val_str)
                            draw[score] = val
                            flat[score] = val
                        except ValueError:
                            pass
                    i += 2
                    continue

            # 3. 匹配 负比分
            elif line.startswith("负\t") or line == "负":
                headers = [p.strip() for p in re.split(r"[\t\s]+", line) if p.strip()]
                score_names = [h for h in headers if h != "负"]
                if i + 1 < len(lines):
                    odds_tokens = [p.strip() for p in re.split(r"[\t\s]+", lines[i + 1]) if p.strip()]
                    for score, val_str in zip(score_names, odds_tokens):
                        try:
                            val = float(val_str)
                            away_win[score] = val
                            flat[score] = val
                        except ValueError:
                            pass
                    i += 2
                    continue

            # 4. 匹配 半全场
            elif line.startswith("半全场\t") or line == "半全场":
                headers = [p.strip() for p in re.split(r"[\t\s]+", line) if p.strip()]
                combos = [h for h in headers if h != "半全场"]
                if i + 1 < len(lines):
                    odds_tokens = [p.strip() for p in re.split(r"[\t\s]+", lines[i + 1]) if p.strip()]
                    for combo, val_str in zip(combos, odds_tokens):
                        try:
                            val = float(val_str)
                            half_full_time[combo] = val
                        except ValueError:
                            pass
                    i += 2
                    continue

            i += 1

        return {
            "correctScores": {
                "homeWin": home_win,
                "draw": draw,
                "awayWin": away_win,
                "flat": flat
            },
            "halfFullTime": half_full_time
        }

    def enrich_snapshot(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """
        结构化丰富快照对象中的 markets.crowFullIndex.correctScores 和 markets.halfFullTime
        """
        if not snapshot or not isinstance(snapshot, dict):
            return snapshot

        raw_score = snapshot.get("correctScoreOdds")
        if not raw_score:
            return snapshot

        parsed = self.parse(raw_score)

        if "markets" not in snapshot or not isinstance(snapshot["markets"], dict):
            snapshot["markets"] = {}

        markets = snapshot["markets"]
        if "crowFullIndex" not in markets or not isinstance(markets["crowFullIndex"], dict):
            markets["crowFullIndex"] = {}

        markets["crowFullIndex"]["correctScores"] = parsed["correctScores"]
        markets["halfFullTime"] = parsed["halfFullTime"]

        return snapshot
