"""Pure ingest contract domain.

This module contains no Scrapling imports and no network calls.  It owns the
28-endpoint contract, the 23-bookmaker roster, payload assessment, bundle
assembly, and the machine gate used by ``ingest_spider.py``.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

EURO_CIDS = (
    80, 545, 281, 90, 177, 432, 115, 82, 81, 104, 255,
    110, 2, 474, 649, 800, 482, 386, 826, 16, 1129,
)
CHANGE_CIDS = (1, 3, 8, 12, 47, 42, 48)

TABLE_GROUPS = frozenset({"ah", "ou", "eu"})
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
        )


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

    def bookmaker_for_euro_cid(self, cid: int) -> Bookmaker | None:
        for bookmaker in self.bookmakers:
            if bookmaker.euro_cid == cid:
                return bookmaker
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


@dataclass
class GateReport:
    ok: bool
    errors: list[str]
    counts: dict[str, int]
    slots: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "errors": list(self.errors),
            "counts": dict(self.counts),
            "slots": dict(self.slots),
        }


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


def extract_euro_cids(text: str) -> tuple[list[int], list[int]]:
    start = text.find("var game=Array(")
    if start >= 0:
        end = text.find(");", start)
        segment = text[start:end] if end >= 0 else text[start:]
    else:
        segment = text
    cids = [int(cid) for cid in re.findall(r'"(\d+)\|', segment)]
    seen: set[int] = set()
    duplicates: list[int] = []
    for cid in cids:
        if cid in seen and cid not in duplicates:
            duplicates.append(cid)
        seen.add(cid)
    return cids, duplicates


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


def _has_table(text: str) -> bool:
    return text.count("|") >= 4 or "<table" in text.lower()


def _duplicate_table_rows(text: str) -> list[str]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        rows.append(line)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row] = counts.get(row, 0) + 1
    return [row for row, count in counts.items() if count > 1]


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
    enforce_bookmaker_title: bool = False,
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
        if not stripped:
            if key == "eu_42.html":
                state = "not_offered"
            else:
                errors.append("empty_required_endpoint")
                state = "failed"
        elif not _has_table(text):
            if _has_no_open_marker(text):
                state = "not_offered"
            elif any(tag in text for tag in ("即", "早", "指数变化", "details", "odds")):
                # 移动端 HTML 变盘流水流式列表
                state = "ok"
            else:
                errors.append("empty_required_endpoint")
                state = "failed"
        else:
            duplicates = _duplicate_table_rows(text)
            if duplicates:
                errors.append("duplicate_odds_triplet")
            if enforce_bookmaker_title:
                cid_text = key.split("_", 1)[1].split(".", 1)[0]
                try:
                    cid = int(cid_text)
                except ValueError:
                    cid = -1
                bookmaker = next(
                    (item for item in contract.bookmakers if item.change_cid == cid),
                    None,
                )
                if bookmaker is not None:
                    found_aliases = [
                        item.official_name
                        for item in contract.bookmakers
                        if any(alias.lower() in lowered for alias in (item.official_name, *item.aliases))
                    ]
                    if found_aliases and bookmaker.official_name not in found_aliases:
                        errors.append("bookmaker_mismatch")
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


def build_bundle(
    match: dict[str, Any],
    results: dict[str, EndpointAssessment],
    contract: Contract,
) -> dict[str, Any]:
    payloads = {key: result.text for key, result in results.items()}
    endpoints = {key: result.receipt() for key, result in results.items()}
    required_present = all(key in payloads for key in contract.endpoint_keys)
    all_success = all(result.state != "failed" for result in results.values())
    bundle: dict[str, Any] = {
        "match": dict(match),
        "payloads": payloads,
        "receipt": {
            "endpoints": endpoints,
            "endpoints_count": len(endpoints),
            "all_success": all_success,
            "all_required_present": required_present,
        },
        "gates": {},
    }
    report = validate_bundle(bundle, contract)
    bundle["gates"] = report.to_dict()
    return bundle


def validate_bundle(bundle: dict[str, Any], contract: Contract) -> GateReport:
    errors: list[str] = []
    payloads = bundle.get("payloads", {})
    receipt = bundle.get("receipt", {})
    endpoints = receipt.get("endpoints", {})
    expected = set(contract.endpoint_keys)

    for key in contract.endpoint_keys:
        if key not in payloads:
            errors.append(f"missing_payload:{key}")
        if key not in endpoints:
            errors.append(f"missing_receipt:{key}")
            continue
        text = payloads.get(key, "")
        item = endpoints[key]
        if item.get("chars") != len(text):
            errors.append(f"receipt_chars_mismatch:{key}")
        if item.get("sha256") != _sha256(text):
            errors.append(f"receipt_sha256_mismatch:{key}")
        if item.get("state") == "failed":
            detail = ",".join(item.get("errors", [])) or "unknown"
            errors.append(f"endpoint_failed:{key}:{detail}")

    for key in payloads:
        if key not in expected:
            errors.append(f"unknown_payload:{key}")

    cids: list[int] = []
    duplicates: list[int] = []
    if "1x2d.js" in payloads:
        cids, duplicates = extract_euro_cids(payloads["1x2d.js"])
        for cid in duplicates:
            errors.append(f"duplicate_cid:{cid}")
        for cid in contract.euro_cids:
            if cid not in cids:
                errors.append(f"missing_euro_cid:{cid}")

    slots: dict[str, str] = {}
    for bookmaker in contract.bookmakers:
        name = bookmaker.official_name
        if bookmaker.euro_cid is not None and bookmaker.euro_cid not in cids:
            errors.append(f"slot_missing_euro:{name}:{bookmaker.euro_cid}")
        for endpoint_key in bookmaker.required_endpoints:
            if endpoint_key not in payloads:
                errors.append(f"slot_missing_endpoint:{name}:{endpoint_key}")
        if bookmaker.euro_cid is not None:
            slots[name] = "supported" if bookmaker.euro_cid in cids else "not_offered"
        elif bookmaker.change_cid == 42:
            required = ("ah_42.html", "ou_42.html")
            if all(key in payloads and payloads[key].strip() for key in required):
                slots[name] = "supported"
            else:
                slots[name] = "not_offered"
                errors.append(f"slot_missing_change_evidence:{name}")
        elif name == "Polymarket":
            slots[name] = "supported" if "polymarket.json" in payloads else "not_offered"
            if "polymarket.json" not in payloads:
                errors.append("slot_missing_polymarket")
        else:
            slots[name] = "supported" if bookmaker.required_endpoints and all(
                key in payloads for key in bookmaker.required_endpoints
            ) else "not_offered"

    counts = {
        "payload_keys": len(payloads),
        "bookmaker_slots": len(contract.bookmakers),
        "euro_cids": sum(1 for cid in contract.euro_cids if cid in cids),
        "change_tables": sum(1 for endpoint in contract.endpoints if endpoint.group in TABLE_GROUPS),
    }
    return GateReport(ok=not errors, errors=errors, counts=counts, slots=slots)
