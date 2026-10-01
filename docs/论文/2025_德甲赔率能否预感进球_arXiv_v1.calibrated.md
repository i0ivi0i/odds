# Do Betting Markets Sense a Goal Coming? Evidence from the German Bundesliga

> 重建说明：模式 page-aligned；来源 `2025_德甲赔率能否预感进球_arXiv_v1.pdf`；共 26 页；原图逐页查看 26/26 页。
> 核图证据：前次 task-2.log 成功记录确认第1–8页；本次核查第5、7、9–26页。第13页首次超时，第二次成功；第23页另行核实首行标签。原文错误与跨页矛盾均保留并标注。

## Page 01: Do Betting Markets Sense a Goal Coming? Evidence from the German Bundesliga

源页：第 1 页

### 页面目的

- Present authors, affiliations and abstract.

### 布局地图

- Centered title, two author affiliations and corresponding-author line above date and abstract; arXiv identifier is vertical at the left; printed page 1.

### 按区域确认内容

#### 区域 1：原文正文与标注

arXiv:2505.21275v1 [econ.GN] 27 May 2025

Do Betting Markets Sense a Goal Coming?

Evidence from the German Bundesliga

David Winkelmann† ⋆ and Christian Deutscher‡

†Department of Business Administration and Economics, Bielefeld University,
Bielefeld, Germany

‡Department of Psychology and Sports Science, Bielefeld University, Bielefeld,
Germany

⋆Corresponding author: david.winkelmann@uni-bielefeld.de

June 11, 2025

Abstract
We use the fertile ground of betting markets to study the anticipation of major news
in financial markets. While there is a considerable body of literature on the accuracy and
efficiency of betting markets after important in-match events, there are no studies dealing
with the anticipation of such events. This paper tracks bookmaker odds and betting stakes
to provide insights into the movement of both prior to goals. Utilising high-resolution (1
Hz) data from a leading European bookmaker for a full season of the top German football
league, we analyse whether market participants anticipate major news. In particular,
we consider the case of the first goal scored within a match, with its strong impact on
the match outcome. Using regression models and state-space models (SSMs) accounting
for an underlying market activity level, we investigate whether the bookmaker adjusts
odds and bettors tend to place higher stakes on the scoring team right before the first
goal is scored. Our results indicate that neither side of the market anticipates goals by
significantly adjusting their behaviour.
Keywords: live betting, market anticipation, regression models, state-space models,
time series analysis

### 视觉备注

- The displayed date June 11, 2025 differs from the arXiv sidebar date 27 May 2025; both are preserved.

## Page 02: 1 Introduction

源页：第 2 页

### 页面目的

- Introduce news responses in betting and financial markets.

### 布局地图

- Bold Section 1 followed by two complete paragraphs and a single-line next paragraph; footer 2.

### 按区域确认内容

#### 区域 1：原文正文与标注

1 Introduction

Sports betting markets hold significant economic relevance, with a turn-over exceeding 40
billion euros in Europe alone in 2021 (Michels et al., 2023). Given the increased competition
in recent years and the resulting narrower margins, bookmakers have to be excellent predictors
of match outcomes to remain profitable (Che et al., 2017; Winkelmann et al., 2024). Such
preciseness is particularly crucial for the growing live-betting market, where bets are placed
during an ongoing match. Here, bookmakers must promptly adjust odds in response to in-
match dynamics and major news, such as goals (Ötting et al., 2024).

Sports betting markets are similar to general stock markets. Specifically, placing a bet is
akin to buying a company’s stock (Sauer, 1998). However, in contrast to financial markets,
the value of the uncertain asset (the outcome of a bet) becomes known after a fixed deadline
(Thaler and Ziemba, 1988). Recent financial market literature examines the effect of news on
stock prices (see e.g. Chua and Tsiaplias, 2019, and Haroon and Rizvi, 2020). Studies suggest
that news sentiment and media coverage can predict stock price movements and volatility. On
the one hand, positive news lead to quick increases in stock returns, while on the other hand,
negative news causes delayed reactions (Heston and Sinha, 2017). Incorporating financial news
data generally improves prediction accuracy compared to using stock features alone (Dahal
et al., 2023). Market news is perceived differently by investors (Ben-Rephael et al., 2017), and
even fake news can impact stock markets (Clarke et al., 2019). In financial markets, stock
price movements before major corporate decisions may result from both insider trading and
market anticipation (Jarrell and Poulsen, 1989; Jain and Sunderman, 2014; Tunyi, 2021). In
contrast, news in betting markets typically become unambiguously observable to all market
participants at the same point in time. Although this provides an excellent environment for
analysing the impact of news on market behaviour, to date, there is only limited research
in this area. Some indication on the efficiency of betting markets after major events comes
from studies using betting exchange data (see e.g. Gil and Levitt, 2007; Choi and Hui, 2014,
and Croxson and Reade, 2014). Relying on live-betting markets, Ötting et al. (2024) show
that bettors tend to overreact to news in football. However, we are unaware of any study
investigating the anticipation of in-match news in sports betting markets.

Given the characteristics of sports betting markets as fertile ground for analysing arbitrage

### 视觉备注

- The page ends with analysing arbitrage; the sentence continues on page 3. Ötting is restored from the separated diaeresis in the text layer.

## Page 03: 2 Data

源页：第 3 页

### 页面目的

- Explain the study setting and introduce the dataset.

### 布局地图

- Opening introduction continuation, two further paragraphs, then Section 2 and the beginning of the data description; footer 3.

### 按区域确认内容

#### 区域 1：原文正文与标注

opportunities (Miller Jr and Rapach, 2013), in-match data allows to accurately analyse the
anticipation of news by market participants. As football is a low-scoring sport, the first goal is
crucial to the match outcome (Lago-Peñas et al., 2016). Therefore, this event is of particular
interest when considering major news in football. Studying the anticipation of goals can reveal
whether betting markets are rational or contain inefficiencies that skilled bettors can exploit.
If odds do not fully reflect the probability of an impending goal, then market participants
may have arbitrage opportunities. For example, if bettors systematically anticipate goals
before they occur (due to tactical momentum or match dynamics), this would suggest that
bookmakers adjust their odds reactively rather than proactively.

Our study relies on in-match data from the German Bundesliga season 2018/19 provided
by a large European bookmaker. This unique data features a high resolution of 1 Hz on the
bookmaker’s odds and stakes placed by bettors. Additionally, it includes information on the
precise time of major events during the match, such as goals and red cards. We consider
only matches with at least one goal and focus particularly on the market behaviour of the
bookmaker and bettors just before the first goal of a match to capture potential anticipation
effects. If bettors were to anticipate the first goal, they could generate positive returns by
betting on the team that eventually scores the goal. Highly dynamic markets, such as both the
financial market and the sports betting market, involve serial correlation in the not directly
observable market activity level. This naturally translates to a state-space modelling (SSM)
approach, as it was previously suggested by e.g. Choi and Hui (2014); Croxson and Reade
(2014); Ötting et al. (2024) for sports betting markets and e.g. Jacquier et al. (2002); Al-
Anaswah and Wilfling (2011) for general financial markets. This allows to relate observed
relative stakes to a (latent) state of the market.

The remainder of the paper is structured as follows: Section 2 details our data. In Sec-
tion 3, we examine the anticipating behaviour of the bookmaker, while Section 4 considers
the perspective of bettors. Finally, Section 5 concludes the paper.

2 Data

The data consists of pre-match and in-match betting odds for home wins, draws, and away
wins, along with detailed records of stakes placed by bettors for all 306 matches from the

### 视觉备注

- The number 306 appears before the page break; the season details continue on page 4. Lago-Peñas is restored from the separated tilde.

## Page 04: Data: First-goal timing

源页：第 4 页

### 页面目的

- Define the analysis sample and first-goal time.

### 布局地图

- Three text regions around a horizontal boxplot; footnotes 1 and 2 below the last paragraph; footer 4.

### 按区域确认内容

#### 区域 1：原文正文与标注

2018/19 Bundesliga season. The 1 Hz resolution of the betting activity results in strong
volatility in stakes over time. We thus aggregate the data into one-minute intervals to mitigate
such noise in the observed stakes. To focus on the odds movement and betting activity as
indicators of anticipating the match’s first goal, we exclude all 17 scoreless matches from the
sample. Descriptive statistics for the 289 matches featuring at least one goal highlight the
importance of the first goal for the final outcome. In 204 matches, the team scoring the first
goal ultimately won (70.6%), while the opposing team won 29 matches (10.0%), and there
were 56 draws (19.4%).

Football matches consist of two 45-minute halves, a half-time break of about 15 minutes,
and typically a few minutes of injury time. The longer a match remains scoreless, the higher
the chances for a draw and the lower the chances of a win by any team. Therefore, betting
odds crucially depend on the time left to play. We denote the minutes elapsed since the
kick-off by t, and the minute of the first goal in match i by T<sub>i</sub>.<sup>1</sup>


#### 区域 2：Figure 1横向箱线图

- Horizontal axis: Minute; ticks: 0, 20, 40, 60, 80, 100. No y-axis title. Box, median line, whiskers and isolated late-goal points show the first-goal distribution; no numerical quantiles are printed.

Figure 1: Boxplot of the minute T<sub>i</sub> in which the first goal was scored in the 289 non-scoreless
matches of the 2018/19 German Bundesliga season.

Figure 1 shows a boxplot of the minute the opening goal was scored. In our sample, the
first goal was scored anywhere between the first minute of a match and late during injury
time of the second half. Approximately 75% of the goals were scored during the first half.
The variable mintogoal<sub>it</sub> = T<sub>i</sub> − t indicates the time remaining between the current minute
t and the minute of the actual goal T<sub>i</sub> in match i.<sup>2</sup> To analyse potential shifts in betting
odds and stakes placed in the minutes preceding the first goal, we consider only those 256

<sup>1</sup> Note that for the first half, t always corresponds to the actual minute of the match. Due to variation in
the first half’s injury time, the second half starts at approximately minute t = 60.

<sup>2</sup> Note that this information becomes known only after the goal is scored.

### 视觉备注

- No numerical quartiles are printed in Figure 1: avoid treating visual estimates as transcribed values. The second half begins at approximately elapsed minute t=60.

## Page 05: Data: Implied probabilities and in-match covariates

源页：第 5 页

### 页面目的

- Define probabilities, expected-goal differences and red-card indicators.

### 布局地图

- Opening two-line continuation, normalization fraction, then a long covariate paragraph; footer 5.

### 按区域确认内容

#### 区域 1：原文正文与标注

matches (covering 9,245 minutes with a 0:0 score) where the first goal was scored from minute
6 onwards.

Analysing potential anticipation of goals by market participants involves examining both
bettors and bookmakers. Anticipating goals would result in shifts in odds set by bookmakers
and changes in stakes placed by bettors, respectively. Bookmakers set their odds based on
the expected outcome probability, often derived from forecasting models. Following previous
literature (see, e.g. Feddersen et al., 2017; Deutscher et al., 2018; Winkelmann et al., 2021), we
calculate implied winning probabilities from the betting odds, correcting for the bookmakers’
margin, as follows:

improb<sub>itj</sub> = (1/O<sub>itj</sub>)/(1/O<sub>ith</sub> + 1/O<sub>itd</sub> + 1/O<sub>ita</sub>), j = h, d, a.

for a home win (h), a draw (d), and an away win (a). We denote the in-match implied

probability for the team scoring the first goal as improb<sub>it</sub>. Typically, fixed match charac-
teristics, such as information on the relative team strengths, potential home advantage, and

possible injuries of players from both teams, are incorporated into the pre-match implied

probabilities, denoted by impprobpre<sub>it</sub>. During the course of the match, betting markets po-
tentially respond to in-match dynamics (Michels et al., 2023). Therefore, we consider the

expected goals of both teams until minute t of match i. Expected goals describe the number

of goals to be expected given the scoring opportunities teams have had. As expected goals

can be observed by bookmakers and bettors, they could potentially influence both betting

odds and stakes placed. We denote the difference in (cumulative) expected goals between

both teams from the beginning of the match until minute t from the perspective of the team

scoring the first goal by xgdiff<sub>it</sub>. We observe the difference in expected goals right before
the first goal to range between -2.28 to 1.85, indicating that there are expected as well as

surprising goals given the previous course of the match. On average, the expected goals for

the scoring team are higher by 0.13 in the last minute before the goal occurs, suggesting that

the team scoring the first goal had slightly more opportunities to score beforehand. Beyond

goals, red cards constitute a very important event expected to affect (implied) winning prob-

abilities. We capture red cards by the variables redcardteam<sub>it</sub> (and redcardopp<sub>it</sub>), taking the
value one if the team scoring the first goal (and the team conceding it, respectively) received

### 视觉备注

- The source spells the pre-match variable impprobpre with two p characters on this page; preserve it rather than standardizing to improbpre.

## Page 06: Data: Relative stakes and sentiment

源页：第 6 页

### 页面目的

- Define bettor-side variables and descriptive behaviour.

### 布局地图

- Red-card continuation above relative-stakes and sentiment paragraphs; ends with correlation discussion; footer 6.

### 按区域确认内容

#### 区域 1：原文正文与公式

a red card. Of the seven matches where a red card was issued before the first goal, the team
with the numerical advantage scored the first goal in six. In our sample, we do not observe
any matches where red cards were issued to both teams before the first goal was scored.

While the bookmaker’s behaviour can be obtained from the odds offered, the stakes placed
represent the bettors’ behaviour. Since betting on draws is unpopular (in our dataset, only
about 13% of the money is placed on draws), we focus on the stakes placed on the team scoring
the first goal relative to the total stakes placed on both teams at each minute, denoted by
stakerel<sub>it</sub>. Analysing relative stakes (compared to other match outcomes) rather than absolute
stakes avoids potential inaccuracies in the absolute stakes driven by closed markets, which can
occur in case of penalty kicks or VAR decisions (Ötting et al., 2024). To investigate bettors’
general behaviour, we examine descriptive statistics on the average relative stakes placed on
the team eventually scoring the first goal throughout the scoreless period. Average relative
stakes on the team scoring the first goal exhibit strong variation between 2.8% and 97.1%,
with a mean of 58.1% and a median of 65.0%, indicating that bettors tend to place more
money on teams eventually scoring the first goal.

More specifically, we find that bettors prefer betting on the home team (53.4% of relative
stakes are placed on home teams and 46.6% on away teams). This aligns with (Staněk, 2017)
and (Buhagiar et al., 2018), who report higher betting volumes on home teams. To account
for bettors’ behaviour, we introduce the variable home<sub>t</sub> taking value 1 if we consider relative
stakes placed on the home team in match i (i.e. the home team scores the first goal in match
i). Additionally, previous literature suggests that bettors tend to place more money on their
favourite teams (Na et al., 2019). Consequently, it can be expected that the teams’ sentiment
influences the distribution of stakes between the two teams. As a proxy, we consider the
variable volumediff<sub>t</sub> denoting the difference in the average absolute stakes per minute placed
on the two teams over all matches with a score of 0:0 contained in the dataset (see Table 5 in
the Appendix for an overview of average stakes for each team).

Table 1 presents summary statistics for the key variables in our dataset. We also examine
the correlation coefficients between these variables (see Table 6 in the Appendix). There are
only a few correlations worth highlighting (absolute value of correlation coefficient larger than
0.35). Unsurprisingly, pre-match and in-match implied probabilities are highly correlated as
long as the match remains scoreless. This is expected, as in the absence of major news,

### 视觉备注

- The source indexes home and volumediff by t in this prose, despite explaining the match index i; this inconsistency is retained.

## Page 07: Table 1: Summary statistics

源页：第 7 页

### 页面目的

- Report key-variable statistics and an example match.

### 布局地图

- Six-column ten-row table at the top, followed by correlations and Dortmund–Stuttgart example; footer 7.

### 按区域确认内容

#### 区域 1：顶部Table 1

Table 1: Summary statistics of the key variables in the dataset.

| Variable | Mean | Standard deviation | Minimum | Maximum | Median |
| --- | --- | --- | --- | --- | --- |
| t | 29.141 | 23.55 | 1 | 109 | 23 |
| mintogoal | 29.141 | 23.55 | 1 | 109 | 23 |
| improb | 0.435 | 0.175 | 0.046 | 0.922 | 0.416 |
| improbpre | 0.467 | 0.188 | 0.048 | 0.915 | 0.432 |
| redcardteam | 0.003 | 0.062 | 0 | 1 | 0 |
| redcardopp | 0.025 | 0.155 | 0 | 1 | 0 |
| xgdiff | 0.077 | 0.42 | -2.284 | 2.047 | 0.026 |
| home | 0.573 | 0.495 | 0 | 1 | 1 |
| volumediff | 6.881 | 16.425 | -46.715 | 46.773 | 7.583 |
| stakerel | 0.581 | 0.288 | 0 | 1 | 0.651 |

#### 区域 2：表后原文正文

pre-match winning probabilities (a strong predictor for match outcomes) should align closely
with in-match winning probabilities. Both variables are also correlated with the difference
in the volume (volumediff ) and relative stakes (stakerel ), indicating that bettors tend to
place more money on the favourite teams, according to implied probabilities. Furthermore,
a positive difference in the average absolute stakes placed on a team over the whole season
typically translates into higher relative stakes in a specific match. Except for the time variable,
where we include linear, quadratic, and interaction terms, the variance inflation factors do
not indicate multicollinearity among the covariates for the regression models considered in
Section 3.

Figure 2 illustrates relative stakes and implied probabilities for an example match between
Borussia Dortmund and VfB Stuttgart in the 2018/19 Bundesliga season. The final result
was 3:1, with Borussia Dortmund scoring the first goal 79 minutes after kick-off (in this case,
minute 62 of the match). Borussia Dortmund was denoted to be the clear pre-match favourite
with an implied winning probability (indicated by the red solid line) of 74.7%. In contrast,
VfB Stuttgart had a winning probability of only 9.5% at the start of the match. While the
implied probabilities for a Stuttgart win remained relatively constant during the scoreless
period of the match, the implied probability for Dortmund decreased to 57.4% before the first
goal was scored. Although the relative stakes exhibited much more fluctuation throughout
the match, stakes placed on Borussia Dortmund were, on average, about three times higher
during the scoreless period of the match, with only one minute where higher stakes were
placed on VfB Stuttgart.

### 视觉备注

- The prose describes Dortmund as red; Figure 2 on the following page labels Dortmund black. Both source descriptions are preserved.

## Page 08: Figure 2 and 3 Do bookmakers anticipate goals?

源页：第 8 页

### 页面目的

- Display example-market paths and introduce bookmaker models.

### 布局地图

- Dual-axis Figure 2 and its right-side legends above Section 3, introductory paragraph and Section 3.1; footer 8.

### 按区域确认内容

#### 区域 1：Figure 2双纵轴折线图

- Horizontal axis: Minute; ticks: 0, 20, 40, 60, 80. Left axis: Implied probability; right axis: Relative stakes; both axes have labels 0.25, 0.50, 0.75.
- Team legend: Borussia Dortmund (black), VfB Stuttgart (red). Line Type legend: Implied probability (solid), Relative stakes (dotted). The gray hatched region is the half time break.

Figure 2: Implied probabilities (solid lines) and relative stakes (dotted lines) in the 2018/19
German Bundesliga match between Borussia Dortmund (black lines) and VfB Stuttgart (red
lines) for the time period until the opening goal was scored by Dortmund. The gray hatched
area corresponds to the half time break.

#### 区域 2：Section 3与3.1正文

3 Do bookmakers anticipate goals?

This section examines whether bookmakers anticipate goals and adjust their odds accord-
ingly. If bookmakers do anticipate goals, we would observe higher implied probabilities and,
consequently, lower odds for the team that eventually scores the opening goal. Initially, we
introduce basic model formulations that account for in-match dynamics. Finally, we explicitly
analyse whether bookmakers anticipate goals and adjust the implied winning probabilities and
odds.

3.1 Basic model formulations

To understand how bookmakers’ odds evolve during a match, we formulate linear regression
models to explain in-match implied win probabilities improb<sub>it</sub> at minute t for the team scoring

### 视觉备注

- The Figure 2 caption and team legend use Dortmund black and Stuttgart red, contradicting the preceding prose; the plotted colors are not silently exchanged.

## Page 09: Basic model formulations: Models 1 and 2

源页：第 9 页

### 页面目的

- Specify the first two bookmaker regressions.

### 布局地图

- Prose surrounds two centered, numbered equations; red-card and expected-goal covariates introduced below; footer 9.

### 按区域确认内容

#### 区域 1：原文正文与公式

the first goal in match i by covariates. For the first model, we only consider the pre-match
implied probabilities improbpre<sub>t</sub> and propose the following formulation for the predictor of
the first linear regression model (Model 1):

ν<sub>it</sub> = β<sub>0</sub> + β<sub>1</sub> · improbpre<sub>t</sub> (1)

with E(improb<sub>it</sub>) = ν<sub>it</sub>. Considering multiple observations for each match, we cluster standard
errors at the match level to ensure correct p-values (Zeileis, 2004; Robitzsch and Grund, 2022).

The left column of Table 2 presents the estimated coefficients and standard errors for the
first model. We find a strong and statistically significant relationship between pre-match and
in-match implied probabilities. However, on average, implied probabilities for the team scoring
the first goal, before the goal occurs, are lower within the match than they are pre-match, as
β̂<sub>0</sub> + β̂<sub>1</sub> < 1.

While pre-match probabilities comprehensively determine in-match implied probabilities
at the start of a match, the probability of any team winning decreases (and the likelihood
of a draw increases) as the match proceeds scoreless (see the example match in Figure 2).
Consequently, we incorporate the minutes elapsed t of match i into the linear predictor. Given
that this effect is expected to be stronger later in the match, we also include a quadratic
effect of t. Furthermore, as observed in Figure 2, there is a stronger adjustment in implied
probabilities during the match when pre-match implied probabilities are larger. Therefore, we
include an interaction term between t and improbpre<sub>t</sub>. This leads to the following formulation
for Model 2:

ν<sub>it</sub> = β<sub>0</sub> + β<sub>1</sub> · improbpre<sub>i</sub> + β<sub>2</sub> · t<sub>it</sub> + β<sub>3</sub> · t<sub>it</sub><sup>2</sup> + β<sub>4</sub> · improbpre<sub>i</sub> · t<sub>it</sub> (2)

In addition to the time elapsed, we expect major in-match events to influence the match
outcome and, consequently, implied probabilities. Therefore, we include whether the team
under consideration (and its opponent, respectively) has received a red card. Furthermore,
we account for in-match dynamics by considering the difference in expected goals between the
opponents, divided by the current minute xgdiff<sub>it</sub>/t<sub>it</sub>. By dividing by the minute, we ensure
that the value of the covariate can increase or decrease over time. Positive values correspond

### 视觉备注

- Model 1 uses improbpre_t, while Model 2 uses improbpre_i; original indices are retained rather than harmonized.

## Page 10: Model 3 and 3.2 Anticipation of goals

源页：第 10 页

### 页面目的

- Specify in-match dynamics and the anticipation test.

### 布局地图

- Two-line centered Model 3 above model results; Section 3.2 and anticipation-covariate paragraph below; footer 10.

### 按区域确认内容

#### 区域 1：原文正文与公式

to situations where the team that eventually scores the first goal has had better goal-scoring
opportunities. This leads to the formulation of Model 3:

ν<sub>it</sub> = β<sub>0</sub> + β<sub>1</sub> · improbpre<sub>i</sub> + β<sub>2</sub> · t<sub>it</sub> + β<sub>3</sub> · t<sub>it</sub><sup>2</sup> + β<sub>4</sub> · improbpre<sub>i</sub> · t<sub>it</sub> + β<sub>5</sub> · redcardteam<sub>it</sub> + β<sub>6</sub> · redcardopp<sub>it</sub> + β<sub>7</sub> · xgdiff<sub>it</sub>/t<sub>it</sub> (3)

The second and third columns of Table 2 present results for the models that include in-
match dynamics. All covariates have a statistically significant impact on the implied winning
probability. Additionally, the Akaike Information Criterion (AIC) favours the most complex
model (Model 3). In the initial minutes, in-match implied probabilities are almost entirely
determined by the pre-match implied probabilities. However, as a scoreless match progresses,
implied probabilities decrease, with the development depending on the pre-match implied
probabilities, as indicated by the interaction term. This aligns with the prior expectation
that draws become more likely the longer the score remains 0:0. Only for very small pre-
match implied probabilities, we find in-match implied probabilities, on average, to increase
very slightly for the first minutes of matches before they decrease again. Receiving a red card
decreases implied winning probabilities by about 12 percentage points. In contrast, a red card
of the opponent increases implied probabilities by approximately 17 percentage points. This
difference occurs due to our perspective of the team that eventually takes the lead. If a team
demonstrates higher expected goals per minute, this also increases the implied probability for
this team, highlighting that bookmakers account for in-match dynamics.

3.2 Anticipation of goals

The descriptive analysis indicates that the average difference in expected goals is slightly
greater than zero just before the first goal occurs. This suggests that teams scoring the first
goal have more opportunities to score before the initial goal. Simultaneously, bookmakers
adjust their odds based on expected goals. This raises the question of whether bookmakers
respond to in-match dynamics beyond the observable measure of expected goals. To inves-
tigate this, we extend Model 3 by including the covariate 1/mintogoal<sub>it</sub>. The value of this
covariate increases before the first goal and reaches 1 in the minute before the goal occurs.

### 视觉备注

- The displayed quadratic time term is t_it squared; reciprocal mintogoal is introduced as a covariate, not as an observed pre-goal signal.

## Page 11: Table 2 and Model 4

源页：第 11 页

### 页面目的

- Report basic bookmaker estimates and specify anticipation.

### 布局地图

- Three-model table at the top, then the three-line Model 4 and a results paragraph; footer 11.

### 按区域确认内容

#### 区域 1：Table 2

Table 2: Estimated coefficients and 95%-confidence intervals for the basic linear regression model on bookmakers and models (Model 1- 3).

Response variable: Implied probability in-match.

|  | Model 1 | Model 2 | Model 3 |
| --- | --- | --- | --- |
| Implied probability pre-match | 0.885 | 1.016 | 1.003 |
|  | [0.856, 0.914] | [0.995, 1.038] | [0.990, 1.016] |
| Minute |  | 0.002 | 0.001 |
|  |  | [0.001, 0.002] | [0.001, 0.002] |
| Minute<sup>2</sup> |  | -0.000011 | -0.000013 |
|  |  | [-0.000018, -0.000004] | [-0.000018, -0.000008] |
| Implied probability pre-match · Minute |  | -0.004 | -0.004 |
|  |  | [-0.005, -0.003] | [-0.005, -0.003] |
| Red card team |  |  | -0.120 |
|  |  |  | [-0.124, -0.116] |
| Red card opponent |  |  | 0.173 |
|  |  |  | [0.136, 0.210] |
| xgdiff per minute |  |  | 0.163 |
|  |  |  | [0.075, 0.250] |
| Constant | 0.022 | -0.010 | -0.004 |
|  | [0.009, 0.035] | [-0.022, 0.003] | [-0.011, 0.004] |
| Observations | 9,425 | 9,425 | 9,425 |
| Akaike Inf. Crit. | -28,320 | -35,000 | -42,160 |

#### 区域 2：Model 4与原文结果

Model 4 is formulated as follows:

ν<sub>it</sub> = β<sub>0</sub> + β<sub>1</sub> · improbpre<sub>i</sub> + β<sub>2</sub> · t<sub>it</sub> + β<sub>3</sub> · t<sub>it</sub><sup>2</sup> + β<sub>4</sub> · improbpre<sub>i</sub> · t<sub>it</sub> + β<sub>5</sub> · redcardteam<sub>it</sub> + β<sub>6</sub> · redcardopp<sub>it</sub> + β<sub>7</sub> · xgdiff<sub>it</sub>/t<sub>it</sub> + β<sub>8</sub> · mintogoal<sub>it</sub><sup>−1</sup> (4)

In the results (see Table 3), we find that the parameter estimates are virtually unchanged from
Model 3. We observe a statistically insignificant effect for the remaining minutes until the
goal is scored. This indicates that bookmakers do not anticipate goals beyond the observable
expected goals and do not adjust their odds accordingly. This result remains robust even
when the expected goals covariate is excluded. In summary, this section demonstrates that
bookmakers adjust their implied outcome probabilities based on pre-match team strength and
in-match information. However, they do not anticipate goals by adjusting probabilities before
they occur. This potentially allows bettors to generate positive returns if they can anticipate
goals. Whether bettors actually do anticipate goals is the subject of the next section.

### 视觉备注

- All three table columns print 9,425 observations, whereas page 5 states 9,245 minutes; the source discrepancy is preserved.

## Page 12: Table 3 and 4 Do bettors anticipate goals?

源页：第 12 页

### 页面目的

- Report the bookmaker anticipation coefficient and start bettor modelling.

### 布局地图

- One-model table above Section 4 and Section 4.1; the last paragraph continues onto page 13; footer 12.

### 按区域确认内容

#### 区域 1：Table 3

Table 3: Estimated coefficients and 95%-confidence intervals for the linear regression models on bookmakers including remaining minutes to goal (Model 4).

Response variable: Implied probability in-match.

|  | Model 4 |
| --- | --- |
| Implied probability pre-match | 1.003 |
|  | [0.990, 1.016] |
| Minute | 0.001 |
|  | [0.001, 0.002] |
| Minute<sup>2</sup> | -0.000013 |
|  | [-0.000018, -0.000008] |
| Implied probability pre-match · Minute | -0.004 |
|  | [-0.005, -0.003] |
| Red card team | -0.120 |
|  | [-0.124, -0.116] |
| Red card opponent | 0.173 |
|  | [0.136, 0.209] |
| xgdiff per minute | 0.165 |
|  | [0.077, 0.253] |
| mintogoal<sup>−1</sup> | -0.005 |
|  | [-0.012, 0.002] |
| Constant | -0.003 |
|  | [-0.010, 0.004] |
| Observations | 9,425 |
| Akaike Inf. Crit. | -42,180 |

#### 区域 2：Section 4与4.1原文

4 Do bettors anticipate goals?

We now turn to the perspective of bettors placing stakes. To account for the highly dynamic
betting market with serial correlation in the underlying activity level, we incorporate a latent
variable capturing the current level of market activity. Initially, we aim to explain the relative
stakes placed on the team scoring the first goal by the same covariates as those used for the
bookmaker’s implied probabilities. Finally, based on the suggestions of previous literature
and our descriptive findings on bettors’ behaviour, we additionally include the home and
volumediff covariates to this model to enhance its explanatory power.

4.1 Model formulation

We consider the target variable y<sub>t</sub>, representing the relative stakes placed on the team scoring
the first goal in a match. As no bets can be placed when the market is closed (e.g. directly after
a red card or after a penalty decision), we exclude those 60 observations from the analysis,

### 视觉备注

- Table 3 has opponent red-card upper CI 0.209, unlike Table 2’s 0.210; no rounding harmonization is applied.

## Page 13: 4.1 Model formulation: BEINF and latent states

源页：第 13 页

### 页面目的

- Define the response distribution and state process.

### 布局地图

- Opening sample-size continuation, zero-one-inflated beta density, precision expression, prose and AR(1) equation; footer 13.

### 按区域确认内容

#### 区域 1：原文正文与公式

reducing the total observations to 9,185 minutes. In the extreme case, all stakes placed during
a given period are on one team. The target variable, hence, can take values between 0 and
1. Given this support of the variable, we apply a zero-one-inflated beta distribution (Ospina
and Ferrari, 2012; Rigby et al., 2019):

y<sub>t</sub> ∼ BEINF(μ<sub>t</sub>, σ, π, λ).


| Condition | f(y<sub>t</sub>) |
| --- | --- |
| y<sub>t</sub> = 0 | π |
| y<sub>t</sub> ∈ (0, 1) | (1 − π − λ) · h(y<sub>t</sub>) |
| y<sub>t</sub> = 1 | λ |

where h(y<sub>t</sub>) corresponds to the density function of a standard beta distribution. This model

formulation aligns with previous work by Michels et al. (2023) for modelling relative stakes

in betting markets. We parametrise the distribution in terms of its mean µ and a precision

parameter γ = μ(1−μ)/σ<sup>2</sup> − 1. We model  the  mean  dependent  on  covariates  and  apply  the  inverse

logit link function to the linear predictor: μ<sub>it</sub> = logit<sup>−1</sup>(η<sub>it</sub>).

Previous literature on finance and betting markets indicates the existence of an underlying

(unobserved) market activity level that reflects the market’s nervousness. Consequently, we

include a latent state variable that captures market activity and model serial correlation in

the state using an AR(1) process. Assuming a finite number of distinct states with clear

interpretations, such as low and high levels of market activity, would lack the necessary

flexibility to adequately model financial time series and capture gradual changes. Instead, we

employ continuous-valued state-space models (SSMs) in discrete time, aligning with previous

literature on stochastic volatility models for share returns (Langrock et al., 2012; Barra et al.,
2017) and particularly stakes in betting markets (Michels et al., 2023; Ötting et al., 2024).

We consider the relative stakes placed on the team scoring the first goal in match i at

minute t, denoted y<sub>it</sub>, as the state-dependent observation process {y<sub>it</sub>}. This process is as-

sumed to be driven by an underlying state process {s<sub>it</sub>}. For simplicity, we will omit the

match index i in the following. The state process can be described as

s<sub>t</sub> = ϕs<sub>t−1</sub> + σ<sub>s</sub>ϵ<sub>t</sub>

### 视觉备注

- The endpoint mass is π at zero and λ at one. The later prose’s all-team/all-opponent descriptions are retained even if their interpretation appears reversed.

## Page 14: Figure 3 and 4.2 Results

源页：第 14 页

### 页面目的

- Define stationary initialization and present initial SSM results.

### 布局地图

- Stationary normal and predictor in upper paragraph; three-row dependency diagram; Section 4.2 results below; footer 14.

### 按区域确认内容

#### 区域 1：原文正文与公式

with |ϕ| as the persistence parameter, and σ<sub>s</sub> > 0 and ϵ<sub>t</sub> ∼ N(0, 1) specify the distribution of

the error term. We assume the initial state s<sub>1</sub> to be generated by the stationary distribution

of the state process: δ ∼ N(0, √[σ<sub>s</sub><sup>2</sup>/(1−ϕ<sup>2</sup>)]). The state active at observation t determines the

current state-dependent distribution. The linear predictor for the mean of the observation

process in the SSM η<sub>t</sub> is extended by the state variable: η<sub>t</sub> = ν<sub>t</sub> + s<sub>t</sub>. The dependence

structure of the SSM is illustrated in Figure 3 (see Appendix C for technical details on the

implementation).

#### 区域 2：Figure 3依赖结构

- State chain: … → s<sub>t−1</sub> → s<sub>t</sub> → s<sub>t+1</sub> → … .
- At each of t−1, t, t+1: covariate x points downward to response y; state s points upward to response y. No arrow joins successive responses or covariates.

Figure 3: Dependence structure of the SSM with latent state s<sub>t</sub>, covariates x<sub>t</sub> and response
variable y<sub>t</sub>.

4.2 Results

Table 4 presents the estimated coefficients along with their confidence intervals. Firstly, we
consider the same covariates as in the final bookmaker’s model in Section 3.2, but extended
by the state process. Parameter estimates for this SSM are provided in the left column of
Table 4. Results for the state process, with ϕˆ close to 1, indicate strong serial correlation in
the underlying market activity level. Indeed, the AIC clearly favours this model over a model
without state process (∆AIC = 9, 355; see Appendix D for a model without state process).

Estimates for the state-dependent covariates confirm descriptive findings that bettors tend
to place higher (relative) stakes on favourites with higher (pre-match) implied winning prob-
abilities, as implied by the bookmaker’s odds. Simultaneously, the results suggest that the
distribution of relative stakes between both teams does not depend on the minute (neither in
the linear form nor the quadratic and interaction terms). While the effect of a red card for
the team scoring the goal is negative but insignificant, relative stakes significantly increase

### 视觉备注

- The original normal distribution prints a square root in its second argument, representing a standard deviation; it is not silently rendered as variance.

## Page 15: Final SSM and 5 Discussion

源页：第 15 页

### 页面目的

- Specify the final bettor model and open discussion.

### 布局地图

- Continuation and estimated distribution parameters above two-line Equation 5, results paragraph and bold Section 5; footer 15.

### 按区域确认内容

#### 区域 1：原文正文与公式

when the opponent receives a red card. This also applies to teams showing a comparative
advantage during the match, as indicated by the difference in expected goals per minute.
Regarding the potential anticipation of goals by bettors, the model does not provide evidence
for adjusted behaviour of bettors before the first goal. The estimated coefficients πˆ = 0.00096
and λˆ = 0.00053 are close to the empirical probabilities that all stakes are placed on the team
(and the opponent, respectively) in a given minute. The precision parameter is estimated as
γˆ = 16.065.

Following the descriptive analysis on bettors’ tendency to place higher stakes on home
teams and those with higher sentiment, we additionally include the corresponding covariates
in the final model. Simultaneously, the time-dependent covariates appear insignificant in the
basic model. Therefore, we exclude the additional covariates (quadratic effect and interaction
term) from the final model formulation (for the full model including all covariates, see Table 8
in the Appendix). The linear predictor for the final model is given as follows:

ν<sub>it</sub> = β<sub>0</sub> + β<sub>1</sub> · improbpre<sub>i</sub> + β<sub>2</sub> · t<sub>it</sub> + β<sub>3</sub> · redcardteam<sub>it</sub> + β<sub>4</sub> · redcardopp<sub>it</sub> + β<sub>5</sub> · home<sub>t</sub> + β<sub>6</sub> · volumediff<sub>t</sub> + β<sub>7</sub> · xgdiff<sub>it</sub>/t<sub>it</sub> + β<sub>8</sub> · mintogoal<sub>it</sub><sup>−1</sup>. (5)

Results in the right column of Table 4 confirm the high serial correlation in the market
activity level. In this final model, the effect of red cards for both teams is significant. The
findings corroborate bettors’ tendency to place higher relative stakes on teams with higher
sentiment. However, higher relative stakes on the home teams are not verified, given that we
control for pre-match implied probabilities and the difference in the average betting volume
between both teams. Again, there is no evidence for anticipation observed in bettors’ be-
haviour. While applying various models throughout this section, the findings on the potential
anticipation of goals are robust: relative stakes placed on the team eventually scoring the goal
do not increase prior to its occurrence.

5 Discussion

In this paper, we explore whether market participants anticipate the first goal of a match
by adjusting odds and stakes toward the team eventually scoring the goal. Although major
events, such as red cards and in-match dynamics reflected by expected goals, significantly

### 视觉备注

- Equation 5 uses home_t and volumediff_t, not match-indexed it. Estimated π=0.00096, λ=0.00053 and γ=16.065 are preserved.

## Page 16: Table 4 and Discussion (continued)

源页：第 16 页

### 页面目的

- Report basic and final SSM estimates and continue discussion.

### 布局地图

- Two-model table fills the upper portion; discussion continuation below; footer 16.

### 按区域确认内容

#### 区域 1：顶部Table 4

Table 4: Estimated coefficients and 95%-confidence intervals for the state-space models (SSMs) with beta distribution for bettors.

Response variable: Relative stakes team.

|  | Basic SSM | Final SSM |
| --- | --- | --- |
| ϕ | 0.984 | 0.974 |
|  | [0.981 0.987] | [0.972, 0.977] |
| σ<sub>s</sub> | 0.176 | 0.183 |
|  | [0.165 0.188] | [0.176, 0.190] |
| Implied probability pre-match | 4.520 | 1.753 |
|  | [3.990, 5.051] | [1.648, 1.859] |
| Minute | 0.002 | 0.000 |
|  | [-0.007, 0.011] | [-0.002, 0.003] |
| Minute<sup>2</sup> | 0.00001 |  |
|  | [-0.00006, 0.00009] |  |
| Implied probability pre-match · Minute | -0.004 |  |
|  | [-0.020, 0.013] |  |
| Red card team | -0.630 | -0.767 |
|  | [-1.499, 0.240] | [-1.346, -0.188] |
| Red card opponent | 0.661 | 0.681 |
|  | [0.389, 0.932] | [0.215, 1.147] |
| xgdiff per minute | 3.497 | 3.627 |
|  | [3.118, 3.875] | [3.552, 3.702] |
| home |  | -0.005 |
|  |  | [-0.185, 0.175] |
| volumediff |  | 0.047 |
|  |  | [0.042, 0.051] |
| mintogoal<sup>−1</sup> | 0.089 | 0.096 |
|  | [-0.159, 0.336] | [-0.031, 0.222] |
| Constant | -1.785 | -0.762 |
|  | [-2.058, -1.513] | [-0.969, -0.555] |
| Observations | 9,185 | 9,185 |
| Akaike Inf. Crit. | -14,581.68 | -14,715.64 |

#### 区域 2：表后Discussion续文

impact the behaviour of both sides of the market, our findings reveal that neither odds nor
stakes show significant adjustments right before the first goal. Thus, we can conclude that
neither bookmakers nor bettors anticipate the first goal of a match.

The results add important knowledge for financial markets and betting markets in par-
ticular. They demonstrate that neither professional bookmakers nor (predominantly non-
professional) bettors can anticipate the occurrence of major news. In comparison to financial
markets, football betting benefits from the absence of insider trading. Apart from match-
fixing (Ötting et al., 2018), which was not detected in the season considered in this paper,
both market sides adjust their actions in response to processing the information available.
Hence, our findings can clearly differentiate between insider trading and market anticipation,

### 视觉备注

- Basic SSM 0.089 is the mintogoal reciprocal coefficient, not volumediff. Blank Basic home/volume cells and comma-free CIs for ϕ/σ_s are preserved.

## Page 17: Discussion (continued)

源页：第 17 页

### 页面目的

- Discuss implications, league limitations and match-fixing extensions.

### 布局地图

- Two justified paragraphs without repeated heading, beginning mid-sentence; footer 17.

### 按区域确认内容

#### 区域 1：原文正文与参考文献

a distinction that is challenging in financial markets (Jain and Sunderman, 2014; Tunyi, 2021).
Bookmaker odds are rigid as we do not observe adjustments beyond expected goals and red
cards. Conversely, (relative) stakes placed by bettors are much more volatile. Yet, we identify
an underlying latent variable capturing the level of market activity to exhibit strong serial
correlation. Arbitrage would occur if bettors were able to predict goals; however, our results
indicate that bettors do not anticipate goals by increasing stakes on the teams scoring the
first goal. This suggests that bookmakers do not face negative consequences from failing to
anticipate goals.

While the setting of the German Bundesliga appears advantageous, there is also a draw-
back. The high level of information availability could potentially reduce market inefficiencies.
Elaad et al. (2020) show that bookmaker margins are smaller for higher leagues. This is
potentially driven by stronger competition among bookmakers in higher tiers or increased
market transparency due to greater media coverage. Following the argument that less infor-
mation is available for smaller leagues, implicit knowledge of bettors could be more valuable,
possibly leading to a stronger anticipation effect of goals by fans. Additionally, our findings
form the basis for further investigations into in-match betting. The risk of match-fixing has
been a subject of interest in the literature for several years (Ötting et al., 2018; Forrest and
McHale, 2019). As our results indicate no significant adjustments towards the team eventually
scoring the first goal, observing such anticipatory behaviour and a significant change in stakes
placed on the team could potentially signal fraudulent activity. However, to analyse whether
our model could correctly identify fixed matches, we would need to extend our analysis to
matches where fixing was proven. Furthermore, absolute stakes should also be considered in
such an analysis.

### 视觉备注

- The page ends with the need to consider absolute stakes in match-fixing analysis; no figure or footnote accompanies the discussion.

## Page 18: References

源页：第 18 页

### 页面目的

- List references from Al-Anaswah to Dahal.

### 布局地图

- References heading followed by ten hanging-indent entries, italic publication titles and footer 18.

### 按区域确认内容

#### 区域 1：原文正文与参考文献

References

Al-Anaswah, N. and Wilfling, B. (2011). Identification of speculative bubbles using state-space
models with Markov-switching. Journal of Banking & Finance, 35(5):1073–1086.

Barra, I., Hoogerheide, L., Koopman, S. J., and Lucas, A. (2017). Joint Bayesian analysis of
parameters and states in nonlinear non-Gaussian state space models. Journal of Applied
Econometrics, 32(5):1003–1026.

Ben-Rephael, A., Da, Z., and Israelsen, R. D. (2017). It depends on where you search:
institutional investor attention and underreaction to news. Review of Financial Studies,
30(9):3009–3047.

Buhagiar, R., Cortis, D., and Newall, P. W. (2018). Why do some soccer bettors lose more
money than others? Journal of Behavioral and Experimental Finance, 18:85–93.

Che, X., Feddersen, A., and Humphreys, B. R. (2017). Price setting and competition in fixed
odds betting markets. In The Economics of Sports Betting, pages 38–51. Edward Elgar
Publishing.

Choi, D. and Hui, S. K. (2014). The role of surprise: understanding overreaction and under-
reaction to unanticipated events using in-play soccer betting market. Journal of Economic
Behavior & Organization, 107:614–629.

Chua, C. L. and Tsiaplias, S. (2019). Information flows and stock market volatility. Journal
of Applied Econometrics, 34(1):129–148.

Clarke, J., Chen, H., Du, D., and Hu, Y. J. (2019). Fake news, investor attention, and market
reaction. PSN: Political Communication (Topic).

Croxson, K. and Reade, J. J. (2014). Information and efficiency: goal arrival in soccer betting.
The Economic Journal, 124(575):62–91.

Dahal, K., Pokhrel, N. R., Gaire, S., Mahatara, S., Joshi, R. P., Gupta, A., Banjade, H., and
Joshi, J. (2023). A comparative study on effect of news sentiment on stock price prediction
with deep learning architecture. PLOS ONE, 18(4):e0284695.

### 视觉备注

- The first entry is Al-Anaswah and Wilfling (2011); the final Dahal et al. entry ends with PLOS ONE 18(4):e0284695.

## Page 19: References (continued)

源页：第 19 页

### 页面目的

- List references from Deutscher to Lago-Peñas.

### 布局地图

- Twelve hanging-indent entries without a repeated heading; footer 19.

### 按区域确认内容

#### 区域 1：原文正文与参考文献

Deutscher, C., Frick, B., and Ötting, M. (2018). Betting market inefficiencies are short-lived
in German professional football. Applied Economics, 50(30):3240–3246.

Elaad, G., Reade, J. J., and Singleton, C. (2020). Information, prices and efficiency in an
online betting market. Finance Research Letters, 35:101291.

Feddersen, A., Humphreys, B. R., and Soebbing, B. P. (2017). Sentiment bias and asset prices:
evidence from sports betting markets and social media. Economic Inquiry, 55(2):1119–1129.

Forrest, D. and McHale, I. G. (2019). Using statistics to detect match fixing in sport. IMA
Journal of Management Mathematics, 30(4):431–449.

Gil, R. G. R. and Levitt, S. D. (2007). Testing the efficiency of markets in the 2002 World
Cup. The Journal of Prediction Markets, 1(3):255–270.

Haroon, O. and Rizvi, S. A. R. (2020). COVID-19: Media coverage and financial markets
behavior – a sectoral inquiry. Journal of Behavioral and Experimental Finance, 27:100343.

Heston, S. L. and Sinha, N. R. (2017). News vs. sentiment: predicting stock returns from
news stories. Financial Analysts Journal, 73(3):67–83.

Jacquier, E., Polson, N. G., and Rossi, P. E. (2002). Bayesian analysis of stochastic volatility
models. Journal of Business & Economic Statistics, 20(1):69–87.

Jain, P. and Sunderman, M. (2014). Stock price movement around the merger announcements:
insider trading or market anticipation? Managerial Finance, 40(8):821–843.

Jarrell, G. A. and Poulsen, A. B. (1989). Stock trading before the announcement of tender
offers: insider trading or market anticipation? The Journal of Law, Economics, and
Organization, 5(2):225–248.

Kitagawa, G. (1987). Non-Gaussian state-space modeling of nonstationary time series. Journal
of the American Statistical Association, 82(400):1032–1041.

Lago-Peñas, C., Gómez-Ruano, M., Megías-Navarro, D., and Pollard, R. (2016). Home ad-
vantage in football: examining the effect of scoring first on match outcome in the five major
European leagues. International Journal of Performance Analysis in Sport, 16(2):411–421.

### 视觉备注

- Ötting, Lago-Peñas, Gómez-Ruano and Megías-Navarro diacritics have been restored from separated text-layer accents against this page.

## Page 20: References (continued)

源页：第 20 页

### 页面目的

- List references from Langrock to Rigby.

### 布局地图

- Ten hanging-indent references, italic publication titles and centered footer 20.

### 按区域确认内容

#### 区域 1：原文正文与参考文献

Langrock, R. and King, R. (2013). Maximum likelihood estimation of mark-recapture-recovery
models in the presence of continuous covariates. The Annals of Applied Statistics, 7(3):1709–
1732.

Langrock, R., MacDonald, I. L., and Zucchini, W. (2012). Some nonstandard stochastic
volatility models and their estimation using structured hidden Markov models. Journal of
Empirical Finance, 19(1):147–161.

Mews, S., Langrock, R., Ötting, M., Yaqine, H., and Reinecke, J. (2024). Maximum ap-
proximate likelihood estimation of general continuous-time state-space models. Statistical
Modelling, 24(1):9–28.

Michels, R., Ötting, M., and Langrock, R. (2023). Bettors’ reaction to match dynamics:
evidence from in-game betting. European Journal of Operational Research, 310(3):1118–
1127.

Miller Jr, T. W. and Rapach, D. E. (2013). An intra-week efficiency analysis of bookie-quoted
NFL betting lines in NYC. Journal of Empirical Finance, 24:10–23.

Na, S., Su, Y., and Kunkel, T. (2019). Do not bet on your favourite football team: the
influence of fan identity-based biases and sport context knowledge on game prediction
accuracy. European Sport Management Quarterly, 19(3):396–418.

Ospina, R. and Ferrari, S. L. (2012). A general class of zero-or-one inflated beta regression
models. Computational Statistics & Data Analysis, 56(6):1609–1623.

Ötting, M., Langrock, R., and Deutscher, C. (2018). Integrating multiple data sources in
match-fixing warning systems. Statistical Modelling, 18(5-6):483–504.

Ötting, M., Michels, R., Langrock, R., and Deutscher, C. (2024). Demand for live betting:
an analysis using state-space models. Applied Stochastic Models in Business and Industry,
40(2):527–541.

Rigby, R. A., Stasinopoulos, M. D., Heller, G. Z., and De Bastiani, F. (2019). Distributions
for Modeling Location, Scale, and Shape: Using GAMLSS in R. Chapman and Hall/CRC.

### 视觉备注

- Langrock and King’s reference wraps its page range 1709–1732; Rigby et al. closes the page with Chapman and Hall/CRC.

## Page 21: References (continued)

源页：第 21 页

### 页面目的

- Complete the bibliography from Robitzsch to Zucchini.

### 布局地图

- Nine hanging-indent entries without a repeated heading; centered footer 21.

### 按区域确认内容

#### 区域 1：原文参考文献与公式

Robitzsch, A. and Grund, S. (2022). miceadds: some additional multiple imputation functions,
especially for ’mice’. R package version 3.13-12.

Sauer, R. D. (1998). The economics of wagering markets. Journal of Economic Literature,
36(4):2021–2064.

Staněk, R. (2017). Home bias in sport betting: evidence from Czech betting market. Judgment
and Decision Making, 12(2):168–172.

Thaler, R. H. and Ziemba, W. T. (1988). Anomalies: parimutuel betting markets: racetracks
and lotteries. Journal of Economic Perspectives, 2(2):161–174.

Tunyi, A. A. (2021). Revisiting acquirer returns: evidence from unanticipated deals. Journal
of Corporate Finance, 66:101789.

Winkelmann, D., Deutscher, C., and Ötting, M. (2021). Bookmakers’ mispricing of the
disappeared home advantage in the German Bundesliga after the COVID-19 break. Applied
Economics, 53(26):3054–3064.

Winkelmann, D., Ötting, M., Deutscher, C., and Makarewicz, T. (2024). Are betting mar-
kets inefficient? Evidence from simulations and real data. Journal of Sports Economics,
25(1):54–97.

Zeileis, A. (2004). Econometric computing with HC and HAC covariance matrix estimators.
Journal of Statistical Software, 11(10):1–17.

Zucchini, W., MacDonald, I. L., and Langrock, R. (2017). Hidden Markov Models for Time
Series: An Introduction Using R. Chapman and Hall/CRC, New York.

### 视觉备注

- Staněk’s caron and Ötting’s umlaut are confirmed on this page; the R package version 3.13-12 is bibliographic content, not a runtime requirement.

## Page 22: Appendix A: Average absolute stakes

源页：第 22 页

### 页面目的

- Report scaled average stakes for all 18 Bundesliga teams.

### 布局地图

- Appendix and Section A headings above caption and a two-column descending table; footer 22.

### 按区域确认内容

#### 区域 1：Appendix A与Table 5

Appendix

A Average absolute stakes per minute placed on teams

Table 5: Average absolute stakes per minute placed on the 18 German Bundesliga teams in the 2018/19 season for all matches during the time period with a score of 0:0. Note that all actual stakes are transformed by the same fixed constant, since we are not allowed to provide any information on the actual money placed.

| Team | Average stakes per minute |
| --- | --- |
| Borussia Dortmund | 55.70 |
| Borussia M’gladbach | 36.80 |
| Eintracht Frankfurt | 34.68 |
| Bayern München | 32.99 |
| RB Leipzig | 27.55 |
| Schalke 04 | 25.51 |
| Bayer Leverkusen | 25.50 |
| 1899 Hoffenheim | 23.20 |
| Werder Bremen | 20.88 |
| Hertha BSC | 17.26 |
| VfL Wolfsburg | 16.51 |
| VfB Stuttgart | 12.57 |
| FSV Mainz 05 | 11.23 |
| FC Augsburg | 10.25 |
| SC Freiburg | 9.84 |
| Hannover 96 | 9.05 |
| Fortuna Düsseldorf | 8.98 |
| 1. FC Nürnberg | 8.93 |

### 视觉备注

- The figures are transformed by a common fixed constant and are not actual disclosed currency amounts; Munich/Düsseldorf/Nürnberg umlauts are restored.

## Page 23: Appendix B: Correlation coefficients

源页：第 23 页

### 页面目的

- Present the complete key-variable correlation matrix.

### 布局地图

- Landscape-oriented table rotated within a portrait source page; ten variable columns and ten data rows; folio 23.

### 按区域确认内容

#### 区域 1：旋转Table 6

B Correlation coefficients between key variables

Table 6: Correlation coefficients between the key variables in the dataset.

|  | t | mintogoal | improb | improbpre | redcardteam | redcardopp | xgdiff | home | volumediff | stakerel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nrinterval | 1 | −0.239 | −0.157 | 0.031 | −0.017 | 0.168 | 0.214 | 0.046 | 0.056 | 0.058 |
| mintogoal | −0.239 | 1 | 0.086 | 0.031 | −0.028 | −0.036 | −0.077 | 0.046 | 0.056 | 0.028 |
| improb | −0.157 | 0.086 | 1 | 0.951 | −0.119 | 0.125 | 0.270 | 0.325 | 0.656 | 0.599 |
| improbpre | 0.031 | 0.031 | 0.951 | 1 | −0.081 | 0.006 | 0.307 | 0.334 | 0.704 | 0.619 |
| redcardteam | −0.017 | −0.028 | −0.119 | −0.081 | 1 | −0.010 | −0.042 | −0.072 | −0.026 | −0.089 |
| redcardopp | 0.168 | −0.036 | 0.125 | 0.006 | −0.010 | 1 | 0.048 | 0.101 | −0.029 | 0.054 |
| xgdiff | 0.214 | −0.077 | 0.270 | 0.307 | −0.042 | 0.048 | 1 | 0.120 | 0.265 | 0.328 |
| home | 0.046 | 0.046 | 0.325 | 0.334 | −0.072 | 0.101 | 0.120 | 1 | 0.011 | 0.081 |
| volumediff | 0.056 | 0.056 | 0.656 | 0.704 | −0.026 | −0.029 | 0.265 | 0.011 | 1 | 0.686 |
| stakerel | 0.058 | 0.028 | 0.599 | 0.619 | −0.089 | 0.054 | 0.328 | 0.081 | 0.686 | 1 |

### 视觉备注

- The first column heading is t but the first row label literally reads nrinterval, confirmed by a second focused visual check; this mismatch is preserved.

## Page 24: Appendix C: Technical details on the SSM implementation

源页：第 24 页

### 页面目的

- Explain maximum likelihood approximation and forward recursion.

### 布局地图

- Section C heading and prose alternating with integral, discretization sum and matrix product equations; footer 24.

### 按区域确认内容

#### 区域 1：原文参考文献与公式

C Technical details on the SSM implementation

We estimate model parameters using the maximum likelihood method. The analytical evalu-
ation of this likelihood is typically intractable, as it involves T -dimensional integrals, where
T corresponds to the number of observations. Instead, we rely on approximation methods as
introduced by Kitagawa (1987). The exact likelihood, given the model structure incorporating
the Markov property of the state process and conditional independence of observations (see
Figure 3), can be written as follows:

L<sub>T</sub>(Θ) = ∫⋯∫ f(s<sub>1</sub>)f(y<sub>1</sub>|s<sub>1</sub>) ∏<sub>t=2</sub><sup>T</sup> f(s<sub>t</sub>|s<sub>t−1</sub>)f(y<sub>t</sub>|s<sub>t</sub>) ds<sub>T</sub> … ds<sub>1</sub>. (6)

Here, Θ denotes the parameter vector. We discretise the state space by defining m intervals

B<sub>i</sub> = (b<sub>i−1</sub>, b<sub>i</sub>) with length h = (b<sub>m</sub>−b<sub>0</sub>)/m and midpoints b<sub>i</sub><sup>*</sup> = (b<sub>i</sub>−b<sub>i−1</sub>)/2. If m is chosen

sufficiently large, we can approximate the likelihood up to some decimal places as follows

(Langrock et al., 2012):


L<sub>T</sub>(Θ) ≈ h<sup>T</sup> ∑<sub>i<sub>1</sub>=1</sub><sup>m</sup> ⋯ ∑<sub>i<sub>T</sub>=1</sub><sup>m</sup> f(b<sub>i<sub>1</sub></sub><sup>*</sup>)f(y<sub>1</sub>|b<sub>i<sub>1</sub></sub><sup>*</sup>) ∏<sub>t=2</sub><sup>T</sup> f(b<sub>i<sub>t</sub></sub><sup>*</sup>|b<sub>i<sub>t−1</sub></sub><sup>*</sup>)f(y<sub>t</sub>|b<sub>i<sub>t</sub></sub><sup>*</sup>). (7)

This approximated likelihood can be calculated at computational costs of order O(Tm<sup>2</sup>) when
using the forward algorithm (Zucchini et al., 2017, Chapter 11). In fact, the likelihood reduces
to that of an m-state hidden Markov model (HMM), enabling the application of well-known
HMM tools. The transition probability matrix Γ, encompassing the probabilities of switching
from one state to another γ<sub>ij</sub> = f(s<sub>t</sub> = b<sub>j</sub><sup>*</sup>|s<sub>t−1</sub> = b<sub>i</sub><sup>*</sup>), i, j = 1, …, m is fully determined by
ϕ and σ<sub>s</sub>. The state-dependent densities f(y<sub>t</sub>|s<sub>t</sub> = b<sub>i</sub>) are provided by the m × m diagonal
matrix P(y<sub>t</sub>). We can now reformulate and recursively calculate the (approximate) likelihood
stated in Equation (7) by

L<sub>T</sub>(Θ) ≈ δP(y<sub>1</sub>)ΓP(y<sub>2</sub>) … ΓP(y<sub>T</sub>)1

with 1 = (1, …, 1)′ ∈ ℝ<sup>m</sup>.

### 视觉备注

- The source midpoint formula uses (b_i−b_(i−1))/2 rather than a sum; preserve the apparent source error. Matrix 1 is a column vector, not a scalar.

## Page 25: Appendix D: Bettors’ model without state process

源页：第 25 页

### 页面目的

- Finish implementation details and report the no-state model.

### 布局地图

- BFGS/discretization paragraph at top; bold Section D then Table 7 caption and single-estimate table; footer 25.

### 按区域确认内容

#### 区域 1：SSM实现续文

For the given longitudinal dataset, we assume independence between matches and calcu-
late the total likelihood as the product of individual likelihoods for each match. We employ
the Broyden–Fletcher–Goldfarb–Shanno (BFGS) algorithm, a quasi-Newton method for nu-
merical maximisation, to obtain parameter estimates in Python, subject to technical details
(Zucchini et al., 2017). To balance the trade-off between computation time and an accurate
discretisation of the state space, we use m = 95 intervals, which is close to the conservative
choice proposed in, for example, Langrock and King (2013); Mews et al. (2024), with bounds
−b<sub>0</sub> = b<sub>m</sub> = 3.


#### 区域 2：Appendix D与Table 7

D Bettors’ model without state process

Table 7: Estimated coefficients and 95%-confidence intervals for the beta regression model on bettors without state process.

Response variable: Relative stakes team.

|  | Estimate |
| --- | --- |
| Implied probability pre-match | 4.333 |
|  | [4.148, 4.517] |
| Minute | 0.008 |
|  | [0.005, 0.011] |
| Minute<sup>2</sup> | -0.00001 |
|  | [-0.00004, 0.00003] |
| Implied probability pre-match · Minute | -0.014 |
|  | [-0.018, -0.009] |
| Red card team | -0.591 |
|  | [-0.904, -0.277] |
| Red card opponent | 0.418 |
|  | [0.291, 0.545] |
| xgdiff per minute | 7.961 |
|  | [7.508, 8.414] |
| mintogoal<sup>−1</sup> | -0.109 |
|  | [-0.216, -0.003] |
| Constant | -1.700 |
|  | [-1.788, -1.611] |
| Observations | 9,185 |
| Akaike Inf. Crit. | -5,226.72 |

### 视觉备注

- The state discretization uses m=95 and bounds −b_0=b_m=3. No-state mintogoal coefficient is −0.109 with CI [−0.216, −0.003].

## Page 26: Appendix E: Results for the full bettors’ model

源页：第 26 页

### 页面目的

- Present the full SSM specification estimates.

### 布局地图

- Bold Section E, Table 8 caption and response-variable line above one estimate column with alternating CIs; footer 26.

### 按区域确认内容

#### 区域 1：Appendix E与Table 8

E Results for the full bettors’ model

Table 8: Estimated coefficients and 95%-confidence intervals for the state-space model (SSM) with beta distribution for bettors including all variables.

Response variable: Relative stakes team.

|  | Estimate |
| --- | --- |
| ϕ | 0.974 |
|  | [0.970, 0.978] |
| σ<sub>s</sub> | 0.183 |
|  | [0.174, 0.193] |
| Implied probability pre-match | 1.929 |
|  | [1.594, 2.263] |
| Minute | 0.004 |
|  | [-0.004, 0.012] |
| Minute<sup>2</sup> | 0.00000 |
|  | [-0.00007, 0.00008] |
| Implied probability pre−match · Minute | -0.007 |
|  | [-0.022, 0.008] |
| Red card team | -0.777 |
|  | [-1.601, 0.047] |
| Red card opponent | 0.682 |
|  | [0.310, 1.054] |
| xgdiff per minute | 3.640 |
|  | [1.641, 5.639] |
| Home | -0.009 |
|  | [-0.178, 0.161] |
| Volume | 0.047 |
|  | [0.041, 0.052] |
| mintogoal<sup>−1</sup> | 0.095 |
|  | [-0.454, 0.645] |
| Constant | -0.842 |
|  | [-1.052, -0.631] |
| Observations | 9,185 |
| Akaike Inf. Crit. | -14,712.72 |

### 视觉备注

- Home and Volume are capitalized source row labels. Minute squared is printed 0.00000, and the full-model mintogoal CI is wider than in the final reduced model.





