import test from "node:test";
import assert from "node:assert/strict";

import { parseCliArgs } from "../src/cli.js";

test("schedule 命令兼容 npm 吞掉 --format 后留下的裸格式参数", () => {
  const args = parseCliArgs(["schedule", "openclaw-json"]);

  assert.equal(args.command, "schedule");
  assert.equal(args.scheduleDate, null);
  assert.equal(args.format, "openclaw-json");
});

test("schedule 命令仍支持显式日期和格式参数", () => {
  const args = parseCliArgs([
    "schedule",
    "2026-06-11",
    "--format",
    "openclaw-json",
  ]);

  assert.equal(args.command, "schedule");
  assert.equal(args.scheduleDate, "2026-06-11");
  assert.equal(args.format, "openclaw-json");
});

test("schedule 与 analyze 支持通用 agent-json 与 json 格式", () => {
  const args1 = parseCliArgs(["schedule", "--format", "agent-json"]);
  assert.equal(args1.format, "agent-json");

  const args2 = parseCliArgs(["analyze", "2990354", "--format", "json"]);
  assert.equal(args2.format, "agent-json");
});

test("review 命令识别比赛输入并保留历史窗口", () => {
  const args = parseCliArgs(["review", "2990354", "--history-window", "15"]);

  assert.equal(args.command, "review");
  assert.equal(args.input, "2990354");
  assert.equal(args.historyWindow, 15);
});
