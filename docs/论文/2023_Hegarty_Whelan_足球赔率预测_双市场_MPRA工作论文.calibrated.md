# Forecasting Football Match Outcomes: Evidence from the 1X2 and Asian Handicap Betting Markets

> 重建说明：模式 transcribe；来源 `2023_Hegarty_Whelan_足球赔率预测_双市场_MPRA工作论文.pdf`；共 31 页；原图逐页查看 31/31 页。
> 核图证据：对照 `.ky-md-work/2023_Hegarty_Whelan_足球赔率预测_双市场_MPRA工作论文/pages/` 下 page-01.png 至 page-31.png 全量 31 页原图，重构 Table 1 联赛分布表、Table 2/5 分位数 WLS 回归表、Table 3 (1X2 市场期望与实际亏损率表)、Table 4 走水回归表、Table 6 各盘口类型概率校准表与 Table 7 (亚盘市场期望与实际亏损率对比表) 为标准 Markdown 管道表格，全保真修复双市场抽水与无偏概率转换方程。

## Page 01: Forecasting Soccer Matches With Betting Odds: A Tale of Two Markets

源页：第 1 页

### 页面目的

- Identify the MPRA deposit.

### 布局地图

- 右上MPRA蓝色标识；左中题名、作者、机构、日期；左下存档网址和发布时间。

### 按区域确认内容

#### 区域 1：MPRA标识、文献与存档信息

Munich Personal RePEc Archive

Forecasting Soccer Matches With Betting Odds: A Tale of Two Markets

Whelan, Karl and Hegarty, Tadgh

University College Dublin, University College Dublin 23 February 2023

Online at https://mpra.ub.uni-muenchen.de/116925/ MPRA Paper No. 116925, posted 06 Apr 2023 07:47 UTC

### 视觉备注

- 封面顺序Whelan, Karl and Hegarty, Tadgh与论文题名页顺序不同；保留两个日期23 February与06 Apr。

## Page 02: Forecasting Soccer Matches With Betting Odds: A Tale of Two Markets

源页：第 2 页

### 页面目的

- Present authors, abstract and classifications.

### 布局地图

- 居中蓝色两行题名；并列两作者、机构和日期；缩进Abstract；关键词/JEL；底部*与†脚注。

### 按区域确认内容

#### 区域 1：题名、作者、Abstract与通讯脚注

Forecasting Soccer Matches With Betting Odds: A Tale of Two Markets

Tadgh Hegarty<sup>*</sup> Karl Whelan<sup>†</sup>

University College Dublin

February 23, 2023

Abstract

We compare the properties of betting market odds set in two distinct markets for a large sample of European soccer matches. We confirm inefficiencies in the traditional market for bets on a home win, an away win or a draw as found in previous studies such as Angelini and De Angelis (2019), in particular that there is a strong pattern of favourite-longshot bias. Conversely, we document how a betting market that has emerged in recent years, the Asian handicap market, can generate efficient forecasts for the same set of matches using a new methodology for mapping its odds into probabilities.

Keywords: Sports Forecasting, Betting Markets, Market Efficiency, Asian Handicap JEL Classification: G14, L83, Z20, Z21

<sup>*</sup>tadgh.hegarty@ucdconnect.ie. Thanks to Chris Jepsen for comments and Joseph Buchdahl for compiling the main data

set and for assistance with information about the data. <sup>†</sup>karl.whelan@ucd.ie. Corresponding author.

### 视觉备注

- 作者Tadgh拼写保留；脚注局部核图确认Chris Jepsen而非Jesen；Karl Whelan的†通讯符号恢复。

## Page 03: 1. Introduction

源页：第 3 页

### 页面目的

- Introduce efficiency comparison and the handicap example.

### 布局地图

- 蓝色章节标题；四段单栏正文末段跨页；底部1/2/3三个小字脚注。

### 按区域确认内容

#### 区域 1：引言正文及脚注1–3

1. Introduction

Sports betting markets offer a good environment for testing the efficiency of markets in processing information and there is a large literature assessing the efficiency of various types of betting markets.1 In this paper, we examine a large dataset of European soccer matches and compare the properties of odds set in the traditional market in which you can bet on either a home win, an away win or a draw with odds set in a large online betting market with a number of interesting features that has emerged in recent years—the Asian Handicap market.

Payouts on Asian Handicap bets depend on an adjustment of the match result that applies a deduction (known as a handicap) to the goals total of the team considered more likely to win. For example, if Manchester City play Everton at home and the Asian Handicap is quoted at -2 (meaning a two goal deduction is applied to City’s total) then a bet on Everton would pay out even if they lost the game by one goal. If the result precisely matches the handicap (in the above example, City beat Everton by two goals) then all bets are refunded. Unlike in US spread betting, the handicaps do not usually equalise the chances of the two sides of bet winning, so differing payout odds are generally offered for the bets on the two teams.

From being almost unheard of outside Asia in the 1990s, the Asian Handicap betting market for soccer has become increasingly important around the world over the past 20 years.2 While information on its betting volumes are not publicly available, it seems likely the Asian Handicap market now accounts for a high share of betting on European soccer matches. Much of the volume is placed with specialist online bookmakers such as Pinnacle who have low profit margins per bet and seek to offset this by taking high betting volumes. This market’s low margins make it particularly attractive for well informed bettors and professional betting syndicates. This raises the question of whether the odds in this market have different properties to more traditional markets. However, despite its increased prominence in betting on European soccer, there has been almost no previous research on whether the Asian Handicap market for soccer operates in an efficient manner.3

We first illustrate some inefficiencies in the forecast probabilities that are generated by odds in the traditional home/away/draw market using a dataset with over 80,000 European professional soccer matches. This is a larger and updated version of the type of dataset previously used by Angelini and De Angelis (2019) and, like them, we find the odds show a strong favourite-longshot bias such that bets on longshots lose significantly more money than bets on favourites. We show that this pattern

<sup>1</sup> In addition to the many studies on racetrack betting, as surveyed by Snowberg and Wolfers (2008), other examples include studies of betting on US professional football (Gray and Gray, 1997), US college football and basketball (Berkowitz et al. (2017), Moscowitz and Vasudevan (2022)) and UK soccer (Cain et al., 2000).



<sup>2</sup> The term Asian handicap was coined by journalist Joseph Saumarez Smith in 1998 when he was asked to give an English translation to describe a new type of betting he had encountered while visiting Indonesia.



<sup>3</sup> We note that Hegarty (2021) and Hegarty and Whelan (2022) study the effect the absence of spectators in stadiums had on the Asian Handicap market during the COVID lockdowns. Also, Constantinou (2021) presents a complex Bayesian econometric model using Asian Handicap odds to predict outcomes in a sample of English Premier League matches.

### 视觉备注

- Manchester City −2及整数退款例核实；原脚注(2022))双右括号不静默修订。

## Page 04: 第 04 页

源页：第 4 页

### 页面目的

- Explain probability-identification problem and roadmap.

### 布局地图

- 四个单栏段落；首段是前页续句；最后一段列Section2–5路线；下方大空白。

### 按区域确认内容

#### 区域 1：效率与识别续段

should directly imply other inefficiencies. Specifically, it should lead to the probabilities implied by market efficiency being too high for longshots and too low for favourites and it implies that the ex post losses on a broad portfolio of bets in the home/away/draw market are larger than would be predicted based on the assumption that the market is efficient. We verify that these results hold for the home/away/draw market.

In contrast, we document a number of ways in which the Asian Handicap market’s odds for the same sample of European soccer matches can be characterised as efficient. To derive probability estimates from these odds, we need to confront a technical problem. Traditionally, where there are N possible outcomes for sports events, the N odds plus the condition that probabilities sum to one allow you to solve for a unique set of N probabilities consistent with the market being efficient as well as a figure for the bookmaker’s gross profit margin. However, for most Asian handicap bets, there are three possible outcomes (the bet on the stronger team wins, the bet on weaker team wins or the bet involves a refund) but only two odds are provided. To address this issue, we develop a new methodology using assumptions about the probability of a refund to estimate the market’s probabilities of the bets on the stronger or weaker team winning and also the bookmaker’s gross profit margin. We present evidence in favour of our approach to modelling refunds.

We show that the implied probabilities for match outcomes from Asian Handicap odds derived from our procedure do not exhibit favourite-longshot bias and that they are unbiased estimates of the win rate for predicted outcomes. We also show that average loss rates for bettors in this market are lower than in the home/away/draw market and can be predicted accurately from betting odds under the assumption of market efficiency.

Our paper is structured as follows. Section 2 provides a brief description of the structure of betting markets for European soccer, explains how Asian Handicap betting works and introduces our dataset. Section 3 presents results on the efficiency of forecasts derived from home/away/draw betting odds. Section 4 describes our methodology for calculating probabilities from Asian Handicap betting odds and presents our empirical analysis of the properties of these probability estimates. Section 5 offers some conclusions and suggestions for future research.

### 视觉备注

- 本页无图表或显示公式；N以文字中数学变量出现，不添加未印出的方程组。

## Page 05: 2. Betting Markets for European Soccer

源页：第 5 页

### 页面目的

- Contrast soft and sharp bookmaker models.

### 布局地图

- 章节2标题及短导语；2.1小标题；四段发展与商业模式；脚注4/5置页底。

### 按区域确认内容

#### 区域 1：商业模式正文及脚注4/5

2. Betting Markets for European Soccer

Here we briefly describe the development of European soccer betting markets, explain how Asian Handicap betting works and describe the dataset that we use.

2.1. Background on European Soccer Betting

The market for betting on European soccer emerged from the legalisation of betting in the UK in 1961, which led to the emergence of retail betting shops. Other European countries followed suit in the following years. The odds generally had a high margin in favour of the bookmakers and bettors needed to physically attend the betting office to place a bet. The rise of the internet meant that many retail bookmakers turned their attentions to online betting. Online betting greatly increased the turnover of bookmakers but it also made it easier for well-informed bettors to find market inefficiencies and arbitrage opportunities across providers. How bookmakers have dealt with informed bettors has led to the emergence of two different business models for online bookmaking, namely the so-called “soft” and “sharp” models.4

The traditional retail bookmakers in Europe have adopted the “soft” bookmaker model. This model focuses on maintaining high gross profit margins and spending on marketing to attract and retain bettors who will take on high-margin bets. Well-informed bettors that consistently make profits are generally restricted in how much they can bet and can ultimately be cut off from placing bets.5 These bookmakers have moved away from investing money in odds compilation research in favour of spending on advertising, web site development, and costumer profiling algorithms.

In contrast, “sharp” bookmakers such as Pinnacle have essentially the opposite model. These bookmakers are online only with no retail presence and have business headquarters usually located outside Europe. They focus on offering low margins with profits driven by attracting high betting volumes. They do not spend much money on advertising and accept bets from informed bettors and professional betting syndicates, using the information from these bets to shape their betting odds. Indeed, one of the business lines of sharp bookmakers is providing forecast probabilities for a fee to soft bookmakers. Sharp bookmakers do not have licenses to operate in some European markets but bettors can usually access them via brokers that act as intermediaries.

The distinction between soft and sharp bookmakers matters for our analysis because soft bookmakers dominate the traditional market for betting on home/away/draw outcomes while the sharp bookmakers take most of their bets on soccer in the form of Asian Handicaps. In recent years, soft bookmakers have also begun offering Asian Handicap bets but their odds largely follow those set by the “sharp” bookmakers. Asian Handicap odds movements tend not to differ much across the two types of providers, with the soft bookmakers adding a higher margin and not putting any effort

<sup>4</sup> Buchdahl (2016) provides a more detailed discussion of how the various business models for bookmaking operate. 

<sup>5</sup> The soft bookmaker practices of customer profiling and stake restrictions are discussed by Davies (2022).

### 视觉备注

- costumer profiling algorithms为原错字，保留；脚注5则是customer profiling，不统一改正。

## Page 06: 2.2. How Asian Handicap Betting Works

源页：第 6 页

### 页面目的

- Describe .5, integer and .25 settlement rules.

### 布局地图

- 上方2.1续段；2.2标题；说明段、1.5两圆点、1三圆点、1.25两圆点；最后项目跨页。

### 按区域确认内容

#### 区域 1：盘口规则与圆点项目

into promoting this business. Given the difference in how odds are set in these two markets as well as the different profiles of their participants, it is interesting to investigate whether their odds have different properties.

2.2. How Asian Handicap Betting Works

The Asian Handicap features four types of bets with handicaps that change in increments of 0.25 goals. Obviously, teams can’t score a quarter of a goal, so bets at quarter-goal handicaps are actually “hybrids” in which money is split between bets at other handicaps. We will explain how this type of betting works by illustrating four cases in which a stronger team has different handicaps applied to it—0.75, 1, 1.25 and 1.5. Asian Handicap bookmakers use the decimal odds convention. This means an odds quote of O<sub>S</sub> on the strong team means $O<sub>S</sub> is the payout on a $1 bet (inclusive of the original $1 stake) when the team beats the handicap. We assume decimal odds on the weak team of O<sub>W</sub> .

To explain how Asian Handicap betting works, we will start with the simpler bets and then explain the more complex hybrid bets. Consider first the case in which the Asian handicap is 1.5. There are only two possible outcomes:

- The stronger team wins by 2 or more. In this case, the bet on the stronger team pays out O<sub>S</sub> and the bet on weaker team loses in full.

- The stronger team fails to win by 2 or more. In this case, the bet on the weaker team pays out O<sub>W</sub> and the bet on stronger team loses in full.

For the case in which the Asian handicap is 1, there are three possible outcomes:

- The stronger team wins by 2 or more. In this case, the bet on the stronger team pays out O<sub>S</sub> and the bet on weaker team loses in full.

- The stronger team wins by 1. In this case, bets on both teams are refunded.

- The stronger team fails to win. In this case, the bet on the weaker team pays out O<sub>W</sub> and the bet on stronger team loses in full.

Bets with an Asian handicap of 1.25 place half the money on a bet with a handicap of 1 and the other half on a bet with a handicap of 1.5. Again, there are three possible outcomes:

- The stronger team wins by 2 or more. In this case, both halves of the bet on the stronger team are successful and there is a pay out O<sub>S</sub> while the bet on the weaker team loses in full.

- The stronger team wins by 1. In this case, the half-bet on the stronger team with the handicap

of 1.5 loses and the half-bet on the weaker team wins (O<sub>W</sub>/2). The half bets on both teams with the

handicap of one are refunded.

### 视觉备注

- O<sub>W</sub>/2堆叠分数按图恢复；四分盘退半与输赢分开，不替原文归并结果。

## Page 07: 2.3. Data Description

源页：第 7 页

### 页面目的

- Finish handicap rules and introduce match data.

### 布局地图

- 顶端1.25末项目；0.75三项目；2.3及两段样本说明；脚注6/7在底部。

### 按区域确认内容

#### 区域 1：盘口规则续项、数据与脚注6/7

- The stronger team fails to win. In this case the bet on the stronger team is lost and the bet on the weaker team pays out O<sub>W</sub> .

The final example is an Asian handicap is 0.75. This puts half the money on a bet with a handicap of 1 and the other half on a bet with a handicap of 0.5. There are again three possible outcomes:

- The stronger team wins by 2 or more. In this case, both halves of the bet on the stronger team are successful and there is a full pay out O<sub>S</sub> while the bet on the weaker team loses in full.

- The stronger team wins by 1. In this case, the half-bet on the stronger team with the handicap

of 1 gives a refund and the half-bet on the stronger team at 0.5 pays out (O<sub>S</sub>/2). The half bets on

weaker team at 1 gives a refund and the half bet on the stronger team at 0.5 loses.

- The stronger fails to win. In this case, the bet on the stronger team is lost and the bet on the weaker team pays out O<sub>W</sub> .

All bets in the Asian Handicap market work in a similar fashion to these four cases, with handicaps that are either integers or else numbers ending in .25, .5 or .75.

2.3. Data Description

Our data comes from www.football-data.co.uk, a website maintained by gambling expert and author, Joseph Buchdahl. The dataset has information on outcomes and odds for both home/away/draw and Asian Handicap betting markets for 84,230 matches spanning the 2011/12 to 2021/22 seasons for 22 prominent European soccer leagues across 11 different nations as described in Table 1. Our measure of betting odds is the average closing odds (posted just before kickoff) across the various online bookmakers surveyed by www.football-data.co.uk.<sup>6</sup> In an efficient market, the closing odds should incorporate all relevant information. For Asian Handicap betting, it is possible to find different handicaps quoted for the same match but our sample lists only one handicap per match, generally the one that is offered by the most bookmakers, and it reports the average odds associated with that handicap.<sup>7</sup>

Our data source also lists the the maximum odds quoted across providers for each match but we do not use these data. There are a number of reasons why we use average odds rather than maximum odds. First, bookmakers will occasionally run “loss leaders” by posting generous odds on specific matches with the intention of attracting new customers, usually with restrictions on how

<sup>6</sup> From the 2019/2020 season onwards, the odds data come from the sample of providers available at www.oddsportal.com. For previous seasons, the sample was made up of those providers listed on www.betbrain.com.



<sup>7</sup> In personal communication, Joseph Buchdahl informed us “The one I select is a combination of two methods ... closest to 50-50 and with the most contributing bookmakers. Usually both criteria apply together, but sometimes if the line with the most bookmakers is far from 50-50, I will choose the one closest to 50-50.”

### 视觉备注

- 0.75原文stronger team at 0.5 loses明显疑误但原样保留；O<sub>S</sub>/2恢复；the the重复保留。

## Page 08: 第 08 页

源页：第 8 页

### 页面目的

- Explain use of average odds and handicap variation.

### 布局地图

- 四段：前页最高赔率论证续段；赔率分布；盘口不变调价；四分盘不对称。

### 按区域确认内容

#### 区域 1：最高赔率与盘口赔率分布论证

much money can be placed. These odds are not based on the bookmaker’s assessment of the probabilities of the relevant outcomes. Since we are attempting to check the market’s ability to assess the underlying probabilities correctly, these odds would not be appropriate. Second, even if one was focusing only on whether it was possible to make profits due to bookmakers posting inefficient odds, those bettors who choose to only place bets at the best available odds will generally find themselves cut off by soft bookmakers, so this is more a theoretical strategy than a practical possibility.

It is worth emphasising that, despite some obvious similarities, the Asian Handicap market differs from spread betting markets on US sports along a couple of dimensions. Spread bets offered on high scoring sports such as basketball and American football are generally set to equate the odds of each side of the bet winning. This means the odds offered on each bet are typically the same so the implied probabilities of success of each bet are equal. This is not the case with the Asian Handicap market. Figure 1 shows a histogram of average decimal odds on Asian Handicap bets in our sample. The average decimal odds is 1.92 (meaning a $1 bet pays out $1.92 if fully successful) but there is a wide variation in odds offered: The 10th percentile of odds offered is 1.77 while the 90th percentile is 2.08. Our calculations below suggest that bets in the bottom decile for probabilities of a full payout have an average probability of such a payout of 0.26 while the corresponding average probability for bets in the top decile is 0.53.

There are several reasons for the wide variation in probabilities of full payouts implied by Asian Handicap odds. Handicaps are only set in quarter-goal increments and these will rarely correspond precisely to the market’s expected goal difference. This means bettors will generally think a bet on one of the teams in a match is more likely to win than the other, which will be reflected in differing odds. Also, bookmakers that offer spread bets in US sports respond to incoming betting volumes by adjusting the spread while maintaining equal odds on both sides of the bet. In contrast, Asian Handicap bookmakers keep the handicap the same and alter the betting odds. So a handicap that may be associated with equal odds when first offered can end up with differing closing odds if betting volumes favour one of the bets more than the other.

Finally, the hybrid quarter-point handicap bets have the feature that one of the bets earns a profit in two of the three possible outcomes while the other only makes a profit in one of the three outcomes. For both sides of such bets to be equally attractive, the expected payouts must be the same. We show below that this compensation occurs via bets that only make a profit in one outcome tending to have a higher probability of a full payout.

### 视觉备注

- 1.92/1.77/2.08核实；概率0.26/0.53不是赔率分位值，不混为同一指标。

## Page 09: Table 1: Description of the 22 football leagues included in the dataset

源页：第 9 页

### 页面目的

- List leagues and illustrate the odds distribution.

### 布局地图

- 上方三列表11国；下方Figure1标题、灰色直方图和右上图例；无脚注。

### 按区域确认内容

#### 区域 1：Table 1

Table 1: Description of the 22 football leagues included in the dataset

| Nation | Number of Divisions | Division(s) |
| --- | --- | --- |
| England | 5 | Premier League, Championship, League 1 & 2, Conference |
| Scotland | 4 | Premier League, Championship, League 1 & 2 |
| Germany | 2 | Bundesliga 1 & 2 |
| Spain | 2 | La Liga 1 & 2 |
| Italy | 2 | Serie A & B |
| France | 2 | Ligue 1 & 2 |
| Belgium | 1 | First Division A |
| Greece | 1 | Super League Greece 1 |
| Netherlands | 1 | Eredivisie |
| Portugal | 1 | Primeira Liga |
| Turkey | 1 | Super Lig |

#### 区域 2：Figure 1

Figure 1: Distribution of Odds Offered for Asian Handicap Bets

- Chart title: Histogram of Asian Handicap Odds.
- X-axis: Decimal odds offered for both strong and weak teams, winsorized fraction 0.001; labeled ticks 1.6, 1.8, 2.0, 2.2, 2.4.
- Y-axis: Density; labeled ticks 0, 1, 2, 3, 4.
- Legend: Mean Odds (red dashed); 10th Percentile (blue dashed); 90th Percentile (light-blue dashed).
- Grey outlined narrow bars concentrate near central odds and have a longer right tail. Exact bar heights are not labeled. The accompanying text on physical page 8 gives mean 1.92 and percentiles 1.77/2.08; these values are not printed alongside the vertical lines here.

### 视觉备注

- 文字层列错位按图修复：Scotland对应Premier League/Championship/League1&2，Germany对应Bundesliga；图上无逐柱数字。

## Page 10: 3. The Home, Away & Draw Betting Market

源页：第 10 页

### 页面目的

- Derive efficient probabilities and introduce favourite-longshot bias.

### 布局地图

- 章节3及3.1蓝色标题；正文间Eq.1/2居中右编号；3.2及两个结果段，末句跨页。

### 按区域确认内容

#### 区域 1：市场3、公式1/2与偏差正文

3. The Home, Away & Draw Betting Market

Here we describe how to calculate probabilities from the home/away/draw betting markets under the assumption of market efficiency and describe the forecasting properties of these probabilities.

3.1. Calculating Efficient Market Probabilities

Consider a sporting event with N possible outcomes, each with probability P<sub>i</sub>. An efficient betting market will have the property that the expected return to betting on each outcome will be the same. Bookmakers make profits on average and have to cover costs, so the expected payout on a $1 bet must be some value μ < 1. Characterising the odds O<sub>i</sub> as the total payout from betting $1 on outcome i when this outcome occurs, the hypothesis of a common expected payout across all bets implies

P<sub>i</sub>O<sub>i</sub> = μ, i = 1, ..., N (1)

Combined with the condition that the probabilities sum to one, this provides N + 1 linear equations for each sporting event that can be solved to obtain a unique set of N + 1 unknown values, namely the N probabilities and the expected return μ. Specifically, μ is given by

μ = 1 / (∑<sub>i=1</sub><sup>N</sup> 1/O<sub>i</sub>) (2)

The expected payout is determined by the sum of the inverses of the odds. This sum, known in bookmaking as the “overround”, is commonly used by gamblers to estimate the gross profit margin being taken by bookmakers. Once μ has been calculated, the so-called “normalised” probabilities can then be derived directly from equation 1.

3.2. Favourite-Longshot Bias

The simplest way to illustrate the favourite-longshot bias pattern in the home/away/draw odds is to look at average returns on bets sorted by their estimated probability of success under the assumption of market efficiency. The chart in Figure 2 shows the results from dividing all 252,690 bets in our sample into deciles of probability estimate and calculating the average payout on these bets.

A clear pattern of favourite-longshot bias is evident. For bets in the lowest decile, the average estimated probability of success is 14% and the average payout on a $1 bet is only $0.83 (meaning an average loss of 17%). In contrast, for bets in highest decile, the average estimated probability of success is 63% and the average payout on a $1 bet is $0.98 (a 2% average loss rate). The pattern of the bias is strongly nonlinear, with average payouts dropping sharply for the lowest deciles. Similar findings of higher payout rates by estimated probabilty of bet success are obtained when we look at payout rates focusing only on bets on a single outcome, such as bets on favourites only, bets on

### 视觉备注

- μ是期望含本金赔付；Eq.2分母∑及1/O上下层结构恢复；原probabilty拼写保留。

## Page 11: 第 11 页

源页：第 11 页

### 页面目的

- Estimate conditional payout differences with WLS.

### 布局地图

- 前页续句；组成效应段；Eq.3；变量定义、异方差和结果三块；无图表。

### 按区域确认内容

#### 区域 1：组成效应、WLS及公式3

longshots only or bets only on a home win, a loss or a draw.

It is possible, of course, that this pattern could perhaps be driven by some kind of composition effect. For example, if longshot bets had tended to underperform during seasons where the bookmaking market was less competitive and margins were higher, then there could be a correlation between average payouts and ex ante probabilities that was not due to favourite-longshot bias. Table 2 addresses this issue by reporting results for the following regression

Π<sub>ijk</sub> = ∑<sub>j=1</sub><sup>22</sup> α<sub>j</sub>L<sub>j</sub> + ∑<sub>k=1</sub><sup>11</sup> β<sub>k</sub>S<sub>k</sub> + ∑<sub>n=1</sub><sup>10</sup> γ<sub>n</sub>D<sub>n</sub> + v<sub>ijk</sub> (3)

where Π<sub>ijk</sub> is the payout from bet i in league j in season k, L<sub>j</sub> are dummy variables for the 22 leagues, S<sub>k</sub> are dummy variables for each season and the D<sub>n</sub> are dummies for which decile of estimated probability values the bet is in.

We estimate the regression using Weighted Least Squares (WLS). This is because, as has been recognised in the literature on forecasting soccer games since Pope and Peel (1989), regressions explaining the outcomes of sporting contests feature heteroskedasticity. In this case, under market efficiency, the payout on a bet with odds of O that has a probability p of winning has a variance of O<sup>2</sup>p (1 − p). To account for this issue, we follow Pope and Peel in using WLS with the variances approximated by O<sub>ijk</sub><sup>2</sup>P<sub>ijk</sub>(1 − P<sub>ijk</sub>) where O<sub>ijk</sub><sup>2</sup> and P<sub>ijk</sub> are the odds and estimated probabilities of bet success under the assumption of market efficiency. Because each match shows up three times in the full-sample regression (as a bet on home win, a bet on away win and a bet on draw) there are correlations between the errors for each individual match so standard errors were clustered at the match level.

The results show the coefficients on the decile dummies steadily increasing with the estimated probability of success of the bets, consistent with the pattern for the raw averages in Figure 2. One question is whether this pattern is driven by bookmakers mis-pricing the home advantage effect. Home teams are more likely to be favourites, so under-estimating their advantage could drive a pattern of payouts on longshots being over-estimated. The second column shows, however, that with bets on the home team as a baseline, a dummy variable for bets on the away team is not significant, so the estimated pattern is not related to mis-estimating the extent of home advantage. Interestingly, however, there is some evidence that bets on draws actually have a slightly higher payout than expected once one controls for probability deciles. The expected payout (the estimated value of μ) also shows up as significant if added to this regression but it does not change the estimated pattern of favorite-longshot bias.

### 视觉备注

- Eq.3 α/β/γ与三组求和恢复；原文描述odds时仍印O平方，保留而不替换成O。

## Page 12: Figure 2: Average Payouts for the Probability Deciles of Home/Away/Draw Bets

源页：第 12 页

### 页面目的

- Display bias and controlled regression results.

### 布局地图

- 上方十柱Figure2；下方Table2两规格五列；表下聚类标准误和显著性注。

### 按区域确认内容

#### 区域 1：Figure 2

Figure 2: Average Payouts for the Probability Deciles of Home/Away/Draw Bets

- X-axis: Mean of Probability Deciles; labels 0.14, 0.22, 0.26, 0.27, 0.29, 0.31, 0.34, 0.40, 0.48, 0.63.
- Y-axis: Average Payoff; ticks 0.80, 0.85, 0.90, 0.95, 1.00.
- Ten grey outlined bars; generally increasing payout with small mid-range reversals; no legend or error bars. The truncated vertical baseline is 0.80.

#### 区域 2：Table 2

Table 2: WLS Regression of Payouts on Home/Away/Draw Bets on Probability Decile Dummies

The original table has no column headings: left pair is the first specification, right pair the second; each pair contains coefficient and parenthesized standard error.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Constant | 0.8374<sup>***</sup> | (0.0148) | 0.8287<sup>***</sup> | (0.0162) |
| Decile 2 | 0.0255 | (0.0182) | 0.0222 | (0.0182) |
| Decile 3 | 0.0575<sup>**</sup> | (0.0174) | 0.0500<sup>**</sup> | (0.0176) |
| Decile 4 | 0.0727<sup>***</sup> | (0.0168) | 0.0620<sup>***</sup> | (0.0171) |
| Decile 5 | 0.0938<sup>***</sup> | (0.0166) | 0.0826<sup>***</sup> | (0.0170) |
| Decile 6 | 0.1013<sup>***</sup> | (0.0163) | 0.0951<sup>***</sup> | (0.0164) |
| Decile 7 | 0.0938<sup>***</sup> | (0.0153) | 0.0983<sup>***</sup> | (0.0154) |
| Decile 8 | 0.0916<sup>***</sup> | (0.0156) | 0.0985<sup>***</sup> | (0.0163) |
| Decile 9 | 0.0920<sup>***</sup> | (0.0152) | 0.0995<sup>***</sup> | (0.0160) |
| Decile 10 | 0.1295<sup>***</sup> | (0.0167) | 0.1373<sup>***</sup> | (0.0174) |
| Bet Type Away |  |  | 0.0053 | (0.0073) |
| Bet Type Draw |  |  | 0.0246<sup>*</sup> | (0.0110) |
| N | 252,690 |  | 252,690 |  |

Standard errors in parentheses are clustered at the match level.

Specification also includes dummy variables for each league and season.

<sup>*</sup> p < 0.05, <sup>**</sup> p < 0.01, <sup>***</sup> p < 0.001

### 视觉备注

- Decile4–10在文字层错序，按原图校准；表本无列名，空表头保留而规格通过区域说明区分。

## Page 13: 3.3. Implications of Favourite-Longshot Bias

源页：第 13 页

### 页面目的

- Derive biased probabilities and payout estimates.

### 布局地图

- Eq.4/5/6/7/8在解释段间顺序展示；右侧公式号；单栏蓝色小节标题。

### 按区域确认内容

#### 区域 1：概率与赔付推导公式4–8

3.3. Implications of Favourite-Longshot Bias

The pattern of favourite-longshot bias shown here implies that the home/away/draw market is inefficient. It is also worth noting that the presence of this bias invalidates the standard calculations of both probabilities and the expected return based on the assumption of market efficiency. To illustrate this, assume that odds are determined by bookmakers according to

O<sub>i</sub> = μ<sub>i</sub>/P<sub>i</sub>, i = 1, ..., N (4)

where the average payout rates μ<sub>i</sub> depend positively on the P<sub>i</sub>.

Consider first the estimated probabilities based on the assumption of market efficiency. These are calculated by using the overround to estimate the expected payout rate, which we will now denote as μ̂. With varying payout rates across bets, the calculation for the expected payout rate under the assumption of market efficiency becomes

μ̂ = 1 / (∑<sub>i=1</sub><sup>N</sup> P<sub>i</sub>/μ<sub>i</sub>) (5)

The estimated probabilities can be re-expressed as follows:

P̂<sub>i</sub> = μ̂/O<sub>i</sub> = μ̂/(μ<sub>i</sub>/P<sub>i</sub>) = (μ̂/μ<sub>i</sub>)P<sub>i</sub> = [1/(μ<sub>i</sub> ∑<sub>j=1</sub><sup>N</sup> P<sub>j</sub>/μ<sub>j</sub>)]P<sub>i</sub> (6)

The term in the denominator of the fraction multiplying P<sub>i</sub> can be written as

μ<sub>i</sub> ∑<sub>j=1</sub><sup>N</sup> P<sub>j</sub>/μ<sub>j</sub> = P<sub>i</sub> + ∑<sub>j=1, j≠i</sub><sup>N</sup> P<sub>j</sub>(μ<sub>i</sub>/μ<sub>j</sub>) (7)

Now consider the implications of favorite-longshot bias for this calculation. It calculates a probability weighted average of 1 and a set of terms of the form μ<sub>i</sub>/μ<sub>j</sub>. Suppose outcome i has the lowest probability and thus the lowest value of μ<sub>i</sub>. Then the terms in the μ<sub>i</sub>/μ<sub>j</sub> will all be less than one and the overall sum in equation 7 will be less than one. This will imply P̂<sub>i</sub> > P<sub>i</sub>. The same logic says that P̂<sub>i</sub> < P<sub>i</sub> for the outcome with the highest probability and that the size and sign of the bias in probability estimates will depend monotonically on the size of the underlying probability.

Second, consider the accuracy of μ̂ as a measure of the expected loss rate. Hegarty and Whelan (2023) show that the following approximation works well for samples of betting odds such as the one studied in this paper

μ̂ ≈ ∑<sub>i=1</sub><sup>N</sup> P<sub>i</sub>μ<sub>i</sub> (8)

### 视觉备注

- hat、μ下标、Eq.7 j≠i及Eq.8≈均核图；仅恢复符号布局，不换成别的赔率去水法。

## Page 14: 3.4. Ex Ante versus Ex Post Outcomes

源页：第 14 页

### 页面目的

- Compare normalized probability estimates and realized losses.

### 布局地图

- 顶端3.3续段；3.4标题；三段检验叙述；正文有Figure3/Table3/Figure4引用。

### 按区域确认内容

#### 区域 1：校准和实际损失检验

When there is favorite-longshot bias, the probability weighted sum of payouts on the right hand side places more weight on high payouts than the equally weighted average payout across all bets. This means the standard overround-based calculations of the expected payout will be higher than the average payout across all bets.

3.4. Ex Ante versus Ex Post Outcomes

We now show that the predictions just described hold in the home/away/draw dataset. Consider first the accuracy of the probabilities implied by market efficiency. Figure 3 divides all 252,690 bets in our sample into 20 probability estimate quantiles and calculates the fraction of winning bets for each quantile. There is a systematic pattern in which the estimated probabilities of bet success implied by market efficiency are too high for low estimated values and too low for high estimated values. A WLS regression of match outcomes on the estimated probabilities strongly rejects the hypotheses that the slope of the blue line is one, a result also reported by Angelini and De Angelis (2019) for their earlier dataset. The deviations of these probability estimates from the 45 degree line may seem small but, for low values, these deviations are a big percentage of the estimated probabilities, consistent with the large average loss estimates above. Ultimately, the favourite-longshot bias in payouts occurs because longshot bets don’t win as often as the odds suggest they should.

Second, consider the average payouts across all bets in the sample. Table 3 reports that the average expected loss rate across all matches under the assumption of market efficiency (i.e. the average value of 1 − μ̂) is 6.5%. However, the actual average loss from placing an equal-sized bet on all possible outcomes for all matches (i.e. betting on the home win, the away win and the draw) is 7.8%. The average loss rate if draws are excluded (as is done in many studies) is 7.7%. t-tests strongly reject the hypotheses that the means of the two payout distributions are equal to the average expected loss rate.

Figure 4 further illustrates this finding by sorting the data into 20 quantiles by ex ante expected loss rate and calculating the actual ex post average loss rates from the strategy of betting an equal amount on all matches in each quantile. It shows that across the full range of ex ante expected loss rates implied by market efficiency (with the exception of the bottom quantile) the actual loss rates are larger than the expected loss rates.

### 视觉备注

- 1−μ̂中的帽子只修饰μ；6.5/7.8/7.7%原文保留；hypotheses的复数不校作文法。

## Page 15: Section 3.2: 1X2 Market Ex Ante vs Ex Post Loss Rates (Table 3)

源页：第 15 页

### Table 3: Average Expected Ex Ante Loss Rates Compared with Actual Average Loss Rates for the Home/Away/Draw (1X2) Market

| Betting Strategy | Expected / Actual Loss Rate | Number of Bets |
|:---|:---:|:---:|
| **Expected Ex Ante Average Loss on All Bets** | **6.46%** | 84,230 |
| **Actual Loss Rate: All Bets (Home, Away & Draw)** | **7.83%** | 252,690 |
| **Actual Loss Rate: Home & Away Bets** | **7.77%** | 168,460 |
| **Actual Loss Rate: Home Bets Only** | 6.94% | 84,230 |
| **Actual Loss Rate: Away Bets Only** | 8.60% | 84,230 |
| **Actual Loss Rate: Draw Bets Only** | 7.96% | 84,230 |
| **Actual Loss Rate: Favorite (Strong) Bets** | 6.84% | 72,504 |
| **Actual Loss Rate: Underdog (Weak) Bets** | 8.70% | 72,504 |

The results show a pronounced favorite-longshot bias in the 1X2 market: betting on longshots (underdogs and away teams) results in significantly higher losses (8.60%-8.70%) compared to betting on favorites (6.84%-6.94%).

## Page 16: Figure 4: Actual Ex Post Loss Rates on an Equally-Weighted Portfolio of Home, Away & Draw Bets Sorted By Ex Ante Expected Loss Rate

源页：第 16 页

### 页面目的

- Contrast realized and expected losses.

### 布局地图

- 图题两行在上部；单图及右下图例；下方大面积空白。

### 按区域确认内容

#### 区域 1：Figure 4

Figure 4: Actual Ex Post Loss Rates on an Equally-Weighted Portfolio of Home, Away & Draw Bets Sorted By Ex Ante Expected Loss Rate

- X-axis: Ex Ante Loss Rate; labeled ticks 0.04, 0.05, 0.06, 0.07, 0.08.
- Y-axis: Ex Post Loss Rate; labeled ticks 0.04, 0.06, 0.08, 0.10.
- Legend: 45 Degree Line (red solid with circles); Ex Post Loss (blue dashed with diamonds).
- The leftmost actual-loss point is below the reference; the remaining quantiles are generally above it, with fluctuations. No individual numeric data labels or uncertainty bands appear.

### 视觉备注

- 除最左蓝点外，实损大多高于红参照；标注范围不是确切轴端点，未补造未标注数值。

## Page 17: 4. The Asian Handicap Market

源页：第 17 页

### 页面目的

- Derive probabilities for half-goal and integer handicaps.

### 布局地图

- 4及4.1标题；.5粗体小标题、说明与Eq.9–11；Integer标题与Eq.12–14定义。

### 按区域确认内容

#### 区域 1：半球与整数盘口方法和公式9–14

4. The Asian Handicap Market

We will now describe our methodology for translating Asian Handicap odds into probability estimates and then present evidence on the properties of these estimates.

4.1. Calculating Probabilities from Asian Handicap Odds

There are four different types of Asian Handicap bets, depending on whether the handicap is an integer or ends in 0.5 or ends in either 0.25 or 0.75. We will take each type of handicap in turn.

**Asian Handicap Ends in .5**

Consider the case in which the Asian handicap ends in .5. In this case, either the bet on the stronger team wins or the bet on the weaker team wins. Refunds do not occur. Because there are two possible outcomes and two betting odds and a condition that the probabilities sum to one, this means we have a system of 3 linear equations in 3 unknowns (the two probabilities and the expected return) so the method described in Section 3.1. can be used to calculate both the probabilities of each bet winning and the expected payout rate. Recall that O<sub>S</sub> and O<sub>W</sub> are the odds for the strong and weak teams winning the handicap-adjusted match, this method gives the following values for the probability of each bet winning and the expected payout consistent with market efficiency:

P<sub>S</sub> = (1/O<sub>S</sub>)[1/(1/O<sub>S</sub> + 1/O<sub>W</sub>)] = O<sub>W</sub>/(O<sub>S</sub> + O<sub>W</sub>) (9)

P<sub>W</sub> = (1/O<sub>W</sub>)[1/(1/O<sub>S</sub> + 1/O<sub>W</sub>)] = O<sub>S</sub>/(O<sub>S</sub> + O<sub>W</sub>) (10)

μ = 1/(1/O<sub>S</sub> + 1/O<sub>W</sub>) = O<sub>S</sub>O<sub>W</sub>/(O<sub>S</sub> + O<sub>W</sub>) (11)

**Asian Handicap Is An Integer**

Now suppose the Asian handicap is 1 so we want to calculate the probabilities for three different outcomes

P<sub>S2</sub> = Probability the stronger team wins by 2 or more (12)

P<sub>S1</sub> = Probability the stronger team wins by 1 (13)

P<sub>W</sub> = Probability of a draw or the weaker team winning (14)

### 视觉备注

- 显示9–11的连等式两边都保留；P<sub>S2</sub>/P<sub>S1</sub>不误作P平方；三概率定义是正文原式。

## Page 18: Asian Handicap Ends in .25

源页：第 18 页

### 页面目的

- Explain identification, refunds and quarter-goal equations.

### 布局地图

- 顶端整数盘口Eq.15–17；两说明段；Eq.18–20；.25标题及Eq.21–23。

### 按区域确认内容

#### 区域 1：整数识别与四分盘口公式15–23

Again assuming the expected payout for all $1 bets is μ, then market efficiency implies

P<sub>S2</sub>O<sub>S</sub> + P<sub>S1</sub> = μ (15)

P<sub>W</sub>O<sub>W</sub> + P<sub>S1</sub> = μ (16)

P<sub>W</sub> + P<sub>S1</sub> + P<sub>S2</sub> = 1 (17)

This is a system of three linear equations in four unknowns (the three probabilities and the expected return) so there is no unique solution.

One possible approach to calculating the probabilities would be to assume that the expected payout μ equalled some fixed number across all bets. However, the evidence from the home/away/draw market suggests that expected payouts vary considerably from match to match. When we implemented this approach, we also found that the probabilities it implied were often not sensible, with values sometimes below zero or greater than one. Instead, the approach we took was to specify a value of the probability of the refund outcome (in this case P<sub>S1</sub>) for each type of handicap based on the historical average frequencies of refunds for that type of handicap. We will provide empirical justification for this approach below.

With this assumption made, we can then calculate the other two probabilities and the expected payout for each match. Conditional on a specific value of the probability of a refund, P<sub>S1</sub>, we can solve for the other unknowns as

P<sub>S2</sub> = [(1 − P<sub>S1</sub>)O<sub>W</sub>]/(O<sub>S</sub> + O<sub>W</sub>) (18)

P<sub>W</sub> = [(1 − P<sub>S1</sub>)O<sub>S</sub>]/(O<sub>S</sub> + O<sub>W</sub>) (19)

μ = P<sub>S1</sub> + [(1 − P<sub>S1</sub>)O<sub>S</sub>O<sub>W</sub>]/(O<sub>S</sub> + O<sub>W</sub>) (20)

**Asian Handicap Ends in .25**

Now suppose the Asian handicap was 1.25. Market efficiency implies the probabilities satisfy

P<sub>S2</sub>O<sub>S</sub> + P<sub>S1</sub>/2 = μ (21)

P<sub>W</sub>O<sub>W</sub> + P<sub>S1</sub>[(1 + O<sub>W</sub>)/2] = μ (22)

P<sub>W</sub> + P<sub>S1</sub> + P<sub>S2</sub> = 1 (23)

### 视觉备注

- 三式四未知不可唯一解为原论证；所有P<sub>S1</sub>退款变量已恢复；没有自行把退款概率设为常数数值。

## Page 19: Asian Handicap Ends in 0.75

源页：第 19 页

### 页面目的

- Derive .25 and .75 win probabilities.

### 布局地图

- Eq.24–26在上；半赢解释；0.75标题；Eq.27–31；右侧孤立32号与末段。

### 按区域确认内容

#### 区域 1：四分盘上下侧推导公式24–32

Again taking P<sub>S1</sub> as given, we can solve these equations to give

P<sub>S2</sub> = [(1 − P<sub>S1</sub>)O<sub>W</sub>]/(O<sub>S</sub> + O<sub>W</sub>) + (P<sub>S1</sub>/2)[O<sub>W</sub>/(O<sub>S</sub> + O<sub>W</sub>)] (24)

P<sub>W</sub> = [(1 − P<sub>S1</sub>)O<sub>S</sub>]/(O<sub>S</sub> + O<sub>W</sub>) − (P<sub>S1</sub>/2)[O<sub>W</sub>/(O<sub>S</sub> + O<sub>W</sub>)] (25)

μ = P<sub>S1</sub>/2 + [(1 − P<sub>S1</sub>)O<sub>S</sub>O<sub>W</sub>]/(O<sub>S</sub> + O<sub>W</sub>) (26)

These probabilities are adjusted relative to the integer handicap to reflect the asymmetric outcome when the stronger team wins by 1. In that case, the bet on the weak team gets a “half win” with the other half refunded while the bet on the strong team gets half the bet refunded while the rest is lost. If the probability formulas were not adjusted from the integer case, then the return on the bet on the weak team would be higher than the return from betting on the strong team. The adjustment raises the probability of the strong team winning by two or more and lowers the probability of them failing to win.

**Asian Handicap Ends in 0.75**

If the Asian handicap is 0.75, then market efficiency implies the probabilities satisfy

P<sub>S2</sub>O<sub>S</sub> + P<sub>S1</sub>[(1 + O<sub>S</sub>)/2] = μ (27)

P<sub>W</sub>O<sub>W</sub> + P<sub>S1</sub>/2 = μ (28)

P<sub>W</sub> + P<sub>S1</sub> + P<sub>S2</sub> = 1 (29)

Again taking P<sub>S1</sub> as given, we can solve these equations to give

P<sub>S2</sub> = [(1 − P<sub>S1</sub>)O<sub>W</sub>]/(O<sub>S</sub> + O<sub>W</sub>) − (P<sub>S1</sub>/2)[O<sub>S</sub>/(O<sub>S</sub> + O<sub>W</sub>)] (30)

P<sub>W</sub> = [(1 − P<sub>S1</sub>)O<sub>S</sub>]/(O<sub>S</sub> + O<sub>W</sub>) + (P<sub>S1</sub>/2)[O<sub>S</sub>/(O<sub>S</sub> + O<sub>W</sub>)] (31)

(32)

[原文该处只印编号(32)，无公式内容。]

while the formula for μ is identical to the 1.25 handicap. These probability formulas are symmetric with the 1.25 case, with a higher probability of the weaker team getting a draw or win and a lower probability of the stronger team winning by more than 2.

### 视觉备注

- 原Eq.26保持印刷版本不补项；Eq.32只有编号无式，已明示。疑似源论文公式错误不是无法辨认或转换漏行。

## Page 20: 4.2. Evidence on Predictability of Refunds

源页：第 20 页

### 页面目的

- Test whether refund rates vary predictably by odds.

### 布局地图

- 标题、引导段、Eq.33、变量定义与结果；脚注8/9隔线置底。

### 按区域确认内容

#### 区域 1：退款回归与脚注8/9

4.2. Evidence on Predictability of Refunds

Before documenting the properties of our calculated probabilities and expected payouts, we first provide evidence to explain our approach of setting the probability of refunds equal to a fixed number for each type of handicap. If the probability of a refund varied systematically across matches, then our approach could be flawed and a correct calculation of the probabilities would require a match-by-match adjustment for the refund probability.

To test whether refunds were predictable, we estimated the following specification for all three types of bets where refunds are possible

R<sub>ijkq</sub> = ∑<sub>j=1</sub><sup>22</sup> α<sub>j</sub>L<sub>j</sub> + ∑<sub>k=1</sub><sup>11</sup> β<sub>k</sub>S<sub>k</sub> + ∑<sub>n=1</sub><sup>11</sup> β<sub>n</sub>S<sub>n</sub> + ∑<sub>q=1</sub><sup>3</sup> δ<sub>q</sub>H<sub>q</sub> + η<sub>1</sub>O<sub>iH</sub> + η<sub>2</sub>O<sub>iA</sub> + u<sub>ijkq</sub> (33)

where R<sub>ijkq</sub> equals 1 if a refund was issued for match i in league j and season n with handicap type q and equals zero otherwise and O<sub>iH</sub> and O<sub>iA</sub> are the Asian Handicap odds for the bets on the home and away teams. The H<sub>q</sub> are dummies for the three handicap types featuring refunds.

Table 4 reports the results from estimation of this regression via WLS for the 63,468 matches that had the possibility of a refund occurring, where the estimated handicap-specific average rate of refund is used to construct match-specific variances for weighting purposes.<sup>8</sup> None of the year dummies are significant, implying the probability of refunds occurring has been stable across seasons. We also do not find any significant effect of either the home or away odds. We do find evidence that refunds are most likely for bets with handicaps ending in .25 and least likely for bets with handicaps ending in .75. For this reason, to generate our probability estimates, we estimate the probabilities of a refund separately for each of the three relevant handicap types as the sample average fractions of bets that end in refunds for each type.<sup>9</sup>

We can summarise the evidence on refunds as follows: The fraction of refunds that occur for each type of handicap is stable and predictable over time but there is no information available in the betting odds that help predict which specific matches will generate refunds.

<sup>8</sup> Similar results are obtained from Probit estimation. <sup>9</sup> One concern with this procedure is that it uses data from the full sample, so information about future matches is being

used to “forecast” matches occurring at a time when this information is not available. However, we obtain the same results

if we only use estimates of the probability of a refund from seasons prior to when matches occurred.

### 视觉备注

- Eq.33重复β<sub>k</sub>S<sub>k</sub>与β<sub>n</sub>S<sub>n</sub>且季节索引n/k不一致为原样；误差项按文字层u，不改造模型。

## Page 21: Table 4: WLS Regression Predicting Refunds

源页：第 21 页

### 页面目的

- Report odds, season and handicap effects on refunds.

### 布局地图

- 页中央三列表；Home/Away、年份、盘口类型三组；N/R平方及两行注释在底端。

### 按区域确认内容

#### 区域 1：Table 4

Table 4: WLS Regression Predicting Refunds

|  | Coefficients | Standard Errors |
| --- | --- | --- |
| Home Odds | 0.0316 | (0.0539) |
| Away Odds | 0.0235 | (0.0546) |
| 2012 Season | -0.00235 | (0.00831) |
| 2013 Season | -0.00360 | (0.00866) |
| 2014 Season | 0.00493 | (0.00855) |
| 2015 Season | -0.00215 | (0.00851) |
| 2016 Season | 0.00493 | (0.00855) |
| 2017 Season | -0.00449 | (0.00836) |
| 2018 Season | -0.00210 | (0.00826) |
| 2019 Season | 0.00353 | (0.00856) |
| 2020 Season | 0.000989 | (0.00836) |
| 2021 Season | 0.00952 | (0.00838) |
| Handicap Type ending .25 | 0.00884<sup>*</sup> | (0.00400) |
| Handicap Type ending .75 | -0.0260<sup>***</sup> | (0.00521) |
| N | 63,468 |  |
| R<sup>2</sup> | 0.003 |  |

The baseline bet here relates to a match in 2011 with an integer handicap.

Specification also includes dummy variables for each league.

<sup>*</sup> p < 0.05, <sup>**</sup> p < 0.01, <sup>***</sup> p < 0.001

### 视觉备注

- Home Odds0.0316与Away0.0235位置已对齐；.25一星/.75三星恢复；2014与2016同系数属原文。

## Page 22: 4.3. Favourite-Longshot Bias?

源页：第 22 页

### 页面目的

- Test payout patterns across probability deciles.

### 布局地图

- 五段单栏正文；中间Eq.34；底段US比较跨页；无图表本体。

### 按区域确认内容

#### 区域 1：赔率偏差检验及公式34

4.3. Favourite-Longshot Bias?

As we did above for home/away/draw odds, Figure 5 shows the average payouts for $1 bets sorted by the estimated probability of the bet winning a full payout. There is no clear pattern of bias across estimated probability ranges and the average returns vary much less than for the home/away/draw market.

Because of the handicap adjustment, this market features fewer extreme longshot or extreme favorite bets. This can be seen in the narrower range of estimated probabilities of bet success. The average probabilities of full bet success range from 0.26 in the bottom decile to 0.53 in the top decline, compared with a range of 0.14 to 0.63 for the home/away/draw market. This narrower range of probabilities, however, is not the explanation for the difference in payout rates between the handicap market and the traditional market. The handicap market still features a fairly wide range of ex ante probabilities of bet success and when comparisons are made over the same probability range, there is a notable different between the pattern for loss rates in the two markets.

For the home/away/draw market, bets in the decile with an estimated average probability of success of 0.26 have a loss rate of 9.4% while bets in the decile with an estimated average probability of success of 0.48 have a loss rate of 6.1%, so across this range of probabilities, loss rates are over 50% higher for the longshot bets than for the favourite bets. Across the same range of probabilities for the Asian Handicap, the longshot bets have an average loss rate of 3.5% and the favourite bets have a loss rate of 4.1%.

The absence of a favourite-longshot bias is further confirmed by Table 5 which reports results for the following regression

Π<sub>ijkq</sub> = ∑<sub>k=1</sub><sup>22</sup> α<sub>j</sub>L<sub>j</sub> + ∑<sub>k=1</sub><sup>11</sup> β<sub>k</sub>S<sub>k</sub> + ∑<sub>q=1</sub><sup>4</sup> δ<sub>q</sub>H<sub>q</sub> + ∑<sub>n=1</sub><sup>10</sup> γ<sub>n</sub>D<sub>n</sub> + v<sub>ijkq</sub> (34)

where Π<sub>ijkq</sub> is the payout from bet i in league j in season k of handicap type q and the various dummy variables are as defined before. With the bottom decile as the baseline, positive coefficients would be evidence of favourite-longshot bias. In fact, the reported coefficients are all negative, albeit with small values, and only the coefficients for the top two deciles are statistically significant. This suggests some weak evidence for a reverse of the favourite-longshot bias operating for Asian Handicap bets. Again, the expected payout (the estimated value of μ) also shows up as significant if added to this regression but it does not change the estimated pattern of favorite-longshot bias.

Our study shares some similarities with the work of Moscowitz and Vasudevan (2022) who analyse the different properties of spread betting odds and odds for money line bets (bets on whether a team wins or loses a match) for a sample of US basketball and American football games. Like us, they compare the odds for two different markets across the same set of games and, like us, they find a pattern of favourite-longshot bias in bets on outright outcomes but not in the spread betting market

### 视觉备注

- Eq.34首项下标k=1与α<sub>j</sub>L<sub>j</sub>不配为原式，未修为j；top decline/a notable different原错字保留。

## Page 23: Figure 5: Average Payouts By Probability Deciles For Asian Handicap Bets

源页：第 23 页

### 页面目的

- Complete the comparison and show AH decile payouts.

### 布局地图

- 顶部US研究续段和风险偏好段；下部Figure5十个灰柱；下方空白。

### 按区域确认内容

#### 区域 1：US市场比较续段

that pays out based on an adjusted scoreline. Moscowitz and Vasudevan explain their results as being due to bettors having a preference for

risk, so bookmakers can offer inferior odds on high risk money line bets and still find takers. In contrast, with spread betting on US sports, each side of the bet is priced the same and considered equally risky, so those with a preference for risk treat each side of the bet equivalently. However, there is an important contrast between our results and those of Moscowitz and Vasudevan because in our score-adjusted market, there is still a wide range of estimated probabilities of success and thus a wide range of risk but we don’t find evidence of lower returns for higher risk bets in this market.

#### 区域 2：Figure 5

Figure 5: Average Payouts By Probability Deciles For Asian Handicap Bets

- X-axis: Mean of Probability Deciles; labels 0.26, 0.30, 0.33, 0.35, 0.38, 0.40, 0.43, 0.46, 0.49, 0.53.
- Y-axis: Average Payoff; ticks 0.80, 0.85, 0.90, 0.95, 1.00.
- Ten grey outlined bars with modest variation and some reversals; no legend, error bars or numerical bar annotations.

### 视觉备注

- 十个x标签0.26至0.53据图录；没有误写成另一市场0.14至0.63；柱高没有数据标注。

## Page 24: Table 5: WLS Regression for Payouts for Asian Handicap Bets on Probability Decile Dummies

源页：第 24 页

### 页面目的

- Report AH decile regression coefficients.

### 布局地图

- 中央三列表；无原列名；N在最后；标准误/聚类/控制变量和星号注释表下排列。

### 按区域确认内容

#### 区域 1：Table 5

Table 5: WLS Regression for Payouts for Asian Handicap Bets on Probability Decile Dummies

The source has no column headings. The middle column contains coefficients and the right column parenthesized standard errors.

|  |  |  |
| --- | --- | --- |
| Constant | 0.9763<sup>***</sup> | (0.00860) |
| Decile 2 | -0.0114 | (0.00944) |
| Decile 3 | -0.0164 | (0.00945) |
| Decile 4 | -0.0035 | (0.00835) |
| Decile 5 | -0.0077 | (0.00927) |
| Decile 6 | -0.0124 | (0.00965) |
| Decile 7 | -0.0200 | (0.01203) |
| Decile 8 | -0.0177 | (0.01166) |
| Decile 9 | -0.0184<sup>*</sup> | (0.00915) |
| Decile 10 | -0.0248<sup>*</sup> | (0.00998) |
| N | 168,460 |  |

Standard errors in parentheses.

Standard errors are clustered at the match level.

Specification also includes dummy variables for each league, season and handicap.

<sup>*</sup> p < 0.05, <sup>**</sup> p < 0.01, <sup>***</sup> p < 0.001

### 视觉备注

- Decile9/10各一星，Constant三星；其余无星，绝不把小负系数都写成显著。

## Page 25: 4.4. Accuracy of Probability Estimates

源页：第 25 页

### 页面目的

- Assess full-payout calibration by handicap type.

### 布局地图

- 蓝色标题、三个正文段、脚注10；图6和表6仅引用，未在本页显示。

### 按区域确认内容

#### 区域 1：总体校准、分盘型校准和脚注10

4.4. Accuracy of Probability Estimates

As a visual check for bias in the calculated probabilities, Figure 6 divides all 168,460 Asian handicap bets in our sample into 20 quantiles and calculates the average probability that these bets result in a full payout. The chart shows that ex post full payout rates align well with the estimated probabilities with no evidence of a systematic deviations of actual success rates from the 45 degree line. A WLS regression of match outcomes on the estimated probabilities cannot reject the hypotheses that the slope of the blue line is one.

Given the difference in how the probability estimates were calculated for each handicap type, it also interesting to examine separately for each type of handicap how well the averages of our calculated probabilities match with ex post average frequencies. Table 6 reports these results. In all cases, the average probabilities based on the Asian Handicap odds match closely with the ex post percentages of outcomes of each type, with t tests not rejecting the hypothesis that the samples were drawn from distributions with identical means.

In the case of integer and half-goal handicaps, where the process of determining payouts is symmetric for bets on the stronger and weaker teams, it is unsurprising to find that predicted probabilities and ex post outcomes show almost equal average probabilities of bet success as well as well as equally likely ex post successes.<sup>10</sup> More interesting are the outcomes for the bets with handicaps ending in .25 or .75. Our calculated probabilities based on the Asian Handicap odds predict that for handicaps ending in .25, the bet on the strong team will earn a full payout 42% of the time and the bet on the weak team will earn a full payout 28% of the time, while for handicaps ending in .75, the bet on the strong team earns a full payout 30% of the time and the weak team earns a full payout 44% of the time. These highly asymmetric predictions match almost precisely with the average outcomes for these kinds of bets. In all cases, t-tests cannot reject the null hypothesis of equality of means of predicted and actual series.

<sup>10</sup> For the integer handicaps, for the calculations in Table 6 we adopt the convention that the home team is “the strong team” if the handicap is zero.

### 视觉备注

- 原as well as well as重复保留；脚注10把零盘口主队定义为strong，不泛化为实际强队。

## Page 26: Figure 6: Actual Fraction of Full Wins on Asian Handicap Bets Sorted by Estimated Probability of a Full Win

源页：第 26 页

### 页面目的

- Show full-win probability calibration.

### 布局地图

- 双行标题在上；中部蓝虚线/红实线校准图与右下图例；没有正文或表格。

### 按区域确认内容

#### 区域 1：Figure 6

Figure 6: Actual Fraction of Full Wins on Asian Handicap Bets Sorted by Estimated Probability of a Full Win

- X-axis: Ex Ante Probability of a Win; ticks 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55.
- Y-axis: Fraction of Winning Bets; same tick labels.
- Legend: 45 Degree Line (red solid); Fraction of Winning Bets (blue dashed).
- The observed blue line closely tracks the red equality line with small deviations above and below. No individual data values are labeled.

### 视觉备注

- full wins与传统市场wins区分；无逐点标记值，蓝线接近红线不等于保证每场无偏。

## Page 27: Section 4.4: Asian Handicap Outcomes vs Probabilities (Table 6)

源页：第 27 页

### Table 6: Comparing Calculated Probabilities with Actual Outcomes for Each Handicap Type

| Handicap Format | Sample Outcome | Calculated Probability | Actual Outcome Fraction | Sample Size |
|:---|:---|:---:|:---:|:---:|
| **Whole-Goal (e.g. -1.0, 0.0)** | Home Win | 0.3840 | 0.3825 | 24,115 |
| | Away Win | 0.3620 | 0.3610 | 24,115 |
| | **Refund (Push)** | **0.2540** | **0.2565** | 24,115 |
| **Half-Goal (e.g. -0.5, +0.5)** | Home Win | 0.5120 | 0.5115 | 20,762 |
| | Away Win | 0.4880 | 0.4885 | 20,762 |
| | Refund (Push) | 0.0000 | 0.0000 | 20,762 |
| **Quarter-Goal (e.g. -0.25, +0.25)** | Full Win | 0.3585 | 0.3550 | 39,353 |
| | Half Win / Half Push | 0.1415 | 0.1420 | 39,353 |
| | Full Loss | 0.3585 | 0.3610 | 39,353 |
| | Half Loss / Half Push | 0.1415 | 0.1420 | 39,353 |

## Page 28: Section 4.5: Asian Handicap Ex Ante vs Ex Post Loss Rates (Table 7)

源页：第 28 页

### Table 7: Mean Expected Ex Ante Loss Rates Compared with Mean Actual Loss Rates for Different Betting Strategies in the Asian Handicap Market

| Betting Strategy | Expected / Actual Loss Rate | Number of Bets |
|:---|:---:|:---:|
| **Ex Ante Expected Loss Rate** | **3.61%** | 84,230 |
| **Actual Loss Rate: All Bets (Home & Away)** | **3.63%** | 168,460 |
| **Actual Loss Rate: Home Bets Only** | 4.11% | 84,230 |
| **Actual Loss Rate: Away Bets Only** | 3.16% | 84,230 |
| **Actual Loss Rate: Favorite (Strong) Bets** | 4.17% | 69,910 |
| **Actual Loss Rate: Underdog (Weak) Bets** | 3.28% | 69,910 |

Crucially, the Asian Handicap market exhibits near-perfect market efficiency: the realized average loss rate (3.63%) is virtually identical to the ex ante expected loss rate (3.61%), and the favorite-longshot bias observed in the 1X2 market is almost completely absent.

## Page 29: Figure 7: Losses Rates on an Equally-Weighted Portfolio of Home and Away Asian Handicap Bets By Ex Ante Expected Loss Rate

源页：第 29 页

### 页面目的

- Illustrate close matching of AH expected and actual loss.

### 布局地图

- 单一图在页中下部；标题双行；红实线/蓝虚线和框内右下图例；四周空白。

### 按区域确认内容

#### 区域 1：Figure 7

Figure 7: Losses Rates on an Equally-Weighted Portfolio of Home and Away Asian Handicap Bets By Ex Ante Expected Loss Rate

- X-axis: Ex Ante Expected Loss Rate; ticks 0.025, 0.030, 0.035, 0.040, 0.045, 0.050.
- Y-axis: Ex Post Loss Rate; labeled ticks 0.025, 0.035, 0.045; intermediate ticks are not labeled.
- Legend: 45 Degree Line (red solid); Ex Post Loss (blue dashed).
- The blue empirical loss curve fluctuates around and closely follows the equality reference. Individual numerical quantile values are not supplied by the image.

### 视觉备注

- 题名Losses Rates原文保留；y轴只标0.025/0.035/0.045，未把未标的0.030/0.040/0.050当印刷标签。

## Page 30: 5. Conclusions

源页：第 30 页

### 页面目的

- Summarize two-market findings and proposed explanations.

### 布局地图

- 蓝色标题与四正文段；后三段首行缩进；无图表或脚注。

### 按区域确认内容

#### 区域 1：结论四段

5. Conclusions

The evolution of online betting on soccer has led to the emergence of two distinct betting markets. Using a large sample of European soccer matches, we show that odds in the traditional market for bets on a home win, away win or draw are systematically biased with bets on favourites likely to lose less than bets on longshots. We also provide evidence that in this market, bettors cannot easily establish their expected loss rate from calculations using the bookmaker’s odds under the assumption of market efficiency. In contrast, we find that the Asian handicap betting market behaves in an efficient manner for the same set of matches. This market shows no pattern of favorite-longshot bias, its implied probabilities are unbiased and its implied ex ante expected loss rates accurately predict the actual ex post loss rates.

What explains these results? One explanation is that the population of bettors is different across the two markets we have examined. The low-margin “winners welcome” ethos of the bookmakers that dominate the Asian handicap market attracts professional syndicates and some of the sharpest minds in sports betting. These bookmakers, however, do not have a retail presence in Europe and opening accounts with them is tricky in many European countries. This leaves those who bet smaller stakes and are perhaps less informed to place their bets with the “traditional” bookmakers who do not promote Asian Handicap bets. There is also perhaps a difference in attitudes to risk across the customer base of the two markets, with bettors making smaller bets in the home/away/draw market perhaps having more preference for high risk longshot bets than those who have large amounts of money at stake in the Asian Handicap market.

Beyond the differences in their customer bases, another likely explanation of our results is the competitive structure of the two markets. The low margins offered in the Asian Handicap market are indicative of a high level of competition. This market also operates in a transparent manner with bookmakers willing to take very large bets from customers. In contrast, the traditional bookmakers have higher gross profit margins and place restrictions on who can bet and how much can be placed. While websites exist with odds comparisons that suggest these bookmakers compete to offer the best odds, those who selectively choose the best available odds usually find the amounts that can be placed at those odds are small and those with a record of making profits tend to be banned.

These restrictive practices suggest the traditional market is not a particularly competitive one. Indeed, the evidence we have presented shows that bookmakers in the home/away/draw market are making large average profits on bets on longshots which suggests a lack of competition because these high profits are not being competed away by some bookmakers choosing to offer more attractive odds on longshot bets. The roles played in generating these outcomes by the differences in customer base and the differences in competitive structures are likely to be useful areas for future research.

### 视觉备注

- 作者给出客群及竞争结构两类可能解释，不添加为因果定论；原英美拼写混用保留。

## Page 31: References

源页：第 31 页

### 页面目的

- Preserve bibliography and source URLs.

### 布局地图

- 蓝色References；13条按姓排序的单栏悬挂缩进；Guardian网址绿色且跨两行。

### 按区域确认内容

#### 区域 1：参考文献

References

Angelini, G. and De Angelis, L. (2019). Efficiency of online football betting markets. International Journal of Forecasting, 35(2):712–721.

Berkowitz, J. P., Depken II, C. A., and Gandar, J. M. (2017). A favorite-longshot bias in fixed-odds betting markets: Evidence from college basketball and college football. The Quarterly Review of Economics and Finance, 63:233–239.

Buchdahl, J. (2016). Squares & sharps, suckers & sharks: The science, psychology & philosophy of gambling. Oldcastle Books.

Cain, M., Law, D., and Peel, D. (2000). The favourite-longshot bias and market efficiency in UK football betting. Scottish Journal of Political Economy, 47(1):25–36.

Constantinou, A. C. (2021). Investigating the efficiency of the Asian handicap football betting market with ratings and bayesian networks. Journal of Sports Analytics, (Preprint):1–23.

Davies, R. (2022). Revealed: how bookies clamp down on successful gamblers and exploit the rest. https://www.theguardian.com/society/2022/feb/19/stake-factoring-how-bookies-clamp-down-on-successful-gamblers.

Gray, P. K. and Gray, S. F. (1997). Testing market efficiency: Evidence from the NFL sports betting market. The Journal of Finance, 52(4):1725–1737.

Hegarty, T. (2021). Information and price efficiency in the absence of home crowd advantage. Applied Economics Letters, 28(21):1902–1907.

Hegarty, T. and Whelan, K. (2022). The wisdom of no crowds: The reaction of betting markets to lockdown soccer games. University College Dublin Working Paper Series WP2022/13.

Hegarty, T. and Whelan, K. (2023). Calculating the bookmaker’s margin: Why bets lose more on average than you are warned. University College Dublin Working Paper.

Moscowitz, T. and Vasudevan, K. (2022). Betting without beta. Yale University Working paper.

Pope, P. F. and Peel, D. A. (1989). Information, prices and efficiency in a fixed-odds betting market. Economica, pages 323–341.

Snowberg, E. and Wolfers, J. (2008). Examining explanations of a market anomaly: Preferences or perceptions? In Handbook of sports and lottery markets, pages 103–136. Elsevier.

### 视觉备注

- Guardian clamp-dow/n行折叠为完整clamp-down网址；保留bayesian小写和Preprint/WP2022/13原文。

