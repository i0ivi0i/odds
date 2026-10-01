# The Market for English Premier League (EPL) Odds

> 重建说明：模式 page-aligned；来源 `2017_Feng_英超赔率与动态进球分布_arXiv_v5.pdf`；共 24 页；原图逐页查看 24/24 页。

> 校准范围：保留英文正文、原文语病及原始数据，不以摘要代替正文。图形按区域记录轴、图例、事件及可确认数值；未标数值的曲线不推算逐点数据。数学符号按原页恢复；原文疑点仅在视觉备注说明。

## Page 01: Title, authors and Abstract

源页：第 1 页

### 页面目的

- 保留本页 Title, authors and Abstract 的原文与论证顺序。

### 布局地图

- 标题、三列作者单位、日期在上；摘要居中单栏；关键词及四项脚注在下。

### 按区域确认内容

#### 区域 1：本页正文与已标号数学内容

The Market for English Premier League (EPL) Odds∗

arXiv:1604.03614v5 [stat.AP] 5 Jan 2017      Guanhao Feng†            Nicholas Polson‡             Jianeng Xu§

Booth School of Business  Booth School of Business  Department of Statistics
University of Chicago     University of Chicago     University of Chicago

January, 2017

Abstract

This paper employs a Skellam process to represent real-time betting odds for English Premier
League (EPL) soccer games. Given a matrix of market odds on all possible score outcomes, we
estimate the expected scoring rates for each team. The expected scoring rates then define the
implied volatility of an EPL game. As events in the game evolve, we re-estimate the expected
scoring rates and our implied volatility measure to provide a dynamic representation of the
market’s expectation of the game outcome. Using a dataset of 1520 EPL games from 2012-2016,
we show how our model calibrates well to the game outcome. We illustrate our methodology on
real-time market odds data for a game between Everton and West Ham in the 2015-2016 season.
We show how the implied volatility for the outcome evolves as goals, red cards, and corner kicks
occur. Finally, we conclude with directions for future research.

Key words: English Premier League, Sports Betting, Market Odds, Market Expectations, Skellam
Process.

∗ First Draft: April, 2016. We would like to thank the two referees and the associate editor for their valuable comments
on the content of our manuscript and their suggestions for improving the document.

† Address: 5807 S Woodlawn Avenue, Chicago, IL 60637, USA. E-mail address: guanhao.feng@chicagobooth.edu.
‡ Address: 5807 S Woodlawn Avenue, Chicago, IL 60637, USA. E-mail address: nicholas.polson@chicagobooth.edu.
§ Address: 5747 S Ellis Avenue, Chicago, IL 60637, USA. E-mail address: jianeng@uchicago.edu.

### 视觉备注

- 核对标题星号和作者†/‡/§，恢复抽取遗漏的脚注标记；左缘arXiv标识原样保留。

## Page 02: Introduction — The betting market for the EPL

源页：第 2 页

### 页面目的

- 保留本页 Introduction — The betting market for the EPL 的原文与论证顺序。

### 布局地图

- 1及1.1标题位于页顶；四段单栏正文向下排列。

### 按区域确认内容

#### 区域 1：本页正文与已标号数学内容

1 Introduction

1.1 The betting market for the EPL

Gambling on soccer is a global industry with revenues between $700 billion and $1 trillion a
year (see ”Football Betting - the Global Gambling Industry worth Billions.” BBC Sport). Betting on
the result of a soccer match is a rapidly growing market, and online real-time odds exists (Betfair,
Bet365, Ladbrokes). Market odds for all possible score outcomes (0 − 0, 1 − 0, 0 − 1, 2 − 0, ...) as well
as outright win, lose and draw are available in real time. In this paper, we employ a two-parameter
probability model based on a Skellam process and a non-linear objective function to extract the
expected scoring rates for each team from the odds matrix. The expected scoring rates then define
the implied volatility of the game.

A key feature of our analysis is to use the real-time odds to re-calibrate the expected scoring
rates instantaneously as events evolve in the game. This allows us to assess how market expecta-
tions change according to exogenous events such as corner kicks, goals, and red cards. A plot of the
implied volatility provides a diagnostic tool to show how the market reacts to event information.
In particular, we study the evolution of the odds implied final score prediction over the course of
the game. Our dynamic Skellam model fits the scoring data well in a calibration study of 1520 EPL
games from the 2012 - 2016 seasons.

The goal of our study is to show how a parsimonious two-parameter model can flexibly model
the evolution of the market odds matrix of final scores. We provide a non-linear objective function
to fit our Skellam model to instantaneous market odds matrix. We then define the implied volatility
of an EPL game and use this as a diagnostics to show how the market’s expectation changes over
the course of a game.

One advantage of viewing market odds through the lens of a probability model is the ability
to obtain more accurate estimates of winning probabilities. For example, a typical market ”vig”
(or liquidity premium for bookmakers to make a return) is 5 − 8% in the win, lose, draw market.
Now there is also extra information in the final score odds about the win odds. Our approach
helps to extract that information. Another application of the Skellam process is to model final score
outcomes as a function of characteristics (see Karlis and Ntzoufras (2003, 2009).)

### 视觉备注

- 本页无图表或编号公式；1520、2012–2016、5–8%与原页一致，原文语病不改。

## Page 03: Connections with Existing Work

源页：第 3 页

### 页面目的

- 保留本页 Connections with Existing Work 的原文与论证顺序。

### 布局地图

- 页首论文路线段；1.2标题以下三个文献综述段落；末段跨页。

### 按区域确认内容

#### 区域 1：本页正文与已标号数学内容

The rest of the paper is outlined as follows. The next subsection provides connections with
existing research. Section 2 presents our Skellam process model for representing the difference
in goals scored. We then show how to make use of an odds matrix while calibrating the model
parameters. We calculate a dynamic implied prediction of any score and hence win, lose and draw
outcomes, using real-time online market odds. Section 3 illustrates our methodology using an EPL
game between Everton and West Ham during the 2015-2016 season. Finally, Section 4 discusses
extensions and concludes with directions for future research.

1.2 Connections with Existing Work

There is considerable interest in developing probability models for the evolution of the score
of sporting events. Stern (1994) and Polson and Stern (2015) propose a continuous time Brownian
motion model for the difference in scores in a sporting event and show how to calculate the im-
plied volatility of a game. We build on their approach by using a difference of Poisson processes
(a.k.a. Skellam process) for the discrete evolution of the scores of an EPL game, see also Karlis and
Ntzoufras (2003, 2009) and Koopman et al. (2014). Early probabilistic models (Lee 1997) predicted
the outcome of soccer matches using independent Poisson processes. Later models incorporate a
correlation between the two scores and model the number of goals scored by each team using bi-
variate Poisson models (see Maher (1982) and Dixon and Coles (1997)). Our approach follows Stern
(1994) by modeling the score difference (a.k.a. margin of victory), instead of modeling the number
of goals and the correlation between scores directly.

There is also an extensive literature on soccer gambling and market efficiency. For example,
Vecer et al. (2009) estimates the scoring intensity in a soccer game from betting markets. Dixon
and Pope (2004) presents a detailed comparison of odds set by different bookmakers. Fitt (2009)
uses market efficiency to analyze the mispricing of cross-sectional odds and Fitt et al. (2005) models
online soccer spread bets.

Another line of research, asks whether betting markets are efficient and, if not, how to exploit
potential inefficiencies in the betting market. For example, Levitt (2004) discusses the structural
difference of the gambling market and financial markets. The study examines whether bookmakers
are more skilled at game prediction than bettors and in turn exploit bettor biases by setting prices

### 视觉备注

- 蓝色作者年份是文献链接而非公式；本页无图表，最后prices承接第4页。

## Page 04: Skellam Process for EPL scores

源页：第 4 页

### 页面目的

- 保留本页 Skellam Process for EPL scores 的原文与论证顺序。

### 布局地图

- 页首承接综述；2及2.1标题；下部联立式(1)及变量说明。

### 按区域确认内容

#### 区域 1：本页正文与已标号数学内容

that deviate from the market clearing price. Avery and Chevalier (1999) examine the hypothesis that
sentimental bettors act like noise traders and can affect the path of prices in soccer betting markets.

2 Skellam Process for EPL scores

To model the outcome of a soccer game between team A and team B, we let the difference in

scores, N(t) = N<sub>A</sub>(t) − N<sub>B</sub>(t) where N<sub>A</sub>(t) and N<sub>B</sub>(t) are the team scores at time point t. Negative

values of N(t) indicate that team A is behind. We begin at N(0) = 0 and ends at time one with

N(1) representing the final score difference. The probability P(N(1) > 0) represents the ex-ante

odds of team A winning. Half-time score betting, which is common in Europe, is available for the

distribution of N(1/2).

We develop a probabilistic model for the distribution of N(1) given N(t) = ℓ where ℓ is the

current lead. This model, together with the current market odds can be used to infer the expected

scoring rates of the two teams and then to define the implied volatility of the outcome of the match.
We let λ<sup>A</sup> and λ<sup>B</sup> denote the expected scoring rates for the whole game. We allow for the possibility

that the scoring abilities (and their market expectations) are time-varying, in which case we denote
the expected scoring rates after time t by λ<sub>t</sub><sup>A</sup> and λ<sub>t</sub><sup>B</sup> respectively, instead of λ<sup>A</sup>(1 − t) and λ<sup>B</sup>(1 − t).

2.1 Implied Score Prediction from EPL Odds

The Skellam distribution is defined as the difference between two independent Poisson vari-
ables, see Skellam (1946), Sellers (2012), Alzaid et al. (2010), and Barndorff-Nielsen and Shephard
(2012). Karlis and Ntzoufras (2009) shows how Skellam distribution can be extended to a differ-
ence of distributions which have a specific trivariate latent variable structure. Following Karlis and
Ntzoufras (2003), we decompose the scores of each team as

N<sub>A</sub>(t) = W<sub>A</sub>(t) + W(t)

N<sub>B</sub>(t) = W<sub>B</sub>(t) + W(t)  (1)

where W<sub>A</sub>(t), W<sub>B</sub>(t) and W(t) are independent processes with W<sub>A</sub>(t) ∼ Poisson(λ<sup>A</sup>t), W<sub>B</sub>(t) ∼
Poisson(λ<sup>B</sup>t). Here W(t) is a non-negative integer-valued process to induce a correlation between

### 视觉备注

- 恢复抽取遗漏的ℓ及N(1/2)；式(1)中共同项W(t)在两行均有；末句跨页。

## Page 05: Skellam process and remaining-game distribution

源页：第 5 页

### 页面目的

- 保留本页 Skellam process and remaining-game distribution 的原文与论证顺序。

### 布局地图

- 正文交替排列式(2)、联立式(3)、式(4)；页底开始全概率推导。

### 按区域确认内容

#### 区域 1：本页正文与已标号数学内容

the numbers of goals scored. By modeling the score difference, N(t), we avoid having to specify the
distribution of W(t) as the difference in goals scored is independent of W(t). Specifically, we have
a Skellam distribution

N(t) = N<sub>A</sub>(t) − N<sub>B</sub>(t) = W<sub>A</sub>(t) − W<sub>B</sub>(t) ∼ Skellam(λ<sup>A</sup>t, λ<sup>B</sup>t).  (2)

where λ<sup>A</sup>t is the cumulative expected scoring rate on the interval [0, t]. At time t, we have the
conditional distributions

W<sub>A</sub>(1) − W<sub>A</sub>(t) ∼ Poisson(λ<sup>A</sup>(1 − t))

W<sub>B</sub>(1) − W<sub>B</sub>(t) ∼ Poisson(λ<sup>B</sup>(1 − t))  (3)

Now letting N<sup>*</sup>(1 − t), the score difference of the sub-game which starts at time t and ends at time 1
and the duration is (1 − t). By construction, N(1) = N(t) + N<sup>*</sup>(1 − t). Since N<sup>*</sup>(1 − t) and N(t) are

differences of two Poisson process on two disjoint time periods, by the property of Poisson process,
N<sup>*</sup>(1 − t) and N(t) are independent. Hence, we can re-express equation (2) in terms of N<sup>*</sup>(1 − t),

and deduce

N<sup>*</sup>(1 − t) = W<sub>A</sub><sup>*</sup> (1 − t) − W<sub>B</sub><sup>*</sup>(1 − t) ∼ Skellam(λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>)   (4)

where W<sub>A</sub><sup>*</sup> (1 − t) = W<sub>A</sub>(1) − W<sub>A</sub>(t), λ<sup>A</sup> = λ<sub>0</sub><sup>A</sup> and λ<sub>t</sub><sup>A</sup> = λ<sup>A</sup>(1 − t). A natural interpretation of the
expected scoring rates, λ<sub>t</sub><sup>A</sup> and λ<sub>t</sub><sup>B</sup>, is that they reflect the ”net” scoring ability of each team from
time t to the end of the game. The term W(t) model a common strength due to external factors,
such as weather. The ”net” scoring abilities of the two teams are assumed to be independent of
each other as well as the common strength factor. We can calculate the probability of any particular
score difference, given by P(N(1) = x|λ<sup>A</sup>, λ<sup>B</sup>), at the end of the game where the λ’s are estimated
from the matrix of market odds. Team strength and ”net” scoring ability can be influenced by
various underlying factors, such as the offensive and defensive abilities of the two teams. The goal
of our analysis is to only represent these parameters at every instant as a function of the market
odds matrix for all scores.

To derive the implied winning probability, we use the law of total probability. The probability

### 视觉备注

- 核对λᴬt为乘积，λₜᴬ为上下标；星号表示剩余子比赛，未将其当乘号。

## Page 06: Skellam probability mass and draw probability

源页：第 6 页

### 页面目的

- 保留本页 Skellam probability mass and draw probability 的原文与论证顺序。

### 布局地图

- 上部四行式(5)，中间Bessel级数与式(6)，下部式(7)和跨页正文。

### 按区域确认内容

#### 区域 1：本页正文与已标号数学内容

mass function of a Skellam random variable is the convolution of two Poisson distributions:

P(N(1) = x | λ<sup>A</sup>, λ<sup>B</sup>)
= ∑<sub>k=0</sub><sup>∞</sup> P(W<sub>B</sub>(1) = k − x | W<sub>A</sub>(1) = k, λ<sup>B</sup>) P(W<sub>A</sub>(1) = k | λ<sup>A</sup>)

= ∑<sub>k=max{0,x}</sub><sup>∞</sup> {e<sup>−λᴮ</sup>(λ<sup>B</sup>)<sup>k−x</sup>/(k−x)!}{e<sup>−λᴬ</sup>(λ<sup>A</sup>)<sup>k</sup>/k!}

= e<sup>−(λᴬ+λᴮ)</sup> ∑<sub>k=max{0,x}</sub><sup>∞</sup> (λ<sup>B</sup>)<sup>k−x</sup>(λ<sup>A</sup>)<sup>k</sup>/((k−x)!k!)

= e<sup>−(λᴬ+λᴮ)</sup>(λ<sup>A</sup>/λ<sup>B</sup>)<sup>x/2</sup>I<sub>|x|</sub>(2√(λ<sup>A</sup>λ<sup>B</sup>))  (5)

where I<sub>r</sub>(x) is the modified Bessel function of the first kind (for full details, see Alzaid et al. (2010)),
thus has the series representation

I<sub>r</sub>(x) = (x/2)<sup>r</sup> ∑<sub>k=0</sub><sup>∞</sup> (x<sup>2</sup>/4)<sup>k</sup>/(k!Γ(r+k+1)).

The probability of home team A winning is given by

P(N(1) > 0 | λ<sup>A</sup>, λ<sup>B</sup>) = ∑<sub>x=1</sub><sup>∞</sup> P(N(1) = x | λ<sup>A</sup>, λ<sup>B</sup>).  (6)

In practice, we truncate the number of possible goals since the probability of an extreme score
difference is negligible. Unlike the Brownian motion model for the evolution of the outcome in a
sports game (Stern (1994), Polson and Stern (2015)), the probability of a draw in our setting is not
zero. Instead, P(N(1) = 0|λ<sup>A</sup>, λ<sup>B</sup>) > 0 depends on the sum and product of two parameters λ<sup>A</sup> and
λ<sup>B</sup> and thus the odds of a draw are non-zero.

For two evenly matched teams withλ<sup>A</sup> = λ<sup>B</sup> = λ, we have

P(N(1) = 0 | λ<sup>A</sup> = λ<sup>B</sup> = λ) = e<sup>−2λ</sup>I<sub>0</sub>(2λ) = ∑<sub>k=0</sub><sup>∞</sup> (λ<sup>k</sup>/e<sup>λ</sup>)<sup>2</sup>/(k!)<sup>2</sup>.  (7)

Figure 1 shows that this probability is a monotone decreasing function of λ and so two evenly
matched teams with large λ’s are less likely to achieve a draw.

Another quantity of interest is the conditional probability of winning as the game progresses.
If the current lead at time t is ℓ, and N(t) = ℓ = N<sub>A</sub>(t) − N<sub>B</sub>(t), the Poisson property implied

### 视觉备注

- 恢复抽取丢失的根号、分母及阶乘；式(5)首行k=0、后两行max{0,x}按源文保留。

## Page 07: Figure 1 and conditional score difference

源页：第 7 页

### 页面目的

- 保留本页 Figure 1 and conditional score difference 的原文与论证顺序。

### 布局地图

- 页上Figure 1左右子图；图注在下；后半页条件分布和式(8)。

### 按区域确认内容

#### 区域 1：上部左右 Figure 1 与图注

Figure 1: Left: Probability of a draw for two evenly matched teams. Right: Probability of score
differences for two evenly matched teams. Lambda values are denoted by different colors.

#### 区域 2：图注下条件分布推导

that the final score difference (N(1)|N(t) = ℓ )can be calculated by using the fact that N(1) =
N(t) + N<sup>*</sup>(1 − t) and N(t) and N<sup>*</sup>(1 − t) are independent. Specifically, conditioning on N(t) = ℓ ,
we have the identity

N(1) = N(t) + N<sup>*</sup>(1 − t) = ℓ + Skellam(λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>).

We are now in a position to find the conditional distribution (N(1) = x|N(t) = ℓ ) for every
time point t of the game given the current score. Simply put, we have the time homogeneous
condition

P(N(1) = x | λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>, N(t) = ℓ)
= P(N(1) − N(t) = x − ℓ | λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>, N(t) = ℓ)
= P(N<sup>*</sup>(1 − t) = x − ℓ | λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>)  (8)

where λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>, are given by market expectations at time t.

**Figure 1 — visible graphic structure:** Left: Lambda (0,2,4,6,8,10) versus Draw Probability (0.2,0.4,0.6,0.8), a decreasing black curve. Right: Score Difference (−4,−2,0,2,4) versus Probability (0.00–0.30), symmetric curves; legend λ=1,1.5,2,2.5,3, respectively black/red/green/blue/cyan.


### 视觉备注

- Figure 1左轴Lambda/Draw Probability；右轴Score Difference/Probability，图例λ=1,1.5,2,2.5,3；只记录标注不猜逐点值。

## Page 08: Winning and draw probabilities — Market Calibration

源页：第 8 页

### 页面目的

- 保留本页 Winning and draw probabilities — Market Calibration 的原文与论证顺序。

### 布局地图

- 上半页式(9)/(10)，其后失利概率句；下半页2.2及赔率实例。

### 按区域确认内容

#### 区域 1：本页正文与已标号数学内容

Two conditional probabilities of interest are he chances that the home team A wins,

P(N(1) > 0 | λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>, N(t) = ℓ)
= P(ℓ + N<sup>*</sup>(1−t) > 0 | λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>)
= P(Skellam(λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>) > −ℓ | λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>)
= ∑<sub>x&gt;−ℓ</sub> e<sup>−(λₜᴬ+λₜᴮ)</sup>(λ<sub>t</sub><sup>A</sup>/λ<sub>t</sub><sup>B</sup>)<sup>x/2</sup>I<sub>|x|</sub>(2√(λ<sub>t</sub><sup>A</sup>λ<sub>t</sub><sup>B</sup>)).  (9)

and the conditional probability of a draw at time t is

P(N(1) = 0 | λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>, N(t) = ℓ)
= P(ℓ + N<sup>*</sup>(1−t) = 0 | λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>)
= P(Skellam(λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>) = −ℓ | λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>)
= e<sup>−(λₜᴬ+λₜᴮ)</sup>(λ<sub>t</sub><sup>A</sup>/λ<sub>t</sub><sup>B</sup>)<sup>−ℓ/2</sup>I<sub>|ℓ|</sub>(2√(λ<sub>t</sub><sup>A</sup>λ<sub>t</sub><sup>B</sup>)).  (10)

The conditional probability at time t of home team A losing is 1 − P(N(1) > 0|λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>, N(t) = ℓ ).
We now turn to the calibration of our model from given market odds.

2.2 Market Calibration

Our information set at time t, denoted by I<sub>t</sub>, includes the current lead N(t) = ℓ and the market
odds for {Win, Lose, Draw, Score}<sub>t</sub>, where Score<sub>t</sub> = {(i − j) : i, j = 0, 1, 2, ....}. These market odds
can be used to calibrate a Skellam distribution which has only two parameters λ<sub>t</sub><sup>A</sup> and λ<sub>t</sub><sup>B</sup>. The best
fitting Skellam model with parameters {λ̂<sub>t</sub><sup>A</sup>, λ̂<sub>t</sub><sup>B</sup>} will then provide a better estimate of the market’s
information concerning the outcome of the game than any individual market (such as win odds) as
they are subject to a ”vig” and liquidity. Suppose that the fractional odds for all possible final score
outcomes are given by a bookmaker. In this case, the bookmaker pays out three times the amount
staked by the bettor if the outcome is indeed 2-1. Fractional odds are used in the UK, while money-
line odds are favored by American bookmakers with 2 : 1 (”two-to-one”) implying that the bettor
stands to make a $200 profit on a $100 stake. The market implied probability makes the expected
winning amount of a bet equal to 0. In this case, the implied probability p = 1/(1 + 3) = 1/4
and the expected winning amount is µ = −1 ∗ (1 − 1/4) + 3 ∗ (1/4) = 0. We denote this odds as

### 视觉备注

- 原文失利概率写为1−P(N(1)>0)，未擅自减去平局；原句he chances及金额例子保留。

## Page 09: Odds adjustment and market-implied moments

源页：第 9 页

### 页面目的

- 保留本页 Odds adjustment and market-implied moments 的原文与论证顺序。

### 布局地图

- 上部赔率转换及vig段；中部式(11)/(12)；页底均值公式。

### 按区域确认内容

#### 区域 1：本页正文与已标号数学内容

odds(2, 1) = 3. To convert all the available odds to implied probabilities, we use the identity

P(N<sub>A</sub>(1) = i, N<sub>B</sub>(1) = j) = 1/(1 + odds(i,j)).

The market odds matrix, O, with elements o<sub>ij</sub> = odds(i − 1, j − 1), i, j = 1, 2, 3... provides all pos-
sible combinations of final scores. Odds on extreme outcomes are not offered by the bookmakers.
Since the probabilities are tiny, we set them equal to 0. The sum of the possible probabilities is
still larger than 1 (see Dixon and Coles (1997) and Polson and Stern (2015)). This ”excess” prob-
ability corresponds to a quantity known as the ”market vig.” For example, if the sum of all the
implied probabilities is 1.1, then the expected profit of the bookmaker is 10%. To account for this
phenomenon, we scale the probabilities to sum to 1 before estimation.

To estimate the expected scoring rates, λ<sub>t</sub><sup>A</sup> and λ<sub>t</sub><sup>B</sup>, for the sub-game N<sup>*</sup>(1 − t), the odds from
a bookmaker should be adjusted by N<sub>A</sub>(t) and N<sub>B</sub>(t). For example, if N<sub>A</sub>(0.5) = 1, N<sub>B</sub>(0.5) = 0
and odds(2, 1) = 3 at half time, these observations actually says that the odds for the second half
score being 1-1 is 3 (the outcomes for the whole game and the first half are 2-1 and 1-0 respectively,
thus the outcome for the second half is 1-1). The adjusted odds∗ for N<sup>*</sup>(1 − t) is calculated using the
original odds as well as the current scores and given by

odds<sup>*</sup>(x, y) = odds(x + N<sub>A</sub>(t), y + N<sub>B</sub>(t)).                                  (11)

At time t (0 ≤ t ≤ 1), we calculate the implied conditional probabilities of score differences
using odds information

P(N(1) = k | N(t) = ℓ) = P(N<sup>*</sup>(1−t) = k−ℓ)
= (1/c) ∑<sub>i−j=k−ℓ</sub> 1/(1 + odds<sup>*</sup>(i,j))  (12)

where c = ∑<sub>i,j</sub> 1/(1 + odds<sup>*</sup>(i,j)) is a scale factor, ℓ = N<sub>A</sub>(t) − N<sub>B</sub>(t), i,j ≥ 0 and k = 0, ±1, ±2 . . ..

Moments of the Poisson distribution make it straightforward to derive the moments of a Skel-

lam random variable with parameters λ<sup>A</sup> and λ<sup>B</sup>. The unconditional mean and variance are given

by

E[N(1)] = E[W<sub>A</sub>(1)] − E[W<sub>B</sub>(1)] = λ<sup>A</sup> − λ<sup>B</sup>,

### 视觉备注

- 恢复式(12)求和条件i−j=k−ℓ与归一化因子c；式(11)按当前双方比分平移。

## Page 10: Constrained calibration and game simulation

源页：第 10 页

### 页面目的

- 保留本页 Constrained calibration and game simulation 的原文与论证顺序。

### 布局地图

- 顶部方差式；中部式(13)–(16)；页底Figure 2说明段。

### 按区域确认内容

#### 区域 1：本页正文与已标号数学内容

V[N(1)] = V[W<sub>A</sub>(1)] + V[W<sub>B</sub>(1)] = λ<sup>A</sup> + λ<sup>B</sup>.

Therefore, the conditional moments are given by

E[N(1) | N(t) = ℓ] = ℓ + (λ<sub>t</sub><sup>A</sup> − λ<sub>t</sub><sup>B</sup>),

V[N(1) | N(t) = ℓ] = λ<sub>t</sub><sup>A</sup> + λ<sub>t</sub><sup>B</sup>.  (13)

We also need to ensure that Ê[N(1) | N(t) = ℓ] − ℓ ≤ V̂[N(1) | N(t) = ℓ]. A method of moments estimate of λ’s is given by the solution to

Ê[N(1) | N(t) = ℓ] = ℓ + (λ<sub>t</sub><sup>A</sup> − λ<sub>t</sub><sup>B</sup>),

V̂[N(1) | N(t) = ℓ] = λ<sub>t</sub><sup>A</sup> + λ<sub>t</sub><sup>B</sup>,  (14)

where Ê and V̂ are the expectation and variance calculated using market implied conditional probabilities, could be negative. To address this issue, we define the residuals

D<sub>E</sub> = Ê[N(1) | N(t) = ℓ] − [ℓ + (λ<sub>t</sub><sup>A</sup> − λ<sub>t</sub><sup>B</sup>)],

D<sub>V</sub> = V̂[N(1) | N(t) = ℓ] − (λ<sub>t</sub><sup>A</sup> + λ<sub>t</sub><sup>B</sup>).  (15)

We then calibrate parameters by adding the constraints λ<sub>t</sub><sup>A</sup> ≥ 0 and λ<sub>t</sub><sup>B</sup> ≥ 0 and solving the following equivalent constrained optimization problem.

(λ̂<sub>t</sub><sup>A</sup>, λ̂<sub>t</sub><sup>B</sup>) = arg min<sub>λₜᴬ,λₜᴮ</sub> {D<sub>E</sub><sup>2</sup> + D<sub>V</sub><sup>2</sup>}  (16)

subject to λ<sub>t</sub><sup>A</sup> ≥ 0, λ<sub>t</sub><sup>B</sup> ≥ 0.

Figure 2 illustrates a simulation evolution of an EPL game between Everton and West Ham
(March 5th, 2016) with their estimated parameters. It provides a discretized version of Figure 1 in
Polson and Stern (2015). The outcome probability of first half and updated second half are given
in the left two panels. The top right panel illustrates a simulation-based approach to visualizing
how the model works in the dynamic evolution of score difference. In the bottom left panel, from
half-time onwards, we also simulate a set of possible Monte Carlo paths to the end of the game.
This illustrates the discrete nature of our Skellam process and how the scores evolve.

### 视觉备注

- Ê/V̂帽号及D_E/D_V平方已核对；正文bottom left模拟路径措辞照录，不按图2自行改成bottom right。

## Page 11: Figure 2 — Model Diagnostics

源页：第 11 页

### 页面目的

- 保留 Figure 2 — Model Diagnostics 的本页完整内容。

### 布局地图

- 上方2×2概率/模拟图；长图注；下方2.3正文开头。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

Figure 2: The Skellam process model for winning margin and game simulations. The top left
panel shows the outcome distribution using odds data before the match starts. Each bar repre-
sents the probability of a distinct final score difference, with its color corresponding to the result
of win/lose/draw. Score differences larger than 5 or smaller than -5 are not shown. The top right
panel shows a set of simulated Skellam process paths for the game outcome. The bottom row has
the two figures updated using odds data available at half-time.

2.3 Model Diagnostics

To assess the performance our score-difference Skellam model calibration for the market odds,
we have collected data from ladbrokes.com on the correct score odds of 18 EPL games (from Octo-
ber 15th to October 22nd, 2016) and plot the calibration result in Figure 3. The Q-Q plot of log(odds)

#### 区域 2：上部 Figure 2 四面板的图形内容

| Position | Title | Horizontal axis | Vertical axis | Printed probabilities |
| --- | --- | --- | --- | --- |
| Top left | Probability of Score Difference − Before 1st Half | Score Difference −5 to 5 | Probability (%) 0–25 | West Ham Wins = 23.03%; Draw = 19.50%; Everton Wins = 57.47% |
| Top right | Game Simulations − Before 1st Half | Time 0.0–1.0 | Score Difference −6 to 8 | Coloured discrete simulated paths |
| Bottom left | Probability of Score Difference − Before 2nd Half | Score Difference −5 to 5 | Probability (%) 0–35 | West Ham Wins = 15.74%; Draw = 23.18%; Everton Wins = 61.08% |
| Bottom right | Game Simulations − Before 2nd Half | Time 0.0–1.0 | Score Difference −5 to 5 | Shared observed first-half path, then simulated continuations |

Bars: yellow negative margins, blue zero margin, red positive margins. The simulation panels do not print a path count or fitted intensities.

### 视觉备注

- 四幅图纵轴范围不同，已分别记录；抽取中的重复坐标字符不作为正文。

## Page 12: Figure 3 — Zero-inflated Skellam distribution

源页：第 12 页

### 页面目的

- 保留 Figure 3 — Zero-inflated Skellam distribution 的本页完整内容。

### 布局地图

- 页首数据说明；中部左右诊断图；下部零膨胀式(17)。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

is also shown. In average, there are 13 different outcomes per game, i.e., N(1) = −6, −5, ...0, ..., 5, 6.
In total 238 different outcomes are used. We compare our Skellam implied probabilities with the
market implied probabilities for every outcome of the 18 games. If the model calibration is suf-
ficient, all the data points should lies on the diagonal line. Figure 3 left panel demonstrates that

Figure 3: Left: Market implied probabilities for the score differences versus Skellam implied proba-
bilities. Every data point represents a particular score difference; Right: Market log(odds) quantiles
versus Skellam implied log(odds) quantiles. Market odds (from ladbrokes.com) of 18 games in
EPL 2016-2017 are used (in average 13 score differences per game). The total number of outcomes
is 238.

our Skellam model is calibrated by the market odds sufficiently well, except for the underestimated
draw probabilities. Karlis and Ntzoufras (2009) describe this underestimation phenomenon in a
Poisson-based model for the number of goals scored. Following their approach, we apply a zero-
inflated version of Skellam distribution to improve the fit on draw probabilities, namely

P̃(N(1)=0) = p + (1−p)P(N(1)=0)

P̃(N(1)=x) = (1−p)P(N(1)=x) if x ≠ 0.  (17)

Here 0 < p < 1 is an inflation factor and P̃ denotes the inflated probabilities. We also consider

#### 区域 2：中部 Figure 3 的左右诊断图

Left title: Market Implied Probability vs Skellam Implied Probability. Horizontal axis: Market Implied Probability; vertical axis prints Skellam Implied Proability [source spelling]. Both use 0.00–0.25 ticks. Legend: Home team wins (red), Away team wins (yellow), Draw (blue); black equality diagonal. Right title: Q−Q Plot of Log(odds): Market vs Skellam; horizontal Market Implied Log(odds), vertical Skellam Implied Log(odds), ticks 1–7. The quantile marks are very small; individual values cannot be reliably recovered.

### 视觉备注

- 恢复式(17)的≠0；右侧Q–Q微小点不能可靠逐点读值，不转录抽取的q噪声。

## Page 13: Inflation factors and out-of-sample diagnostics

源页：第 13 页

### 页面目的

- 保留 Inflation factors and out-of-sample diagnostics 的本页完整内容。

### 布局地图

- 上部式(18)；下方庄家解释及1520场样本检验，最后一句跨页。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

another type of inflation here

P̃(N(1)=0) = (1+θ)P(N(1)=0)

P̃(N(1)=x) = (1−γ)P(N(1)=x) if x ≠ 0  (18)

where θ is the inflation factor and P(N(1) = 0) = γ/(γ + θ).
Both types of inflation factors have the corresponding interpretation regarding the bookmak-

ers’ way of setting odds. With the first type of factor, the bookmakers generate two different set of
probabilities, one specifically for the draw probability (namely the inflation factor p) and the other
for all the outcomes using the Skellam model. The “market vig” for all the outcomes is a constant.
With the second type, the bookmakers use the Skellam model to generate the probabilities for all the
outcomes. Then they apply a larger “market vig” for draws than others. Yates (1982) also point out
the “collapsing” tendency in forecasting behavior, whereby the bookmakers are inclined to report
forecasts of 50% when they feel they know little about the event. In Figure 3 right panel, we see that
the Skellam implied log(odds) has a heavier right tail than the market implied log(odds). This effect
results from the overestimation of extreme outcomes, which in turn is due to market microstructure
effect due to the market “vig”.

To assess the out-of-sample predictive ability of the Skellam model, we analyze the market
(win, lose, draw) odds for 1520 EPL games (from 2012 to 2016, 380 games per season). However,
the sample covariance of the end of game scores,N<sub>A</sub>(1) and N<sub>B</sub>(1), is close to 0. If we assume
parameters stay the same, then the estimates are λ̂<sup>A</sup> = 1.5 and λ̂<sup>B</sup> = 1.2. Since the probabilities
of win, lose and draw sum to 1, we only plot the market implied probabilities of win and draw.
In Figure 4 left panel, the draw probability is nearly a non-linear function of the win probability.
To illustrate our model, we set the value of λ<sup>A</sup>λ<sup>B</sup> = 1.5 × 1.2 = 1.8 and plot the curve of Skellam
implied probabilities (red line). We further provide the inflated Skellam probabilities (blue line for
the first type and green line for the second type). As expected, the non-inflated Skellam model (red
line) underestimates the draw probabilities while the second type inflated Skellam model (green
line) produces the better fit. We also group games by the market implied winning probability of
home teams P(N(1) > 0): (0.05,0.1], (0.1,0.15], · · · , (0.8,0.85]. We calculate the frequency of home
team winning for each group. In Figure 4 right panel, the barplot of frequencies (x-axis is regarding


### 视觉备注

- 核对θ/γ/p区别；恢复式(18)≠0及λ̂的上标，保持原文市场vig解释。

## Page 14: Figure 4 — Time-Varying Extension

源页：第 14 页

### 页面目的

- 保留 Figure 4 — Time-Varying Extension 的本页完整内容。

### 布局地图

- 上方左右图4；图注和承接上一页的scaled odds句；下部2.4。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

Figure 4: Left: Market implied probabilities of win and draw. The fitted curves are Skellam implied
probabilities with fixed λ<sup>A</sup>λ<sup>B</sup> = 1.8. Right: Market odds and result frequency of home team win-

ning. 1520 EPL games from 2012 to 2016 are used. The dashed line represents: Frequency = Market

Implied Probability

scaled odds) shows that the market is efficient, i.e., the frequency is close to the corresponding
market implied probability and our Skellam model is calibrated to the market outcome for this
dataset.

2.4 Time-Varying Extension

One extension that is clearly warranted is allowing for time-varying {λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>} where the Skel-
lam model is re-calibrated dynamically through updated market odds during the game. We use the
current {λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>} to project possible results of the match in our Skellam model. Here {λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>} re-
veal the market expectation of scoring difference for both teams from time t to the end of the game
as the game progresses. Similar to the martingale approach of Polson and Stern (2015), {λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>}
reveal the best prediction of the game result. From another point of view, this approach is the same
as assuming homogeneous rates for the rest of the game.

An alternative approach to time-varying {λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>} is to use a Skellam regression with condi-
tioning information such as possession percentages, shots (on goal), corner kicks, yellow cards, red

#### 区域 2：上部 Figure 4 两幅图

Left title: Skellam Model with Inflated Zero and Fix Parameter Product. Horizontal: Probability of Home Team Winning (0.2,0.4,0.6,0.8); vertical: Probability of Draw (0.10–0.30). Legend: No Inflation (red), Type I, p = 0.04 (blue), Type II, theta = 0.12 (green), with black market crosses.

Right title: Home Team Wins: Odds vs. Frequency. Horizontal Market Odds (Scaled), labelled 19/1,11/2,3/1,2/1,6/5,4/5,1/2,3/10,1/5. Vertical Frequency (0.0,0.2,0.4,0.6,0.8). Yellow-to-red bars and black equality reference line; individual bar frequencies are not printed.

### 视觉备注

- 图例p=0.04、theta=0.12与λᴬλᴮ=1.8已核对；Fix及右侧线型按原文保留。

## Page 15: Example: Everton vs West Ham (3/5/2016)

源页：第 15 页

### 页面目的

- 保留 Example: Everton vs West Ham (3/5/2016) 的本页完整内容。

### 布局地图

- 上部式(19)；中部第3节与3.1；页底goodness-跨页。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

cards, etc. We would expect jumps in the {λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>} during the game when some important events
happen. A typical structure takes the form

log(λ<sub>t</sub><sup>A</sup>) = α<sub>A</sub> + β<sub>A</sub>X<sub>A,t−1</sub>

log(λ<sub>t</sub><sup>B</sup>) = α<sub>B</sub> + β<sub>B</sub>X<sub>B,t−1</sub>,  (19)

estimated using standard log-linear regression.
Our approach relies on the betting market being efficient so that the updating odds should

contain all information of game statistics. Using log differences as the dependent variable is another
alternative with a state space evolution. Koopman et al. (2014) adopt stochastically time-varying
densities in modeling the Skellam process. Barndorff-Nielsen et al. (2012) is another example of the
Skellam process with different integer valued extensions in the context of high-frequency financial
data. Further analysis is required, and this produces a promising area for future research.

3 Example: Everton vs West Ham (3/5/2016)

We collect the real-time online betting odds data from ladbrokes.com for an EPL game be-
tween Everton and West Ham on March 5th, 2016. By collecting real-time online betting data for
every 10-minute interval, we can show the evolution of betting market prediction on the final re-
sult. We do not account for the overtime for both 1st half and 2nd half of the match and focus on a
90-minute game.

3.1 Implied Skellam Probabilities

Table 1 shows the raw data of odds right the game. We need to transform odds data into
probabilities. For example, for the outcome 0-0, 11/1 is equivalent to a probability of 1/12. Then
we can calculate the marginal probability of every score difference from -4 to 5. We neglect those
extreme scores with small probabilities and rescale the sum of event probabilities to one.

In Figure 5, the probabilities estimated by the model are compared with the market implied
probabilities. As we see, during the course of the game, the Skellam assumption suffices to approx-
imate market expectation of score difference distribution. This set of plots is evidence of goodness-


### 视觉备注

- 3/5/2016由正文March 5th确认；保留原文Table 1 shows...right the game，不改语病。

## Page 16: Table 1 — Figure 5 calibration across time

源页：第 16 页

### 页面目的

- 保留 Table 1 — Figure 5 calibration across time 的本页完整内容。

### 布局地图

- 上部9行赔率矩阵；中部3×3时点面板；图注和两句残段在下。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

| Everton \West Ham | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 11/1 | 12/1 | 28/1 | 66/1 | 200/1 | 450/1 |
| 1 | 13/2 | 6/1 | 14/1 | 40/1 | 100/1 | 350/1 |
| 2 | 7/1 | 7/1 | 14/1 | 40/1 | 125/1 | 225/1 |
| 3 | 11/1 | 11/1 | 20/1 | 50/1 | 125/1 | 275/1 |
| 4 | 22/1 | 22/1 | 40/1 | 100/1 | 250/1 | 500/1 |
| 5 | 50/0 | 50/1 | 90/1 | 150/1 | 400/1 | |
| 6 | 100/1 | 100/1 | 200/1 | 250/1 | | |
| 7 | 250/1 | 275/1 | 375/1 | | | |
| 8 | 325/1 | 475/1 | | | | |

Table 1: Original odds data from Ladbrokes before the game started

#### 区域 2：中部 Figure 5 的 3×3 面板

**Market Implied Probability vs Skellam Implied Probability**

| Top row | Middle row | Bottom row |
| --- | --- | --- |
| t = 0 | t = 0.33 | t = 0.72 |
| t = 0.11 | t = 0.44 | t = 0.83 |
| t = 0.22 | t = 0.61 | t = 0.94 |

Horizontal axis: Score Difference (−4,−3,−2,−1,0,1,2,3,4,5). Vertical axis: Probability (%) (0,20,40,60). Legend Type: Market Implied Prob. (red circles), Skellam Implied Prob. (cyan triangles). The curves compare market and fitted score-difference probabilities at each labelled time; no exact point values are printed.

Figure 5: Market implied probabilities versus the probabilities estimated by the model at different
time points, using the parameters given in Table 3 .

of-fit the Skellam model.
Table 2 shows the model implied probability for the outcome of score differences before the


### 视觉备注

- Table 1的50/0为原页印字，未修成50/1；所有10个空格保留为空。面板未列逐点概率。

## Page 17: Table 2 — Figure 6 outcome probabilities

源页：第 17 页

### 页面目的

- 保留 Table 2 — Figure 6 outcome probabilities 的本页完整内容。

### 布局地图

- 页顶Table 2及说明；中部Figure 6堆叠图；下部比赛事件正文。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

| Score difference | −4 | −3 | −2 | −1 | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Market Prob. (%) | 1.70 | 2.03 | 4.88 | 12.33 | 21.93 | 22.06 | 16.58 | 9.82 | 4.72 | 2.23 |
| Skellam Prob.(%) | 0.78 | 2.50 | 6.47 | 13.02 | 19.50 | 21.08 | 16.96 | 10.61 | 5.37 | 2.27 |

Table 2: Market implied probabilities for the score differences versus Skellam implied probabilities
at different time points. The estimated parameters λ̂<sup>A</sup> = 2.33, λ̂<sup>B</sup> = 1.44.

game, compared with the market implied probability. As we see, the Skellam model appears to
have longer tails. Different from independent Poisson modeling in Dixon and Coles (1997), our
model is more flexible with the correlation between two teams. However, the trade-off of flexibility
is that we only know the probability of score difference instead of the exact scores.

Figure 6: The betting market data for Everton and West Ham is from ladbrokes.com. Market
implied probabilities (expressed as percentages) for three different results (Everton wins, West Ham
wins and draw) are marked by three distinct colors, which vary dynamically as the game proceeds.
The solid black line shows the evolution of the implied volatility (defined in Section 3.2). The
dashed line shows significant events in the game, such as goals and red cards. Five goals in this
game are 13’ Everton, 56’ Everton, 78’ West Ham, 81’ West Ham and 90’ West Ham.

Finally, we can plot these probability paths in Figure 6 to examine the behavior of the two
teams and represent the market predictions on the final result. Notably, we see the probability
change of win/draw/loss for important events during the game: goals scoring and a red card
penalty. In such a dramatic game, the winning probability of Everton gets raised to 90% before the

#### 区域 2：中部 Figure 6 胜平负堆叠图

PROBABILITY OF EITHER TEAM WINNING. Horizontal: 0–90 minutes with Half time marker; vertical total: 100%. Printed initial probabilities: Everton 57.5% (blue), Draw 19.5% (grey), West Ham 23% (burgundy). Event annotations: Everton goal, Everton red card, Everton goal, and three West Ham goals. The caption gives goal times 13′,56′,78′,81′,90′. The band thickness, not cumulative boundary height, represents each outcome probability.

### 视觉备注

- Table 2参数2.33/1.44及20个概率核对；图6caption提及黑线但原图无清晰独立黑色波动率曲线，原文保留。

## Page 18: How the Market Forecast Adapts

源页：第 18 页

### 页面目的

- 保留 How the Market Forecast Adapts 的本页完整内容。

### 布局地图

- 顶部承接逆转段；3.2标题；四段正文，σ公式为行内。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

first goal of West Ham in 78th minutes. The first two goals scored by West Ham in the space of 3
minutes completely reverses the probability of winning. The probability of draw gets raised to 90%
until we see the last-gasp goal of West Ham that decides the game.

3.2 How the Market Forecast Adapts

A natural question arises to how does the market odds (win, lose, draw and actual score) adjust
as the game evolves. This is similar to option pricing where Black-Scholes model uses its implied
volatility to show how market participants’ beliefs change. Our Skellam model mimics its way and
shows how the market forecast adapts to changing situations during the game. See Merton (1976)
for references of jump models.

Our work builds on Polson and Stern (2015) who define the implied volatility of a NFL game.
For an EPL game, we simply define the implied volatility as σ<sub>IV,t</sub> = √(λ<sub>t</sub><sup>A</sup> + λ<sub>t</sub><sup>B</sup>). As the market
provides real-time information about λ<sub>t</sub><sup>A</sup> and λ<sub>t</sub><sup>B</sup>, we can dynamically estimate σ<sub>IV,t</sub> as the game
proceeds. Any goal scored is a discrete Poisson shock to the expected score difference (Skellam
process) between the teams, and our odds implied volatility measure will be updated.

Figure 6 plots the path of implied volatility throughout the course of the game. Instead of a
downward sloping line, we see changes in the implied volatility as critical moments occur in the
game. The implied volatility path provides a visualization of the conditional variation of the market
prediction for the score difference. For example, when Everton lost a player by a red card penalty
at 34th minute, our estimates λ̂<sub>t</sub><sup>A</sup> and λ̂<sub>t</sub><sup>B</sup> change accordingly. There is a jump in implied volatility
and our model captures the market expectation adjustment about the game prediction. The change
in λ̂<sub>A</sub> and λ̂<sub>B</sub> are consistent with the findings of Vecer et al. (2009) where the scoring intensity of the
penalized team drops while the scoring intensity of the opposing team increases. When a goal is
scored in the 13th minute, we see the increase of λ̂<sub>t</sub><sup>B</sup> and the market expects that the underdog team
is pressing to come back into the game, an effect that has been well-documented in the literature.
Another important effect that we observe at the end of the game is that as goals are scored (in the
78th and 81st minutes), the markets expectation is that the implied volatility increases again as one
might expect.

Figure 7 compares the updating implied volatility of the game with implied volatilities of fixed


### 视觉备注

- 恢复σ_IV,t平方根；原文同时使用λ̂ₜᴬ/λ̂ₜᴮ与λ̂_A/λ̂_B，未统一。红牌34分钟为正文值。

## Page 19: Figure 7 — Table 3 implied volatility

源页：第 19 页

### 页面目的

- 保留 Figure 7 — Table 3 implied volatility 的本页完整内容。

### 布局地图

- 上部红/蓝波动率曲线；中部Table 3；下部强度解释正文跨页。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

Figure 7: Red line: the path of implied volatility throughout the game, i.e., σ<sub>t</sub><sup>red</sup> = √(λ̂<sub>t</sub><sup>A</sup> + λ̂<sub>t</sub><sup>B</sup>). Blue lines: the path of implied volatility with constant λ<sup>A</sup> + λ<sup>B</sup>, i.e., σ<sub>t</sub><sup>blue</sup> = √((λ<sup>A</sup> + λ<sup>B</sup>) * (1−t)). Here (λ<sup>A</sup> + λ<sup>B</sup>) = 1,2,...,8.

#### 区域 2：中部 Table 3

| t | 0 | 0.11 | 0.22 | 0.33 | 0.44 | 0.50 | 0.61 | 0.72 | 0.83 | 0.94 | 1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| λ̂<sub>t</sub><sup>A</sup>/(1−t) | 2.33 | 2.51 | 2.53 | 2.46 | 1.89 | 1.85 | 2.12 | 2.12 | 2.61 | 4.61 | 0 |
| λ̂<sub>t</sub><sup>B</sup>/(1−t) | 1.44 | 1.47 | 1.59 | 1.85 | 2.17 | 2.17 | 2.56 | 2.90 | 3.67 | 5.92 | 0 |
| (λ̂<sub>t</sub><sup>A</sup>+λ̂<sub>t</sub><sup>B</sup>)/(1−t) | 3.78 | 3.98 | 4.12 | 4.31 | 4.06 | 4.02 | 4.68 | 5.03 | 6.28 | 10.52 | 0 |
| σ<sub>IV,t</sub> | 1.94 | 1.88 | 1.79 | 1.70 | 1.50 | 1.42 | 1.35 | 1.18 | 1.02 | 0.76 | 0 |

Table 3: The calibrated {λ̂<sub>t</sub><sup>A</sup>, λ̂<sub>t</sub><sup>B</sup>} divided by (1 − t) and the implied volatility during the game.
{λ<sub>t</sub><sup>A</sup>, λ<sub>t</sub><sup>B</sup>} are expected goals scored for rest of the game. The less the remaining time, the less likely
to score goals. Thus {λ̂<sub>t</sub><sup>A</sup>, λ̂<sub>t</sub><sup>B</sup>} decrease as t increases to 1. Diving them by (1 − t) produces an
updated version of λˆ 0’s for the whole game, which are in general time-varying (but not decreasing
necessarily).

(λ<sup>A</sup> + λ<sup>B</sup>). At the beginning of the game, the red line (updating implied volatility) is under the
”(λ<sup>A</sup> + λ<sup>B</sup> = 4)”-blue line; while at the end of the game, it’s above the ”(λ<sup>A</sup> + λ<sup>B</sup> = 8)”-blue line.
As we expect, the value of (λ̂<sub>t</sub><sup>A</sup> + λ̂<sub>t</sub><sup>B</sup>)/(1 − t) in Table 3 increases throughout the game, implying
that the game became more and more intense and the market continuously updates its belief in the

#### 区域 3：上部 Figure 7 曲线及事件标记

Title: Implied volatility with updating / constant lambdas. Horizontal axis prints Time (miniute) [source spelling], ticks 0,20,40,60,80 minutes. Vertical: Implied Volatility, ticks 0.0–3.0. Red updated curve; blue curves labelled 1–8 for constant intensity sums. Vertical event annotations: Goal:E, Red Card:E, Half Time, Goal:E, Goal:W, Goal:W, Goal:W.

### 视觉备注

- Table 3的t=0.83波动率经局部原分辨率复核为1.02；终点分母1−t为零而源表仍写0，照录不计算更正。

## Page 20: Discussion

源页：第 20 页

### 页面目的

- 保留 Discussion 的本页完整内容。

### 布局地图

- 页首单词odds.；4 Discussion标题；三段单栏正文。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

odds.

4 Discussion

The goal of our analysis is to provide a probabilistic methodology for calibrating real-time
market odds for the evolution of the score difference for a soccer game.Rather than directly using
game information, we use the current odds market to calibrate a Skellam model to provide a forecast
of the final result. To our knowledge, our study is the first to offer an interpretation of the betting
market and to show how it reveals the market expectation of the game result through an implied
volatility. One area of future research is studying the index betting. For example, a soccer game
includes total goals scored in match and margin of superiority (see Jackson (1994)). The latter is the
score difference in our model, and so the Skellam process directly applies.

Our Skellam model is also valid for low-scoring sports such as baseball, hockey or American
football with a discrete series of scoring events. For NFL score prediction, Baker and McHale (2013)
propose a point process model that performs as well as the betting market. On the one hand,
our model has the advantage of implicitly considering the correlation between goals scored by
both teams but on the other hand, ignores the sum of goals scored. For high-scoring sports, such
as basketball, the Brownian motion adopted by Stern (1994) is more applicable. Rosenfeld (2012)
provides an extension of the model that addresses concerns of non-normality and uses a logistic
distribution to estimate the relative contribution of the lead and the remaining advantage. Another
avenue for future research, is to extend the Skellam model to allow for the dependent jumpiness of
scores which is somewhere in between these two extremes (see Glickman and Stern (1998), Polson
and Stern (2015) and Rosenfeld (2012) for further examples.)

Our model allows the researcher to test the inefficiency of EPL sports betting from a statistical
arbitrage viewpoint. More importantly, we provide a probabilistic approach for calibrating dynamic
market-based information. Camerer (1989) shows that the market odds are not well-calibrated and
that an ultimate underdog during a long losing streak is underpriced on the market. Golec and
Tamarkin (1991) test the NFL and college betting markets and find bets on underdogs or home
teams win more often than bets on favorites or visiting teams. Gray and Gray (1997) examine the
in-sample and out-of-sample performance of different NFL betting strategies by the probit model.


### 视觉备注

- 无图表和编号公式；保留model discussion及跨页NFL策略句。

## Page 21: Discussion — concluding paragraph

源页：第 21 页

### 页面目的

- 保留 Discussion — concluding paragraph 的本页完整内容。

### 布局地图

- 仅页首三行承接上一页；下方大面积留白。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

They find the strategy of betting on home team underdogs averages returns of over 4 percent, over
commissions. In summary, a Skellam process appears to fit the dynamics of EPL soccer betting very
well and produces a natural lens to view these market efficiency questions.


### 视觉备注

- 原页确为稀疏结尾页，无遗漏整页内容；over commissions原措辞保留。

## Page 22: References — Alzaid to Glickman

源页：第 22 页

### 页面目的

- 保留 References — Alzaid to Glickman 的本页完整内容。

### 布局地图

- References标题；11条单栏悬挂缩进文献；页码22。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

References

Alzaid, A. A., M. A. Omair, et al. (2010). On the poisson difference distribution inference and
applications. Bulletin of the Malaysian Mathematical Sciences Society 8(33), 17–45.

Avery, C. and J. Chevalier (1999, October). Identifying Investor Sentiment from Price Paths: The
Case of Football Betting. The Journal of Business 72(4), 493–521.

Baker, R. D. and I. G. McHale (2013). Forecasting exact scores in national football league games.
International Journal of Forecasting 29(1), 122–130.

Barndorff-Nielsen, O. E., D. G. Pollard, and N. Shephard (2012). Integer-valued Levy processes and
low latency financial econometrics. Quantitative Finance 12(4, SI), 587–605.

Barndorff-Nielsen, O. E. and N. Shephard (2012). Basics of levy processes. Technical report, Eco-
nomics Group, Nuffield College, University of Oxford.

Camerer, C. F. (1989). Does the basketball market believe in the ’hot hand’? American Economic
Review 22(4), 76–76.

Dixon, M. J. and S. G. Coles (1997, January). Modelling Association Football Scores and Ineffi-
ciencies in the Football Betting Market. Journal of the Royal Statistical Society. Series C (Applied
Statistics) 46(2), 265–280.

Dixon, M. J. and P. F. Pope (2004, October). The Value of Statistical Forecasts in the UK Association
Football Betting Market. International Journal of Forecasting 20(4), 697–711.

Fitt, A. D. (2009, April). Markowitz Portfolio Theory for Soccer Spread Betting. IMA Journal of
Management Mathematics 20(2), 167–184.

Fitt, A. D., C. J. Howls, and M. Kabelka (2005, September). Valuation of Soccer Spread Bets. Journal
of the Operational Research Society 57(8), 975–985.

Glickman, M. E. and H. S. Stern (1998, February). A State-Space Model for National Football League
Scores. Journal of the American Statistical Association 93(441), 25–35.


### 视觉备注

- 首条卷期8(33)与原页一致，不以外部数据库更正；没有图或公式。

## Page 23: References — Golec to Sellers

源页：第 23 页

### 页面目的

- 保留 References — Golec to Sellers 的本页完整内容。

### 布局地图

- 13条续页文献，自Golec到Sellers，悬挂缩进。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

Golec, J. and M. Tamarkin (1991, December). The Degree of Inefficiency in the Football Betting
Market: Statistical Tests. Journal of Financial Economics 30(2), 311–323.

Gray, P. K. and S. F. Gray (1997, September). Testing Market Efficiency: Evidence From The NFL
Sports Betting Market. The Journal of Finance 52(4), 1725–1737.

Jackson, D. A. (1994). Index Betting on Sports. The Statistician 43(2), 309.

Karlis, D. and I. Ntzoufras (2003, October). Analysis of Sports Data by Using Bivariate Poisson
Models. Journal of the Royal Statistical Society: Series D (The Statistician) 52(3), 381–393.

Karlis, D. and I. Ntzoufras (2009, April). Bayesian Modelling of Football Outcomes: Using the
Skellam’s Distribution for the Goal Difference. IMA Journal of Management Mathematics 20(2),
133–145.

Koopman, S. J., R. Lit, and A. Lucas (2014). The dynamic skellam model with applications. Tinbergen
Institute Discussion Paper 14-032/IV/DSF73.

Lee, A. J. (1997, September). Modeling Scores in the Premier League: Is Manchester United Really
the Best? Chance 10(1), 15–19.

Levitt, S. D. (2004). Why are gambling markets organized so differently from financial markets?
Economic Journal 114(3), 223–246.

Maher, M. J. (1982, September). Modelling Association Football Scores. Statistica Neerlandica 36(3),
109–118.

Merton, R. C. (1976, January). Option Pricing when Underlying Stock Returns are Discontinuous.
Journal of Financial Economics 3(1-2), 125–144.

Polson, N. G. and H. S. Stern (2015). The Implied Volatility of a Sports Game. Journal of Quantitative
Analysis in Sports 11(2), 145–153.

Rosenfeld, J. W. (2012). An in-game win probability model of the NBA. Thesis, Harvard University.

Sellers, K. F. (2012). A Distribution Describing Differences in Count Data Containing Common
Dispersion Levels. Advances and Applications in Statistical Sciences 7(3), 35–46.


### 视觉备注

- Koopman报告号14-032/IV/DSF73按原页保留；没有References重复标题。

## Page 24: References — Skellam to Yates

源页：第 24 页

### 页面目的

- 保留 References — Skellam to Yates 的本页完整内容。

### 布局地图

- 四条文献位于上半页；下方空白和页码24。

### 按区域确认内容

#### 区域 1：本页主要正文、表格与图注

Skellam, J. G. (1946, January). The Frequency Distribution of the Difference Between Two Poisson
Variates Belonging to Different Populations. Journal of the Royal Statistical Society 109(3).

Stern, H. S. (1994). A Brownian Motion Model for the Progress of Sports Scores. Journal of the
American Statistical Association 89(427), 1128–1134.

Vecer, J., F. Kopriva, T. Ichiba, et al. (2009). Estimating the effect of the red card in soccer: When to
commit an offense in exchange for preventing a goal opportunity. Journal of Quantitative Analysis
in Sports 5(1), 1–20.

Yates, J. F. (1982). External correspondence: Decompositions of the mean probability score. Organi-
zational Behavior and Human Performance 30(1), 132–156.


### 视觉备注

- Skellam条目源文无页码，未补写；Yates期刊跨行断词可合并，不改名称。





