import test from "node:test";
import assert from "node:assert/strict";

import { fetchMatchDataWithFailover, fetchScheduleWithFailover, fetchWithTimeout } from "../src/failover-manager.js";

test("fetchWithTimeout 在超时时正确拒绝", async () => {
  await assert.rejects(
    () =>
      fetchWithTimeout(
        () => new Promise((r) => setTimeout(r, 200)),
        50
      ),
    /Request timeout after 50ms/
  );
});

test("fetchMatchDataWithFailover 主源成功时返回 primary 数据", async () => {
  const mockPrimary = async () => ({
    matchId: "999",
    detail: { basic: { league: "西甲" } },
    markets: {}
  });
  const data = await fetchMatchDataWithFailover("999", {
    primaryFetcher: mockPrimary,
    timeoutMs: 1000
  });
  assert.equal(data.source, "primary:titan007");
  assert.equal(data.detail.basic.league, "西甲");
});

test("fetchMatchDataWithFailover 主源超时后抛错，脚本通道不自动切其他网站", async () => {
  const mockFailingPrimary = async () => {
    throw new Error("504 Gateway Timeout");
  };
  await assert.rejects(
    () =>
      fetchMatchDataWithFailover("1313446", {
        primaryFetcher: mockFailingPrimary,
        timeoutMs: 100,
        maxAttempts: 1
      }),
    /504 Gateway Timeout/
  );
});

test("fetchScheduleWithFailover 主源失败后抛错，脚本通道不自动切其他网站", async () => {
  const mockFailingPrimary = async () => {
    throw new Error("DNS resolution failed");
  };
  await assert.rejects(
    () =>
      fetchScheduleWithFailover({
        primaryFetcher: mockFailingPrimary,
        timeoutMs: 100,
        maxAttempts: 1,
        saleDate: "2026-10-02"
      }),
    /DNS resolution failed/
  );
});
