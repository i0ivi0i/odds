import test from "node:test";
import assert from "node:assert/strict";

import { fetchMatchDataWithFailover, fetchScheduleWithFailover, fetchWithTimeout } from "../src/failover-manager.js";
import { fetchOkoooMatchData, fetchOkoooSchedule } from "../src/okooo-adapter.js";

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

test("fetchOkoooMatchData 构造合规的备用推演数据结构", async () => {
  const data = await fetchOkoooMatchData("1313446");
  assert.equal(data.matchId, "1313446");
  assert.equal(data.source, "secondary:okooo");
  assert.ok(data.failoverNotice.includes("数据源提示"));
  assert.equal(data.markets.asianCompanies.length, 0);
  assert.equal(data.markets.europeCompanies.length, 0);
  assert.ok(data.dataWarnings.length > 0);
  assert.equal(data.analysisReady, false);
});

test("fetchOkoooSchedule 返回规范的备用赛程结构", async () => {
  const sched = await fetchOkoooSchedule({ saleDate: "2026-10-02" });
  assert.equal(sched.date, "2026-10-02");
  assert.ok(sched.source.startsWith("secondary:"));
  assert.ok(Array.isArray(sched.matches));
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

test("fetchMatchDataWithFailover 主源超时或异常时自动无缝切入备用源 (Okooo)", async () => {
  const mockFailingPrimary = async () => {
    throw new Error("504 Gateway Timeout");
  };
  const data = await fetchMatchDataWithFailover("1313446", {
    primaryFetcher: mockFailingPrimary,
    timeoutMs: 100,
    maxAttempts: 1
  });
  assert.equal(data.source, "secondary:okooo");
  assert.ok(data.failoverNotice.includes("数据源提示"));
  assert.equal(data.markets.asianCompanies.length, 0);
  assert.equal(data.analysisReady, false);
});

test("fetchScheduleWithFailover 主源失败时切入备用赛程", async () => {
  const mockFailingPrimary = async () => {
    throw new Error("DNS resolution failed");
  };
  const sched = await fetchScheduleWithFailover({
    primaryFetcher: mockFailingPrimary,
    timeoutMs: 100,
    maxAttempts: 1,
    saleDate: "2026-10-02"
  });
  assert.equal(sched.date, "2026-10-02");
  assert.ok(sched.source.startsWith("secondary:"));
});
