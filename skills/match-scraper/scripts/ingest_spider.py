#!/usr/bin/env python3
"""Single-match, 28-endpoint Scrapling Spider ingester.

The domain contract lives in ``ingest_contract.py``.  This file is the thin
Scrapling adapter and CLI: it sends the 28 requests, delegates every payload
decision to the domain, and writes one atomic ``data/{date}/raw/{matchId}.json``.

Usage:
    py -3.13 skills/match-scraper/scripts/ingest_spider.py \
        --match-id 3073801 --sales-date 2026-10-22 --home 格拉茨风暴 --away 马赛

    py -3.13 skills/match-scraper/scripts/ingest_spider.py \
        --match-id 3073801 --verify
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from scrapling.spiders import Request, Spider

from ingest_contract import (
    EndpointAssessment,
    assess_payload,
    build_bundle,
    decode_body,
    extract_entity,
    load_contract,
    validate_bundle,
)

try:
    from curl_cffi import CurlHttpVersion
except ImportError:  # pragma: no cover - curl_cffi ships with Scrapling
    CurlHttpVersion = None

ROOT = Path(__file__).resolve().parents[3]
REFERER = "https://m.titan007.com/analy/Analysis/{match_id}.htm"


@dataclass(frozen=True)
class RequestPlan:
    key: str
    url: str
    tier: int = 1


def build_request_plan(contract, match_id: str, polymarket_slug: str | None) -> list[RequestPlan]:
    tier1: list[RequestPlan] = []
    tier2: list[RequestPlan] = []
    for spec in contract.endpoints:
        if spec.skip_request:
            continue
        if spec.key == "polymarket.json" and not polymarket_slug:
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
    # 移动端现代云高防 CDN 节点：单并发 + 1.0s 礼貌间隔 + AutoThrottle 自适应退避。
    concurrent_requests = 1
    concurrent_requests_per_domain = 1
    download_delay = 1.0
    autothrottle_enabled = True
    autothrottle_start_delay = 1.0
    autothrottle_target_concurrency = 1.0
    autothrottle_max_delay = 15.0
    max_blocked_retries = 0

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
        self.output_path: Path | None = None
        self.exit_code = 1
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

        manager.add(
            "default",
            FetcherSession(**session_kwargs),
        )

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

    def _record_response(self, response, key: str) -> None:
        spec = self.contract.endpoint(key)
        if spec is None:
            return
        raw = response.body if isinstance(response.body, bytes) else str(response.body).encode()
        text = decode_body(raw, spec.encoding)
        if spec.extraction_type == "markdown":
            if spec.css_selector:
                try:
                    text = response.markdown(css_selector=spec.css_selector, main_content_only=True)
                except Exception as exc:  # extraction failure must be visible, not silent
                    self.failures[key] = f"extract_error:{type(exc).__name__}:{exc}"
                    return
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
            enforce_bookmaker_title=spec.group in {"ah", "ou", "eu"},
        )
        self.results[key] = result
        if result.errors:
            self.logger.warning("endpoint %s failed: %s", key, ", ".join(result.errors))

    async def parse(self, response):
        self._record_response(response, str(response.meta.get("key", "")))
        yield

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

    async def on_close(self) -> None:
        for key in self.contract.endpoint_keys:
            if key in self.results:
                continue
            if key == "polymarket.json" and not self.polymarket_slug:
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
            spec = self.contract.endpoint(key)
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

        bundle = build_bundle(
            match={
                "match_id": self.match_id,
                "sales_date": self.sales_date,
                "home": self.home,
                "away": self.away,
            },
            results=self.results,
            contract=self.contract,
        )
        report = validate_bundle(bundle, self.contract)
        bundle["gates"] = report.to_dict()
        output = self.root / "data" / self.sales_date / "raw" / f"{self.match_id}.json"
        if not report.ok:
            if output.exists():
                output.unlink()
            self.logger.error("ingest blocked: %s", "; ".join(report.errors))
            print(json.dumps({
                "ok": False,
                "match_id": self.match_id,
                "errors": report.errors,
                "counts": report.counts,
            }, ensure_ascii=False))
            self.exit_code = 1
            return

        write_json_atomic(output, bundle)
        readback = validate_bundle(load_bundle(output), self.contract)
        if not readback.ok:
            output.unlink()
            self.logger.error("readback blocked: %s", "; ".join(readback.errors))
            print(json.dumps({
                "ok": False,
                "match_id": self.match_id,
                "errors": readback.errors,
                "counts": readback.counts,
                "stage": "readback",
            }, ensure_ascii=False))
            self.exit_code = 1
            return
        self.output_path = output
        self.exit_code = 0
        print(json.dumps({
            "ok": True,
            "match_id": self.match_id,
            "path": str(output),
            "bytes": output.stat().st_size,
            "counts": report.counts,
        }, ensure_ascii=False))


def write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def load_bundle(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Single-match 28-endpoint Scrapling Spider ingester")
    p.add_argument("--match-id", required=True, help="球探 matchId，例如 3073801")
    p.add_argument("--sales-date", default=date.today().isoformat(), help="销售日 YYYY-MM-DD")
    p.add_argument("--home", default="", help="主队名；提供时做实体核对")
    p.add_argument("--away", default="", help="客队名；提供时做实体核对")
    p.add_argument("--polymarket-slug", default=None, help="Polymarket 事件 slug；不提供则记 not_offered")
    p.add_argument("--browser-fallback", action="store_true", help="HTTP 请求失败时用 StealthyFetcher 逐端点降级（慢）")
    p.add_argument("--proxy", default=None, help="代理通道 URL，例如 http://127.0.0.1:10808")
    p.add_argument("--verify", action="store_true", help="只读复检已有 raw/{matchId}.json，不发请求")
    p.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = Path(args.root)
    if args.verify:
        path = root / "data" / args.sales_date / "raw" / f"{args.match_id}.json"
        if not path.exists():
            print(json.dumps({"ok": False, "error": f"not_found:{path}"}, ensure_ascii=False))
            return 1
        bundle = load_bundle(path)
        report = validate_bundle(bundle, load_contract(root))
        print(json.dumps(report.to_dict(), ensure_ascii=False))
        return 0 if report.ok else 1

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
        spider.start()
    except KeyboardInterrupt:
        print(json.dumps({"ok": False, "error": "interrupted"}, ensure_ascii=False))
        return 130
    return spider.exit_code


if __name__ == "__main__":
    sys.exit(main())
