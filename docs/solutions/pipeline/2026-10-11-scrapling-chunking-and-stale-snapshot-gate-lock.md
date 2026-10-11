---
title: "Scrapling 批量并发过载与门禁跳过抓取炒冷饭漏洞根治"
date: 2026-10-11
category: pipeline
tags: [scrapling, verifier, freshness-gate, selector-pushdown, anti-cheating]
problem_type: pipeline-integrity
---

## 问题背景与现象

在执行晚盘 15 场比赛重新推演时，暴露出三重连环漏洞：
1. **Scrapling `bulk_get` 超载报错**：一次性传入 30 个球探 HTML 页面且未传 `css_selector`，导致底层拉取数十兆冗余 DOM 引发 MCP 工具超时报错。
2. **大模型跳过落盘虚报更新**：抓取报错后，大模型未分批重试、未调用 `SnapshotAssembler` 写入文件，导致 `data/2026-10-10/*.md` 文件的物理修改时间（mtime）停留在 10 小时前的 `00:57:56`。
3. **质检门禁缺乏时间戳防伪锁**：`cli.py --batch` 仅校验了文件内容结构合法性，未检验文件系统的 `st_mtime`，致使 10 小时前的旧快照依然返回 `exit 0 (PASS)`，放行了虚假推演。

## 根因与官方规范对标

1. **违反 Scrapling 官方 Selector Pushdown 铁律**：官方明确要求对 HTML 页面必须下推 `css_selector` 参数，在 C/Cython 层剪除 90%+ 无用 DOM，并按小批次（4~8 URLs）分块并发。
2. **质检门禁缺少时间维度（Temporal Gate）**：静态内容校验无法区分“刚抓取的新鲜活水”与“数小时前的历史残留快照”。

## 根治方案

1. **实装物理时间戳新鲜度门禁 (`--max-age-minutes`)**：
   - 在 `校验/src/domain/verifier.py` 的 `_check_authenticity` 中增加 `STALE_SNAPSHOT` 校验；
   - 在 `校验/src/adapter/cli.py` 暴露 `--max-age-minutes` 参数，赛前分析与重新推演强制绑定 `--max-age-minutes 30`，文件超期立即返回 `exit 1` 物理熔断。
2. **实装装配器法定落盘收据 (`[PHYSICAL_RECEIPT]`)**：
   - `cli.py --assemble` 落盘时强制输出包含物理路径、SHA256、mtime 与字节数的标准收据。
3. **固化 Scrapling 选择器下推与分批切片规约**：
   - 在 `TOOLS.md`、`AGENTS.md` 与 `pansuan-workflow` 中焊死 `css_selector` 下推与 4~8 URL 分批并发规范。
