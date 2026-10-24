"""Scrapling capture adapter and endpoint classification.

This module owns the 28-endpoint contract, the 23-bookmaker roster, payload
assessment, and the capture-to-JSONL boundary.  It never writes SQLite and
never writes a project raw bundle.  ETLX is the only data-row writer.

Usage:
    py -3.13 skills/match-scraper/scripts/ingest_spider.py \
        --match-id 3073801 --sales-date 2026-10-22 --home 格拉茨风暴 --away 马赛
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

EURO_CIDS = (
    80, 545, 281, 90, 177, 432, 115, 82, 81, 104, 255,
    110, 2, 474, 649, 800, 482, 386, 826, 16, 1129,
)
CHANGE_CIDS = (1, 3, 8, 12, 47, 42, 48)

TABLE_GROUPS = frozenset({"ah", "ou", "eu"})
CAPTURE_COOLDOWN_SECONDS = 600
WAF_MARKERS = (
    "just a moment...",
    "cloudflare",
    "access denied",
    "cf-chl-",
    "attention required",
)
NO_OPEN_MARKERS = (
    "未开盘",
    "没有开盘",
    "暂无开盘",
    "暂未开盘",
    "not offered",
    "no odds",
)
CORE_CHANGE_CIDS = frozenset({1, 3, 8, 12, 47, 48})


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _text_hash(raw: bytes | None) -> str:
    if raw is None:
        return ""
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class EndpointSpec:
    key: str
    group: str
    url_template: str
    encoding: str
    extraction_type: str
    css_selector: str | None
    required: bool
    empty_state: str
    gate: str
    tier: int = 1
    aggregation_source: str = ""
    skip_request: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EndpointSpec":
        return cls(
            key=data["key"],
            group=data["group"],
            url_template=data["url"],
            encoding=data["encoding"],
            extraction_type=data["extraction_type"],
            css_selector=data.get("css_selector"),
            required=bool(data["required"]),
            empty_state=data["empty_state"],
            gate=data["gate"],
            tier=int(data.get("tier", 1 if data.get("group") in ("core", "polymarket") else 2)),
            aggregation_source=data.get("aggregation_source", ""),
            skip_request=bool(data.get("skip_request", False)),
        )


@dataclass(frozen=True)
class Bookmaker:
    official_name: str
    aliases: tuple[str, ...]
    euro_cid: int | None
    change_cid: int | None
    required_endpoints: tuple[str, ...]
    no_open_rule: str
    role: str = ""
    forbidden_aliases: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Bookmaker":
        return cls(
            official_name=data["official_name"],
            aliases=tuple(data.get("aliases", ())),
            euro_cid=data.get("euro_cid"),
            change_cid=data.get("change_cid"),
            required_endpoints=tuple(data.get("required_endpoints", ())),
            no_open_rule=data.get("no_open_rule", ""),
            role=data.get("role", ""),
            forbidden_aliases=tuple(data.get("forbidden_aliases", ())),
        )


@dataclass(frozen=True)
class EuroHistoryPoint:
    home: float
    draw: float
    away: float
    timestamp: datetime
    return_rate: float
    kelly: tuple[float, ...]


@dataclass(frozen=True)
class Contract:
    endpoints: tuple[EndpointSpec, ...]
    bookmakers: tuple[Bookmaker, ...]
    non_roster_cids: tuple[int, ...]

    @property
    def endpoint_keys(self) -> tuple[str, ...]:
        return tuple(endpoint.key for endpoint in self.endpoints)

    @property
    def euro_cids(self) -> tuple[int, ...]:
        return tuple(
            bookmaker.euro_cid
            for bookmaker in self.bookmakers
            if bookmaker.euro_cid is not None
        )

    @property
    def change_cids(self) -> tuple[int, ...]:
        return tuple(
            bookmaker.change_cid
            for bookmaker in self.bookmakers
            if bookmaker.change_cid is not None
        )

    def endpoint(self, key: str) -> EndpointSpec | None:
        for endpoint in self.endpoints:
            if endpoint.key == key:
                return endpoint
        return None


@dataclass
class EndpointAssessment:
    key: str
    url: str
    status: int
    text: str
    encoding: str
    state: str
    errors: list[str] = field(default_factory=list)
    raw_bytes: int = 0
    raw_sha256: str = ""
    attempts: int = 1
    fetched_at: str = field(default_factory=_now)
    chars: int = 0
    sha256: str = ""

    def __post_init__(self) -> None:
        self.chars = len(self.text)
        self.sha256 = _sha256(self.text)
        if not self.raw_bytes:
            self.raw_bytes = len(self.text.encode("utf-8"))
        if not self.raw_sha256:
            self.raw_sha256 = self.sha256

    def receipt(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "status": self.status,
            "state": self.state,
            "errors": list(self.errors),
            "raw_bytes": self.raw_bytes,
            "chars": self.chars,
            "sha256": self.sha256,
            "raw_sha256": self.raw_sha256,
            "encoding": self.encoding,
            "attempts": self.attempts,
            "fetched_at": self.fetched_at,
            "empty_state": self.state if self.state == "not_offered" else None,
        }

    def item(self, match_id: str, extraction_type: str = "") -> dict[str, Any]:
        return {
            "match_id": str(match_id),
            "endpoint_key": self.key,
            "content_type": content_type_for(self.key, self.text, extraction_type),
            "content": self.text,
            "chars": self.chars,
            "raw_sha256": self.raw_sha256 or self.sha256,
            "sha256": self.sha256,
            "source_url": self.url,
            "fetched_at": self.fetched_at,
            "status": int(self.status),
            "state": self.state,
            "empty_state": self.state if self.state == "not_offered" else None,
            "extraction_type": extraction_type,
        }


def content_type_for(key: str, text: str, extraction_type: str = "") -> str:
    stripped = text.lstrip("\ufeff \t\r\n")
    if not stripped:
        return "empty"
    if extraction_type == "markdown":
        return "markdown"
    if stripped.startswith("<"):
        return "html"
    if stripped.startswith(("{", "[")):
        try:
            json.loads(text)
            return "json"
        except json.JSONDecodeError:
            pass
    if key.endswith(".js"):
        return "javascript"
    if key.endswith(".json"):
        return "json"
    return "html"


def load_contract(root: Path | str) -> Contract:
    root = Path(root)
    endpoint_data = json.loads((root / "config" / "endpoints.json").read_text(encoding="utf-8"))
    source_data = json.loads((root / "config" / "datasources.json").read_text(encoding="utf-8"))
    primary = source_data["datasources"]["primary_odds"]
    endpoints = tuple(EndpointSpec.from_dict(item) for item in endpoint_data["endpoints"])
    bookmakers = tuple(Bookmaker.from_dict(item) for item in primary["tracked_bookmakers"])
    non_roster = tuple(int(cid) for cid in primary.get("non_roster_cids", ()))
    _validate_contract(endpoints, bookmakers, non_roster)
    return Contract(endpoints=endpoints, bookmakers=bookmakers, non_roster_cids=non_roster)


def _validate_contract(
    endpoints: tuple[EndpointSpec, ...],
    bookmakers: tuple[Bookmaker, ...],
    non_roster: tuple[int, ...],
) -> None:
    keys = [endpoint.key for endpoint in endpoints]
    if len(endpoints) != 28 or len(set(keys)) != 28:
        raise ValueError("endpoint manifest must contain 28 unique keys")
    names = [bookmaker.official_name for bookmaker in bookmakers]
    if len(bookmakers) != 23 or len(set(names)) != 23:
        raise ValueError("bookmaker roster must contain 23 unique official names")
    euro = [bookmaker.euro_cid for bookmaker in bookmakers if bookmaker.euro_cid is not None]
    change = [bookmaker.change_cid for bookmaker in bookmakers if bookmaker.change_cid is not None]
    if len(euro) != 21 or len(set(euro)) != 21 or set(euro) != set(EURO_CIDS):
        raise ValueError("euro cids must be the exact 21-slot set")
    if len(change) != 7 or len(set(change)) != 7 or set(change) != set(CHANGE_CIDS):
        raise ValueError("change cids must be the exact 7-slot set")
    if set(non_roster) != {71, 370, 18, 517, 976}:
        raise ValueError("non-roster cid set is not the documented set")


def decode_body(body: bytes | str, encoding: str) -> str:
    if isinstance(body, str):
        return body
    return body.decode(encoding, errors="replace")


def _js_array_body(text: str, variable: str) -> str:
    marker = f"var {variable}=Array("
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"{variable}_missing")
    start += len(marker)
    end = text.find(");", start)
    if end < 0:
        raise ValueError(f"{variable}_unterminated")
    return text[start:end]


def _parse_game_entries(text: str) -> list[tuple[int, int, str]]:
    body = _js_array_body(text, "game")
    entries: list[tuple[int, int, str]] = []
    for match in re.finditer(r'"(\d+)\|(\d+)\|([^"|]+)', body):
        entries.append((int(match.group(1)), int(match.group(2)), match.group(3).strip()))
    if not entries:
        raise ValueError("game_empty")
    return entries


def extract_euro_cids(text: str) -> tuple[list[int], list[int]]:
    try:
        entries = _parse_game_entries(text)
    except ValueError:
        return [], []
    cids = [cid for cid, _odds_id, _name in entries]
    seen: set[int] = set()
    duplicates: list[int] = []
    for cid in cids:
        if cid in seen and cid not in duplicates:
            duplicates.append(cid)
        seen.add(cid)
    return cids, duplicates


def parse_euro_history(text: str) -> dict[int, tuple[EuroHistoryPoint, ...]]:
    """Parse the 1x2d.js gameDetail history, grouped by euro cid.

    The source format is:
    ``var game=Array("cid|oddsId|name|...", ...);`` and
    ``var gameDetail=Array("oddsId^home|draw|away|MM-DD HH:MM|return|kelly...|YYYY;...")``.
    The year is stored at the end of each history point, so the timestamp is
    assembled from the trailing year and the in-record date/time.
    """
    game_entries = _parse_game_entries(text)
    odds_to_cid = {odds_id: cid for cid, odds_id, _name in game_entries}
    detail_body = _js_array_body(text, "gameDetail")
    detail_entries = re.findall(r'"(\d+)\^([^"]*)"', detail_body)
    if not detail_entries:
        raise ValueError("game_detail_invalid:empty")

    histories: dict[int, list[EuroHistoryPoint]] = {}
    for odds_id_text, body in detail_entries:
        odds_id = int(odds_id_text)
        cid = odds_to_cid.get(odds_id)
        if cid is None:
            continue
        segments = [segment.strip() for segment in body.split(";") if segment.strip()]
        if not segments:
            raise ValueError(f"game_detail_invalid:{odds_id}")
        points = histories.setdefault(cid, [])
        for segment in segments:
            parts = [part.strip() for part in segment.split("|")]
            if len(parts) < 8:
                raise ValueError(f"game_detail_invalid:{odds_id}")
            try:
                home = float(parts[0])
                draw = float(parts[1])
                away = float(parts[2])
                return_rate = float(parts[4])
                year = int(parts[-1])
                timestamp = datetime.strptime(
                    f"{year:04d}-{parts[3]}", "%Y-%m-%d %H:%M"
                )
                kelly = tuple(float(value) for value in parts[5:-1])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"game_detail_invalid:{odds_id}") from exc
            points.append(
                EuroHistoryPoint(
                    home=home,
                    draw=draw,
                    away=away,
                    timestamp=timestamp,
                    return_rate=return_rate,
                    kelly=kelly,
                )
            )
    return {
        cid: tuple(sorted(points, key=lambda point: point.timestamp))
        for cid, points in histories.items()
        if points
    }


def extract_entity(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for name in ("ScheduleID", "scheduleId", "scheduleID", "hometeam_cn", "homeTeam", "guestteam_cn", "guestTeam"):
        match = re.search(rf'\b{name}\s*=\s*"?([^";\r\n]+)"?', text, re.IGNORECASE)
        if match:
            clean_name = "ScheduleID" if "schedule" in name.lower() else ("hometeam_cn" if "home" in name.lower() else "guestteam_cn")
            if clean_name not in result:
                result[clean_name] = match.group(1).strip()
    return result


def _has_no_open_marker(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in NO_OPEN_MARKERS)


def _mobile_stream_rows(text: str) -> list[tuple[str, ...]]:
    """Parse the mobile AsianDetail/OuDetail stream when markdown flattens rows.

    The mobile pages often render one long markdown line containing repeated
    ``即 | home | handicap | away | MM-DD HH:MM`` sequences.  Split those
    sequences explicitly so a real stream is not mistaken for a header-only
    table.
    """
    rows: list[tuple[str, ...]] = []
    pattern = re.compile(
        r"\|\s*(即|早)\s*\|\s*([0-9.]+)\s*\|\s*([^|]+?)\s*\|\s*([0-9.]+)\s*\|\s*(\d{2}-\d{2}\s+\d{2}:\d{2})\s*\|"
    )
    for match in pattern.finditer(text):
        rows.append(tuple(part.strip() for part in match.groups()))
    return rows


def _duplicate_rows(rows: list[tuple[str, ...]]) -> list[str]:
    result: list[str] = []
    counts: dict[str, int] = {}
    for row in rows:
        joined = "|".join(row)
        result.append(joined)
        counts[joined] = counts.get(joined, 0) + 1
    return [row for row in result if counts[row] > 1]


def _table_data_rows(text: str) -> list[tuple[str, ...]]:
    """Return real data rows, not header-only tables.

    A row must have at least three populated cells and at least one numeric
    cell.  Markdown separators and HTML header rows therefore cannot satisfy
    the gate on their own.
    """
    rows: list[tuple[str, ...]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or set(stripped) <= set("|-: "):
            continue
        cells = tuple(cell.strip() for cell in stripped.strip("|").split("|"))
        if len(cells) < 3 or not any(cell for cell in cells):
            continue
        if not any(re.search(r"\d", cell) for cell in cells):
            continue
        rows.append(cells)

    for table_row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", text, flags=re.IGNORECASE | re.DOTALL):
        cells = tuple(
            re.sub(r"<[^>]+>", "", cell).strip()
            for cell in re.findall(
                r"<t[dh]\b[^>]*>(.*?)</t[dh]>", table_row, flags=re.IGNORECASE | re.DOTALL
            )
        )
        if len(cells) < 3 or not any(cell for cell in cells):
            continue
        if not any(re.search(r"\d", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def _has_table(text: str) -> bool:
    return bool(_table_data_rows(text))


def _duplicate_table_rows(text: str) -> list[str]:
    return _duplicate_rows(_table_data_rows(text))


def assess_payload(
    contract: Contract,
    key: str,
    text: str,
    *,
    status: int = 200,
    url: str = "",
    match_id: str | None = None,
    home: str | None = None,
    away: str | None = None,
    raw_bytes: bytes | None = None,
    attempts: int = 1,
    fetched_at: str | None = None,
) -> EndpointAssessment:
    spec = contract.endpoint(key)
    if spec is None:
        return EndpointAssessment(
            key=key, url=url, status=status, text=text, encoding="utf-8",
            state="failed", errors=[f"unknown_endpoint:{key}"],
            raw_bytes=len(raw_bytes or b""), raw_sha256=_text_hash(raw_bytes),
            attempts=attempts, fetched_at=fetched_at or _now(),
        )

    errors: list[str] = []
    state = "ok"
    if status != 200:
        errors.append(f"http_status_{status}")

    lowered = text.lower()
    if any(marker in lowered for marker in WAF_MARKERS):
        errors.append("waf_blocked")
    if "\ufffd" in text:
        errors.append("replacement_char")

    if key == "1x2d.js":
        all_cids, duplicates = extract_euro_cids(text)
        missing = sorted(set(contract.euro_cids) - set(all_cids))
        if missing:
            errors.append("missing_euro_cid:" + ",".join(str(cid) for cid in missing))
        if duplicates:
            errors.append("duplicate_cid:" + ",".join(str(cid) for cid in duplicates))
        try:
            histories = parse_euro_history(text)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            for cid in contract.euro_cids:
                if cid not in histories:
                    errors.append(f"missing_euro_history:{cid}")
        entity = extract_entity(text)
        if match_id and entity.get("ScheduleID") != str(match_id):
            errors.append("entity_mismatch")
        if home and entity.get("hometeam_cn") and entity["hometeam_cn"] != home:
            errors.append("entity_mismatch")
        if away and entity.get("guestteam_cn") and entity["guestteam_cn"] != away:
            errors.append("entity_mismatch")

    elif key == "analy.json":
        stripped = text.strip()
        if not stripped:
            state = "not_offered"
        elif stripped.startswith("{"):
            try:
                payload = json.loads(text)
            except (json.JSONDecodeError, TypeError):
                errors.append("json_invalid")
                payload = None
            if isinstance(payload, dict) and payload.get("had") is None:
                state = "not_offered"
            elif isinstance(payload, (dict, list)):
                state = "ok"
            else:
                state = "failed"
                if "json_invalid" not in errors:
                    errors.append("json_shape_invalid")
        else:
            # 移动端 shijian 页面或技术统计内容
            if len(stripped) >= 50 or any(kw in text for kw in ("比赛事件", "技术统计", "暂无数据", "入球")):
                state = "ok"
            else:
                errors.append("empty_required_endpoint")
                state = "failed"

    elif key == "polymarket.json":
        try:
            payload = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            errors.append("json_invalid")
            payload = None
        if payload in ([], None):
            state = "not_offered"
        elif isinstance(payload, (dict, list)):
            state = "ok"
        else:
            state = "failed"
            if "json_invalid" not in errors:
                errors.append("json_shape_invalid")

    elif spec.group in TABLE_GROUPS:
        stripped = text.strip()
        rows = _table_data_rows(text)
        if len(rows) < 2:
            mobile_rows = _mobile_stream_rows(text)
            if mobile_rows:
                rows = mobile_rows
        if not stripped:
            if spec.group == "eu" or key in ("ah_42.html", "ou_42.html"):
                state = "not_offered"
            else:
                errors.append("empty_required_endpoint")
                state = "failed"
        elif not rows:
            if _has_no_open_marker(text):
                state = "not_offered"
            elif key not in ("eu_42.html",) and any(tag in text for tag in ("即", "早", "指数变化", "details", "odds")):
                # 移动端 HTML 变盘流水流式列表
                state = "ok"
            else:
                errors.append("empty_required_endpoint")
                state = "failed"
        else:
            duplicates = _duplicate_rows(rows)
            if duplicates:
                errors.append("duplicate_odds_triplet")
            state = "failed" if errors else "ok"

    elif key == "analysis.html":
        stripped = text.strip()
        if len(stripped) < 200 and "porlet_" not in text and "Analysis" not in text and "jsonData" not in text:
            errors.append("empty_required_endpoint")
        state = "failed" if errors else "ok"

    elif key == "odds.html":
        stripped = text.strip()
        if len(stripped) < 200 and "analy_sbAllOdds" not in text and "lineupObj" not in text:
            errors.append("empty_required_endpoint")
        state = "failed" if errors else "ok"

    elif spec.group == "panorama":
        stripped = text.strip()
        if not stripped:
            errors.append("empty_required_endpoint")
        elif stripped.startswith("{") and "companies" in stripped:
            try:
                data = json.loads(text)
                if match_id and str(data.get("scheduleId", "")) != str(match_id):
                    errors.append("schedule_id_mismatch")
                if not data.get("companies"):
                    errors.append("empty_companies_list")
            except (json.JSONDecodeError, TypeError):
                errors.append("json_invalid")
        elif not _has_table(text):
            errors.append("empty_required_endpoint")
        state = "failed" if errors else "ok"

    else:
        errors.append("unhandled_endpoint_group")
        state = "failed"

    if errors:
        state = "failed"
    return EndpointAssessment(
        key=key,
        url=url,
        status=status,
        text=text,
        encoding=spec.encoding,
        state=state,
        errors=errors,
        raw_bytes=len(raw_bytes) if raw_bytes is not None else len(text.encode("utf-8")),
        raw_sha256=_text_hash(raw_bytes) if raw_bytes is not None else "",
        attempts=attempts,
        fetched_at=fetched_at or _now(),
    )


import argparse
import asyncio
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from scrapling.spiders import Request, Spider

try:
    from curl_cffi import CurlHttpVersion
except ImportError:  # pragma: no cover - curl_cffi ships with Scrapling
    CurlHttpVersion = None

ROOT = Path(__file__).resolve().parents[3]
REFERER = "https://m.titan007.com/analy/Analysis/{match_id}.htm"
ANALYSIS_DELIVERY_KEY = "polymarket.json"


@dataclass(frozen=True)
class RequestPlan:
    key: str
    url: str
    tier: int = 1


def build_request_plan(contract: Contract, match_id: str, polymarket_slug: str | None) -> list[RequestPlan]:
    tier1: list[RequestPlan] = []
    tier2: list[RequestPlan] = []
    for spec in contract.endpoints:
        if spec.skip_request:
            continue
        if spec.key == ANALYSIS_DELIVERY_KEY and not polymarket_slug:
            continue
        values = {"match_id": match_id, "polymarket_slug": polymarket_slug or ""}
        plan = RequestPlan(key=spec.key, url=spec.url_template.format(**values), tier=spec.tier)
        if spec.tier == 1:
            tier1.append(plan)
        else:
            tier2.append(plan)
    return tier1 + tier2


def _session_kwargs(match_id: str) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "headers": {
            "Referer": REFERER.format(match_id=match_id),
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        },
        "timeout": 30,
    }
    if CurlHttpVersion is not None:
        kwargs["http_version"] = CurlHttpVersion.V1_1
    return kwargs


class IngestSpider(Spider):
    name = "match-scraper-ingest"
    # 单并发 + 1.0~2.0s 礼貌抖动 + AutoThrottle 自适应退避。
    concurrent_requests = 1
    concurrent_requests_per_domain = 1
    autothrottle_enabled = True
    autothrottle_start_delay = 1.0
    autothrottle_target_concurrency = 1.0
    autothrottle_max_delay = 15.0
    max_blocked_retries = 0

    @property
    def download_delay(self) -> float:
        """Base 1.0s plus 0-1s jitter so requests do not form a fixed rhythm."""
        return random.uniform(1.0, 2.0)

    def __init__(
        self,
        *,
        match_id: str,
        sales_date: str,
        home: str = "",
        away: str = "",
        polymarket_slug: str | None = None,
        browser_fallback: bool = False,
        proxy: str | None = None,
        root: Path = ROOT,
    ) -> None:
        self.contract = load_contract(root)
        self.match_id = str(match_id)
        self.sales_date = sales_date
        self.home = home
        self.away = away
        self.polymarket_slug = polymarket_slug
        self.browser_fallback = browser_fallback
        self.proxy = (
            proxy
            or os.environ.get("ALL_PROXY")
            or os.environ.get("HTTPS_PROXY")
            or os.environ.get("HTTP_PROXY")
        )
        self.root = Path(root)
        self.results: dict[str, EndpointAssessment] = {}
        self.failures: dict[str, str] = {}
        super().__init__()

    def configure_sessions(self, manager) -> None:
        from scrapling.fetchers import FetcherSession

        session_kwargs: dict[str, Any] = {
            "impersonate": "chrome",
            "stealthy_headers": True,
            "timeout": 30,
            "retries": 0,
            "retry_delay": 5,
        }
        if self.proxy:
            session_kwargs["proxy"] = self.proxy
            self.logger.info("using proxy: %s", self.proxy)

        manager.add("default", FetcherSession(**session_kwargs))

    async def on_start(self, resuming: bool = False) -> None:
        self.results.clear()
        self.failures.clear()
        self.logger.info("ingest start match=%s endpoints=%s", self.match_id, len(self.contract.endpoints))

    async def start_requests(self):
        for plan in build_request_plan(self.contract, self.match_id, self.polymarket_slug):
            yield Request(
                plan.url,
                callback=self.parse,
                sid="default",
                meta={"key": plan.key},
                **_session_kwargs(self.match_id),
            )

    def _record_response(self, response, key: str) -> EndpointAssessment | None:
        spec = self.contract.endpoint(key)
        if spec is None:
            return None
        raw = response.body if isinstance(response.body, bytes) else str(response.body).encode()
        text = decode_body(raw, spec.encoding)
        if spec.extraction_type == "markdown":
            if spec.css_selector:
                try:
                    text = response.markdown(css_selector=spec.css_selector, main_content_only=True)
                except Exception as exc:  # extraction failure must be visible, not silent
                    self.failures[key] = f"extract_error:{type(exc).__name__}:{exc}"
                    return None
            else:
                try:
                    text = response.markdown(main_content_only=False)
                except Exception:
                    text = decode_body(raw, spec.encoding)

        result = assess_payload(
            self.contract,
            key,
            text,
            status=int(response.status),
            url=str(response.url),
            match_id=self.match_id,
            home=self.home or None,
            away=self.away or None,
            raw_bytes=raw,
            attempts=getattr(getattr(response, "request", None), "_retry_count", 0) + 1,
        )
        self.results[key] = result
        if result.errors:
            self.logger.warning("endpoint %s failed: %s", key, ", ".join(result.errors))
        return result

    async def parse(self, response):
        key = str(response.meta.get("key", ""))
        result = self._record_response(response, key)
        if result is None or key == ANALYSIS_DELIVERY_KEY:
            return
        spec = self.contract.endpoint(key)
        yield result.item(self.match_id, spec.extraction_type if spec else "")

    async def _browser_fetch(self, request: Request, key: str) -> None:
        try:
            from scrapling.fetchers import StealthyFetcher

            response = await asyncio.to_thread(
                StealthyFetcher.fetch,
                request.url,
                headless=True,
                network_idle=False,
                timeout=30000,
                wait=1000,
            )
        except Exception as exc:
            self.failures[key] = f"browser_fallback_error:{type(exc).__name__}:{exc}"
            self.logger.error("endpoint %s browser fallback failed: %s", key, self.failures[key])
            return
        self._record_response(response, key)

    async def on_error(self, request: Request, error: Exception) -> None:
        key = str(request.meta.get("key", ""))
        self.failures[key] = f"{type(error).__name__}:{error}"
        self.logger.error("endpoint %s request error: %s", key, self.failures[key])
        if self.browser_fallback:
            await self._browser_fetch(request, key)

    def _missing_result(self, key: str, reason: str) -> EndpointAssessment:
        spec = self.contract.endpoint(key)
        return EndpointAssessment(
            key=key,
            url="",
            status=0,
            text="",
            encoding=spec.encoding if spec else "utf-8",
            state="failed",
            errors=[reason],
            attempts=0,
        )

    def _fill_missing(self) -> None:
        for key in self.contract.endpoint_keys:
            if key in self.results:
                continue
            spec = self.contract.endpoint(key)
            if key == ANALYSIS_DELIVERY_KEY and not self.polymarket_slug:
                self.results[key] = EndpointAssessment(
                    key=key,
                    url="",
                    status=0,
                    text="[]",
                    encoding="utf-8",
                    state="not_offered",
                    attempts=0,
                )
                continue
            if spec is not None and spec.skip_request:
                self.results[key] = assess_payload(
                    self.contract,
                    key,
                    "",
                    status=200,
                    url="",
                    attempts=0,
                )
                continue
            if key in self.failures:
                self.results[key] = self._missing_result(key, f"request_error:{self.failures[key]}")
            else:
                self.results[key] = self._missing_result(key, "request_not_completed")

        if "1x2d.js" in self.results:
            entity = extract_entity(self.results["1x2d.js"].text)
            self.home = self.home or entity.get("hometeam_cn", "")
            self.away = self.away or entity.get("guestteam_cn", "")

    async def on_close(self) -> None:
        self._fill_missing()

    def build_export_items(self) -> list[dict[str, Any]]:
        self._fill_missing()
        items: list[dict[str, Any]] = []
        for key in self.contract.endpoint_keys:
            if key == ANALYSIS_DELIVERY_KEY:
                continue
            spec = self.contract.endpoint(key)
            result = self.results.get(key)
            if result is None:
                result = self._missing_result(key, "request_not_completed")
                self.results[key] = result
            items.append(result.item(self.match_id, spec.extraction_type if spec else ""))
        return items


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Single-match Scrapling item export for ETLX")
    p.add_argument("--match-id", required=True, help="球探 matchId，例如 3073801")
    p.add_argument("--sales-date", default=date.today().isoformat(), help="销售日 YYYY-MM-DD")
    p.add_argument("--home", default="", help="主队名；提供时做实体核对")
    p.add_argument("--away", default="", help="客队名；提供时做实体核对")
    p.add_argument("--polymarket-slug", default=None, help="Polymarket 事件 slug；不提供则记 not_offered")
    p.add_argument("--browser-fallback", action="store_true", help="HTTP 请求失败时用 StealthyFetcher 逐端点降级（慢）")
    p.add_argument("--proxy", default=None, help="代理通道 URL，例如 http://127.0.0.1:10808")
    p.add_argument("--output", default=None, help="临时 JSONL 路径；默认在系统临时目录生成")
    p.add_argument("--force", action="store_true", help="跳过同一输出文件 10 分钟冷却；仅在主人明确要求重新分析时使用")
    p.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)
    return p


def _cached_capture_is_valid(path: Path, match_id: str) -> bool:
    """A cached JSONL is reusable only when it is a complete, same-match capture."""
    try:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(lines) != 27:
            return False
        items = [json.loads(line) for line in lines]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False
    keys = {str(item.get("endpoint_key", "")) for item in items}
    return (
        len(keys) == 27
        and all(str(item.get("match_id")) == str(match_id) for item in items)
        and all(str(item.get("state")) in {"ok", "not_offered"} for item in items)
    )


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    output = Path(args.output) if args.output else None
    if output and not args.force:
        try:
            age = time.time() - output.stat().st_mtime
        except OSError:
            age = None
        if (
            age is not None
            and age < CAPTURE_COOLDOWN_SECONDS
            and _cached_capture_is_valid(output, args.match_id)
        ):
            print(json.dumps({
                "ok": False,
                "cached": True,
                "match_id": args.match_id,
                "path": str(output),
                "skipped": "cooldown",
                "remaining_seconds": int(CAPTURE_COOLDOWN_SECONDS - age),
            }, ensure_ascii=False))
            return 0
    root = Path(args.root)
    spider = IngestSpider(
        match_id=args.match_id,
        sales_date=args.sales_date,
        home=args.home,
        away=args.away,
        polymarket_slug=args.polymarket_slug,
        browser_fallback=args.browser_fallback,
        proxy=args.proxy,
        root=root,
    )
    try:
        result = spider.start()
    except KeyboardInterrupt:
        print(json.dumps({"ok": False, "error": "interrupted"}, ensure_ascii=False))
        return 130
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"{type(exc).__name__}:{exc}"}, ensure_ascii=False))
        return 1

    items = spider.build_export_items()
    exported = {str(item.get("endpoint_key")) for item in result.items}
    for item in items:
        if str(item.get("endpoint_key")) not in exported:
            result.items.append(item)

    if output is None:
        fd, name = tempfile.mkstemp(prefix=f"match-{spider.match_id}-", suffix=".jsonl")
        os.close(fd)
        output = Path(name)
    try:
        result.items.to_jsonl(output)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"export_failed:{type(exc).__name__}:{exc}"}, ensure_ascii=False))
        return 1

    states = Counter(str(item.get("state", "missing")) for item in result.items)
    failed = sorted(
        str(item.get("endpoint_key"))
        for item in result.items
        if item.get("state") == "failed"
    )
    print(json.dumps({
        "ok": not failed,
        "match_id": spider.match_id,
        "path": str(output),
        "items": len(result.items),
        "states": dict(states),
        "failed": failed,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
