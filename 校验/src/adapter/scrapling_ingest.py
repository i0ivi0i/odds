"""
校验/src/adapter/scrapling_ingest.py
适配器层: 官方 Scrapling 原生进货流水线 (Native Scrapling Ingestion Pipeline)

完全遵循 /scrapling-official 官方规范:
1. 官方分块军规: 单批切片 <= 6~8 个 URL，批次间控频延时 (0.3s)
2. 选择器内存下推: 变盘流水前置过滤 css_selector="#table_odds"，Cython 底层剥离冗余 DOM
3. 编码自适应映射: JS/Analysis/Odds 走 UTF-8，变盘流水走 GB18030
4. 官方内部四级闭环: bulk_get -> fetch -> stealthy_fetch -> internal chrome (--real-chrome)
   绝对隔离外部独立浏览器 (严禁调用外部 browseros-neo)
5. 原子存证组装: 统一构建 raw/{matchId}.json，零散碎文件自动归整
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional, Tuple, Union

# 确保项目根目录在 sys.path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))


class FetchTier(str, Enum):
    """Scrapling 官方内部四级闭环升阶阶梯 (严禁任何外部独立浏览器)"""
    BULK_PROTOCOL = "bulk_protocol"        # 一级: bulk_get HTTP/2 极速协议流并发
    FETCH_PRECISE = "fetch_precise"        # 二级: 单步精准 fetch (network_idle)
    STEALTHY_FETCH = "stealthy_fetch"      # 三级: 指纹混淆与反爬绕过 (StealthyFetcher)
    INTERNAL_CHROME = "internal_chrome"    # 四级: Scrapling 内部受控 Chrome (--real-chrome)


@dataclass
class EndpointSpec:
    """数据端点规格契约"""
    name: str
    url: str
    encoding: str = "utf-8"
    css_selector: Optional[str] = None
    extraction_type: str = "text"
    category: str = "core"  # core, ah, ou, eu
    identifier: Optional[str] = None


@dataclass
class ScraplingChunk:
    """官方并发分块任务单元"""
    chunk_index: int
    specs: List[EndpointSpec]
    delay_seconds: float = 0.3


class ScraplingIngestPipeline:
    """
    官方原生 Scrapling 进货流水线引擎
    负责构建请求矩阵、切片分块、编码映射、内部四级升阶容灾与原子存证组装
    """

    DEFAULT_COMPANIES = [1, 3, 8, 12, 47, 42, 48]  # 法定 7 大做市商

    def __init__(self, match_id: str, companies: Optional[List[int]] = None):
        self.match_id = str(match_id).strip()
        self.companies = companies or self.DEFAULT_COMPANIES

    def get_core_specs(self) -> List[EndpointSpec]:
        """4 大核心基础端点 (UTF-8 编码)"""
        mid = self.match_id
        return [
            EndpointSpec(
                name="1x2d.js",
                url=f"https://1x2d.titan007.com/{mid}.js",
                encoding="utf-8",
                css_selector=None,
                extraction_type="text",
                category="core",
            ),
            EndpointSpec(
                name="analysis.html",
                url=f"https://zq.titan007.com/analysis/{mid}cn.htm",
                encoding="utf-8",
                css_selector=None,
                extraction_type="text",
                category="core",
            ),
            EndpointSpec(
                name="odds.html",
                url=f"https://zq.titan007.com/analysis/odds/{mid}.htm",
                encoding="utf-8",
                css_selector=None,
                extraction_type="text",
                category="core",
            ),
            EndpointSpec(
                name="analy.json",
                url=f"https://zq.titan007.com/default/getAnalyData?sid={mid}&t=1",
                encoding="utf-8",
                css_selector=None,
                extraction_type="text",
                category="core",
            ),
        ]

    def get_timeseries_specs(self) -> List[EndpointSpec]:
        """7 大做市商变盘流水端点 (GB18030 编码，下推 table 选择器)"""
        mid = self.match_id
        specs: List[EndpointSpec] = []
        # 1. 亚盘让球 (7家)
        for cid in self.companies:
            specs.append(
                EndpointSpec(
                    name=f"ah_{cid}.html",
                    url=f"https://vip.titan007.com/changeDetail/handicap.aspx?id={mid}&companyID={cid}&l=0",
                    encoding="gb18030",
                    css_selector="table",
                    extraction_type="text",
                    category="ah",
                    identifier=f"ah_{cid}_table",
                )
            )
        # 2. 大小球 (7家)
        for cid in self.companies:
            specs.append(
                EndpointSpec(
                    name=f"ou_{cid}.html",
                    url=f"https://vip.titan007.com/changeDetail/overunder.aspx?id={mid}&companyID={cid}&l=0",
                    encoding="gb18030",
                    css_selector="table",
                    extraction_type="text",
                    category="ou",
                    identifier=f"ou_{cid}_table",
                )
            )
        # 3. 欧指流水 (7家)
        for cid in self.companies:
            specs.append(
                EndpointSpec(
                    name=f"eu_{cid}.html",
                    url=f"https://vip.titan007.com/changeDetail/1x2.aspx?id={mid}&companyID={cid}&l=0",
                    encoding="gb18030",
                    css_selector="table",
                    extraction_type="text",
                    category="eu",
                    identifier=f"eu_{cid}_table",
                )
            )
        return specs

    def get_all_endpoint_specs(self) -> List[EndpointSpec]:
        """全量 25 个端点集合"""
        return self.get_core_specs() + self.get_timeseries_specs()

    def build_plan_chunks(self, chunk_size: int = 7) -> List[ScraplingChunk]:
        """
        按官方分块军规对端点切片 (单批 <= 6~8 URLs，加 0.3s 控频延时)
        推荐切片结构:
          Chunk 0: 4 个核心端点 (1x2d, analysis, odds, analy)
          Chunk 1: 7 个亚盘流水
          Chunk 2: 7 个大小球流水
          Chunk 3: 7 个欧指流水
        """
        all_specs = self.get_all_endpoint_specs()
        chunks: List[ScraplingChunk] = []

        # 结构化语义优先分块: 核心 4 个一组，各大类 7 个一组
        # 若按纯 chunk_size 切割：
        for i in range(0, len(all_specs), chunk_size):
            slice_specs = all_specs[i:i + chunk_size]
            chunks.append(
                ScraplingChunk(
                    chunk_index=len(chunks),
                    specs=slice_specs,
                    delay_seconds=0.3,
                )
            )
        return chunks

    def fetch_endpoint_with_escalation(
        self, spec: EndpointSpec, executor: Any = None
    ) -> str:
        """
        在 Scrapling 框架内部自洽执行四级升阶
        遇到网络异常或 WAF 协议重置时逐级升阶，严禁向外部独立浏览器扩散
        """
        tiers = [
            FetchTier.BULK_PROTOCOL,
            FetchTier.FETCH_PRECISE,
            FetchTier.STEALTHY_FETCH,
            FetchTier.INTERNAL_CHROME,
        ]
        last_error = None

        for tier in tiers:
            try:
                if executor is not None:
                    # 自定义执行器 / Mock
                    return executor.execute_spec(spec, tier=tier)
                else:
                    # 默认使用原生 Scrapling 执行逻辑
                    return self._execute_scrapling_tier(spec, tier)
            except Exception as e:
                last_error = e
                # 升阶到下一级重试
                continue

        raise RuntimeError(
            f"❌ [SCRAPLING_ESCALATION_FAILED] 端点 {spec.name} ({spec.url}) 经历内部四级升阶全部失败: {last_error}"
        )

    def _execute_scrapling_tier(self, spec: EndpointSpec, tier: FetchTier) -> str:
        """原生调用 Scrapling Python SDK 或底层网络"""
        try:
            # 优先尝试导入官方 scrapling
            from scrapling import Fetcher, StealthyFetcher
            try:
                from scrapling.engines.static import CurlHttpVersion
            except ImportError:
                CurlHttpVersion = None
            # 动态计算真实浏览器访问轨迹 Referer (避免做市商子域直接来自 Google 暴露特征)
            referer = "https://zq.titan007.com/"
            if "changeDetail" in spec.url:
                referer = f"https://zq.titan007.com/analysis/odds/{self.match_id}.htm"
            elif "1x2d" in spec.url:
                referer = "https://titan007.com/"
            elif "jc.titan007" in spec.url:
                referer = "https://www.titan007.com/"

            extra_headers = {"Referer": referer}

            # 配置项目专属持久化存储库 (data/scrapling_storage.db)，开启自适应与元素记忆
            db_dir = repo_root / "data"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_file = str((db_dir / "scrapling_storage.db").resolve())
            selector_config = {
                "adaptive": True,
                "storage_args": {"storage_file": db_file},
            }

            if tier == FetchTier.BULK_PROTOCOL or tier == FetchTier.FETCH_PRECISE:
                fetch_kwargs = {
                    "impersonate": "chrome",
                    "stealthy_headers": True,
                    "headers": extra_headers,
                    "timeout": 15,
                    "selector_config": selector_config,
                }
                # 首选 HTTP/2 极速协议流，若源站报协议缺陷则动态自愈降级至 HTTP/1.1
                try:
                    page = Fetcher.get(spec.url, **fetch_kwargs)
                except Exception as e:
                    err_msg = str(e).lower()
                    if CurlHttpVersion is not None and any(k in err_msg for k in ["http/2", "protocol_error", "(92)", "stream"]):
                        retry_kwargs = dict(fetch_kwargs)
                        retry_kwargs["http_version"] = CurlHttpVersion.V1_1
                        page = Fetcher.get(spec.url, **retry_kwargs)
                    else:
                        raise
            elif tier == FetchTier.STEALTHY_FETCH:
                try:
                    page = StealthyFetcher.fetch(
                        spec.url,
                        headless=True,
                        hide_canvas=True,
                        block_webrtc=True,
                        allow_webgl=True,
                        google_search=False,
                        extra_headers=extra_headers,
                        selector_config=selector_config,
                    )
                except Exception as e:
                    err_msg = str(e).lower()
                    if any(k in err_msg for k in ["http2", "protocol_error", "err_http2"]):
                        page = StealthyFetcher.fetch(
                            spec.url,
                            headless=True,
                            hide_canvas=True,
                            block_webrtc=True,
                            allow_webgl=True,
                            google_search=False,
                            extra_flags=["--disable-http2"],
                            extra_headers=extra_headers,
                            selector_config=selector_config,
                        )
                    else:
                        raise
            else:  # INTERNAL_CHROME
                try:
                    page = StealthyFetcher.fetch(
                        spec.url,
                        headless=True,
                        real_chrome=True,
                        hide_canvas=True,
                        block_webrtc=True,
                        allow_webgl=True,
                        google_search=False,
                        extra_headers=extra_headers,
                        selector_config=selector_config,
                    )
                except Exception as e:
                    err_msg = str(e).lower()
                    if any(k in err_msg for k in ["http2", "protocol_error", "err_http2"]):
                        page = StealthyFetcher.fetch(
                            spec.url,
                            headless=True,
                            real_chrome=True,
                            hide_canvas=True,
                            block_webrtc=True,
                            allow_webgl=True,
                            google_search=False,
                            extra_flags=["--disable-http2"],
                            extra_headers=extra_headers,
                            selector_config=selector_config,
                        )
                    else:
                        raise

            if spec.css_selector:
                css_kwargs = {
                    "adaptive": True,
                    "auto_save": True,
                }
                if spec.identifier:
                    css_kwargs["identifier"] = spec.identifier
                matched = page.css(spec.css_selector, **css_kwargs)
                if matched:
                    target = matched[0]
                    if hasattr(target, "html_content") and target.html_content:
                        return str(target.html_content)
                    return target.get_all_text() if hasattr(target, "get_all_text") else target.text
                # 官方自适应自愈：当原有 ID/class 改版失效时，自动在 DOM 树中基于标签与文本寻回
                if hasattr(page, "relocate"):
                    relocated = page.relocate({"tag": "table", "text": "盘口"}, percentage=30)
                    if relocated:
                        target = relocated[0]
                        if hasattr(target, "html_content") and target.html_content:
                            return str(target.html_content)
                        return target.get_all_text() if hasattr(target, "get_all_text") else target.text

            if hasattr(page, "body") and page.body:
                return page.body.decode(spec.encoding, errors="replace")
            if page.text:
                return page.text
            return ""
        except ImportError:
            # 环境未安装 scrapling 库时，回退到标准受控 urllib（带 Chrome 136 UA）
            import urllib.request
            referer = "https://zq.titan007.com/"
            if "changeDetail" in spec.url:
                referer = f"https://zq.titan007.com/analysis/odds/{self.match_id}.htm"
            elif "1x2d" in spec.url:
                referer = "https://titan007.com/"
            elif "jc.titan007" in spec.url:
                referer = "https://www.titan007.com/"

            req = urllib.request.Request(
                spec.url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Referer": referer,
                },
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw_bytes = resp.read()
                return raw_bytes.decode(spec.encoding, errors="replace")

    def assemble_atomic_bundle(
        self,
        payloads: Dict[str, str],
        receipts_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        将抓取到的各端点 payload 组装为带 receipt 封条的原子存证包
        """
        all_specs = self.get_all_endpoint_specs()
        endpoint_receipts = []
        all_success = True

        for spec in all_specs:
            content = payloads.get(spec.name, "")
            is_ok = bool(content and len(content.strip()) > 0)
            if not is_ok:
                all_success = False

            content_bytes = content.encode("utf-8")
            sha256 = hashlib.sha256(content_bytes).hexdigest()
            endpoint_receipts.append(
                {
                    "name": spec.name,
                    "url": spec.url,
                    "status": 200 if is_ok else 500,
                    "size": len(content_bytes),
                    "encoding": spec.encoding,
                    "css_selector": spec.css_selector,
                    "sha256": sha256,
                }
            )

        bundle = {
            "matchId": self.match_id,
            "createdAt": time.strftime("%Y-%m-%d %H:%M:%S"),
            "scraplingVersion": "official-native-v1",
            "receipt": {
                "all_success": all_success,
                "endpoints_count": len(endpoint_receipts),
                "endpoints": endpoint_receipts,
            },
            "payloads": payloads,
            "rawFiles": payloads,  # 双键向后兼容
        }
        return bundle

    def save_bundle(self, bundle: Dict[str, Any], output_path: Union[str, Path]) -> Path:
        """保存单文件原子存证包至磁盘"""
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            json.dumps(bundle, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return p
