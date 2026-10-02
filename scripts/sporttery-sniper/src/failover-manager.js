import { fetchMatchData as fetchTitanMatchData, fetchJcSchedule as fetchTitanSchedule } from "./titan007.js";
import { fetchOkoooMatchData, fetchOkoooSchedule } from "./okooo-adapter.js";

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
 * 具备双轨热备与自动熔断的单场数据提取
 */
export async function fetchMatchDataWithFailover(input, options = {}) {
  const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
  const maxAttempts = options.maxAttempts ?? 2;
  const primaryFn = options.primaryFetcher || (() => fetchTitanMatchData(input));
  const backupFn = options.backupFetcher || (() => fetchOkoooMatchData(input));

  // 1. 尝试主数据源 (titan007)
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const data = await fetchWithTimeout(primaryFn, timeoutMs);
      return {
        ...data,
        source: data.source || "primary:titan007"
      };
    } catch (err) {
      if (attempt < maxAttempts) {
        await new Promise((r) => setTimeout(r, 200));
        continue;
      }
      console.error(
        `[failover] 主数据源 (titan007) 尝试 ${attempt} 次失败 (${err.message})，正在无缝启动备用热备源 (澳客网)...`
      );
    }
  }

  // 2. 主源失败，无缝切入备用数据源 (澳客网 / 官方镜像)
  const backupData = await backupFn();
  return backupData;
}

/**
 * 具备双轨热备的赛程列表同步
 */
export async function fetchScheduleWithFailover(options = {}) {
  const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
  const maxAttempts = options.maxAttempts ?? 2;
  const primaryFn = options.primaryFetcher || (() => fetchTitanSchedule(globalThis.fetch, options));
  const backupFn = options.backupFetcher || (() => fetchOkoooSchedule(options));

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const data = await fetchWithTimeout(primaryFn, timeoutMs);
      return {
        ...data,
        source: data.source || "primary:titan007"
      };
    } catch (err) {
      if (attempt < maxAttempts) {
        await new Promise((r) => setTimeout(r, 200));
        continue;
      }
      console.error(
        `[failover] 主赛程源 (titan007) 失败 (${err.message})，正在无缝切至备用赛程源...`
      );
    }
  }

  return await backupFn();
}
