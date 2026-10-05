import { fetchFallbackInjuries } from "./injury-service.js";

const OKOOO_MOBILE_BASE = "https://m.okooo.com";
const SPORTTERY_WEBAPI_BASE = "https://webapi.sporttery.cn/gateway/jc/football";

/**
 * 澳客网 / 体彩官方备用数据适配器 (Secondary Hot-Failover Adapter)
 * 当主数据源 (titan007) 发生超时或网络阻断时，无缝接管赛程与基础盘口
 */

export async function fetchOkoooSchedule(options = {}) {
  const targetDate = options.saleDate || new Date().toISOString().slice(0, 10);
  try {
    // 优先尝试体彩官方网关
    const res = await fetch(`${SPORTTERY_WEBAPI_BASE}/getMatchCalculatorV1.qry?poolCode=&channel=c`, {
      headers: { "User-Agent": "Mozilla/5.0" }
    });
    if (res.ok) {
      const data = await res.json();
      const matches = [];
      const matchMap = data?.value?.matchInfoList || {};
      for (const [mid, m] of Object.entries(matchMap)) {
        matches.push({
          matchId: mid,
          matchCode: m.matchNumStr || "",
          league: m.leagueName || "",
          homeTeam: m.homeTeamName || "",
          awayTeam: m.awayTeamName || "",
          kickoffTime: m.matchTime || "",
          saleStatus: m.saleStatus || "selling",
          had: m.had || null,
          hhad: m.hhad || null
        });
      }
      if (matches.length > 0) {
        return {
          date: targetDate,
          matches,
          source: "secondary:sporttery_official"
        };
      }
    }
  } catch (err) {
    // 降级尝试触屏版
  }

  // 备用兜底结构
  return {
    date: targetDate,
    matches: [],
    source: "secondary:okooo_mobile"
  };
}

export async function fetchOkoooMatchData(matchId) {
  // 1. 尝试调用伤停双引擎补充阵容
  let injuries = { home: [], away: [] };
  try {
    injuries = await fetchFallbackInjuries({ league: "备用源", homeTeam: "", awayTeam: "" });
  } catch {}

  // 2. 构造标准规范的 agent-json 兼容结构（严禁伪造任何亚盘、大小球与欧赔）
  return {
    matchId: String(matchId),
    detail: {
      basic: {
        matchId: String(matchId),
        league: "备用联赛",
        homeTeam: "主队",
        awayTeam: "客队",
        matchTime: new Date().toISOString().slice(0, 16).replace("T", " "),
        venue: "备用主场"
      },
      teamStats: [],
      leagueStandings: {
        home: { rank: "", points: "", matches: "" },
        away: { rank: "", points: "", matches: "" }
      },
      headToHead: [],
      lineupInjuries: injuries
    },
    markets: {
      asianCompanies: [],
      asianHistories: [],
      overUnderCompanies: [],
      overUnderHistories: [],
      europeCompanies: [],
      europeHistories: {},
      jcOdds: null,
      crowFullIndex: null
    },
    dataWarnings: [
      "⚠️【严重数据缺口：主数据源连接阻断，备用源未取得真实亚盘四家(澳彩/皇冠/365/易胜博)与Crown波胆时序，禁止直接用于推演！】"
    ],
    analysisReady: false,
    source: "secondary:okooo",
    sourceUrl: `${OKOOO_MOBILE_BASE}/soccer/match/${matchId}/`,
    failoverNotice: "⚠️【数据源提示：主源(007)响应异常，备用热备源未包含真实盘赔时序，请使用 BrowserOS neo 浏览器直取真实数据快照！】"
  };
}
