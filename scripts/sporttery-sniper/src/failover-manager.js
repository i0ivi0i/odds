import { fetchMatchData as fetchTitanMatchData, fetchJcSchedule as fetchTitanSchedule } from "./titan007.js";

const DEFAULT_TIMEOUT_MS = 30000;

export async function fetchWithTimeout(fn, timeoutMs = DEFAULT_TIMEOUT_MS) {
  return Promise.race([
    fn(),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error(`Request timeout after ${timeoutMs}ms`)), timeoutMs)
    )
  ]);
}

/**
 * 单场数据提取：脚本通道只打球探；失败重试后抛错，由分析流程补抓。缺资料不能硬推。
 */
export async function fetchMatchDataWithFailover(input, options = {}) {
  const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
  const maxAttempts = options.maxAttempts ?? 2;
  const primaryFn = options.primaryFetcher || (() => fetchTitanMatchData(input));
  let lastError;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const data = await fetchWithTimeout(primaryFn, timeoutMs);
      return {
        ...data,
        source: data.source || "primary:titan007"
      };
    } catch (err) {
      lastError = err;
      if (attempt < maxAttempts) {
        await new Promise((r) => setTimeout(r, 200));
        continue;
      }
      console.error(
        `[failover] 主数据源 (titan007) 尝试 ${attempt} 次失败 (${err.message})。脚本通道未再抓其他网站；分析流程须补齐伤停与时序，缺、错、少不能硬推。`
      );
    }
  }

  throw lastError;
}

/**
 * 赛程列表同步：脚本通道只打球探；失败重试后抛错，由分析流程补抓。
 */
export async function fetchScheduleWithFailover(options = {}) {
  const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
  const maxAttempts = options.maxAttempts ?? 2;
  const primaryFn = options.primaryFetcher || (() => fetchTitanSchedule(globalThis.fetch, options));
  let lastError;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const data = await fetchWithTimeout(primaryFn, timeoutMs);
      return {
        ...data,
        source: data.source || "primary:titan007"
      };
    } catch (err) {
      lastError = err;
      if (attempt < maxAttempts) {
        await new Promise((r) => setTimeout(r, 200));
        continue;
      }
      console.error(
        `[failover] 主赛程源 (titan007) 失败 (${err.message})。脚本通道未再抓其他网站；分析流程须补齐赛程后再推。`
      );
    }
  }

  throw lastError;
}
