import { test } from "node:test";
import assert from "node:assert/strict";
import { fetchFallbackInjuries, TEAM_ALIASES, loadBbsToken } from "../src/injury-service.js";

test("TEAM_ALIASES 包含五大联赛核心球队映射", () => {
  assert.ok(TEAM_ALIASES["阿森纳"].includes("arsenal"));
  assert.ok(TEAM_ALIASES["皇家马德里"].includes("real madrid"));
  assert.ok(TEAM_ALIASES["拜仁慕尼黑"].includes("bayern munich"));
  assert.ok(TEAM_ALIASES["国际米兰"].includes("inter"));
  assert.ok(TEAM_ALIASES["巴黎圣日耳曼"].includes("psg"));
});

test("loadBbsToken 正确读取已配置的密钥", () => {
  const token = loadBbsToken();
  assert.ok(typeof token === "string");
});

test("fetchFallbackInjuries 对不支持的联赛返回空结构而不崩溃", async () => {
  const result = await fetchFallbackInjuries({
    league: "未知次级联赛",
    homeTeam: "队伍A",
    awayTeam: "队伍B",
  });
  assert.deepEqual(result, { home: [], away: [] });
});
