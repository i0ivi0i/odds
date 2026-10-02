import fs from "node:fs";
import path from "node:path";
import os from "node:os";

// 常见俱乐部中英对照表（主流五大联赛 + 常见热门球队）
export const TEAM_ALIASES = {
  // 英超 (Premier League)
  "阿森纳": ["arsenal", "ars"],
  "曼城": ["manchester city", "man city", "mci"],
  "曼彻斯特城": ["manchester city", "man city", "mci"],
  "利物浦": ["liverpool", "liv"],
  "切尔西": ["chelsea", "che"],
  "热刺": ["tottenham", "tottenham hotspur", "spurs", "tot"],
  "托特纳姆热刺": ["tottenham", "tottenham hotspur", "spurs", "tot"],
  "曼联": ["manchester united", "man utd", "mun"],
  "曼彻斯特联": ["manchester united", "man utd", "mun"],
  "纽卡斯尔联": ["newcastle united", "newcastle", "new"],
  "纽卡斯尔": ["newcastle united", "newcastle", "new"],
  "阿斯顿维拉": ["aston villa", "villa", "avl"],
  "布莱顿": ["brighton", "brighton & hove albion", "bha"],
  "西汉姆联": ["west ham", "west ham united", "whu"],
  "西汉姆": ["west ham", "west ham united", "whu"],
  "狼队": ["wolverhampton", "wolves", "wol"],
  "富勒姆": ["fulham", "ful"],
  "布伦特福德": ["brentford", "bre"],
  "水晶宫": ["crystal palace", "cry"],
  "埃弗顿": ["everton", "eve"],
  "伯恩茅斯": ["bournemouth", "bou"],
  "诺丁汉森林": ["nottingham forest", "nfo"],
  "伊普斯维奇": ["ipswich", "ipswich town", "ips"],
  "莱斯特城": ["leicester", "leicester city", "lei"],
  "南安普敦": ["southampton", "sou"],

  // 西甲 (La Liga)
  "皇家马德里": ["real madrid", "rma"],
  "皇马": ["real madrid", "rma"],
  "巴塞罗那": ["barcelona", "bar"],
  "巴萨": ["barcelona", "bar"],
  "马德里竞技": ["atletico madrid", "atlético madrid", "atm"],
  "马竞": ["atletico madrid", "atlético madrid", "atm"],
  "皇家社会": ["real sociedad", "rso"],
  "毕尔巴鄂竞技": ["athletic bilbao", "athletic club", "ath"],
  "毕尔巴鄂": ["athletic bilbao", "athletic club", "ath"],
  "塞维利亚": ["sevilla", "sevilla fc", "sev"],
  "皇家贝蒂斯": ["real betis", "betis", "bet"],
  "贝蒂斯": ["real betis", "betis", "bet"],
  "比利亚雷亚尔": ["villarreal", "vil"],
  "瓦伦西亚": ["valencia", "val"],
  "赫罗纳": ["girona", "gir"],

  // 德甲 (Bundesliga)
  "拜仁慕尼黑": ["bayern munich", "bayern münchen", "fc bayern", "fcb"],
  "拜仁": ["bayern munich", "bayern münchen", "fc bayern", "fcb"],
  "多特蒙德": ["dortmund", "borussia dortmund", "bvb"],
  "多特": ["dortmund", "borussia dortmund", "bvb"],
  "勒沃库森": ["leverkusen", "bayer leverkusen", "b04"],
  "莱比锡红牛": ["rb leipzig", "leipzig", "rbl"],
  "莱比锡": ["rb leipzig", "leipzig", "rbl"],
  "法兰克福": ["eintracht frankfurt", "frankfurt", "sge"],
  "斯图加特": ["stuttgart", "vfb stuttgart", "vfb"],

  // 意甲 (Serie A)
  "国际米兰": ["inter", "inter milan", "internazionale", "int"],
  "国米": ["inter", "inter milan", "internazionale", "int"],
  "AC米兰": ["ac milan", "milan", "acm"],
  "米兰": ["ac milan", "milan", "acm"],
  "尤文图斯": ["juventus", "juv"],
  "尤文": ["juventus", "juv"],
  "那不勒斯": ["napoli", "nap"],
  "罗马": ["roma", "as roma", "rom"],
  "拉齐奥": ["lazio", "laz"],
  "亚特兰大": ["atalanta", "ata"],
  "佛罗伦萨": ["fiorentina", "fio"],

  // 法甲 (Ligue 1)
  "巴黎圣日耳曼": ["paris saint-germain", "psg", "paris sg"],
  "大巴黎": ["paris saint-germain", "psg", "paris sg"],
  "摩纳哥": ["monaco", "as monaco", "asm"],
  "马赛": ["marseille", "om"],
  "里尔": ["lille", "losc"],
  "里昂": ["lyon", "ol"],
};

// 内存缓存 (TTL 10 分钟)
let cachedFplData = null;
let cachedFplTime = 0;
const cachedBbsLeagueInjuries = new Map();
const cachedBbsTeamPlayers = new Map();

/**
 * 读取本地配置的 Big Balls API 密钥
 * 优先读取项目通用配置 config/api_keys.json，其次检查用户目录通用配置
 */
export function loadBbsToken() {
  if (process.env.BBS_API_KEY?.trim()) {
    return process.env.BBS_API_KEY.trim();
  }

  // 1. 优先读取项目通用配置 config/api_keys.json
  const candidateConfigPaths = [
    path.resolve(process.cwd(), "config", "api_keys.json"),
    path.resolve(process.cwd(), "..", "..", "config", "api_keys.json"),
    path.join(os.homedir(), ".config", "odds", "api_keys.json"),
  ];

  for (const cfgPath of candidateConfigPaths) {
    if (fs.existsSync(cfgPath)) {
      try {
        const parsed = JSON.parse(fs.readFileSync(cfgPath, "utf8"));
        const key = parsed?.bigballs?.primary_key || parsed?.bigballs?.backup_key;
        if (key && !key.includes("[REDACTED]")) return key;
      } catch {}
    }
  }

  // 2. 备用兼容路径
  const homeDir = os.homedir();
  const tokenFile = path.join(homeDir, ".gemini", "config", "bigballs_token.txt");
  if (fs.existsSync(tokenFile)) {
    try {
      const val = fs.readFileSync(tokenFile, "utf8").trim();
      if (val) return val;
    } catch {}
  }
  const jsonFile = path.join(homeDir, ".gemini", "config", "bigballs_tokens.json");
  if (fs.existsSync(jsonFile)) {
    try {
      const parsed = JSON.parse(fs.readFileSync(jsonFile, "utf8"));
      return parsed.primary_key || parsed.backup_key || "";
    } catch {}
  }
  return "";
}

function cleanStr(str) {
  return String(str || "").toLowerCase().replace(/[^a-z0-9]/g, "");
}

function isTeamMatch(targetName, candidates) {
  if (!targetName || !candidates || !candidates.length) return false;
  const targetClean = cleanStr(targetName);
  for (const c of candidates) {
    const candidateClean = cleanStr(c);
    if (!candidateClean) continue;
    if (targetClean === candidateClean) return true;
    if (targetClean.includes(candidateClean) || candidateClean.includes(targetClean)) {
      return true;
    }
  }
  return false;
}

/**
 * 引擎一：FPL 官方数据源（覆盖英超 20 队，包含详细出战概率）
 */
async function getFplInjuries(teamName) {
  const now = Date.now();
  if (!cachedFplData || now - cachedFplTime > 600000) {
    try {
      const res = await fetch("https://fantasy.premierleague.com/api/bootstrap-static/", {
        headers: { "User-Agent": "Mozilla/5.0" },
      });
      if (res.ok) {
        cachedFplData = await res.json();
        cachedFplTime = now;
      }
    } catch {}
  }
  if (!cachedFplData?.teams || !cachedFplData?.elements) {
    return [];
  }

  const aliases = TEAM_ALIASES[teamName] || [teamName];
  const matchedTeam = cachedFplData.teams.find((t) =>
    isTeamMatch(t.name, aliases) || isTeamMatch(t.short_name, aliases)
  );
  if (!matchedTeam) return [];

  const teamId = matchedTeam.id;
  const injured = cachedFplData.elements.filter((p) => {
    if (p.team !== teamId) return false;
    if (p.status === "i" || p.status === "d" || p.status === "s" || p.status === "u") return true;
    if (p.chance_of_playing_next_round !== null && p.chance_of_playing_next_round < 100) return true;
    return false;
  });

  return injured.map((p) => {
    let reason = p.news || "";
    if (p.chance_of_playing_next_round !== null && p.chance_of_playing_next_round !== undefined) {
      const chanceText = `出战概率 ${p.chance_of_playing_next_round}%`;
      reason = reason ? `${chanceText} (${reason})` : chanceText;
    } else if (!reason) {
      reason = "伤停缺阵";
    }
    return {
      number: "-",
      player: p.web_name || `${p.first_name} ${p.second_name}`.trim(),
      reason,
      source: "FPL官方",
    };
  });
}

/**
 * 引擎二：Big Balls Sports Data API（覆盖五大联赛及全球主要赛事）
 */
async function getBbsInjuries(leagueKey, teamName) {
  const token = loadBbsToken();
  if (!token) return [];

  const now = Date.now();
  let leagueInjuries = cachedBbsLeagueInjuries.get(leagueKey);
  if (!leagueInjuries || now - leagueInjuries.time > 600000) {
    try {
      const res = await fetch(`https://api.bigballsdata.com/v1/injuries?league=${leagueKey}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "User-Agent": "Antigravity/1.0",
        },
      });
      if (res.ok) {
        const injData = await res.json();
        const value = injData?.data?.injuries?.value || injData?.data?.injuries || [];
        leagueInjuries = { list: Array.isArray(value) ? value : [], time: now };
        cachedBbsLeagueInjuries.set(leagueKey, leagueInjuries);
      }
    } catch {}
  }

  const injuriesList = leagueInjuries?.list || [];
  if (!injuriesList.length) return [];

  // 获取球队英文检索词
  const aliases = TEAM_ALIASES[teamName] || [teamName];
  const queryName = aliases[0];

  let teamPlayers = cachedBbsTeamPlayers.get(queryName);
  if (!teamPlayers || now - teamPlayers.time > 600000) {
    try {
      const pRes = await fetch(
        `https://api.bigballsdata.com/v1/players?team=${encodeURIComponent(queryName)}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "User-Agent": "Antigravity/1.0",
          },
        }
      );
      if (pRes.ok) {
        const pData = await pRes.json();
        teamPlayers = { list: pData?.data || [], time: now };
        cachedBbsTeamPlayers.set(queryName, teamPlayers);
      }
    } catch {}
  }

  const playerRoster = teamPlayers?.list || [];
  const matched = [];

  // 交叉匹配伤员
  for (const player of playerRoster) {
    const pClean = cleanStr(player.name);
    for (const inj of injuriesList) {
      const iClean = cleanStr(inj.full_name || inj.display_name);
      if (pClean && iClean && (pClean === iClean || pClean.includes(iClean) || iClean.includes(pClean))) {
        matched.push({
          number: player.jersey_number || "-",
          player: player.name || inj.display_name || "未知球员",
          reason: inj.injury_type || "伤停缺阵",
          source: "BigBallsAPI",
        });
        break;
      }
    }
  }

  return matched;
}

/**
 * 统一多源伤停补全接口 (纯 Node.js，零 Python，零第三方 npm 依赖)
 */
export async function fetchFallbackInjuries({ league = "", homeTeam = "", awayTeam = "" }) {
  const result = { home: [], away: [] };
  const cleanLeague = String(league).toLowerCase();

  // 1. 英超 -> FPL 官方高精接口
  if (cleanLeague.includes("英超") || cleanLeague.includes("premier")) {
    const [homeFpl, awayFpl] = await Promise.all([
      getFplInjuries(homeTeam),
      getFplInjuries(awayTeam),
    ]);
    result.home = homeFpl;
    result.away = awayFpl;
    return result;
  }

  // 2. 西甲、意甲、德甲、法甲、美职足 -> Big Balls API
  let bbsLeague = null;
  if (cleanLeague.includes("西甲") || cleanLeague.includes("la liga") || cleanLeague.includes("laliga")) {
    bbsLeague = "la_liga";
  } else if (cleanLeague.includes("意甲") || cleanLeague.includes("serie a") || cleanLeague.includes("seriea")) {
    bbsLeague = "serie_a";
  } else if (cleanLeague.includes("德甲") || cleanLeague.includes("bundesliga")) {
    bbsLeague = "bundesliga";
  } else if (cleanLeague.includes("法甲") || cleanLeague.includes("ligue 1") || cleanLeague.includes("ligue1")) {
    bbsLeague = "ligue_1";
  } else if (cleanLeague.includes("美职") || cleanLeague.includes("mls")) {
    bbsLeague = "mls";
  }

  if (bbsLeague) {
    const [homeBbs, awayBbs] = await Promise.all([
      getBbsInjuries(bbsLeague, homeTeam),
      getBbsInjuries(bbsLeague, awayTeam),
    ]);
    result.home = homeBbs;
    result.away = awayBbs;
    return result;
  }

  return result;
}
