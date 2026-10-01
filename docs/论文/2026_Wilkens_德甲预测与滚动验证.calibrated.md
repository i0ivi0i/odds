# Research article

> 重建说明：模式 transcribe；来源 `2026_Wilkens_德甲预测与滚动验证.pdf`；共 18 页；原图逐页查看 1/18 页。
>
> 补充：正文按 PDF 文字层原样转写，未改写、未翻译、未凭看图补字。公式和上下标若在文字层里已经乱，保留原样，以 PDF 原页为准，不许猜。 已对原图：第1页（题名 Can simple models predict football...）。未列入的页只核对了文字层与页码，未打开原图。

## Page 01: Research article

源页：第 1 页

Research article

                                                                                                                              Journal of Sports Analytics

Can simple models predict football —
                                                                                                                                         Vol. 12(0): 1–18
                                                                                                                                   © The Author(s) 2026
                                                                                                                                 Article reuse guidelines:
and beat the odds? Lessons from the                                                                                    sagepub.com/journals-permissions
                                                                                                                      DOI: 10.1177/22150218261416681

German Bundesliga                                                                                                         journals.sagepub.com/home/san




Sascha Wilkens1,*


Abstract
This study examines whether a simple model based on expected goals (xG) can generate accurate forecasts and identify
proﬁtable signals in football betting markets. The model uses recent xG to estimate win–draw–loss probabilities via a
Skellam distribution, with isotonic regression applied for calibration, and evaluates the performance over eleven
Bundesliga seasons (2014/15 through 2024/25). While bookmaker odds tend to exhibit superior statistical calibration,
the xG-based model captures certain signals not fully reﬂected in market prices. In simulated betting, the model yields
a return on investment of approximately 10% using average market odds, increasing to nearly 15% under the best available
prices. Proﬁts stem predominantly from home win bets, while backing away wins is consistently loss-making. The results
show some robustness to modelling choices, though proﬁtability varies considerably by season and bet type. The study
highlights the potential of simple models as practical tools for identifying predictive value in structured football data.

Keywords
football forecasting, expected goals (xG), betting markets, value betting, Bundesliga
Received: 11 August 2025; accepted: 30 December 2025




Introduction                                                                models may capture distinct patterns or structural tendencies
                                                                            that are underweighted or overlooked by the market.
Forecasting football match outcomes has drawn sustained                        Despite their appeal, predictive models in football face
academic and practitioner interest, particularly as granular                the sport’s inherent complexity. Outcomes are shaped by
performance metrics such as expected goals (xG) have
                                                                            low-frequency, high-impact events and inﬂuenced by a
enabled more systematic modelling of team strength and                      wide range of factors. Betting markets, while often
match dynamics. Initially developed within online analytics                 information-efﬁcient, embed structural features and behav-
communities, xG is now deeply embedded in modern foot-
                                                                            ioural biases that complicate the interpretation of odds.
ball practice. English Premier League clubs, for instance,                  These challenges necessitate models that are both statistic-
use xG-based frameworks to inform player recruitment                        ally coherent and robust to real-world constraints.
and tactical decisions, supported by evidence of substantial
                                                                               This paper contributes to the literature by systematically
value generation through data-informed strategies (Tippett,                 evaluating the predictive and economic value of a simple,
2019, 2024). These models evaluate shot quality and efﬁ-                    robust model for the German Bundesliga. Using eleven
ciency rather than raw outcomes such as scored goals,
allowing probabilistic assessments that are more robust to
randomness and variance in match results. They also                         1
provide an empirical basis for estimating outcome probabil-                     Independent researcher, London, United Kingdom
ities that can be compared and potentially combined with                    *The views expressed in this paper are those of the author and do not
those implied by bookmaker odds. Methodologies used to                      necessarily reﬂect the views and policies of any company he is afﬁliated
evaluate football markets mirror techniques in ﬁnancial                     with. The contents do not constitute investment advice.
and economic forecasting, where market data act as                          Corresponding author:
proxies for latent probabilities (Kain and Logan, 2014).                    Sascha Wilkens, Independent researcher, London, United Kingdom.
Even when their forecasts are not perfectly calibrated, such                Email: Wilkens@gmx.de

                  Creative Commons Non Commercial CC BY-NC: This article is distributed under the terms of the Creative Commons Attribution-
                  NonCommercial 4.0 License (https://creativecommons.org/licenses/by-nc/4.0/) which permits non-commercial use, reproduction and
distribution of the work without further permission provided the original work is attributed as speciﬁed on the SAGE and Open Access page (https://us.
sagepub.com/en-us/nam/open-access-at-sage).

## Page 02: 2 Journal of Sports Analytics

源页：第 2 页

2                                                                                                      Journal of Sports Analytics


seasons of data, it applies this xG-based framework to           Previous research
convert recent match performance into outcome probabil-
                                                                 Football outcome prediction has been studied through three
ities, ﬁnetuned through isotonic regression. These forecasts
                                                                 principal lenses: statistical modelling, market-based infer-
are compared with bookmaker-implied probabilities in
                                                                 ence and hybrid or machine learning approaches. Each
terms of calibration and predictive accuracy and used to
                                                                 reﬂects a different philosophy of how match dynamics
identify value bets in simulated betting strategies. A dedi-
                                                                 and uncertainty can be understood, with implications for
cated robustness check also examines how much of the eco-
                                                                 model calibration, practical implementation and relevance
nomic performance is attributable to the isotonic calibration
                                                                 to betting contexts.
layer. While xG-based forecasts are slightly less well cali-
brated than market odds, they capture certain signals that
translate into consistent, albeit modest, proﬁtability:
average market odds yield a return on investment (ROI) of        Statistical modelling approaches
about 10%, increasing to nearly 15% under best-available         Statistical models have long underpinned football forecast-
prices. Selective strategies optimised for ROI or Sharpe         ing, with Poisson-based methods providing the foundation.
ratio can exceed 10%, though based on a relatively small
                                                                 Maher (1982) modelled goals as independent Poisson pro-
number of bets. Notably, home win bets generate the bulk         cesses linked to team strengths; Dixon and Coles (1997)
of proﬁts, while away bets remain persistently unproﬁtable.      introduced temporal weighting and corrections for low-
These ﬁndings remain largely robust across seasons, param-
                                                                 scoring outcomes and inefﬁciencies.
eter variations and staking approaches.                              The Skellam distribution, capturing the difference between
    Conceptually, this study is related to the xG-based per-     two Poisson variables, naturally models win-draw-loss results.
formance framework of Brechot and Flepp (2020), who
                                                                 Karlis and Ntzoufras (2009) used Bayesian estimation in this
analyse how random variation in ﬁnishing and goalkeeping         setting, while Xenopoulos (2016) conﬁrmed its empirical val-
distorts observed results and construct xG-based efﬁciency       idity. However, the assumption of goal independence is often
ratios and league tables for ex-post assessment of team per-     disputed. Bivariate Poisson models address this by introducing
formance. In contrast, the present paper examines whether a      scoring correlation, improving the modelling of draws, as
similarly parsimonious xG-driven model can deliver eco-          shown by Karlis and Ntzoufras (2003) and Groll et al.
nomically valuable ex-ante forecasts and reveal mispricings      (2018). More ﬂexible dynamic or latent-state approaches –
in football betting markets.                                     e.g. the score-driven multivariate models of Koopman and
    The paper is organised as follows. In Section “Previous      Lit (2015) and the copula-structured hidden Markov model
research”, a structured overview of prior research on foot-      of Ötting et al. (2023) – enhance ﬁt but reduce interpretability
ball forecasting is provided, covering statistical models,       and increase calibration effort. Michels et al. (2025) cater for a
market-based approaches, hybrid methods and supporting           more general dependence structure and show that richer correl-
literature. In Section “Data and modelling framework”,           ation patterns can substantially improve ﬁt.
                                                                     Recent xG models estimate scoring potential from
the data are introduced and the modelling framework is out-
                                                                 shot-level data – e.g. location, angle, assist type – offering
lined, based on expected goals and the derivation of prob-
                                                                 more stable proxies for team strength than realised goals.
abilistic forecasts. Furthermore, a post-calibration             Brechot and Flepp (2020) use such an xG framework to dis-
ﬁnetuning of the model forecasts through isotonic regres-        entangle luck from skill in realised results, constructing
sion is discussed. Potential value betting strategies are        xG-based league tables and offensive/defensive efﬁciency
described in Section “Devising a betting strategy”.              ratios that show how short runs of matches can diverge
Besides the identiﬁcation of opportunities and baseline          from underlying performance. Fu (2024) and Mead et al.
benchmarks, several money management strategies are              (2023) highlight how feature choice and data source
introduced. Section “Results” presents the main results,         impact predictive accuracy. Dynamic rating systems such
beginning with an evaluation of the model’s calibration          as Elo and pi-ratings, which update based on results, goal
and predictive accuracy and then evaluating the proﬁtability     margins and opponent strength, remain widely used and
of betting strategies after threshold optimisation, including    have outperformed ofﬁcial rankings in predictive tasks
                                                                 (Hvattum and Arntzen, 2010; Lasek et al., 2013). A
performance by bet type. In Section “Robustness and sensi-
                                                                 recent comprehensive treatment of these models and their
tivity analysis”, the robustness and sensitivity of results to   implementation in football contexts is provided by Egidi
key modelling choices are explored, focusing on                  et al. (2025).
elements such as the historical xG calibration window,               Together, these statistical approaches form the backbone
odds selection, staking method and the use or omission of        of football forecasting, with ongoing work focused on reﬁn-
isotonic calibration. Section “Conclusion and outlook” con-      ing match dynamics, enriching input features and improv-
cludes and outlines avenues for future research.                 ing evaluation.

## Page 03: Wilkens 3

源页：第 3 页

Wilkens                                                                                                                   3


Market-based models and efﬁciency                                   Overall, markets appear broadly – but not fully – efﬁ-
                                                                cient. Odds embed rich information but remain subject to
Betting markets serve as a benchmark for probabilistic fore-
                                                                frictions and behavioural distortions.
casts, aggregating public sentiment, expert judgement and
contextual factors. While generally effective at incorporat-
ing information, they show structural and behavioural pat-      Hybrid and machine learning approaches
terns that can lead to persistent mispricing – creating
                                                                Machine learning (ML) has become prominent in football
scope for model-based strategies.
                                                                prediction, offering tools to model nonlinear patterns and
    A key research strand evaluates market efﬁciency ex
                                                                feature interactions. These approaches often extend clas-
post. Forrest et al. (2005), Goddard and Asimakopoulos
                                                                sical models, especially when leveraging domain-speciﬁc
(2004) and Vlastakis et al. (2009) show that while book-
                                                                inputs like expected goals, team ratings or recent form.
maker odds are well calibrated, they are not fully efﬁcient.
                                                                Methods include tree-based ensembles, support vector
Mispricings stem from overrounds, limited competition,
                                                                machines (SVM), neural networks and probabilistic graph-
pricing conventions and behavioural biases. Using a com-
                                                                ical models.
bination of Monte Carlo simulations and multi-season
                                                                    Bayesian networks capture uncertainty and structural
European football odds, Winkelmann et al. (2024) caution
                                                                dependencies in outcomes. Joseph et al. (2006) demon-
that many reported anomalies are consistent with sampling
                                                                strated early promise, with later work integrating form
variation and ﬁnd little evidence of persistent, exploitable    and rating dynamics. Comparative studies benchmark ML
inefﬁciencies. Work on value betting explores proﬁtability.     models against Poisson or Elo-type baselines. Singh et al.
Franck et al. (2010) ﬁnd better pricing accuracy on             (2025) and Fischer and Heuer (2025) evaluate families
exchanges than with bookmakers. Feng et al. (2016) infer        like SVMs, random forests and neural networks, often con-
scoring intensities from odds using a Skellam framework         cluding that feature quality matters more than model class.
and improve calibration by adjusting for draw overpricing.          Some work assesses proﬁtability as well as accuracy.
Kaunitz et al. (2017) use simple ﬁlters to identify proﬁtable   Stübinger and Knoll (2018) and Hubacek et al. (2019) simu-
strategies, while Constantinou et al. (2013) apply Bayesian     late betting strategies using ML forecasts, highlighting the
networks that outperform odds. Egidi et al. (2025: Chapter      importance of calibrated inputs and market-derived fea-
7) provide a recent, systematic comparison between              tures. Tree-based methods generally perform well, but
state-of-the-art statistical models and bookmaker odds, like-   rely heavily on effective feature engineering. Baboota and
wise concluding that margins and small, unstable mispri-        Kaur (2019), Kozak and Glowania (2021) and
cings leave limited scope for persistent outperformance.        Edalatpanah and Hess (2024) report strong results across
    Implied probability calibration is central. Strumbelj       top European leagues, particularly for high-conﬁdence pre-
(2014) proposes margin-adjusted methods to reconstruct          dictions. Berrar et al. (2024) likewise emphasise that
fair odds and enable comparison with model forecasts.           thoughtful feature design often outweighs algorithmic
Behavioural biases are well documented. Franke (2020)           complexity.
and Brown and Yang (2021) examine phenomena such as                 Recent work integrates spatiotemporal and player-level
the favourite-longshot bias and other pricing distortions.      data. Hewitt and Karakus (2023) enhance xG models with
Drawing on in-play Bundesliga odds and volumes, Ötting          player roles and context, while Bialkowski et al. (2014)
et al. (2025) ﬁnd that bettors behave as if equalisers          use unsupervised learning to extract team formations – sig-
create strong momentum, even though estimated win prob-         nalling a shift toward tactical modelling beyond team aggre-
abilities change little, underscoring the psychological com-    gates. Explainability is gaining focus. Cavus and Biecek
ponent of pricing. Brown and Yang (2019) show that              (2022) apply SHAP and LIME to xG-based models,
forecast accuracy improves with crowd diversity and             improving interpretability and supporting transparent
market depth.                                                   decision-making.
    In-play and high-frequency studies offer a dynamic              Together, machine learning methods offer promising
view. Croxson and Reade (2014) show that exchange               applications to football forecasting, though their success
odds adjust almost instantaneously to goals and display         depends critically on feature design, calibration and
little subsequent drift, while Winkelmann and Deutscher         interpretability.
(2025) ﬁnd no systematic adjustment of odds or stakes in
the seconds leading up to goals in the Bundesliga, suggest-
ing that markets neither strongly anticipate nor underreact     Other approaches and supporting literature
to such events. Michels et al. (2023) and Ötting et al.         Beyond core modelling, related work addresses evaluation
(2024) document strong shifts in trading volume and             metrics, betting strategy, behavioural factors and data
stake distribution around short-term performance swings,        resources – all shaping how football forecasting systems
revealing limits to real-time efﬁciency.                        are developed and applied.

## Page 04: 4 Journal of Sports Analytics

源页：第 4 页

4                                                                                                           Journal of Sports Analytics


   A key focus is betting strategy and bankroll manage-           Table 1. Statistics for goals, xG, match outcomes and odds.
ment. The Kelly criterion (Kelly, 1956) remains founda-           Number of matches                   3,366
tional for sizing bets under uncertainty. Uhrin et al.
(2021) show that fractional Kelly offers favourable               A. Goal statistics
risk-adjusted returns with noisy models. Buchdahl (2003)                                              Home team                Away team
provides a widely cited guide on ﬁxed-odds betting, cover-        Mean                                1.69                     1.34
                                                                  Median                              1                        1
ing expected value and margin correction. Kopriva (2015)          Standard deviation                  1.39                     1.23
contrasts utility theory with observed behaviour, revealing       Minimum                             0                        0
consistent deviations from optimal staking. Effective             Maximum                             8                        7
capital allocation is thus as important as accurate prediction.
   On model evaluation, Wunderlich and Memmert (2020)             B. Expected goals (xG)
                                                                                                      Home team                Away team
provide a taxonomy of forecasting approaches, from expert-
                                                                  Mean                                1.66                     1.32
driven to ML hybrids. Wheatcroft (2022) recommends                Median                              1.50                     1.16
log-loss and Brier scores over ranked probability scores in       Standard deviation                  0.97                     0.84
football, stressing calibration and sharpness. Behavioural        Minimum                             0.00                     0.00
and heuristic forecasting is another active strand. Tippett       Maximum                             6.88                     6.50
(2017) argues that simple, data-driven methods can rival
                                                                  C. Match outcome distribution
expert judgement. His later works (Tippett, 2019, 2024)                                               Home win       Draw Away win
further support the consistency of analytical approaches          Statistic                           44.5%          24.9% 30.5%
over intuition, echoing broader behavioural economics
insights.                                                         D. Odds and market-implied probabilities
   Finally, new data resources enhance transparency and                                         Home win             Draw      Away win
                                                                  Odds: Mean                    2.79                 4.25      4.46
reproducibility. Dubitzky et al. (2019) introduce an open-        Odds: Minimum                 1.03                 2.99      1.10
access database spanning over 200,000 matches across              Odds: Maximum                 21.17                19.50     46.75
52 leagues. Bassek et al. (2025) expand this with                 Market-implied probability:   44.4%                24.0%     31.7%
Bundesliga-speciﬁc spatiotemporal data, enabling more               Mean
granular tactical analysis.                                       Market-implied probability:   4.5%                 4.9%      2.1%
   Against a backdrop of increasingly complex forecasting           Minimum
methods, this study examines whether a straightforward,           Market-implied probability:   93.0%                31.9% 86.8%
                                                                    Maximum
interpretable model can nevertheless uncover reliable
signals that reﬂect structural inefﬁciencies and offer predict-   This table summarises the statistics for all Bundesliga matches from the
ive leverage over market odds.                                    2014/15 through 2024/25 seasons. Panels A and B report descriptive
                                                                  statistics on actual and expected goals for home and away teams,
                                                                  respectively. Panel C shows the relative frequency of each match outcome.
                                                                  Panel D presents odds and market-implied probabilities across the three
Data and modelling framework                                      result types.

Data
The setup uses match data and xG values for the                   goals per match, with considerable variation. Up to eight
1. Bundesliga during the eleven seasons from 2014/15 to           goals per team are observed in individual matches. The
2024/25 (source: https://understat.com). This is comple-          expected goals largely mimic this picture, although with
mented by bookmaker and betting exchange data for the             less variation and extremes (an xG value of 0.0 indicates
same period (source: https://www.football-data.co.uk).            that a team has not attempted a single shot in the entire
The latter consists of closing odds, i.e. the last odds           match). Across all matches, the average expected goals for
before a match starts. For each time point, the average           home teams (1.66) exceeds that of away teams (1.32), indi-
quotes are obtained – with the panel typically consisting         cating a typical home advantage of approximately 0.34 xG.
of about 15 providers each. This ensures a sufﬁciently rep-       This asymmetry is reﬂected in both actual and expected
resentative picture of market-implied probabilities as well       goal statistics and is implicitly captured in the model
as liquidity for any bets to be placed at these odds.             through venue-speciﬁc xG aggregation (see Section
Section “Robustness and sensitivity analysis” examines            “Generating predictions from historical xG”).
how the results change when the ‘best’ available odds are            Home wins are more common than away wins, while
used instead of the averages.                                     draws occur in about one-fourth of the cases. Odds imply
   Table 1 provides a descriptive overview of the overall         payout multiples as low as 1.03 for favourites (3% gross
dataset. With 18 teams in the league, there are 306 matches       return) as well as enormous upsides (more than 4,000%
per season, yielding a total of 3,366 over the course of the      for an away-team win). Notably, the means of the market-
analysis. On average, teams score between one and two             implied probabilities (corrected for the ‘overround’; see

## Page 05: Wilkens 5

源页：第 5 页

Wilkens                                                                                                                               5




Figure 1. Joint distribution of home and away goals. The heatmap shows the joint distribution (in percentages) of home and away goals in
Bundesliga matches from the 2014/15 through 2024/25 seasons (restricted to results where both teams scored 0 to 6 goals). Darker cells
indicate more frequent outcomes. The dotted diagonal indicates draws; outcomes below this line coincide with wins of the home team.


Section “Identiﬁcation of value bets”) in Panel D are very           match-level proxy for offensive output that is less sensitive
close to those of the actual realisations (Panel C).                 to variance than realised goals.
   Since goals are the ultimate metric for match outcomes,              Consider two opposing teams, denoted A (home) and B
Figure 1 visualises the joint distribution of home and away          (away), with pre-match expected goals xGA and xGB . In the
goals. Most matches cluster around low-scoring outcomes              model, these expected-goal ﬁgures are taken directly as the
such as 1–1, 2–1 and 2–0. Notably, the mass of the distribu-         Poisson intensity parameters, i.e. λA : = xGA and
tion lies below the diagonal, reﬂecting the asymmetric               λB : = xGB . Conditional on these intensities, the number
nature of match results in favour of the home teams.                 of goals scored by each team is assumed to follow inde-
                                                                     pendent Poisson distributions:1
Modelling framework based on expected goals                                            GA ∼ P(λA ),     GB ∼ P(λB )                 (1)
From xG to probabilistic forecasts. Expected goals provide a         When applied for prediction purposes, the values for λ must
granular, quantitative measure of scoring potential, con-            be estimated ex ante, i.e. prior to the match, using only pre-
structed from the sum of shot-level probabilities within a           match information. For the actual match outcome (win,
match. Each shot’s xG is estimated based on features                 draw or loss) – deﬁned here from the perspective of team
such as location, angle and assist type, often using speciﬁc         A – it sufﬁces to model the goal difference:
models trained on large datasets (Mead et al., 2023).
Aggregating these values yields team-level xG, a                                 GDA, B = GA − GB ∼ Skellam(λA , λB )               (2)

## Page 06: 6 Journal of Sports Analytics

源页：第 6 页

6                                                                                                 Journal of Sports Analytics


The resulting (discrete) distribution is of Skellam type         favourites despite being the away team – yet the current
(Skellam, 1946) and yields closed-form expressions for           model classiﬁes them using away xG alone. However,
the probabilities of each outcome through P(GD > 0),             since xG performance already reﬂects underlying team
P(GD = 0) and P(GD < 0). In this way, pre-match xG               strength and venue remains a structural driver, the incre-
inputs fully determine the Poisson intensities and, through      mental beneﬁt of such a reclassiﬁcation is not obvious.
the Skellam distribution, the corresponding match-outcome        The home vs. away distinction on the other hand offers a
probabilities.                                                   transparent and empirically grounded baseline for the
                                                                 analysis.
Generating predictions from historical xG. In order to produce
probabilistic forecasts of match outcomes, pre-match esti-
                                                                 Model assumptions and simpliﬁcations. The modelling frame-
mates of expected goals are required for both teams
                                                                 work relies on several simplifying assumptions:
involved. The values for λ for a certain match day t are
obtained as the average over the previous n matches.
                                                                   • Zero-inﬂation. The Poisson model tends to underesti-
Thereby, home and away performances are treated separ-
                                                                     mate the frequency of goalless matches. Although
ately – i.e. for each upcoming ﬁxture, λ estimates are
                                                                     this issue is well documented, its impact is limited
based on the team’s recent matches in the same venue
                                                                     here because the model uses goal differences – redu-
context (home or away), ensuring the forecasts reﬂect
                                                                     cing the inﬂuence of matches where both teams score
location-speciﬁc scoring potential:
                                                                     zero equally. A more ﬂexible alternative would be a
                                 1 n                                zero-inﬂated Poisson model (Lambert, 1992), though
                  λcontext : =        λ(context)          (3)        this would increase calibration complexity.
                                 n i=1 t−i
                                                                   • Overdispersion. Real-world goal data often exhibit
with context ∈ {home, away}. As an example, to estimate λ            greater variance than the Poisson distribution
for Bayern Munich when it faces a home match, one uses               allows (where the mean equals the variance). A nega-
the n xG values from its previous home matches. The                  tive binomial distribution (Cameron and Trivedi,
moving-average approach reﬂects recent scoring potential             1998: pp. 70–77) could accommodate this through
while smoothing out the volatility of individual matches.            an added dispersion parameter, but again at the cost
In the baseline speciﬁcation, n = 3 is chosen, capturing a           of interpretability and greater estimation uncertainty.
short-term performance window while retaining sufﬁcient            • Goal dependence. The model assumes that home and
sample stability. Section “Robustness and sensitivity ana-           away team goals are independent random variables.
lysis” analyses the sensitivity of the results to this choice.       In reality, scoring may be interdependent within a
    A practical limitation of the method is its reduced cover-       match – for instance, an early goal can shift tactics
age at the start of each season and immediately after                and increase the likelihood of further goals (or
extended breaks, such as the winter pause. This results              tighten defence). Such within-game dynamics
from a deliberate modelling choice: team-level expected              violate the independence assumption. A bivariate
goals are estimated only from matches within the current             Poisson model or a latent shared-component struc-
competitive phase. Rolling averages are not carried over             ture (e.g. GA = X1 + X0 and GB = X2 + X0 with
across seasonal boundaries or long interruptions, ensuring           Xi ∼ P(λi )) (Karlis and Ntzoufras, 2003) could intro-
that forecasts reﬂect recent form rather than outdated infor-        duce positive correlation and better reﬂect shared
mation. As a consequence, the setup ultimately reduces               match conditions. However, such models are harder
forecast coverage to 2,118 out of 3,366 matches.                     to estimate and risk overﬁtting.
    As shown in Figure 2, the empirical goal difference dis-       • Opponent independence. Each team’s expected goals
tribution aligns well with the Skellam-based xG model as             are estimated independently of their opponent. More
per (2), particularly around central outcomes such as                elaborate models might weight past performance by
draws and one-goal margins. Moderate underestimation in              opponent quality, potentially including time decay.
the tails suggests the model may understate extreme out-             However, such reﬁnements would reduce model
comes but remains a strong candidate for win-draw-loss               transparency and again increase the risk of model
modelling.                                                           over-complexity.
    While this study adopts a home vs. away classiﬁcation to       • Feature omission. The model excludes contextual
capture venue-speciﬁc scoring tendencies, an alternative             features such as injuries, weather or tactical forma-
framing would be to distinguish matches based on favourite           tions. While these could improve forecasts, they
vs. longshot status, using pre-match market-implied prob-            also introduce subjectivity, data sparsity and difﬁcul-
abilities. This segmentation aligns closely with how                 ties in reproducibility. Notably, home advantage is
betting markets assess relative team strength. For instance,         implicitly accounted for, as the xG inputs are based
when Bayern Munich visit VfL Bochum, they are strong                 on match-speciﬁc home/away performance.

## Page 07: Wilkens 7

源页：第 7 页

Wilkens                                                                                                                              7




Figure 2. Distribution of goal differences – empirical vs. model. The histogram compares the empirical distribution of goal differences
in Bundesliga matches with a Skellam distribution that, for each match, uses pre-match expected goals (λhome , λaway ) deﬁned as
venue-speciﬁc rolling averages of the previous three xG values for each team.


   • Aggregation level. Teams are treated as single entities         forecasts. In the context of football outcomes, this prevents
     without decomposing performance to the player level.            counterintuitive corrections where more conﬁdent model
     An alternative would be to allow for more responsive            predictions are mapped to lower empirical success rates,
     modelling under line-up changes. For example,                   while allowing a ﬂexible, data-driven adjustment of misca-
     Hewitt and         Karakus (2023)        propose      a         librated regions.
     position-adjusted xG model that captures team                       Calibration is applied separately to each outcome type –
     strength from the bottom up. The necessity and useful-          home win, draw, away win – using a rolling window of two
     ness of such granular player-level modelling for win,           seasons (so that all results and reliability plots are strictly
     draw and loss forecasting, however, is not obvious.             out-of-sample with respect to their calibration window;
                                                                     see Section “Results”). Within each window, isotonic
    While these simpliﬁcations might limit (in-sample) cali-         regression is trained on model probabilities and binary
bration accuracy, they allow for a robust and easy-to-follow         outcome indicators.2 Each ﬁtted function is stored as a
framework and, at the same time, the generation of inde-             piecewise-linear mapping deﬁned by threshold–value
pendent ‘signals’ that might be useful for actual betting            pairs {(xj , yj )}. During application, the calibration function
strategies. The relevance and importance of some of the              is evaluated through linear interpolation between thresh-
assumptions is further analysed as part of the sensitivity           olds. Outside the ﬁtted range, linear extrapolation is used
analyses in Section “Robustness and sensitivity analysis”.           based on the edge slopes. Final calibrated probabilities are
                                                                     clipped to the interval [0.05, 0.95] to avoid extreme
Model ﬁnetuning through isotonic regressions. The Skellam-           values and maintain robustness. Since isotonic regression
based model produces structured forecasts of match out-              is applied independently to each outcome class, the result-
comes, but the raw probabilities are often not fully                 ing probabilities are subsequently renormalised to sum to
aligned with empirical outcome frequencies. To address               one for each match.
this, isotonic regression is applied as a post-processing cali-          Figure 3 illustrates the isotonic regression on the example
bration step. It estimates a non-decreasing function                 of a given in-sample two-season calibration window. Panel
f : [0, 1] → [0, 1] that maps predicted probabilities pi to          (a) shows the empirical frequency of home wins against
calibrated probabilities   p̂i = f (pi ), minimising the empir-      the baseline (Skellam) model probabilities, with the ﬁtted iso-
                    
ical squared error ni=1 (f (pi ) − yi )2 where yi ∈ {0, 1} indi-     tonic regression overlaid as a monotonic step function. Panel
cates whether the outcome occurred. The monotonicity                 (b) visualises the corresponding mapping function used to
constraint ensures that higher predicted probabilities corres-       transform the baseline model probabilities into their cali-
pond to at least as high empirical frequencies, which is con-        brated equivalents. For this process, the model probabilities
sistent with the expected behaviour of well-calibrated               are binned into ﬁxed-width intervals over the [0, 1] range,

## Page 08: 8 Journal of Sports Analytics

源页：第 8 页

8                                                                                                            Journal of Sports Analytics




Figure 3. Finetuning model probabilities via isotonic regression. In order to illustrate the ﬁnetuning step, the ﬁgure shows calibration
and reliability plots for home win probabilities within a single in-sample calibration window (2018/19 through 2019/20 seasons). Panel
(a) displays the isotonic regression ﬁt applied to baseline Skellam-based xG model probabilities, together with empirical outcome
frequencies. Panel (b) compares reliability curves for the baseline and ﬁnetuned (isotonic-adjusted) probabilities. Each point represents
the empirical frequency of home wins within a bin of predicted probabilities (with a minimum of 10 observations). The dashed diagonal
line indicates perfect calibration.




and empirical outcome frequencies are computed within each            Betfair) – the key objective is the identiﬁcation of value
bin to serve as local calibration targets.                            bets. These are wagers where the model assigns a higher
   The method builds on the original formulation of isotonic          probability to an outcome than is implied by the market.
regression by Robertson et al. (1988) and its application to                Let oddsi denote the decimal odds offered for outcome i,
probability calibration in classiﬁcation settings by Zadrozny         i.e. the total payout (including stake) per unit bet. For
and Elkan (2002). Its effectiveness for multiclass settings           example, odds of 2.50 mean that a successful bet with a
has been conﬁrmed empirically by Niculescu-Mizil and                  stake of 1.00 returns 2.50 (1.00 stake plus 1.50 proﬁt).
Caruana (2005). Compared to parametric methods such as                Behavioural research has shown that the way odds are pre-
Platt scaling (Platt, 1999), isotonic regression is more ﬂexible      sented – whether as decimal quotes (e.g. 2.50), fractional
but requires more data to avoid overﬁtting. Earlier work by           odds (e.g. 3/2) or implied probabilities (e.g. 40%) – can inﬂu-
Zadrozny and Elkan (2001) also provides a comparative                 ence bettor decision-making and contribute to systematic
evaluation of calibration techniques and highlights the trade-
                                                                      pricing anomalies in betting markets (Brown and Yang,
offs between interpretability, ﬂexibility and data efﬁciency.
                                                                      2021). The raw market-implied probability is calculated as
   In this setup, the isotonic step does not replace the
                                                                       p̃Market
                                                                         i       = 1/oddsi . However, since betting odds typically
Skellam model, but acts as a one-dimensional, monotone
                                                                      incorporate a margin for the bookmaker – the overround –
calibration layer applied to its output probabilities.
                                                                      the sum of raw probabilities will exceed one:
Structural information enters through the xG-based                     Market
Skellam speciﬁcation; isotonic regression only adjusts sys-                j p̃j    > 1. In order to obtain a probability distribution
tematic probability bias without changing the ordering of ﬁx-         for comparison with model estimates, the raw values are nor-
                                                                                                                       
tures or introducing additional predictors. It thus serves as a       malised (Strumbelj, 2014): pMarket
                                                                                                     i     = p̃Market
                                                                                                               i      / j p̃Market
                                                                                                                            j      . For
data-driven adjustment to an already structured model rather          example, market odds of 1.60, 3.50 and 5.00 for home win,
than as a standalone ﬂexible forecasting device.                      draw and away win correspond to implied probabilities of
                                                                      approximately 56%, 26% and 18%. The correction ensures
                                                                      that the adjusted market-implied probabilities across all out-
Devising a betting strategy                                           comes sum to one, placing them on equal footing with
                                                                      model-derived forecasts.
Identiﬁcation of value bets                                                 A bet on outcome i is considered to offer positive
In order to apply the prediction model in a betting context –         expected value (EV) if the model assigns a higher probabil-
whether against bookmakers or on a betting exchange (e.g.             ity to that outcome than the market does. Assuming a stake

## Page 09: Wilkens 9

源页：第 9 页

Wilkens                                                                                                                        9


of one unit, the EV used here is deﬁned as:                      receives a constant stake. However, more reﬁned approaches
                                                                 dynamically adjust stake sizes according to perceived edge
                 EVi = pModel
                        i     · oddsi − 1.                (4)    and risk. One such method is the fractional Kelly criterion
This expression reﬂects the expected net return per unit         (Kelly, 1956), which recommends bet sizing in proportion
stake and is directly applicable in betting simulations and      to the estimated advantage while reducing the volatility asso-
staking decisions. An alternative, more information-focused      ciated with full Kelly staking (Uhrin et al., 2021). For a given
deﬁnition sometimes used in earlier literature is                outcome i, the fractional Kelly stake is deﬁned as:
pModel
 i     /pMarket
         i      − 1, but both are positively correlated under                                         EVi
reasonably efﬁcient pricing and lead to very similar                                 Stakei = f ·                            (5)
                                                                                                    oddsi − 1
signals in practice. In real-world markets, not all outcomes
of a single match – home win, draw and away win – will           where f ∈ (0, 1] denotes the chosen Kelly fraction. This
simultaneously offer positive EV since this would other-         framework ensures that larger bets are placed when the
wise imply a risk-free arbitrage opportunity.                    model signals a stronger edge, with smaller positions taken
   A complementary practical step consists in imposing           when conﬁdence is more modest.
thresholds to ﬁlter out low-quality betting opportunities           This study considers ﬂat betting as a base case and frac-
and mitigate risks stemming from model miscalibration or         tional Kelly staking as an alternative (see Section “Money
market frictions. The speciﬁc threshold choices are deter-       management strategy: fractional Kelly”); other approaches
mined via in-sample calibration and discussed in Section         – such as drawdown-aware rules, staking caps or
“Threshold ‘optimisation’”.                                      portfolio-style allocations – may offer further adaptability
                                                                 to market frictions and individual risk preferences.

Baseline strategies as benchmark                                 Results
To benchmark the model-based betting strategy, two simple
baselines are implemented and evaluated out-of-sample.           Calibration and predictive accuracy
These serve as reference points for assessing whether the        Before deploying forecasts in a betting context, their cali-
model delivers meaningful improvements over uninformed           bration and predictive accuracy must be assessed to
or market-driven heuristics.                                     ensure statistical reliability and practical relevance. The
                                                                 ﬁrst step is to compare the model probabilities – as well
                                                                 as those implied by market odds – to actual (out-of-sample)
   Historical frequency-based strategy. This benchmark gen-      realisations of the matches in scope.
erates a prediction for each match by drawing randomly               The reliability diagrams in Figure 4 group the matches
from the historical league-wide outcome frequencies.             into ‘bins’ by their probabilities and contrast those with the
These proportions are computed over a rolling window of          empirical occurrences, and are based on forecasts for the
past matches consistent with the model’s xG lookback             out-of-sample seasons 2016/17 through 2024/25, using the
horizon (n = 3 matches per team, venue-speciﬁc). Based           two-season rolling isotonic calibration described in Section
on these rolling frequencies, an outcome is selected for         “Data and modelling framework”. As an illustration, for all
each match and used as the forecast. For example, if             matches in which the model forecasts a home win with
recent proportions are 45% home wins, 25% draws and              60% probability, what proportion of those matches has actu-
30% away wins, the result is sampled from this categorical       ally been won by the home team? This technique uncovers
distribution. This yields a baseline that is purely frequency-   some subtle miscalibrations of the model. Home win prob-
driven, with no team-speciﬁc or contextual input.                abilities tend to be slightly underconﬁdent at lower levels
                                                                 (e.g. 10-30% bins). Market-implied probabilities exhibit a
   Market favourite strategy. This approach places a bet on      marginally higher reliability. Predictions for all outcomes
the outcome – home win, draw or away win – with the              are largely well calibrated across most bins.
lowest average closing odds, i.e. on the market’s implied            Table 2 presents a numerical comparative assessment of
favourite. The strategy hence reﬂects consensus opinion          model-derived and market-implied forecasts across differ-
of the most likely outcome and tests whether the model           ent match outcomes using log-loss and Brier scores.
can outperform publicly available expectations.                  Bootstrapped 95% conﬁdence intervals (not reported to pre-
                                                                 serve table clarity) lie within approximately ±0.02 of each
                                                                 point estimate and do not materially affect the interpret-
Money management strategy                                        ation. For all three outcome categories – home win, draw
Once qualifying bets have been identiﬁed, a staking strategy     and away win – the market forecasts at least slightly outper-
must be speciﬁed to translate these into actionable positions.   form the Skellam-based model with its isotonic regression
The simplest option is ﬂat betting, whereby each wager           ﬁnetuning. This is in line with the reliability plots as per

## Page 10: 10 Journal of Sports Analytics

源页：第 10 页

10                                                                                                                Journal of Sports Analytics




Figure 4. Predicted probabilities and actual frequencies – reliability. The ﬁgure shows reliability plots for the predicted probabilities of
home win, draw and away win. Panel (a) illustrates the reliability – i.e. the comparison of predicted vs. actual frequencies – of the
ﬁnetuned model probabilities, obtained by applying isotonic regression to the Skellam-based forecasts. Panel (b) displays the
performance of market-implied predictions. Each point reﬂects the empirical frequency of the outcome within a probability bin
containing at least 10 observations. Perfect calibration corresponds to the 45-degree diagonal reference line; deviations indicate
misalignment between predicted probabilities and empirical frequencies. Both model and market forecasts are evaluated out-of-sample
over the 2016/17 through 2024/25 Bundesliga seasons, with model probabilities calibrated via a two-season rolling isotonic regression
(see Section “Data and modelling framework”).



Figure 4. When aggregating across all outcomes, the                          divergence is not uncommon: log-loss rewards sharp and
model’s combined log-loss is lower than the market’s                         conﬁdent forecasts and penalises overconﬁdence harshly,
(1.25 vs. 1.41), although the Brier score comparison slightly                whereas the Brier score is a quadratic loss and more tolerant
favours the market (model: 0.63, market: 0.59). This                         of moderate probability errors. Overall, the results suggest
                                                                             that while the market demonstrates superior calibration on
Table 2. Predictive accuracy of model and market forecasts.                  a per-category basis, the model may retain competitive
                                                                             overall discrimination power.
                   Log-loss                       Brier score
Outcome            Model          Market          Model           Market
Home win           0.6635         0.6223          0.2348          0.2166
                                                                             Model-based betting
Draw               0.5624         0.5581          0.1876          0.1861     Threshold ‘optimisation’. Although a forecast indicating posi-
Away win           0.5945         0.5482          0.2030          0.1842     tive expected value (EV > 0) may appear sufﬁcient to
All                1.2497         1.4075          0.6254          0.5869     justify a bet, this is rarely reliable in practice. Small advan-
Log-loss and Brier scores compare model and market forecasts across          tages are often indistinguishable from noise, and even
match outcomes. Lower scores indicate better probabilistic calibration and   modest model miscalibrations or market frictions can
predictive accuracy. The rows for home win, draw and away win treat each
result as a separate binary classiﬁcation problem, whereas the “All” row
                                                                             render such bets unproﬁtable. Furthermore, the choice of
reports multiclass scores based on the full probability vector               optimisation metric can affect the results – for example,
[P(Home), P(Draw), P(Away)].                                                 prioritising total P&L over ROI.

## Page 11: Wilkens 11

源页：第 11 页

Wilkens                                                                                                                             11




Figure 5. Illustration of grid search for parameter optimisation. On the example of home win bets within a single calibration window
(2018/19 through 2019/20 seasons), the grid search for ‘optimal’ in-sample parameters across EVmin and oddsmax is illustrated using
heatmaps. The visualised ‘slices’ correspond to scenarios where the third parameter, Δpmin = 0.10, is held constant – although it
remains part of the full grid search. The minimum odds threshold is ﬁxed throughout at oddsmin = 1.25. The grid search targets three
separate optimisation criteria: (a) highest total P&L, (b) highest ROI and (c) highest Sharpe ratio. The parameter combination yielding
the optimal value is marked in blue.




    Basic thresholds are introduced to determine empirically         these is computed, and the actual parameter set is selected
where potentially attractive bets can be found. They act as a        as the one closest to this median proﬁle. Each criterion
form of practical ‘calibration’, narrowing the betting universe.     involves trade-offs: maximising P&L may favour high-
Concretely, dynamic thresholds in a rolling-window setup are         variance outcomes, while Sharpe ratio optimisation can be
used. Based on information from an in-sample period – set            overly sensitive to small sample volatility. The resulting opti-
again to two seasons here – the following ﬁlters are applied:        mised thresholds are used for the subsequent out-of-sample
a minimum expected value EVmin , a maximum allowable                 period. By rolling forward by one year each, this algorithm
odds level oddsmax and a minimum probability ‘edge’                  is continued across the entire study period.
Δpmin , where Δp : = pModel − pMarket . The rationale for                Figure 5 illustrates the threshold optimisation process.
applying these thresholds is to ensure that only sufﬁciently         For the example used, it is evident that the maximisation
strong signals are considered: EVmin ﬁlters out marginal bets        of the P&L aims for higher odds and thus greater potential
with low expected return, oddsmax limits exposure to high-           payouts. For both ROI and Sharpe ratio, higher risk bets are
variance, low-probability outcomes, and Δpmin requires a             constrained, however, as not commensurate with the opti-
material divergence between model and market views to act            misation goal.
on perceived inefﬁciencies. Lastly, oddsmin = 1.25 is
imposed as a constant, avoiding the placement of bets with           Out-of-sample performance. The results from the rolling-
too low odds.                                                        window procedure and seasonal bet placements are sum-
    The betting opportunities are then scanned with the help         marised in Table 3. Performance metrics are reported only
of a grid search,3 and, individually for home, draw and              for season–outcome combinations with at least ﬁve qualify-
away bets, the thresholds are tuned by varying EVmin ,               ing bets (see also Section “Threshold ‘optimisation”’), to
oddsmax and Δpmin . Independent grid searches are carried            avoid overinterpreting very small samples. Depending on
out that aim for (a) the highest total P&L, (b) the highest          whether the in-sample optimisation targets the highest
ROI and (c) the highest Sharpe ratio. The search ranges over         P&L, ROI or Sharpe ratio, the resulting out-of-sample per-
              EVmin ∈ {0.05, 0.10, . . . , 0.50},             (6)    formance differs noticeably.
                                                                         When aiming for the highest P&L in the calibration
            oddsmax ∈ {1.50, 2.00, . . . , 10.00},            (7)    phases (Panel A), the majority of the bets that are placed
                                                                     back home wins. About one-third of them are won and gen-
              Δpmin ∈ {0.05, 0.10, . . . , 0.25},             (8)
                                                                     erate ca. 17% ROI. The inherent P&L volatility, however,
yielding 900 parameter combinations for each outcome type            renders the Sharpe ratio rather unattractive. Draw and away
and optimisation criterion. In order to mitigate overﬁtting,         bets are placed less frequently and are successful in only
parameter combinations are only retained if they generate            around 20% of the cases. Backing away wins in particular
at least ﬁve qualifying bets within the calibration window.          is detrimental to the overall strategy and exhibits a standalone
For each metric, the ﬁve best-performing parameter sets are          ROI of approximately -17%. In all three types of bets, the
then identiﬁed, the median value of each parameter across            maximum drawdown (DD) suggests a rather high degree

## Page 12: 12 Journal of Sports Analytics

源页：第 12 页

12                                                                                                                      Journal of Sports Analytics


Table 3. Betting strategy – performance.
                        Bets              Wins              Win %              Total P&L              ROI                 Sharpe              Max DD
A. Optimised for P&L
Home win             321                    116             36.1%                 54.25                16.9%               0.10                21.97
Draw                 139                     29             20.9%                 17.33                12.5%               0.05                20.41
Away win             107                     21             19.6%                −17.73               −16.6%              −0.09                36.63
All                  567                    166             29.3%                 53.85                 9.5%               0.05                41.09

B. Optimised for ROI
Home win              38                     10             26.3%                  3.78                 9.9%               0.05                 7.00
Draw                  28                      8             28.6%                 13.79                49.3%               0.20                 8.00
Away win              58                     11             19.0%                −10.40               −17.9%              −0.10                23.79
All                  124                     29             23.4%                  7.17                 5.8%               0.03                16.68

C. Optimised for Sharpe
Home win               12                     2             16.7%                 −7.20               −60.0%              −0.63                 7.26
Draw                   20                     6             30.0%                 11.67                58.3%               0.23                 7.00
Away win               32                     9             28.1%                  3.76                11.8%               0.06                 9.62
All                    64                    17             26.6%                  8.23                12.9%               0.06                10.41

D. Benchmark strategies
Hist. freq.        1,734                    596             34.4%              −144.56                 −8.3%              −0.05               178.86
Market fav.        2,754                  1,447             52.5%              −159.65                 −5.8%              −0.06               189.48
This table reports the out-of-sample betting performance by optimisation metric and outcome type. Each strategy was optimised on past seasons to
maximise one of the three performance metrics – P&L, ROI and Sharpe ratio, with the results shown in Panels A, B and C, respectively. The ﬁgures for the
two benchmark strategies, based on historical outcome frequencies and market favourites, are presented in Panel D.


of instability across time, leading to periods of noticeable                 in Table 3, the pattern is again clear: home win bets drive
decreases in cumulative P&L. Overall, across all outcomes,                   most gains, draw bets play a minor role, and away bets
a positive ROI remains – which would have been markedly                      underperform.
higher if away bets were not to be placed.                                       While the strategy evaluation abstracts from execution
   The in-sample optimisation with respect to the highest                    frictions, several real-world constraints should be noted.
ROI (Panel B) leads to substantially fewer placed bets.                      First, odds may not be available at meaningful volume, par-
The overall ROI amounts to about 6% in this setup, still                     ticularly for less liquid outcomes. Second, transaction costs
in conjunction with a very low Sharpe ratio. In line with                    such as spreads, commissions or slippage could erode prof-
this, even fewer bets are placed when targeting the                          itability — especially at small edges or high turnover.
highest Sharpe ratio during the in-sample grid search                        Third, some bookmakers impose limits or account restric-
(Panel C). The very limited number of positions renders                      tions that may hinder systematic execution. These factors
the resulting statistics not very insightful. The scarcity of                suggest that the reported returns represent an upper bound
the bets is driven by the very restrictive in-sample optimisa-               and should be interpreted as indicative of latent signal
tion that, in many cases, tends to demand a large EVmin or                   quality rather than readily realisable proﬁts.
Δp. Such constellations – required for positive, low-
volatility betting returns that can lead to an attractive
Sharpe ratio – are not often encountered.                                    Robustness and sensitivity analysis
   The two baseline strategies that place bets based on his-
torical occurrence rates and market favourites, respectively,                Season-by-season performance
consistently lose money (Panel D), with ROI of -8% (histor-                  Figure 7 illustrates the out-of-sample performance across
ical frequency) and -6% (market favourite). Notably,                         individual Bundesliga seasons, on the example of the
despite a high win rate, the low odds on favourites result                   in-sample grid search optimised for the highest P&L.
in a negative ROI owing to poor payout. This is in line                      These results offer a more granular view of the overall per-
with expectations, given that betting markets do not offer                   formance patterns documented in Section “Results”, where
sustainable gains for uninformed bettors. As such, the                       pooled metrics indicate a certain proﬁtability in terms of
simple model developed and tested here outperforms                           cumulative P&L.
naive strategies.                                                               The generally high variability of the P&L over time is
   Figure 6 visualises the cumulative P&L, additionally                      evident. Some seasons exhibit broad proﬁtability (e.g.
broken down by outcome type, on the example of an opti-                      2019/20), others underperform across the board. These
mised in-sample grid search for the highest P&L. As seen                     ﬂuctuations are consistent with the earlier ﬁndings in

## Page 13: Wilkens 13

源页：第 13 页

Wilkens                                                                                                                         13




Figure 6. Cumulative P&L of betting strategy. The plot illustrates the cumulative P&L broken down by outcome type – home win,
draw, away win – and aggregated across all bets (“All”). The results are based on optimising the in-sample parameter search for the
highest P&L, i.e. aligned with Panel A in Table 3.




Figure 7. Season-by-season performance of betting strategy. This ﬁgure shows the P&L by season and outcome type – home win,
draw, away win – and aggregated across all bets (“All”). The ﬁgures are based on optimising the in-sample parameter search for the
highest P&L. Each bar shows the number of placed bets as additional information.


Section “Results”. The number of bets placed also ﬂuc-             in-sample optimisation explicitly targets those metrics
tuates notably, despite the in-sample grid search span-            (not shown here).
ning a period of two years. The picture is very similar               The pattern suggests that value opportunities in the
for ROI and Sharpe ratio, and likewise when the                    market are inherently irregular or that the identiﬁcation

## Page 14: 14 Journal of Sports Analytics

源页：第 14 页

14                                                                                                        Journal of Sports Analytics




Figure 8. Sensitivity of xG estimates and model probabilities to the historical estimation window. Panel (a1) shows the average xG for
home teams across all matches as a function of the length of the historical averaging window n. Panel (a2) presents the corresponding
average xG values for away teams. The xG estimates are computed as rolling means over the previous n venue-speciﬁc matches, as
described in Section “Generating predictions from historical xG”. The grey-shaded areas represent the 90% conﬁdence intervals. The
resulting changes in probabilities for home wins and away wins, relative to the base case of n = 3 matches for the xG averaging, are
provided in Panels (b1) and (b2).


algorithm lacks sufﬁcient speciﬁcity. Given a combination              When translating the xG averages into actual match
of sparse opportunity and high variance, systematically             probabilities, Figure 8 also provides the distribution of the
betting – at least under the current speciﬁcation – is unlikely     differences over the base case. The majority of those are
to be consistently proﬁtable in the long run.                       in the region of ±20 percentage points but can in extreme
                                                                    cases also reach ±50 percentage points. This means that
Parameter sensitivity                                               the modelled outcome distribution can shift noticeably –
xG values: ‘calibration’ window. The estimation of the xG           in extreme instances even reversing the model-implied
values is a crucial part of the modelling framework. The            favourite.
use of the average of the most recent n = 3 home or away               The sensitivity of the ultimate proﬁtability of the strat-
matches is varied between n ∈ {1, 2, . . . , 6}. Across the         egies to the xG determination (not shown here in detail)
entire dataset, according to Figure 8, the averages are             is moderate. For n = 1, the total P&L amounts to −62
nearly unaffected. This implies that, at least on average, the      (−6% ROI), with home bets accounting for −16 (−3%
probabilities for home wins, draws and away wins are also           ROI). With a shorter averaging period for the xG values,
not sensitive to the estimation window for the xG values.           model probabilities (and hence betting opportunities) are
As expected, the respective 90% conﬁdence corridors for             available for more matches compared to the base case,
home and away xG are becoming narrower for increasing n.            whereas for n = 6 the opposite holds and coverage is

## Page 15: Wilkens 15

源页：第 15 页

Wilkens                                                                                                                                               15


Table 4. Betting strategy – performance using average vs. best odds.
                       Bets             Wins              Win %               Total P&L              ROI                  Sharpe              Max DD
I. Average odds
Home win               321              116               36.1%                54.25                  16.9%                0.10               21.97
Draw                   139               29               20.9%                17.33                  12.5%                0.05               20.41
Away win               107               21               19.6%               −17.73                 −16.6%               −0.09               36.63
All                    567              166               29.3%                53.85                   9.5%                0.05               41.09

II. Best odds
Home win               321              116               36.1%                72.31                  22.5%                0.12               21.34
Draw                   139               29               20.9%                24.69                  17.8%                0.07               19.24
Away win               107               21               19.6%               −12.78                 −11.9%               −0.06               33.75
All                    567              166               29.3%                84.22                  14.9%                0.07               39.17
This table reports the out-of-sample betting performance under ﬂat stakes, comparing the use of average odds (Section I) and best available odds
(Section II). Strategies were optimised for P&L.

Table 5. Betting strategy – performance across different money management strategies.
                       Bets             Wins              Win %               Total P&L              ROI                  Sharpe              Max DD
I. Average odds
Home win               321              116               36.1%                54.25                  16.9%                0.10               21.97
Draw                   139               29               20.9%                17.33                  12.5%                0.05               20.41
Away win               107               21               19.6%               −17.73                 −16.6%               −0.09               36.63
All                    567              166               29.3%                53.85                   9.5%                0.05               41.09

II. Fractional Kelly (f = 0.50)
Home win                321             116               36.1%                  8.56                   2.7%               0.11                2.36
Draw                    139              29               20.9%                  1.65                   1.2%               0.09                1.16
Away win                107              21               19.6%                 −2.63                  −2.5%              −0.13                4.59
All                     567             166               29.3%                  7.57                   1.3%               0.06                3.23
This table reports the out-of-sample betting performance comparing two staking strategies: ﬂat betting (Section I) and fractional Kelly betting with f =
0.50 (Section II). Strategies were optimised for P&L.

reduced. In the case of n = 6, the resulting P&L is equal to                 Money management strategy: fractional Kelly. Table 5 high-
−14 (−4% ROI), whereby +33 (+15% ROI) stem from                              lights the effect of fractional Kelly staking with f = 0.50
home bets. These results indicate that using only the most                   on out-of-sample betting performance relative to the previ-
recent xG value for each team is insufﬁcient for the model’s                 ously described ﬂat betting approach. Since only the staking
predictions. The absence of a clear trend or dominant perform-               is amended compared to the base case, the number of bets
ance across values of n further suggests that – ceteris paribus –            placed and won is identical in this scenario.
there is no universally optimal calibration window.                              The fractional Kelly method produces more moderate
                                                                             total proﬁts and ROI, reﬂecting its more conservative
Odds: securing best ones in the market. The main results in                  stake sizing. Sharpe ratios remain low and close to those
Section “Out-of-sample performance” rely on the assump-                      observed under ﬂat betting, while maximum drawdowns
tion that average market odds can be secured for all bets.                   exhibit a pronounced reduction, indicating improved
This guarantees a certain liquidity and realistic execution                  capital preservation.
setup. In an ideal case, bets could be placed at the best                        More adaptive approaches could further reﬁne capital
odds instead. The results of this modiﬁcation – in compari-                  allocation. For example, dynamic Kelly schemes adjust f
son to the base case – are shown in Table 4.                                 based on recent performance volatility, drawdown con-
    Notably, the better odds are used for the actual bets but                straints or uncertainty around the EV estimate. Such strat-
not for determining the betting decision itself; the latter are              egies could offer improved risk control in volatile regimes
still based on the same grid search as before, to ensure that                or help preserve capital. At the same time, however, they
the trading ‘signal’ itself is robust enough. The P&L for                    also introduce additional complexity and calibration risk,
backing away wins is still negative, but the total P&L is                    which may counteract the simplicity and transparency
now substantially higher (84 vs. 54). The same is true for                   goals of the current framework.
the ROI (15% vs. 10%). The high P&L volatility (low
Sharpe ratio) and considerable drawdown risk remain a                        Impact of isotonic calibration. Finally, in order to gauge
concern even in this more optimistic scenario.                               whether the positive ROI are driven primarily by the

## Page 16: 16 Journal of Sports Analytics

源页：第 16 页

16                                                                                                     Journal of Sports Analytics


isotonic calibration layer or by the underlying xG-Skellam       execution. Similarly, while richer feature sets or dynamic
signal, the betting performance was recomputed with the          inputs might improve accuracy, any such additions should
isotonic regression step removed. With isotonic calibration,     be judged by whether they enhance usability without under-
the main ﬂat-stake strategy based on average odds achieves       mining the core strengths of simplicity, robustness and low
a total proﬁt of about 54, corresponding to an ROI of            model risk. In contrast to recent studies that employ
roughly 10%. Without isotonic calibration, applying the          complex machine learning architectures or context-aware
same selection mechanism directly to the raw Skellam prob-       expected points models (Bassek et al., 2025; Cavus and
abilities still produces a positive but much smaller proﬁt of    Biecek, 2022), this study deliberately prioritises structural
around 6, with an ROI close to 1%. The incremental gain          parsimony and interpretability.
from isotonic regression is therefore material, but the under-       In summary, the analysis shows that simple, data-driven
lying xG-Skellam model already exhibits some predictive          models – if well-constructed and properly ﬁltered – can
value on its own.                                                extract meaningful signals and, in some settings, deliver
   The cross-section of bets indicates that the main role        economically viable returns from football betting markets.
of isotonic calibration is to trim poorly calibrated             As economist Tim Harford observed: “The power of a
away-win positions. Without the additional step, away            good model lies not in its complexity, but in its ability to
bets generate a strongly negative ROI of about −38%              illuminate.”
and substantial drawdowns; after applying isotonic
regression, their loss rate moderates to roughly −17%,           ORCID iD
while home and draw bets remain broadly similar in               Sascha Wilkens      https://orcid.org/0000-0002-2856-0881
number and performance. In this sense, isotonic regres-
sion primarily acts as a conservative ﬁlter on the most
                                                                 Funding
fragile part of the forecast spectrum, rather than as an
independent source of proﬁtability.                              The author(s) received no ﬁnancial support for the research,
                                                                 authorship, and/or publication of this article.

Conclusion and outlook                                           Declaration of conﬂicting interests
This paper evaluates whether simple, xG-based models can         The authors declared no potential conﬂicts of interest with respect
generate accurate and economically valuable football fore-       to the research, authorship, and publication of this article.
casts. Using a Skellam distribution to convert recent xG
values – augmented by isotonic regression to improve fore-       Data availability
cast calibration – into match probabilities, the model is        Historical xG data and betting quotes are freely available from
assessed across eleven Bundesliga seasons by comparing           Understat and Football-Data, respectively.
predictive accuracy and calibration to those of bookmaker-
implied probabilities.
                                                                 Notes
    While market odds remain better calibrated, the
xG-based model captures certain structural signals that          1. λ is equal to both expected value and variance of the distribu-
translate into modest but consistent proﬁtability in simu-          tion in this case.
lated betting, with the strongest performance observed for       2. Fixed-width binning with 20 bins is used to reduce noise, drop-
home win outcomes. Away bets tend to dilute returns.                ping bins with fewer than 10 samples.
The isotonic calibration layer improves both reliability         3. This implies that the 2014/15 and 2015/16 seasons form the
and proﬁtability mainly by trimming poorly calibrated               ﬁrst in-sample period and that the ﬁrst out-of-sample forecasts
away-win positions, while robustness checks show that               are for the 2016/17 season.
the underlying xG-Skellam probabilities already contain a
modest positive signal on their own. Performance shows           References
some robustness but varies across seasons and bet types.         Baboota R and Kaur H (2019) Predictive analysis and modelling
Alternative staking methods, such as fractional Kelly,              football results using machine learning approach for English
help reduce drawdown risk but trade off against total return.       Premier League. International Journal of Forecasting 35(2):
    A natural next step would be to explore ensemble-style          741–755.
forecasts that combine model- and market-based probabil-         Bassek M, Rein R, Weber H, et al. (2025) An integrated dataset of
ities. Since the model uncovers latent inefﬁciencies while          spatiotemporal and event data in elite soccer. Scientiﬁc Data
markets offer strong calibration, blending the two could            12: 195.
improve reliability and economic performance without sac-        Berrar D, Lopes P and Dubitzky W (2024) A data- and knowledge-
riﬁcing interpretability. Although this study abstracts from        driven framework for developing machine learning models to
frictions such as slippage or betting limits, future work           predict soccer match outcomes. Machine Learning 113:
could simulate such effects to better approximate real-world        8165–8204.

## Page 17: Wilkens 17

源页：第 17 页

Wilkens                                                                                                                                  17


Bialkowski A, Lucey P, Carr P, et al. (2014) Identifying team style     Franke M (2020) Do market participants misprice lottery-type
   in soccer using formations learned from spatiotemporal track-           assets? Evidence from the European soccer betting market.
   ing data. In: Proceedings of the IEEE International Conference          The Quarterly Review of Economics and Finance 75: 1–18.
   on Data Mining Workshops (ICDMW), pp. 9–14. Shenzhen,                Fu S (2024) Comparative analysis of expected goals models:
   China: IEEE.                                                            Evaluating predictive accuracy and feature importance in
Brechot M and Flepp R (2020) Dealing with randomness in match              European soccer. In: Proceedings of the 2nd International
   outcomes: How to rethink performance evaluation in European             Conference on Machine Learning and Automation, Adana,
   club football using expected goals. Journal of Sports                   Turkey.
   Economics 21(4): 335–362.                                            Goddard J and Asimakopoulos I (2004) Modelling football match
Brown A and Yang F (2019) The wisdom of large and small                    results and the efﬁciency of ﬁxed-odds betting. Journal of
   crowds: Evidence from repeated natural experiments in sports            Forecasting 23(1): 51–66.
   betting. International Journal of Forecasting 35(1): 288–296.        Groll A, Kneib T, Mayr A, et al. (2018) On the dependency of
Brown A and Yang F (2021) Framing effects and the market selec-            soccer scores – a sparse bivariate Poisson model for the
   tion hypothesis. Southern Economic Journal 88(1): 399–413.              UEFA European football championship 2016. Journal of
Buchdahl J (2003) Fixed Odds Sports Betting: Statistical Forecasting       Quantitative Analysis in Sports 14(2): 65–79.
   and Risk Management. London: High Stakes Publishing.                 Hewitt JH and Karakus O (2023) A machine learning approach for
Cameron AC and Trivedi PK (1998) Regression Analysis of Count              player and position adjusted expected goals in football (soccer).
   Data. Cambridge: Cambridge University Press.                            Franklin Open 4: 100034.
Cavus M and Biecek P (2022) Explainable expected goal models            Hubacek O, Sourek G and Zelezny F (2019) Exploiting sports-
   for performance analysis in football analytics. In: 9th                 betting market using machine learning. International Journal
   International Conference on Data Science and Advanced                   of Forecasting 35(2): 783–796.
   Analytics (DSAA), pp. 1–9. Shenzhen, China: IEEE.                    Hvattum LM and Arntzen HB (2010) Using Elo ratings for match
Constantinou AC, Fenton NE and Neil M (2013) Proﬁting from an              result prediction in association football. International Journal
   inefﬁcient association football gambling market: Prediction,            of Forecasting 26(3): 460–470.
   risk     and    uncertainty     in   the     Premier     League.     Joseph A, Fenton N and Neil M (2006) Predicting football results
   Knowledge-Based Systems 50: 60–86.                                      using Bayesian nets and other machine learning techniques.
Croxson K and Reade JJ (2014) Information and efﬁciency: Goal arrival      Knowledge-Based Systems 19(7): 544–553.
   in soccer betting. The Economic Journal 124(575): 62–91.             Kain KJ and Logan TD (2014) Are sports betting markets predic-
Dixon MJ and Coles SG (1997) Modelling association football                tion markets? Evidence from a new test. Journal of Sports
   scores and inefﬁciencies in the football betting market.                Economics 15(1): 45–63.
   Journal of the Royal Statistical Society: Series C (Applied          Karlis D and Ntzoufras I (2003) Analysis of sports data by using
   Statistics) 46(2): 265–280.                                             bivariate Poisson models. The Statistician 52(3): 381–393.
Dubitzky W, Lopes P, Davis J, et al. (2019) The open international      Karlis D and Ntzoufras I (2009) Bayesian modelling of football out-
   soccer database for machine learning. Machine Learning 108:             comes: Using the Skellam’s distribution for the goal difference.
   9–28.                                                                   IMA Journal of Management Mathematics 20(2): 133–145.
Edalatpanah SA and Hess M (2024) Advancing football analytics:          Kaunitz L, Zhong S and Kreiner J (2017) Beating the bookies with
   Predictive modeling and performance analysis in the                     their own numbers – and how the online sports betting market
   Bundesliga using machine learning. Computational                        is rigged. Working paper, University of Tokyo.
   Engineering and Technology Innovations 1(4): 233–247.                Kelly JL (1956) A new interpretation of information rate. The Bell
Egidi L, Karlis D and Ntzoufras I (2025) Predictive Modelling for          System Technical Journal 35(4): 917–926.
   Football Analytics. New York (NY): Chapman and Hall/CRC.             Koopman SJ and Lit RA (2015) A dynamic bivariate Poisson
Feng G, Polson N and Xu J (2016) The market for English Premier            model for analysing and forecasting match results in the
   League (EPL) odds. Journal of Quantitative Analysis in Sports           English Premier League. Journal of the Royal Statistical
   12(4): 167–178.                                                         Society: Series A (Statistics in Society) 178(1): 167–186.
Fischer M and Heuer A (2025) Match predictions in soccer:               Kopriva F (2015) Constant bet size? Don’t bet on it! testing
   Machine learning vs. Poisson approaches. In: Memmert D                  expected utility theory on Betfair data. Working paper,
   (ed.) Artiﬁcial Intelligence and Machine Learning in Sports             Charles University.
   Science. Berlin/Heidelberg: Springer, pp. 91–102.                    Kozak J and Glowania S (2021) Heterogeneous ensembles of clas-
Forrest D, Goddard J and Simmons R (2005) Odds-setters as fore-            siﬁers in predicting Bundesliga football results. Procedia
   casters: The case of English football. International Journal of         Computer Science 192: 1573–1582.
   Forecasting 21(3): 551–564.                                          Lambert D (1992) Zero-inﬂated Poisson regression, with an appli-
Franck E, Verbeek E and Nüesch S (2010) Prediction accuracy                cation to defects in manufacturing. Technometrics 34(1): 1–14.
   of different market structures: Bookmakers versus a betting          Lasek J, Szlavik Z and Bhulai S (2013) The predictive power of
   exchange. International Journal of Forecasting 26(3):                   ranking systems in association football. International Journal
   448–459.                                                                of Applied Pattern Recognition 1(1): 26–46.

## Page 18: 18 Journal of Sports Analytics

源页：第 18 页

18                                                                                                           Journal of Sports Analytics


Maher MJ (1982) Modelling association football scores. Statistica      Stübinger J and Knoll F (2018) Beat the bookmaker: Winning
   Neerlandica 36(3): 109–118.                                            football bets with machine learning. In: Bramer M and
Mead J, O’Hare A and McMenemy P (2023) Expected goals in                  Petridis M (eds.) Artiﬁcial Intelligence XXXV. SGAI 2018,
   football: Improving model performance and demonstrating                Lecture Notes in Computer Science, Vol. 11311. Cham:
   value. PloS one 18(4): e0282295.                                       Springer, pp. 219–233.
Michels R, Ötting M and Karlis D (2025) Extending the Dixon and        Tippett J (2017) The Football Code: The Science of Predicting the
   Coles model: An application to women’s football data. Journal          Beautiful Game. Independently published.
   of the Royal Statistical Society: Series C (Applied Statistics)     Tippett J (2019) The Expected Goals Philosophy: A Game-
   71(1): 167–186.                                                        Changing Way of Analysing Football. Independently published.
Michels R, Ötting M and Langrock R (2023) Bettors’ reaction to         Tippett J (2024) xGenius: Expected Goals and the Science of
   match dynamics – evidence from in-game betting. European               Winning Football Matches. London: Bloomsbury Publishing.
   Journal of Operational Research 310(3): 1118–1127.                  Uhrin M, Sourek G, Hubacek O, et al. (2021) Optimal sports
Niculescu-Mizil A and Caruana R (2005) Predicting good prob-              betting strategies in practice: An experimental review. IMA
   abilities with supervised learning. In: Proceedings of the             Journal of Management Mathematics 32(4): 465–489.
   22nd International Conference on Machine Learning                   Vlastakis N, Dotsis G and Markellos RN (2009) How efﬁcient
   (ICML), pp. 625–632. New York (NY): ACM.                               is the European football betting market? Evidence from
Ötting M, Deutscher C, Singleton C, et al. (2025) Betting on              arbitrage and trading strategies. Journal of Forecasting 28(5):
   momentum in contests. Economic Inquiry 63(4): 1066–1089.               426–444.
Ötting M, Langrock R and Maruotti A (2023) A copula-based              Wheatcroft E (2022) Evaluating probabilistic forecasts of
   multivariate hidden Markov model for modelling momentum                football matches: The case against the ranking probability
   in football. AStA Advances in Statistical Analysis 107(1): 9–27.       score. Journal of Quantitative Analysis in Sports 17(4):
Ötting M, Michels R, Langrock R, et al. (2024) Demand for live            273–287.
   betting: An analysis using state-space models. Applied              Winkelmann D and Deutscher C (2025) Do betting markets sense
   Stochastic Models in Business and Industry 40(2): 527–541.             a goal coming? Evidence from the German Bundesliga.
Platt JC (1999) Probabilistic outputs for support vector machines         Working paper, University of Cologne.
   and comparisons to regularized likelihood methods. In:              Winkelmann D, Ötting M, Deutscher C, et al. (2024) Are betting
   Smola AJ, Bartlett P, Schölkopf B and Schuurmans D (eds.)              markets efﬁcient? Evidence from simulations and real data.
   Advances in Large Margin Classiﬁers. Cambridge (MA):                   Journal of Sports Economics 25(1): 54–97.
   MIT Press, pp. 61–74.                                               Wunderlich F and Memmert D (2020) Forecasting the outcomes of
Robertson T, Wright FT and Dykstra RL (1988) Order Restricted             sports events: A review. European Journal of Sport Science
   Statistical Inference. New York (NY): John Wiley & Sons.               20(3): 328–340.
Singh S, Sharma J, Kumar S, et al. (2025) The evolution of football    Xenopoulos P (2016) Using Skellam’s distribution to assess soccer
   betting: A machine learning approach to match outcome forecast-        team performance. Working paper, Pomona College.
   ing and bookmaker odds estimation. In: Saraswat M, Rajan A and      Zadrozny B and Elkan C (2001) Obtaining calibrated probability
   Chakravorty A (eds.) Congress on Smart Computing                       estimates from decision trees and naive Bayesian classiﬁers.
   Technologies. CSCT 2024. Smart Innovation, Systems and                 In: Proceedings of the 18th International Conference on
   Technologies, Vol. 121. Singapore: Springer, pp. 117–130.              Machine Learning (ICML), pp. 609–616. San Francisco
Skellam JG (1946) The frequency distribution of the difference            (CA): Morgan Kaufmann.
   between two Poisson variates belonging to different popula-         Zadrozny B and Elkan C (2002) Transforming classiﬁer scores
   tions. Journal of the Royal Statistical Society. Series A              into accurate multiclass probability estimates. In: Proceedings
   (General) 109(3): 296.                                                 of the 8th ACM SIGKDD International Conference on
Strumbelj E (2014) On determining probability forecasts from betting      Knowledge Discovery and Data Mining (KDD), pp. 694–699.
   odds. International Journal of Forecasting 30(4): 934–943.             New York (NY): ACM.
