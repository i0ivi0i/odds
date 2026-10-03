# Bayesian Weighted Discrete-Time Dynamic Models for Association Football Prediction

> 重建说明：模式 transcribe；来源 `2025_Macri_足球贝叶斯加权动态模型_arXiv.pdf`；共 26 页；原图逐页查看 26/26 页。
> 核图证据：对照 `.ky-md-work/2025_Macri_足球贝叶斯加权动态模型_arXiv/pages/` 下 page-01.png 至 page-26.png 全量 26 页原图，重构 Table 1-7 全量标准 Markdown 管道表格，全保真修复目标进球泊松/负二项/Skellam模型方程 (1)-(4)、动态随机游走先验 (5)-(7)、共度先验与连续 Spike-and-Slab 混合分布 (8)-(11) 及 MCMC 诊断矩阵。

## Page 01: Bayesian weighted discrete-time dynamic models for association

源页：第 1 页

Bayesian weighted discrete-time dynamic models for association
                                                                                      football prediction
                                                           Roberto Macrı̀-Demartino               ∗, Leonardo Egidi         , and Nicola Torelli
                                                 Department of Economics, Business, Mathematics, and Statistics “Bruno de Finetti”, University of Trieste,
                                                                                   Via A. Valerio 4/1, Trieste, 34127, Italy


                                                                THIS IS A PREPRINT WHICH HAS NOT YET BEEN PEER REVIEWED
arXiv:2508.05891v1 [stat.ME] 7 Aug 2025




                                                                                                   Abstract

                                                     In recent years, great emphasis has been placed on the prediction of association football. Due to this,
                                                 several studies have proposed different types of statistical models to predict the outcome of a football match.
                                                 However, most existing approaches usually assume that the offensive and defensive abilities of teams remain
                                                 static over time. We introduce a Bayesian dynamic approach for football goal-based models that uses
                                                 period-specific commensurate priors to flexibly weight the evolution of attacking and defensive abilities. Our
                                                 approach assigns separate, time-varying precisions for each ability and period, controlled via spike-and-slab
                                                 hyperpriors. This adaptive shrinkage borrows information about teams’ strength when past and current
                                                 performance aligns and allows rapid adjustments when teams experience substantial changes (e.g., transfer
                                                 windows or coaching changes). We integrate this framework into six standard goal-based models evaluating
                                                 predictive performance using data from the last five seasons of the German Bundesliga, English Premier
                                                 League, and Spanish La Liga. Compared with the other discrete-time dynamic models, our adaptive approach
                                                 yields better predictive performance. The proposed methodology has also been implemented in the free and
                                                 open source R package footBayes.
                                                 Keywords: Commensurate prior, Hierarchical models, Historical borrowing, Posterior predictive, Sport
                                                 Analytics


                                          1     Introduction
                                          Quantitative analysis of association football (soccer), hereafter referred to as football, and more specifically,
                                          matches’ prediction is a rapidly evolving discipline, increasingly valued by participants, coaches, owners, and
                                          gamblers looking to gain a competitive advantage. Consequently, there is a growing demand for information that
                                          supports better decision making.
                                               The outcome of football matches can be predicted using two main statistical modelling frameworks. In the
                                          goal-based (or direct) approach, the actual numbers of goals scored by each team is a count variable – most
                                          commonly modelled via Poisson or Negative-Binomial regression. The expected goal counts are functions of
                                          team attributes (e.g., offensive and defensive abilities) and, when relevant, home-field advantage. In contrast,
                                          result-based (or indirect) models predict one of three outcomes – home win, draw, or away win – typically through
                                          ordered probit (Koning, 2000) or logit (Carpita et al., 2015, 2019) regressions. Furthermore, the widespread
                                          popularity of large datasets promoted the use of machine learning (ML) tools, yielding a fundamentally different
                                              ∗ Corresponding author e-mail: roberto.macridemartino@deams.units.it




                                                                                                       1

## Page 02: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 2 页

Bayesian weighted discrete-time dynamic models for association football prediction                         Preprint


modelling approach based on a random forest Breiman (2001). The potential of using this as a new results-based
model was first explored by Schauberger and Groll (2018) to assess the predictive performance of different types
of random forests compared to classical Poisson regression methods on data containing all matches of the FIFA
World Cups 2002–2014. Along these lines, Groll et al. (2019a), Groll et al. (2019b), Groll et al. (2021), and Groll
et al. (2024) further expand this framework. It is worth noting that the result-based framework is formally nested
within the goal-based one. Specifically, match results are derived from the underlying goal counts, while knowing
only the three-way result provides no information about the actual goals scored, potentially misestimating team
strength (Egidi and Torelli, 2021). Therefore, we focus on the richer goal-based structure, which not only yields
three-way predictions but also captures the magnitude of outcomes.
    In the simplest goal-based formulation, team-specific goal counts are assumed conditionally independent
given team abilities or covariates, resulting in a double Poisson model (Maher, 1982; Baio and Blangiardo,
2010; Groll and Abedieh, 2013; Egidi et al., 2018, among others). To relax the strong independence assumption,
several generalisations introduce score dependence. Dixon and Coles (1997) extended the work of Maher (1982)
by allowing (a slightly negative) correlation between scores and incorporating a dependence parameter into their
model to account for it. Karlis and Ntzoufras (2003) introduced in a frequentist framework the bivariate Poisson
model, designed to account for positive goal dependencies. Furthermore, Ntzoufras (2011) extended it from a
Bayesian perspective.
    A main assumption of previous models is the invariance of team-specific parameters, implying static offensive
and defensive abilities over time. However, it is recognised that team performance is inherently dynamic,
fluctuating over years and possibly within seasons. One simple approach is the time decay weighting used by
Dixon and Coles (1997), in which older match outcomes are downweighted so that recent games have more
influence on estimated abilities. However, a more formal approach is to treat team abilities as time-varying
parameters. Specifically, a continuous-time dynamic extension of the double Poisson model was introduced
by Rue and Øyvind Salvesen (2000), while Koopman and Lit (2015) and Koopman and Lit (2019) integrated
bivariate Poisson models in a state-space framework, allowing the abilities of the team to vary according to a state
vector. Alternatively, Owen (2011) proposed a Bayesian discrete-time approach based on an evolution component
that describes the stochastic behaviour of time-dependent parameters. Here, the evolution component is specified
as a random walk prior distribution structure for both the attack and defence parameters. Recent developments
include Egidi et al. (2018), which incorporates betting odds and other refinements, and Macrı̀ Demartino et al.
(2025), that evaluate predictive performance improvements when the ranking of a team is added as a covariate in
dynamic models. However, a key limitation of the approach proposed by Owen (2011) is the assumption of a
constant and common evolution precision for both attack and defence parameters. This constraint may limit
the predictive performance of the goal-based model, ignoring the fact that a team’s performance can fluctuate
more during certain periods (e.g., early season transfers, midseason managerial changes). Furthermore, forcing
the same evolution precision for both attack and defence neglects that these abilities can have different rates of
change – defensive abilities may adapt more slowly than offensive ones, or vice versa.
    In the present work, we try to fill this gap by proposing a Bayesian weighted discrete-time approach that
incorporates time-specific commensurate priors (Hobbs et al., 2011, 2012) for both attack and defence parameters.
This provides a formal mechanism for letting the prior distributions at a specific time to adaptively borrow
information from the previous time, but only to the extent that the data support it. By introducing flexible and
dynamic evolution precision, we obtain a more accurate and adaptive modelling of team abilities over time,
improving the predictive performances.

                                                         2

## Page 03: Section 2: Goal-Based Models (Poisson & Negative Binomial)

源页：第 3 页

Bayesian weighted discrete-time dynamic models for association football prediction                         Preprint

The paper is organised as follows. Section 2 presents the Poisson and Negative Binomial goal-based models used in this study. Furthermore, Section 3 describes the commensurate prior framework and introduces our proposed dynamic weighted approach for the offensive and defensive abilities of the teams in the goal-based models. In Section 4, we apply our methodology to some of the top European leagues, namely: the German Bundesliga, English Premier League (EPL), and Spanish La Liga. A total of five seasons from 2020 to 2025 are used from each league to perform the study. Finally, Section 5 provides concluding remarks that outline limitations, advantages, and potential future research directions.

### 2 Goal-based models

This section presents the statistical goal-based models used to predict the chosen competition outcomes. Through an in-depth analysis, our aim is to provide a comprehensive overview of the methodologies applied to predict football matches, highlighting both their statistical foundations and practical implementations in sports analytics.

#### 2.1 Poisson-based models

Let $(x_{i,n}, y_{j,n})$ represent the observed number of goals scored by the home and the away team in the $n$-th match, with $i \ne j = 1, \dots, N_T$ and $n = 1, \dots, N$. A simple double Poisson (DP) model (Maher, 1982) assumes that the goal counts follow two conditionally independent Poisson distributions:

$$X_{i,n} \mid \lambda_{1,n} \sim \text{Poisson}(\lambda_{1,n}), \quad Y_{j,n} \mid \lambda_{2,n} \sim \text{Poisson}(\lambda_{2,n}), \quad X_{i,n} \perp Y_{j,n} \mid \lambda_{1,n}, \lambda_{2,n} \tag{1}$$

where the (non-negative) parameters $\lambda_{1,n}$ and $\lambda_{2,n}$ are the expected scoring rates of the home and away teams, respectively, in the $n$-th match. In Maher’s model, the rate at which a team is expected to score is a function of both its own offensive ability and the defensive ability of its opponent:

$$\log \lambda_{1,n} = \beta_0 + \text{home} + \beta_{h_n}^{att} + \beta_{a_n}^{def}$$
$$\log \lambda_{2,n} = \beta_0 + \beta_{a_n}^{att} + \beta_{h_n}^{def} \tag{2}$$

where the parameter $\beta_0$ is a common intercept, 'home' captures the well-known home-field advantage, and $\beta_{h_n}^{att}$ and $\beta_{a_n}^{def}$ represent the unknown attacking and defensive abilities of the home team $h_n$ and the away team $a_n$ in the $n$-th match.

However, it is widely recognised that the scores of two competing football teams are positively correlated. Thus, the independence assumption in the double Poisson model (1) might be too restrictive. To account for this correlation, Karlis and Ntzoufras (2003) introduced the bivariate Poisson (BP) model, which explicitly captures the dependence between goal counts.

## Page 04: Section 2: Bivariate Poisson, Negative Binomial & Skellam Alternatives

源页：第 4 页

Bayesian weighted discrete-time dynamic models for association football prediction                             Preprint

The joint distribution for the goals scored by the home and away teams under this model is given by the bivariate Poisson probability mass function:

$$P_{X_{i,n}, Y_{j,n}}(x_{i,n}, y_{j,n}) = \exp(-(\lambda_{1,n} + \lambda_{2,n} + \lambda_{3,n})) \frac{\lambda_{1,n}^{x_{i,n}} \lambda_{2,n}^{y_{j,n}}}{x_{i,n}! y_{j,n}!} \sum_{k=0}^{\min(x_{i,n}, y_{j,n})} \binom{x_{i,n}}{k} \binom{y_{j,n}}{k} k! \left( \frac{\lambda_{3,n}}{\lambda_{1,n} \lambda_{2,n}} \right)^k \tag{3}$$

where $\mathbb{E}(X_{i,n}) = \lambda_{1,n} + \lambda_{3,n}$ and $\mathbb{E}(Y_{j,n}) = \lambda_{2,n} + \lambda_{3,n}$. The parameter $\lambda_{3,n} = \text{cov}(X_{i,n}, Y_{j,n})$ measures the covariance between the two goal counts, representing the dependence between the scores of the two teams. Furthermore, the scoring rates $\lambda_{1,n}$ and $\lambda_{2,n}$ are defined as in (2). Additionally, in Equation (3), we model the covariance $\lambda_{3,n}$ to not depend on other predictors:

$$\log \lambda_{3,n} = \eta_0$$

The bivariate Poisson model generalizes the double Poisson model. Specifically, when $\lambda_{3,n} = 0$, the goal counts become independent, and the bivariate Poisson model reduces precisely to the double Poisson model described in (1).

#### 2.2 Negative Binomial and Skellam alternatives

Poisson models assume equal mean and variance, which may not hold in real-world football data – especially in competitions where overdispersion (sample variance exceeds the sample mean) is observed in the number of goals. To handle this, a common approach is to replace each Poisson marginal with a negative binomial (NB) distribution (Reep et al., 1971). That is:

$$X_{i,n} \sim \text{NB}(\lambda_{1,n}, \gamma), \quad Y_{j,n} \sim \text{NB}(\lambda_{2,n}, \gamma)$$

where $\lambda_{1,n}$ and $\lambda_{2,n}$ follow the same log-linear structure introduced in Section 2.1, and $\gamma > 0$ is the dispersion parameter.

Alternatively, Karlis and Ntzoufras (2009) suggest using the Skellam distribution (Skellam, 1946), which directly models the difference in goal:

$$Z_n = X_{i,n} - Y_{j,n}$$

The corresponding probability mass function is given by:

$$P_{Z_n}(z_n) = \exp(-(\lambda_{1,n} + \lambda_{2,n})) \left( \frac{\lambda_{1,n}}{\lambda_{2,n}} \right)^{z_n/2} I_{|z_n|}\left( 2 \sqrt{\lambda_{1,n} \lambda_{2,n}} \right), \quad z_n \in \mathbb{Z} \tag{4}$$

where $\mathbb{E}(Z_n) = \lambda_{1,n} - \lambda_{2,n}$ and $\text{Var}(Z_n) = \lambda_{1,n} + \lambda_{2,n}$. Furthermore, $I_h(\cdot)$ is the modified Bessel function of order $h$ (Skellam, 1946).

## Page 05: Section 2.3: Diagonally Inflated Draws & Dynamic Random Walk Priors

源页：第 5 页

Bayesian weighted discrete-time dynamic models for association football prediction                                             Preprint

The parameters $\lambda_{1,n}$ and $\lambda_{2,n}$ adopt the same log-linear structure as in the previous cases.

#### 2.3 Inflating the draws probability

Poisson goal-based models often underestimate the incidence of draws, which are the diagonal elements in goal probability matrices. To mitigate this, Karlis and Ntzoufras (2009) introduced a diagonally inflated bivariate Poisson (DIBP) model as follows:

$$P_{X_{i,n}, Y_{j,n}}(x_{i,n}, y_{j,n}) = \begin{cases} (1 - \omega) \text{BP}(\lambda_{1,n}, \lambda_{2,n}, \lambda_{3,n}) & \text{if } x_{i,n} \ne y_{j,n} \\ (1 - \omega) \text{BP}(\lambda_{1,n}, \lambda_{2,n}, \lambda_{3,n}) + \omega D(x_n, \xi) & \text{if } x_{i,n} = y_{j,n} \end{cases}$$

where $\text{BP}(\cdot)$ is the bivariate Poisson probability mass function as in (3), $\omega \in [0, 1]$ controls the inflation weight, and $D(x_n, \xi)$ is a discrete distribution with parameter vector $\xi$, which favours draw outcomes.

Similarly, to address excess draws in goal differences, the zero-inflated Skellam model (ZISM) (Karlis and Ntzoufras, 2009) can be adopted:

$$P_{Z_n}(z_n) = \begin{cases} (1 - \omega) \text{SM}(\lambda_{1,n}, \lambda_{2,n}) & \text{if } z_n \ne 0 \\ (1 - \omega) \text{SM}(\lambda_{1,n}, \lambda_{2,n}) + \omega D(0, \xi) & \text{if } z_n = 0 \end{cases}$$

#### 2.4 Dynamic prior distributions and identifiability constraints

A structural limitation in the previous models is the assumption of static team-specific parameters, namely, teams are assumed to have a constant performance over time, determined by attack and defence abilities $\beta^{att}$ and $\beta^{def}$, respectively. Several approaches have been proposed to dynamically model team-specific abilities (Rue and Salvesen, 2000; Owen, 2011; Koopman and Lit, 2015, 2019, among others). In particular, Owen (2011) extended the static framework by introducing a discrete-time evolution for team-specific effects:

$$\beta_{i,\tau}^{att} \mid \beta_{i,\tau-1}^{att}, \sigma \sim N\left( \beta_{i,\tau-1}^{att}, \frac{1}{\sigma} \right)$$
$$\beta_{i,\tau}^{def} \mid \beta_{i,\tau-1}^{def}, \sigma \sim N\left( \beta_{i,\tau-1}^{def}, \frac{1}{\sigma} \right) \tag{5}$$

## Page 06: Section 3: Weighted Dynamic Proposal & Commensurate Priors

源页：第 6 页

Bayesian weighted discrete-time dynamic models for association football prediction                         Preprint

While for the initial period $\tau = 1$, the prior distributions are initialised as:

$$\beta_{i,1}^{att} \mid \mu^{att}, \sigma \sim N\left( \mu^{att}, \frac{1}{\sigma} \right)$$
$$\beta_{i,1}^{def} \mid \mu^{def}, \sigma \sim N\left( \mu^{def}, \frac{1}{\sigma} \right) \tag{6}$$

where $\mu^{att}$ and $\mu^{def}$ are the prior means for the initial attack and defence abilities, respectively, and $\sigma$ is the common evolution precision, assumed constant over time and identical between all teams and both team-specific abilities. To ensure identifiability, a zero-sum constraint (Baio and Blangiardo, 2010; Owen, 2011) on the random effects within each period is required:

$$\sum_{i=1}^{N_T} \beta_{i,\tau}^{att} = 0, \quad \sum_{i=1}^{N_T} \beta_{i,\tau}^{def} = 0, \quad \tau = 1, \dots, T \tag{7}$$

### 3 A weighted dynamic proposal

As described in Section 2.4, a key assumption of the discrete-time evolution approach as in (5) is a single constant evolution precision $1/\sigma$ shared by all teams and by both their attack and defence parameters. In this section, we propose a weighted dynamic approach based on commensurate priors, which employ separate, time-varying evolution precisions for attack and defence.

#### 3.1 Commensurate priors

Hobbs et al. (2011) consider the case in which data from a single historical study inform the analysis of a new study by defining the commensurate prior for the parameter of interest $\theta$ as follows:

$$\theta \mid \theta_0, \phi \sim N\left( \theta_0, \frac{1}{\phi} \right) \tag{8}$$

where $\theta_0$ is the estimate from the historical study and $\phi$ is the precision or commensurability parameter.

## Page 07: Section 3.1: Spike-and-Slab Hyperpriors

源页：第 7 页

Bayesian weighted discrete-time dynamic models for association football prediction                               Preprint

Hobbs et al. (2012) proposed two families of priors for $\phi$, a family of gamma distributions that leads to a full conditional posterior distribution, as well as a variant of the 'spike-and-slab' distribution introduced by Mitchell and Beauchamp (1988) for Bayesian variable selection based on a mixture prior with two components:

$$P(\phi < \alpha_1) = 0$$
$$P(\phi < u) = p_l \times \frac{u - \alpha_1}{\alpha_2 - \alpha_1}, \quad \alpha_1 \le u \le \alpha_2 \tag{9}$$
$$P(\phi > \alpha_2) = P(\phi = S) = 1 - p_l$$

where $p_l$ is the probability of a slab, which can be interpreted as the prior probability of incommensurability. The spike component concentrates the probability mass near $\theta_0$, encouraging strong borrowing from historical data, while the slab component allows for greater deviation when current data conflict with historical evidence.

#### 3.2 Weighted dynamic prior distributions

Let $\beta_{i,\tau}^{(k)}$ denote team $T_i$’s ability of type $k$ in period $\tau$, where $k \in \{\text{att}, \text{def}\}$ and $\tau = 1, 2, \dots, T$ indexes the time periods. For each team $T_i$ and each period $\tau = 2, \dots, T$, the prior distributions for the attack and defence abilities are:

$$\beta_{i,\tau}^{att} \mid \beta_{i,\tau-1}^{att}, \phi_{att,\tau} \sim N\left( \beta_{i,\tau-1}^{att}, \frac{1}{\phi_{att,\tau}} \right)$$
$$\beta_{i,\tau}^{def} \mid \beta_{i,\tau-1}^{def}, \phi_{def,\tau} \sim N\left( \beta_{i,\tau-1}^{def}, \frac{1}{\phi_{def,\tau}} \right) \tag{10}$$

where each team's offensive (defensive) ability in period $\tau$ has a normal prior distribution centred on the ability of that team in period $\tau - 1$, with a commensurate parameter $\phi_{k,\tau}$.

## Page 08: Section 3.2: Continuous Two-Component Mixture Prior

源页：第 8 页

Bayesian weighted discrete-time dynamic models for association football prediction                                Preprint

To complete the model specification, we assign spike-and-slab hyperpriors to each precision parameter. Rather than using a discrete spike-and-slab with a point mass at $S$ and a uniform slab on $[\alpha_1, \alpha_2]$ as in (9), we employ a continuous two-component mixture consisting of a highly concentrated spike and a diffuse slab (Hong et al., 2018). For each period and ability of type $k$, where $k \in \{\text{att}, \text{def}\}$, we let:

$$\phi_{k,\tau} \mid \mu_s, \mu_l, \psi_s, \psi_l, p_l \sim N_+(\mu_s, \psi_s) \times (1 - p_l) + N_+(\mu_l, \psi_l) \times p_l \tag{11}$$

where $N_+(\mu, \psi)$ denotes a normal distribution with mean $\mu$ and standard deviation $\psi$ truncated from below at zero (i.e., the half-normal distribution). Specifically, $\mu_s$ and $\mu_l$ represent the means of the spike-and-slab components, respectively, while $\psi_s$ and $\psi_l$ are the corresponding standard deviations, with $0 < \psi_s < \psi_l$.

## Page 09: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 9 页

Bayesian weighted discrete-time dynamic models for association football prediction                         Preprint


4    Application
We evaluate the efficacy of our proposed model using six Bayesian dynamic goal-based models, as described
in Section 2. Our analysis uses data from the five most recent seasons (2020/2021 through 2024/2025) of
three major European football leagues: the German Bundesliga , the English Premier League (EPL), and the
Spanish La Liga. We compare the performance of our proposal with the discrete-time approach of Owen (2011),
which uses a single evolution precision shared between all teams and for both offensive and defensive abilities.
Additionally, we include the extension by Egidi et al. (2018), which introduces a constant evolution precision that
is specific to either attack or defence abilities but shared among all teams. Each season in our datasets is treated
as two discrete-time periods – the first half and the second half of the season, resulting in a total of ten time
periods for analysis. This division is designed to capture midseason structural events, such as winter transfer
windows and breaks, which can significantly alter team composition and performance. For instance, midseason
often brings roster changes (through transfers), managerial turnovers, and player recovery from injuries, all of
which can change the performance of a team in the last half of the season. To comprehensively assess predictive
performance, we consider three distinct prediction scenarios for each league: the entire second half, the last three
rounds, and the last round of the most recent season. These scenarios cover different time horizons and levels of
volatility, allowing us to examine how well each model adapts to changing conditions. In particular, forecasting
over an entire half-season provides a broad view that incorporates the cumulative impact of all post-midseason
changes (e.g., transfers, coaching changes, tactical adjustments). In contrast, focussing on the final three rounds
focusses on a crucial segment of the season often marked by intensified competitive pressure – during this phase,
results can decide championships, European qualification, or relegation, and teams may adjust their strategies
accordingly (e.g., rotating squads to manage fatigue, or adopting more aggressive or defensive tactics as needed).
Finally, predicting only the last round represents the most uncertain scenario. In the final round, teams have
widely varying motivations – some are competing for crucial objectives, while others have little or nothing to lose
– which often leads to surprising outcomes. By examining performance in these three scenarios, we can assess the
robustness and adaptability of our weighted dynamic models under a range of realistic competitive conditions.
    The models are implemented using the probabilistic programming language Stan (Carpenter et al., 2017),
employing Markov Chain Monte Carlo (MCMC) sampling via the R package footBayes (Egidi et al., 2025).
For posterior sampling, we run four independent chains, each consisting of 2000 iterations, with the initial 1000
iterations discarded as burn-in. In the spike-and-slab formulation as in (11), the spike component has mean
𝜇 𝑠 = 100 and standard deviation 𝜓 𝑠 = 0.1, while the slab component has mean 𝜇𝑙 = 0 and standard deviation
𝜓𝑙 = 5, that is,
                         𝜙att, 𝜏 , 𝜙def, 𝜏 | 𝑝 𝑙 ∼ N+ (100, 0.1) × (1 − 𝑝 𝑙 ) + N+ (0, 5) × 𝑝 𝑙 ,

where 𝑝 𝑙 is the prior probability of drawing from the slab that is set to 0.99 (Hobbs et al., 2012; Chen et al.,
2018). The chosen half-normal slab prior is approximately uniform over [0, 3] and decays afterwards, allowing
either minimal borrowing or complete discounting of prior information when necessary (Alt et al., 2025). In
contrast, the spike prior is structured to yield complete pooling when the past information aligns closely with
current observations (Ouma et al., 2022; Zheng and Wason, 2022; Chen et al., 2018; Hobbs et al., 2012). For the
approaches proposed by Owen (2011) and Egidi et al. (2018), the evolution precisions are modelled as

                                            𝜎, 𝜎att , 𝜎def ∼ Cauchy+ (0, 5),



                                                             9

## Page 10: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 10 页

Bayesian weighted discrete-time dynamic models for association football prediction                          Preprint


where Cauchy+ (0, 𝜈) denotes the half-Cauchy distribution with location 0 and scale 𝜈. As noted in Gelman
(2006), the half-Cauchy distribution is a flexible and weakly informative prior for scale parameters in hierarchical
models, with advantageous behaviour near zero and minimal influence on posterior estimates. Finally, for all
models, a weakly informative prior (Gelman et al., 2008) is assigned to the home-effect parameter

                                                  home ∼ N(0, 5).


4.1     Predictive performance
One of the key aspects of sports analytics is the ability to generate accurate future predictions. Bayesian models
naturally provide posterior probabilities for future matches. Considering the posterior predictive distribution
for future observable data D̃, we incorporate the predictive uncertainty of the model, propagated from the
uncertainty of the posterior parameter. Predictions are generated by conditioning future observable values on the
posterior parameter estimates
                                                      ∫
                                        𝑝( D̃ |D) =       𝑝( D̃ |𝜽)𝜋(𝜽 |D)𝑑𝜽.

After obtaining predictions from the models, evaluating their performance is crucial to assessing their predictive
power and reliability. Specifically, we focus on two predictive metrics to rigorously examine the predictive
performance of the models described in Section 2. Additional analyses with two other predictive metrics are
provided in Appendix A.

4.1.1    Predictive metrics

The evaluation of probabilistic forecasts typically involves scoring rules metrics, which assess forecast performance
by comparing predictions with the corresponding outcomes. The Brier score (Brier, 1950), recommended by
Spiegelhalter and Ng (2009), is a non-local and distance-insensitive scoring rule, essentially acting as a mean
squared error for forecasts. It is defined as

                                                      𝑀     3
                                                  1 ∑︁ ∑︁
                                        Brier =             ( 𝑝 𝑟 ,𝑚 − 𝛿𝑟 ,𝑚 ) 2 ,
                                                  𝑀 𝑚=1 𝑟=1

where 𝑝 𝑟 ,𝑚 denotes the predicted probability of outcome 𝑟, with 𝑟 ∈ {home win, draw, away win}, for the 𝑚-th
match played during the forecast period. Here, 𝛿𝑟 ,𝑚 is the Kronecker delta, that is, 1 if the outcome 𝑟 occurs in
the 𝑚-th match. The Brier score ranges from 0, indicating perfect prediction accuracy, to a maximum of 2 when
predictions consistently assign probability 1 to incorrect outcomes.
      While proper scoring rules penalise squared errors, mean-based metrics provide direct, interpretable
summaries of predictive accuracy. The Average of Correct Probabilities (ACP) is defined as the arithmetic mean
of the probabilities assigned to outcomes that actually occurred, that is

                                                                𝑀
                                                          1 ∑︁
                                                ACP =           𝑝 𝑜,𝑚 ,
                                                          𝑀 𝑚=1

where 𝑝 𝑜,𝑚 is the probability assigned to the observed outcome of the 𝑚-th match. Being an arithmetic mean,


                                                           10

## Page 11: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 11 页

Bayesian weighted discrete-time dynamic models for association football prediction                                                   Preprint


the ACP measures the confidence of the average forecast directly on the original probability scale. ACP values
near 1 indicate that the model consistently assigns high probabilities to the true outcomes, whereas values near 0
reflect weaker predictive performance.
          Figure 1 compares the Brier score and the ACP for the proposed weighted dynamic approach compared to
those of Owen (2011) and Egidi et al. (2018), evaluated in the final round of the 2024/2025 season scenario.
The plot includes the bivariate Poisson, diagonal-inflated bivariate Poisson, double Poisson, negative binomial,
Skellam model, and zero-inflated Skellam model. The proposed weighted dynamic approach consistently
demonstrates superior predictive performance, yielding the lowest values for the Brier score and the highest
values for the ACP among all models and competitions. In the Bundesliga, the bivariate Poisson model achieves
the smallest Brier score with a value of 0.593 and the largest ACP value of 0.409. For the EPL, the Skellam
model obtains the lowest Brier score at 0.545 while the diagonal-inflated bivariate Poisson reaches an ACP of
0.449. In La Liga, the diagonal-inflated bivariate Poisson achieves a Brier score of 0.462 and an ACP of 0.485.

                                                  Weighted Dynamic    Owen (2011)        Egidi et al. (2018)


                             Bundesliga                                EPL                                            La Liga



          0.65




                                                                                                                                            Brier Score
          0.60


          0.55


          0.50
 Values




          0.45

                                                                                                                                            ACP



          0.40




                 BP   DIBP   DP    NB     SM   ZISM    BP    DIBP    DP    NB       SM     ZISM         BP     DIBP   DP   NB   SM   ZISM
                                                                      Model

Figure 1: Lineplot comparing Brier Score and Average of Correct Probabilities (ACP) for the proposed weighted dynamic
method with those of Owen (2011) and Egidi et al. (2018), evaluated on the final round of the 2024/2025 season. The
comparison includes six models: Bivariate Poisson (BP), Diagonal-Inflated Bivariate Poisson (DIBP), Double Poisson
(DP), Negative Binomial (NB), Skellam Model (SM), and Zero-Inflated Skellam Model (ZISM), for the Bundesliga, La
Liga, and English Premier League (EPL).

          Table 1 summarises the Brier scores and ACPs for each of the six goal-based models, comparing our
weighted-dynamic forecasts with those of Owen (2011) and Egidi et al. (2018) over the last three matchdays
of the 2024/25 season. Among the three leagues, the weighted dynamic approach consistently achieves the
lowest Brier score and the highest ACP values, reflecting more accurate predictions on decisive matches at the


                                                                     11

## Page 12: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 12 页

Bayesian weighted discrete-time dynamic models for association football prediction                          Preprint


end of the season. In the Bundesliga, our weighted dynamic approach reduces the Brier score from 0.683 to
0.678 compared to the method proposed by Egidi et al. (2018) in the bivariate Poisson model and presents the
highest ACP value of 0.359. In the EPL, the weighted dynamic models outperform the other approaches, yielding
the lowest and highest values for the Brier score and the ACP, respectively. Notably, in the diagonal-inflated
bivariate Poisson model, the Brier score decreases to 0.602, while the ACP reaches a value of 0.421, highlighting
the benefit of draw inflation combined with period-specific weighting in a highly unpredictable competition.
Similarly, in La Liga, the weighted-dynamic models outperform all other approaches, achieving the best results
with a Brier score of 0.499 under the diagonal-inflated bivariate Poisson model, while showing the highest ACP
of 0.454.
### Table 1: Brier Score and Average of Correct Probabilities (ACP)

*Evaluated on the last three rounds of the 2024/2025 season for Bundesliga, EPL, and La Liga.*

| League | Model | Weighted Dynamic Brier | Weighted Dynamic ACP | Owen (2011) Brier | Owen (2011) ACP | Egidi et al. (2018) Brier | Egidi et al. (2018) ACP |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Bundesliga** | Bivariate Poisson | 0.678 | 0.359 | 0.687 | 0.357 | 0.683 | 0.357 |
| | Diag. Infl. Bivariate Poisson | 0.735 | 0.341 | 0.733 | 0.344 | 0.725 | 0.348 |
| | Double Poisson | 0.718 | 0.344 | 0.719 | 0.346 | 0.702 | 0.353 |
| | Negative Binomial | 0.698 | 0.351 | 0.706 | 0.350 | 0.690 | 0.357 |
| | Skellam Model | 0.688 | 0.345 | 0.688 | 0.347 | 0.684 | 0.351 |
| | Zero Infl. Skellam Model | 0.693 | 0.344 | 0.690 | 0.348 | 0.686 | 0.351 |
| **EPL** | Bivariate Poisson | 0.603 | 0.409 | 0.608 | 0.402 | 0.609 | 0.402 |
| | Diag. Infl. Bivariate Poisson | 0.602 | 0.421 | 0.616 | 0.410 | 0.619 | 0.408 |
| | Double Poisson | 0.612 | 0.408 | 0.622 | 0.401 | 0.626 | 0.399 |
| | Negative Binomial | 0.606 | 0.410 | 0.612 | 0.404 | 0.611 | 0.403 |
| | Skellam Model | 0.617 | 0.393 | 0.624 | 0.387 | 0.617 | 0.389 |
| | Zero Infl. Skellam Model | 0.615 | 0.394 | 0.624 | 0.387 | 0.624 | 0.385 |
| **La Liga** | Bivariate Poisson | 0.502 | 0.448 | 0.520 | 0.438 | 0.518 | 0.439 |
| | Diag. Infl. Bivariate Poisson | 0.499 | 0.454 | 0.518 | 0.444 | 0.521 | 0.442 |
| | Double Poisson | 0.503 | 0.450 | 0.522 | 0.439 | 0.518 | 0.441 |
| | Negative Binomial | 0.514 | 0.442 | 0.533 | 0.431 | 0.534 | 0.430 |
| | Skellam Model | 0.553 | 0.408 | 0.554 | 0.407 | 0.556 | 0.406 |
| | Zero Infl. Skellam Model | 0.548 | 0.411 | 0.554 | 0.407 | 0.555 | 0.407 |

Table 2 presents the same comparisons for the second half of last season. Specifically, in the Bundesliga, the
weighted dynamic bivariate Poisson model achieves the lowest Brier score of 0.661 and the highest ACP value of
0.387. In the EPL, the weighted dynamic bivariate Poisson obtains the lowest Brier Score of 0.579, while the
weighted dynamic diagonal-inflated bivariate Poisson model produces an ACP of 0.429. Similarly, in La Liga,
the weighted dynamic diagonal-inflated bivariate Poisson model achieves a Brier score of 0.583 and produces
the highest ACP (0.425).


4.2     Team abilities
One of the crucial aspects of our proposal is how the weighted dynamic approach in (10) influences the evolution
of the attacking and defensive abilities of the teams in the evaluated periods. Figure 2 illustrates the trajectories
of these abilities for the best performing model identified in Section 4.1, when forecasting the final round of
the 2024/2025 season. Specifically, for the Bundesliga the best model is the bivariate Poisson model, for the


                                                          12

## Page 13: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 13 页

Bayesian weighted discrete-time dynamic models for association football prediction                            Preprint


### Table 2: Brier Score and Average of Correct Probabilities (ACP) - Second Half of Season

*Evaluated on the second half of the 2024/2025 season for Bundesliga, EPL, and La Liga.*

| League | Model | Weighted Dynamic Brier | Weighted Dynamic ACP | Owen (2011) Brier | Owen (2011) ACP | Egidi et al. (2018) Brier | Egidi et al. (2018) ACP |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Bundesliga** | Bivariate Poisson | 0.661 | 0.387 | 0.664 | 0.382 | 0.662 | 0.384 |
| | Diag. Infl. Bivariate Poisson | 0.694 | 0.386 | 0.691 | 0.383 | 0.694 | 0.383 |
| | Double Poisson | 0.677 | 0.386 | 0.683 | 0.381 | 0.685 | 0.380 |
| | Negative Binomial | 0.671 | 0.384 | 0.680 | 0.378 | 0.682 | 0.377 |
| | Skellam Model | 0.664 | 0.370 | 0.668 | 0.368 | 0.667 | 0.370 |
| | Zero Infl. Skellam Model | 0.664 | 0.372 | 0.668 | 0.369 | 0.667 | 0.371 |
| **EPL** | Bivariate Poisson | 0.579 | 0.422 | 0.581 | 0.421 | 0.583 | 0.420 |
| | Diag. Infl. Bivariate Poisson | 0.594 | 0.429 | 0.592 | 0.427 | 0.588 | 0.428 |
| | Double Poisson | 0.584 | 0.424 | 0.584 | 0.424 | 0.582 | 0.425 |
| | Negative Binomial | 0.584 | 0.421 | 0.582 | 0.422 | 0.583 | 0.422 |
| | Skellam Model | 0.601 | 0.399 | 0.600 | 0.399 | 0.597 | 0.401 |
| | Zero Infl. Skellam Model | 0.604 | 0.398 | 0.597 | 0.401 | 0.596 | 0.402 |
| **La Liga** | Bivariate Poisson | 0.583 | 0.416 | 0.586 | 0.413 | 0.585 | 0.414 |
| | Diag. Infl. Bivariate Poisson | 0.583 | 0.425 | 0.586 | 0.421 | 0.586 | 0.421 |
| | Double Poisson | 0.585 | 0.419 | 0.585 | 0.416 | 0.585 | 0.416 |
| | Negative Binomial | 0.590 | 0.415 | 0.591 | 0.411 | 0.587 | 0.413 |
| | Skellam Model | 0.583 | 0.401 | 0.589 | 0.395 | 0.594 | 0.394 |
| | Zero Infl. Skellam Model | 0.583 | 0.402 | 0.588 | 0.396 | 0.592 | 0.396 |

                                              13

## Page 14: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 14 页

Bayesian weighted discrete-time dynamic models for association football prediction                                                                      Preprint


                                                                                  Attack   Defense

                                      Weighted Dynamic                             Owen (2011)                                Egidi et al. (2018)




                                                                                                                                                                 Bayern Munich
                    1.0
                    0.5
                    0.0
                   −0.5

                    0.4




                                                                                                                                                                 Hoffenheim
                    0.2

                    0.0

                   −0.2
                    1.0




                                                                                                                                                                 Man City
                    0.5
 Ability values




                    0.0

                   −0.5




                                                                                                                                                                 Man United
                    0.4
                    0.2
                    0.0
                   −0.2




                                                                                                                                                                 Real Madrid
                    0.5

                    0.0

                   −0.5

                   0.75
                   0.50




                                                                                                                                                                 Girona
                   0.25
                   0.00
                  −0.25
                          1   2   3    4   5   6   7     8   9   10   1   2   3   4   5    6   7     8   9   10   1   2   3    4    5    6    7     8   9   10
                                                                                      Period

Figure 2: Trajectories of estimated attacking (solid red lines) and defensive (solid blue lines) abilities with their 50%
credible intervals over ten periods for two representative teams in each league. Results from the proposed weighted dynamic
method are shown alongside corresponding estimates from Owen (2011) and Egidi et al. (2018), all evaluated at the final
round of the 2024/2025 season scenario.


                   Additional analyses on the commensurate precisions for the offensive and defensive abilities parameters are
provided in the Appendix B.


5                   Discussion
This work introduced a Bayesian weighted dynamic framework for football predictions that flexibly models the
evolution of team-specific abilities over time. By using commensurate priors with spike-and-slab hyperparameters,
our approach allows each team’s attack and defence strength in a given period to adaptively borrow information
from past performance. This yields a more responsive and nuanced dynamic model compared to previous
approaches that assume static abilities or a single constant evolution precision. Among six different goal-based
distributions and three major European leagues, we found that this adaptive shrinkage mechanism leads to
consistent improvements in predictive accuracy and a substantial reduction in computational time relative to
earlier dynamic models. The weighted dynamic models captured team performance trajectories more realistically
– for instance, they sharply reflected midseason form fluctuations and major transitions – while maintaining or
improving forecast prediction accuracy. The greatest gains emerged in short-term prediction tasks (e.g., the
final rounds of a season), where the ability to adjust quickly to recent surprises is crucial. Furthermore, in


                                                                                      14

## Page 15: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 15 页

Bayesian weighted discrete-time dynamic models for association football prediction                           Preprint


terms of computation time, the proposed weighted dynamic approach outperforms the dynamic formulations
of Owen (2011) and Egidi et al. (2018) while achieving satisfactory convergence diagnostics for all scenarios
evaluated. Specifically, among all leagues and models, the weighted dynamic model consistently requires the
least computation time to reach convergence. More details are provided in Appendix C.
    In this paper, we maintained the dependence parameter in the bivariate Poisson models constant, but future
work could investigate making the covariance of scores dynamic if needed. These additions would offer a
comprehensive overview of how every aspect of the game evolves, albeit at the cost of T − 1 additional parameters.
Furthermore, incorporating additional predictors or team covariates may improve predictions. Our current
implementation used only past match results to infer team abilities; however, information such as team market
value, recent injuries, or even in-game statistics (shots, expected goals) could be included as covariates influencing
the scoring rates parameters. Future extensions might also consider team-specific or hierarchical evolution
parameters, so that traditionally inconsistent teams are allowed more variation than stable teams.
    Another important direction is the integration with result-based models and other comparative approaches.
Although we focused on goal-based distributions (which naturally yield the three-way process as a consequence),
our methodology could be extended to models that predict match outcomes directly. For instance, in an
ordered probit/logit model or a multi-class logistic model for win–draw–loss, one could let each team’s latent
strength parameter vary over time using the same weighted random-walk prior. In addition, a weighted dynamic
Bradley–Terry-Davidson model for paired comparisons is a natural extension. Our approach could provide a fully
Bayesian weighted dynamic Bradley–Terry-Davidson model by allowing each team’s strength to evolve with our
weighted dynamic approach. Conceptually, this would let the probability of one team beating another adapt
rapidly after major changes (e.g., if a traditionally weak team suddenly improves, the model would downweight
its past information). We expect that such a model would be computationally even simpler (since it has only one
strength per team rather than separate attack/defence), yet still benefit from our weighted dynamic approach.
    We emphasise that the Bayesian weighted dynamic approach presented here is quite general and may find
use in other sports domains. Many sports and competitive systems (e.g., basketball, volleyball, or handball)
involve teams whose skills change over time. By calibrating the commensurate prior to the specific domain, our
strategy of time-specific shrinkage could be applied wherever one has sequential performance data and expects
occasional shifts in the underlying ability. Furthermore, while our focus here has been on domestic leagues with
complete round-robin schedules, future research will focus on high-profile tournaments feature group stages
followed by knockout rounds or hybrid formats such as the UEFA Champions League, FIFA World Cup, and
UEFA European Championship. Finally, the proposed method is implemented in the free and open source R
package footBayes.


Software and Data Availability
All analyses were performed in the R programming language version 4.4.3 (R Core Team, 2025). Data are freely
available online at football-data.co.uk. All computational simulations in Appendix C were conducted on an Intel
Core i7-1260P laptop with 16GB of RAM running Ubuntu 22.04. The code for reproducing this manuscript
is openly available at https://github.com/RoMaD-96/BayesWDFM. The proposed methodology has
also been implemented in the free and open source R package footBayes (from version 2.1.0).




                                                         15

## Page 16: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 16 页

Bayesian weighted discrete-time dynamic models for association football prediction                         Preprint


Acknowledgments
This work has been supported by the project ”SMARTsports: “Statistical Models and AlgoRiThms in sports.
Applications in professional and amateur contexts, with able-bodied and disabled athletes”, funded by the
MIUR Progetti di Ricerca di Rilevante Interesse Nazionale (PRIN) Bando 2022 - grant n. 2022R74PLE (CUP
J53D23003860006).


Appendix A            Ranked Probability Score and Pseudo-R2
For discrete outcomes, it can be beneficial for a scoring rule to account for the proximity or ordering of potential
outcomes. In football, a draw is closer to a home win than an away win. The Ranked Probability Score (RPS)
(Epstein, 1969) is a distance-sensitive scoring measure that evaluates the degree to which the forecast probability
distribution matches the observed outcome, assigning higher scores to probabilistic forecasts that allocate higher
probabilities to outcomes near the actual result. The RPS is defined as

                                                3−1  𝑟           𝑟
                                                                        !2
                                            1 ∑︁ ∑︁             ∑︁
                                    RPS =               𝑝 𝑙,𝑚 −     𝛿𝑙,𝑚 .
                                          3 − 1 𝑟=1 𝑙=1         𝑙=1

As with the Brier score, lower values indicate better predictive performance.
    The pseudo-R2 (Dobson et al., 2001) is defined as the geometric mean of the probabilities assigned to the
actual result of each match.
                                                          𝑀
                                                         Ö              1/𝑀
                                          Pseudo-R2 =           𝑝 𝑜,𝑚           .
                                                          𝑚=1

The geometric mean penalises low-probability predictions more severely than the arithmetic mean. Similarly
to ACP, a pseudo-R2 close to 1 indicates high predictive accuracy, while values approaching 0 suggest weaker
performance.
    Figure 3 compares the RPS and the pseudo-R2 for the proposed weighted dynamic approach compared to
those of Owen (2011) and Egidi et al. (2018), evaluated in the final round of the 2024/2025 season. The proposed
weighted dynamic approach consistently demonstrates superior predictive performance, yielding the lowest RPS
and the highest pseudo-R2 values among all models and competitions. In the Bundesliga, the bivariate Poisson
model achieves the lowest RPS with a value of 0.242 and a pseudo-R2 of 0.372. For the EPL, the zero-inflated
Skellam model obtains the smallest RPS at 0.193, while the Skellam model shows the highest pseudo-R2 at
0.400. In La Liga, the diagonal-inflated bivariate Poisson model presents an RPS of 0.141 and achieves the
highest pseudo-R2 at 0.448.
    Table 3 presents the RPS and Pseudo-R2 values for each of the six goal-based models, comparing our
weighted-dynamic forecasts with those of Owen (2011) and Egidi et al. (2018) over the last three matchdays
of the 2024/25 season. In the Bundesliga, our weighted dynamic approach slightly decreases the RPS from
0.217 to 0.216 compared to the method proposed by Egidi et al. (2018) while reaching the highest value for the
Pseudo-R2 (0.328) in the bivariate Poisson model. In the EPL, the weighted dynamic models yield the smallest
and largest values for the RPS and Pseudo-R2 , respectively. Notably, in the diagonal-inflated bivariate Poisson
model the RPS is 0.224, while in the bivariate Poisson model the Pseudo-R2 is 0.370. Similarly, in La Liga, the


                                                        16

## Page 17: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 17 页

Bayesian weighted discrete-time dynamic models for association football prediction                                                   Preprint


                                                  Weighted Dynamic    Owen (2011)        Egidi et al. (2018)


                             Bundesliga                                EPL                                            La Liga




          0.25




                                                                                                                                            RPS
          0.20




          0.15
 Values




          0.45




                                                                                                                                            Pseudo R^2
          0.40




          0.35




                 BP   DIBP   DP    NB     SM   ZISM    BP    DIBP    DP    NB       SM     ZISM         BP     DIBP   DP   NB   SM   ZISM
                                                                      Model

Figure 3: Lineplot comparing the Ranking Probability Score (RPS) and Pseudo-R2 for the proposed weighted dynamic
method with those of Owen (2011) and Egidi et al. (2018), evaluated on the final round of the 2024/2025 season. The
comparison includes six models: Bivariate Poisson (BP), Diagonal-Inflated Bivariate Poisson (DIBP), Double Poisson (DP),
Negative Binomial (NB), Skellam Model (SM), and Zero-Inflated Skellam Model (ZISM), for the Bundesliga, English
Premier League (EPL), and La Liga.


weighted-dynamic models outperform all other approaches, achieving the best results with an RPS of 0.189 and
a Pseudo-R2 of 0.421 under the diagonal-inflated bivariate Poisson model.
          Table 4 presents the same comparisons for the second half of last season. In the Bundesliga, the weighted
dynamic bivariate Poisson model exhibits the lowest RPS (0.222) and the highest Pseudo-R2 of 0.336. In
the EPL, the weighted dynamic bivariate Poisson presents the lowest RPS (0.205) and the highest Pseudo-R2
(0.380). In La Liga, the weighted dynamic version of the bivariate Poisson, Skellam model, and zero-inflated
Skellam models achieve an RPS value of 0.200 and present the largest Pseudo-R2 (0.375).


Appendix B                      Further analysis on 𝜙att and 𝜙def
Figure 4 shows how the posterior commensurate parameters 𝝓att and 𝝓def for the attacking and defensive abilities
of the teams evolve during the evaluated periods, under the three predictive scenarios and for each of the three
major European leagues. Based on the result obtained in Section 4.1.1, when predicting the final round of the
2024/2025 season, the Bundesliga is modelled with the bivariate Poisson, the EPL with the Skellam model, and
La Liga with the diagonal-inflated bivariate Poisson; when forecasting the last three rounds, the Bundesliga again
uses the bivariate Poisson while both the EPL and La Liga use the diagonal-inflated bivariate Poisson; and when


                                                                     17

## Page 18: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 18 页

Bayesian weighted discrete-time dynamic models for association football prediction                               Preprint


### Table 3: Ranked Probability Score (RPS) and Pseudo-R2

*Evaluated on the last three rounds of the 2024/2025 season.*

| League | Model | Weighted Dynamic RPS | Weighted Dynamic Pseudo-R2 | Owen (2011) RPS | Owen (2011) Pseudo-R2 | Egidi et al. (2018) RPS | Egidi et al. (2018) Pseudo-R2 |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Bundesliga** | Bivariate Poisson | 0.216 | 0.328 | 0.219 | 0.324 | 0.217 | 0.325 |
| | Diag. Infl. Bivariate Poisson | 0.245 | 0.298 | 0.242 | 0.302 | 0.238 | 0.306 |
| | Double Poisson | 0.235 | 0.307 | 0.236 | 0.309 | 0.227 | 0.317 |
| | Negative Binomial | 0.225 | 0.316 | 0.229 | 0.314 | 0.220 | 0.322 |
| | Skellam Model | 0.220 | 0.321 | 0.221 | 0.321 | 0.217 | 0.322 |
| | Zero Infl. Skellam Model | 0.222 | 0.318 | 0.222 | 0.321 | 0.217 | 0.322 |
| **EPL** | Bivariate Poisson | 0.225 | 0.370 | 0.228 | 0.367 | 0.228 | 0.366 |
| | Diag. Infl. Bivariate Poisson | 0.224 | 0.369 | 0.232 | 0.362 | 0.233 | 0.360 |
| | Double Poisson | 0.229 | 0.364 | 0.234 | 0.360 | 0.235 | 0.356 |
| | Negative Binomial | 0.228 | 0.368 | 0.231 | 0.364 | 0.231 | 0.365 |
| | Skellam Model | 0.230 | 0.360 | 0.234 | 0.358 | 0.232 | 0.362 |
| | Zero Infl. Skellam Model | 0.228 | 0.361 | 0.236 | 0.358 | 0.235 | 0.358 |
| **La Liga** | Bivariate Poisson | 0.190 | 0.420 | 0.199 | 0.408 | 0.198 | 0.410 |
| | Diag. Infl. Bivariate Poisson | 0.189 | 0.421 | 0.198 | 0.409 | 0.200 | 0.406 |
| | Double Poisson | 0.190 | 0.419 | 0.199 | 0.407 | 0.199 | 0.410 |
| | Negative Binomial | 0.194 | 0.413 | 0.204 | 0.401 | 0.204 | 0.400 |
| | Skellam Model | 0.211 | 0.392 | 0.213 | 0.391 | 0.214 | 0.390 |
| | Zero Infl. Skellam Model | 0.209 | 0.394 | 0.213 | 0.390 | 0.214 | 0.390 |

### Table 4: Ranked Probability Score (RPS) and Pseudo-R2 - Second Half of Season

*Evaluated on the second half of the 2024/2025 season.*

| League | Model | Weighted Dynamic RPS | Weighted Dynamic Pseudo-R2 | Owen (2011) RPS | Owen (2011) Pseudo-R2 | Egidi et al. (2018) RPS | Egidi et al. (2018) Pseudo-R2 |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Bundesliga** | Bivariate Poisson | 0.222 | 0.336 | 0.224 | 0.334 | 0.223 | 0.335 |
| | Diag. Infl. Bivariate Poisson | 0.237 | 0.319 | 0.237 | 0.321 | 0.237 | 0.320 |
| | Double Poisson | 0.229 | 0.328 | 0.234 | 0.325 | 0.234 | 0.324 |
| | Negative Binomial | 0.226 | 0.330 | 0.232 | 0.327 | 0.232 | 0.326 |
| | Skellam Model | 0.223 | 0.321 | 0.224 | 0.321 | 0.224 | 0.322 |
| | Zero Infl. Skellam Model | 0.223 | 0.322 | 0.224 | 0.321 | 0.224 | 0.322 |
| **EPL** | Bivariate Poisson | 0.205 | 0.380 | 0.206 | 0.378 | 0.207 | 0.377 |
| | Diag. Infl. Bivariate Poisson | 0.211 | 0.378 | 0.210 | 0.377 | 0.209 | 0.378 |
| | Double Poisson | 0.207 | 0.377 | 0.207 | 0.377 | 0.206 | 0.378 |
| | Negative Binomial | 0.207 | 0.377 | 0.207 | 0.377 | 0.207 | 0.377 |
| | Skellam Model | 0.214 | 0.364 | 0.214 | 0.363 | 0.213 | 0.365 |
| | Zero Infl. Skellam Model | 0.215 | 0.363 | 0.213 | 0.365 | 0.212 | 0.366 |
| **La Liga** | Bivariate Poisson | 0.200 | 0.375 | 0.201 | 0.373 | 0.201 | 0.374 |
| | Diag. Infl. Bivariate Poisson | 0.200 | 0.376 | 0.201 | 0.374 | 0.201 | 0.374 |
| | Double Poisson | 0.200 | 0.374 | 0.200 | 0.373 | 0.200 | 0.373 |
| | Negative Binomial | 0.202 | 0.372 | 0.203 | 0.370 | 0.201 | 0.372 |
| | Skellam Model | 0.200 | 0.367 | 0.203 | 0.364 | 0.205 | 0.363 |
| | Zero Infl. Skellam Model | 0.200 | 0.368 | 0.203 | 0.364 | 0.204 | 0.364 |

                          18

## Page 19: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 19 页

Bayesian weighted discrete-time dynamic models for association football prediction                                                                Preprint


forecasting the remaining half-season, the best model for the Bundesliga and EPL is the bivariate Poisson, while
in La Liga it is the diagonal-inflated bivariate Poisson.

                                                                          Attack     Defense

                                Bundesliga                                     EPL                                          La Liga


           15




                                                                                                                                                         Last second half
           10



            5




           15




                                                                                                                                                         Last three rounds
φ values




           10



            5




           15




                                                                                                                                                         Final round
           10



            5


                1   2   3   4     5   6      7   8   9   10   1   2   3   4    5   6    7      8   9   10   1   2   3   4   5    6    7   8   9     10
                                                                              Periods

Figure 4: Posterior means (points) and 95% credible intervals (error bars) of the commensurate parameters for offensive
(red) and defensive (blue) abilities, under the three predictive scenarios for the Bundesliga, English Premier League (EPL),
and La Liga.




Appendix C Computational performance and convergence diagnostics
In terms of computation time, the proposed weighted dynamic approach outperforms the dynamic formulations of
Owen (2011) and Egidi et al. (2018) in all scenarios. Figure 5 shows the distribution of the elapsed computation
times (in seconds) for each method, divided by league and by the six goal-based models considered, evaluated
in the final round of the 2024/2025 season scenario. Specifically, for each model–league pair we performed
ten independent MCMC fits with four independent and parallel chains, each consisting of 2000 iterations, with
the initial 1000 iterations discarded as burn-in. Across all leagues and models, the weighted dynamic model
consistently requires the least computation time to reach convergence. The median run-time under the weighted
dynamic specification is lower than those of Owen (2011) and Egidi et al. (2018) methods for every combination
of league and model. Notably, in the most computationally demanding setting – the zero-inflated Skellam model
– our weighted dynamic model for the EPL is 32% faster than Owen’s version and 55% faster than Egidi et al.
(2018) approach. Even for relatively simpler models such as the double Poisson, the weighted dynamic version
reduces the runtime by approximately 32% with respect to Owen (2011) and by 31% with respect to Egidi et al.

                                                                              19

## Page 20: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 20 页

Bayesian weighted discrete-time dynamic models for association football prediction                                          Preprint


(2018) for the Bundesliga. In La Liga the weighted dynamic negative binomial model is 40% faster than Owen
(2011) and Egidi et al. (2018).

                                                           Weighted Dynamic   Owen (2011)   Egidi et al. (2018)

                                          Bundesliga                           EPL                                La Liga




                                                                                                                                Bivariate Poisson
                          100

                            80

                            60

                            40




                                                                                                                                Diag. Infl. Biv. Poisson
                          125

                          100

                            75

                            80




                                                                                                                                Double Poisson
                            70
 Elapsed Time (seconds)




                            60
                            50
                            40
                           30
                          200




                                                                                                                                Negative Binomial
                          175
                          150
                          125
                          100
                            75
                          1000

                          800




                                                                                                                                Skellam
                          600

                          400

                           200
                          1600




                                                                                                                                Zero−inflated Skellam
                          1200

                          800

                          400



Figure 5: Boxplots of elapsed computation times (in seconds). Results from the proposed weighted dynamic method are
shown alongside corresponding values from Owen (2011) and Egidi et al. (2018), all evaluated at the final round of the
2024/2025 season scenario.

    All three fitting methods achieved satisfactory convergence diagnostics for all the evaluated scenarios. In
particular, we verified that the MCMC chains for each model and method yielded Gelman-Rubin statistic 𝑅ˆ
(Gelman and Rubin, 1992) very close to 1.00 and large bulk and tail effective sample sizes, indicating stable
convergence. Table 5 shows a summary of the convergence metrics of the weighted dynamic method for the
                                                                                                    ˆ bulk and
final round of the 2024/2025 season scenario. Specifically, the means of the Gelman-Rubin statistic 𝑅,
tail effective sample sizes is shown for the 𝜷att , 𝜷def , 𝝓att and 𝝓def parameters. This suggests that the substantial
computational efficiency of the weighted dynamic approach does not come at the expense of sampler stability or
accuracy. Thus, the weighted dynamic model not only provides flexibility for dynamic team-specific parameters,
but does so with a lower computational cost.
                          Similar analyses on computational time and convergence for the other two predictive scenarios (last three
rounds and the second half of the 2024/2025 season) are presented in Figures 6 and 7, as well as Tables 6 and 7.


                                                                              20

## Page 21: MCMC Convergence Diagnostics (Table 5 & Figure 6)

源页：第 21 页

Bayesian weighted discrete-time dynamic models for association football prediction                                                      Preprint

### Table 5: MCMC convergence diagnostics: $\hat{R}$, bulk and tail effective sample sizes (ESS)

*Mean of the $\beta^{att}, \beta^{def}, \phi^{att}$ and $\phi^{def}$ parameters for the proposed weighted dynamic method, all evaluated at the final round of the 2024/2025 season scenario.*

| League | Model | $\beta^{att}: \hat{R}$ | Bulk | Tail | $\beta^{def}: \hat{R}$ | Bulk | Tail | $\phi^{att}: \hat{R}$ | Bulk | Tail | $\phi^{def}: \hat{R}$ | Bulk | Tail |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Bundesliga** | Bivariate Poisson | 1.00 | 4358 | 2889 | 1.00 | 4482 | 2960 | 1.00 | 2980 | 2742 | 1.00 | 3202 | 2711 |
| | Diag. Infl. Biv. Poisson | 1.00 | 4728 | 3020 | 1.00 | 4997 | 3061 | 1.00 | 3882 | 2940 | 1.00 | 4073 | 3157 |
| | Double Poisson | 1.00 | 4917 | 3008 | 1.00 | 5085 | 3012 | 1.00 | 4186 | 3032 | 1.00 | 4089 | 2839 |
| | Negative Binomial | 1.00 | 4036 | 3225 | 1.00 | 4993 | 3101 | 1.00 | 3658 | 2960 | 1.00 | 3878 | 2900 |
| | Skellam Model | 1.00 | 4772 | 3550 | 1.00 | 4802 | 3502 | 1.00 | 3370 | 3411 | 1.00 | 3431 | 3187 |
| | Zero Infl. Skellam Model | 1.00 | 4915 | 3554 | 1.00 | 4962 | 3567 | 1.00 | 3384 | 3338 | 1.00 | 3424 | 3287 |
| **EPL** | Bivariate Poisson | 1.00 | 4473 | 2903 | 1.00 | 4580 | 2980 | 1.00 | 2948 | 2671 | 1.00 | 3240 | 2858 |
| | Diag. Infl. Biv. Poisson | 1.00 | 4637 | 3016 | 1.00 | 4805 | 2983 | 1.00 | 3462 | 2981 | 1.00 | 3675 | 2832 |
| | Double Poisson | 1.00 | 4938 | 2951 | 1.00 | 5197 | 2960 | 1.00 | 3888 | 3114 | 1.00 | 3752 | 2931 |
| | Negative Binomial | 1.00 | 3560 | 3024 | 1.00 | 4824 | 3004 | 1.00 | 3584 | 3100 | 1.00 | 3552 | 3006 |
| | Skellam Model | 1.00 | 4253 | 3299 | 1.00 | 4344 | 3312 | 1.00 | 3415 | 3122 | 1.00 | 3189 | 2978 |
| | Zero Infl. Skellam Model | 1.00 | 4478 | 3370 | 1.00 | 4621 | 3380 | 1.00 | 3444 | 3235 | 1.00 | 3244 | 3074 |
| **La Liga** | Bivariate Poisson | 1.00 | 3898 | 2818 | 1.00 | 4100 | 2886 | 1.00 | 2993 | 2723 | 1.00 | 2933 | 2627 |
| | Diag. Infl. Biv. Poisson | 1.00 | 4289 | 2980 | 1.00 | 4583 | 3027 | 1.00 | 3805 | 2891 | 1.00 | 3592 | 2942 |
| | Double Poisson | 1.00 | 4655 | 2942 | 1.00 | 4820 | 2971 | 1.00 | 4099 | 3121 | 1.00 | 4100 | 3035 |
| | Negative Binomial | 1.00 | 3059 | 2917 | 1.00 | 4523 | 2911 | 1.00 | 3844 | 2878 | 1.00 | 3615 | 2887 |
| | Skellam Model | 1.00 | 3683 | 3168 | 1.00 | 3752 | 3187 | 1.00 | 3187 | 2793 | 1.00 | 3170 | 2978 |
| | Zero Infl. Skellam Model | 1.00 | 4056 | 3287 | 1.00 | 4062 | 3263 | 1.00 | 3382 | 3012 | 1.00 | 3535 | 3179 |


*Figure 6: Boxplots of elapsed computation times (in seconds). Results from the proposed weighted dynamic method are shown alongside corresponding values from Owen (2011) and Egidi et al. (2018), all evaluated at the last three matches of the 2024/2025 season scenario.*

## Page 22: MCMC Convergence Diagnostics (Table 6 & Table 7)

源页：第 22 页

Bayesian weighted discrete-time dynamic models for association football prediction                   Preprint

### Table 6: MCMC convergence diagnostics (Last Three Rounds)

*Evaluated at the last three rounds of the 2024/2025 season scenario.*

| League | Model | $\beta^{att}: \hat{R}$ | Bulk | Tail | $\beta^{def}: \hat{R}$ | Bulk | Tail | $\phi^{att}: \hat{R}$ | Bulk | Tail | $\phi^{def}: \hat{R}$ | Bulk | Tail |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Bundesliga** | Bivariate Poisson | 1.00 | 4532 | 2975 | 1.00 | 4908 | 3048 | 1.00 | 3206 | 2813 | 1.00 | 3436 | 3008 |
| | Diag. Infl. Biv. Poisson | 1.00 | 4722 | 3046 | 1.00 | 4796 | 3014 | 1.00 | 3604 | 2972 | 1.00 | 3830 | 2987 |
| | Double Poisson | 1.00 | 5013 | 3005 | 1.00 | 5258 | 3040 | 1.00 | 4058 | 2998 | 1.00 | 4248 | 3021 |
| | Negative Binomial | 1.00 | 3709 | 3111 | 1.00 | 5273 | 3064 | 1.00 | 3870 | 2979 | 1.00 | 3984 | 3023 |
| | Skellam Model | 1.00 | 4724 | 3469 | 1.00 | 4841 | 3492 | 1.00 | 3308 | 3214 | 1.00 | 3254 | 2999 |
| | Zero Infl. Skellam Model | 1.00 | 4788 | 3552 | 1.00 | 4862 | 3557 | 1.00 | 3364 | 3254 | 1.00 | 3481 | 3337 |
| **EPL** | Bivariate Poisson | 1.00 | 4302 | 2885 | 1.00 | 4413 | 2920 | 1.00 | 3079 | 2829 | 1.00 | 3002 | 2832 |
| | Diag. Infl. Biv. Poisson | 1.00 | 4635 | 2990 | 1.00 | 4785 | 2989 | 1.00 | 3434 | 3057 | 1.00 | 3529 | 2957 |
| | Double Poisson | 1.00 | 4868 | 2978 | 1.00 | 5008 | 2964 | 1.00 | 3647 | 2841 | 1.00 | 3939 | 2914 |
| | Negative Binomial | 1.00 | 3536 | 3022 | 1.00 | 4705 | 2963 | 1.00 | 3540 | 2868 | 1.00 | 3427 | 2675 |
| | Skellam Model | 1.00 | 4643 | 3447 | 1.00 | 4781 | 3457 | 1.00 | 3456 | 3226 | 1.00 | 3390 | 3116 |
| | Zero Infl. Skellam Model | 1.00 | 4628 | 3409 | 1.00 | 4772 | 3440 | 1.00 | 3241 | 3206 | 1.00 | 3338 | 3084 |
| **La Liga** | Bivariate Poisson | 1.00 | 4129 | 2888 | 1.00 | 4026 | 2884 | 1.00 | 2894 | 2843 | 1.00 | 3037 | 2710 |
| | Diag. Infl. Biv. Poisson | 1.00 | 4451 | 3016 | 1.00 | 4584 | 3000 | 1.00 | 3753 | 2999 | 1.00 | 3651 | 2940 |
| | Double Poisson | 1.00 | 4839 | 2969 | 1.00 | 4863 | 2938 | 1.00 | 4056 | 2887 | 1.00 | 4029 | 2939 |
| | Negative Binomial | 1.00 | 2873 | 2821 | 1.00 | 4283 | 2892 | 1.00 | 3862 | 2964 | 1.00 | 3562 | 2886 |
| | Skellam Model | 1.00 | 4210 | 3303 | 1.00 | 4288 | 3292 | 1.00 | 3592 | 3101 | 1.00 | 3450 | 2919 |
| | Zero Infl. Skellam Model | 1.00 | 4259 | 3307 | 1.00 | 4342 | 3317 | 1.00 | 3221 | 3005 | 1.00 | 3289 | 2957 |


### Table 7: MCMC convergence diagnostics (Second Half of Season)

*Evaluated at the second half of the 2024/2025 season scenario.*

| League | Model | $\beta^{att}: \hat{R}$ | Bulk | Tail | $\beta^{def}: \hat{R}$ | Bulk | Tail | $\phi^{att}: \hat{R}$ | Bulk | Tail | $\phi^{def}: \hat{R}$ | Bulk | Tail |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Bundesliga** | Bivariate Poisson | 1.00 | 4980 | 3057 | 1.00 | 5358 | 3135 | 1.00 | 3225 | 2945 | 1.00 | 3584 | 2998 |
| | Diag. Infl. Biv. Poisson | 1.00 | 4784 | 3157 | 1.00 | 4949 | 3128 | 1.00 | 3602 | 2981 | 1.00 | 3552 | 2974 |
| | Double Poisson | 1.00 | 5298 | 3158 | 1.00 | 5502 | 3181 | 1.00 | 4151 | 3136 | 1.00 | 4194 | 3099 |
| | Negative Binomial | 1.00 | 4517 | 3365 | 1.00 | 5063 | 3218 | 1.00 | 3877 | 3129 | 1.00 | 3789 | 3151 |
| | Skellam Model | 1.00 | 4736 | 3501 | 1.00 | 4811 | 3536 | 1.00 | 3495 | 3385 | 1.00 | 3410 | 3324 |
| | Zero Infl. Skellam Model | 1.00 | 4830 | 3592 | 1.00 | 4832 | 3562 | 1.00 | 3432 | 3372 | 1.00 | 3383 | 3340 |
| **EPL** | Bivariate Poisson | 1.00 | 4894 | 2994 | 1.00 | 5053 | 2971 | 1.00 | 3152 | 2855 | 1.00 | 3205 | 2841 |
| | Diag. Infl. Biv. Poisson | 1.00 | 5361 | 3112 | 1.00 | 5581 | 3096 | 1.00 | 3831 | 3102 | 1.00 | 3856 | 3145 |
| | Double Poisson | 1.00 | 5288 | 3017 | 1.00 | 5561 | 3023 | 1.00 | 3968 | 3003 | 1.00 | 3855 | 3083 |
| | Negative Binomial | 1.00 | 4330 | 3294 | 1.00 | 5161 | 3199 | 1.00 | 3605 | 2939 | 1.00 | 3642 | 3191 |
| | Skellam Model | 1.00 | 4707 | 3432 | 1.00 | 4828 | 3475 | 1.00 | 3403 | 3192 | 1.00 | 3430 | 3147 |
| | Zero Infl. Skellam Model | 1.00 | 4610 | 3374 | 1.00 | 4722 | 3407 | 1.00 | 3358 | 3199 | 1.00 | 3299 | 3062 |
| **La Liga** | Bivariate Poisson | 1.00 | 3898 | 2818 | 1.00 | 4100 | 2886 | 1.00 | 2993 | 2723 | 1.00 | 2993 | 2627 |
| | Diag. Infl. Biv. Poisson | 1.00 | 4289 | 2980 | 1.00 | 4583 | 3027 | 1.00 | 3805 | 2891 | 1.00 | 3592 | 2947 |
| | Double Poisson | 1.00 | 4655 | 2942 | 1.00 | 4820 | 2971 | 1.00 | 3491 | 3221 | 1.00 | 3509 | 3045 |
| | Negative Binomial | 1.00 | 3059 | 2917 | 1.00 | 4523 | 2911 | 1.00 | 3844 | 2878 | 1.00 | 3615 | 2887 |
| | Skellam Model | 1.00 | 3683 | 3168 | 1.00 | 3752 | 3187 | 1.00 | 3187 | 2793 | 1.00 | 3170 | 2978 |
| | Zero Infl. Skellam Model | 1.00 | 4056 | 3287 | 1.00 | 4062 | 3263 | 1.00 | 3382 | 3012 | 1.00 | 3535 | 3179 |


## Page 23: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 23 页

Bayesian weighted discrete-time dynamic models for association football prediction                                    Preprint


                                                     Weighted Dynamic   Owen (2011)   Egidi et al. (2018)

                                   Bundesliga                            EPL                                La Liga

                            80




                                                                                                                          Bivariate Poisson
                            70
                            60
                            50
                            40




                                                                                                                          Diag. Infl. Biv. Poisson
                          120

                          100

                            80



                            60




                                                                                                                          Double Poisson
 Elapsed Time (seconds)




                            50

                            40

                          150




                                                                                                                          Negative Binomial
                          130

                          110

                            90

                            70


                          1000




                                                                                                                          Skellam
                          500




                                                                                                                          Zero−inflated Skellam
                          1250
                          1000
                          750
                          500
                          250


Figure 7: Boxplots of elapsed computation times (in seconds). Results from the proposed weighted dynamic method are
shown alongside corresponding values from Owen (2011) and Egidi et al. (2018), all evaluated at the second half of the
2024/2025 season scenario.


References
Alt, E. M., Chen, X., Carvalho, L. M., and Ibrahim, J. G. (2025). hdbayes: An R package for Bayesian analysis
                 of generalized linear models using historical data. arXiv preprint arXiv:2506.20060.

Baio, G. and Blangiardo, M. (2010). Bayesian hierarchical model for the prediction of football results. Journal
                 of Applied Statistics, 37(2):253–264.

Breiman, L. (2001). Random forests. Machine Learning, 45(1):5–32.

Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. Monthey Weather Review,,
                 78(1):1–3.

Carpenter, B., Gelman, A., Hoffman, M. D., Lee, D., Goodrich, B., Betancourt, M., Brubaker, M., Guo, J., Li,
                 P., and Riddell, A. (2017). Stan: A probabilistic programming language. Journal of Statistical Software,
                 76(1):1–32.

                                                                        23

## Page 24: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 24 页

Bayesian weighted discrete-time dynamic models for association football prediction                          Preprint


Carpita, M., Ciavolino, E., and Pasca, P. (2019). Exploring and modelling team performances of the Kaggle
  European soccer database. Statistical Modelling, 19(1):74–101.

Carpita, M., Sandri, M., Simonetto, A., and Zuccolotto, P. (2015). Discovering the drivers of football match
  outcomes with data mining. Quality Technology & Quantitative Management, 12(4):561–577.

Chen, N., Carlin, B. P., and Hobbs, B. P. (2018). Web-based statistical tools for the analysis and design of clinical
  trials that incorporate historical controls. Computational Statistics & Data Analysis, 127:50–68.

Dixon, M. J. and Coles, S. G. (1997). Modelling association football scores and inefficiencies in the football
  betting market. Journal of the Royal Statistical Society: Series C (Applied Statistics), 46(2):265–280.

Dobson, S., Goddard, J. A., and Dobson, S. (2001). The economics of football, volume 10. Cambridge University
  Press Cambridge.

Egidi, L., Macrı̀-Demartino, R., and Palaskas., V. (2025). footBayes: Fitting Bayesian and MLE Football Models.
  R package version 2.1.0.

Egidi, L., Pauli, F., and Torelli, N. (2018). Combining historical data and bookmakers’ odds in modelling football
  scores. Statistical Modelling, 18(5-6):436–459.

Egidi, L. and Torelli, N. (2021). Comparing goal-based and result-based approaches in modelling football
  outcomes. Social Indicators Research, 156(2):801–813.

Epstein, E. S. (1969). A scoring system for probability forecasts of ranked categories. Journal of Applied
  Meteorology (1962-1982), 8(6):985–987.

Gelman, A. (2006). Prior distributions for variance parameters in hierarchical models (comment on article by
  Browne and Draper). Bayesian Analysis, 1(3):515–534.

Gelman, A., Jakulin, A., Pittau, M. G., and Su, Y.-S. (2008). A weakly informative default prior distribution for
  logistic and other regression models. The Annals of Applied Statistics, 2(4):1360 – 1383.

Gelman, A. and Rubin, D. B. (1992). Inference from iterative simulation using multiple sequences. Statistical
  science, 7(4):457–472.

Groll, A. and Abedieh, J. (2013). Spain retains its title and sets a new record – generalized linear mixed models
  on European football championships. Journal of Quantitative Analysis in Sports, 9(1):51–66.

Groll, A., Cristophe, L., Hans, V. E., and Gunther, S. (2019a). A hybrid random forest to predict soccer matches
  in international tournaments. Journal of Quantitative Analysis in Sports, 15(4):271–287.

Groll, A., Hvattum, L. M., Ley, C., Popp, F., Schauberger, G., Van Eetvelde, H., and Zeileis, A. (2021). Hybrid
  machine learning forecasts for the UEFA EURO 2020. arXiv preprint arXiv:2106.05799.

Groll, A., Hvattum, L. M., Ley, C., Sternemann, J., Schauberger, G., and Zeileis, A. (2024). Modeling and
  prediction of the uefa euro 2024 via combined statistical learning approaches. arXiv preprint arXiv:2410.09068.

Groll, A., Ley, C., Schauberger, G., Van Eetvelde, H., and Zeileis, A. (2019b). Hybrid machine learning forecasts
  for the fifa women’s world cup 2019. arXiv preprint arXiv:1906.01131.

                                                         24

## Page 25: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 25 页

Bayesian weighted discrete-time dynamic models for association football prediction                         Preprint


Hobbs, B. P., Carlin, B. P., Mandrekar, S. J., and Sargent, D. J. (2011). Hierarchical commensurate and power prior
  models for adaptive incorporation of historical information in clinical trials. Biometrics, 67(3):1047–1056.

Hobbs, B. P., Sargent, D. J., and Carlin, B. P. (2012). Commensurate priors for incorporating historical
  information in clinical trials using general and generalized linear models. Bayesian Analysis, 7(3):639–674.

Hong, H., Fu, H., and Carlin, B. P. (2018). Power and commensurate priors for synthesizing aggregate and
  individual patient level data in network meta-analysis. Journal of the Royal Statistical Society Series C:
  Applied Statistics, 67(4):1047–1069.

Karlis, D. and Ntzoufras, I. (2003). Analysis of sports data by using bivariate Poisson models. Journal of the
  Royal Statistical Society: Series D (The Statistician), 52(3):381–393.

Karlis, D. and Ntzoufras, I. (2009). Bayesian modelling of football outcomes: using the Skellam’s distribution
  for the goal difference. IMA Journal of Management Mathematics, 20(2):133–145.

Koning, R. H. (2000). Balance in competition in Dutch soccer. Journal of the Royal Statistical Society: Series D
  (The Statistician), 49(3):419–431.

Koopman, S. J. and Lit, R. (2015). A dynamic bivariate Poisson model for analysing and forecasting match
  results in the English Premier League. Journal of the Royal Statistical Society. Series A (Statistics in Society),
  178(1):167–186.

Koopman, S. J. and Lit, R. (2019). Forecasting football match results in national league competitions using
  score-driven time series models. International Journal of Forecasting, 35(2):797–809.

Macrı̀ Demartino, R., Egidi, L., and Torelli, N. (2025). Alternative ranking measures to predict international
  football results. Computational Statistics, 40(4):1899–1917.

Maher, M. J. (1982). Modelling association football scores. Statistica Neerlandica, 36(3):109–118.

Mitchell, T. J. and Beauchamp, J. J. (1988). Bayesian variable selection in linear regression. Journal of the
  american statistical association, 83(404):1023–1032.

Murray, T. A., Hobbs, B. P., and Carlin, B. P. (2015). Combining nonexchangeable functional or survival
  data sources in oncology using generalized mixture commensurate priors. The annals of applied statistics,
  9(3):1549.

Ntzoufras, I. (2011). Bayesian Modeling Using WinBUGS, volume 698. John Wiley & Sons, Hoboken, New
  Jersey, USA.

Ouma, L. O., Grayling, M. J., Wason, J. M., and Zheng, H. (2022). Bayesian modelling strategies for borrowing
  of information in randomised basket trials. Journal of the Royal Statistical Society Series C: Applied Statistics,
  71(5):2014–2037.

Owen, A. (2011). Dynamic Bayesian forecasting models of football match outcomes with estimation of the
  evolution variance parameter. IMA Journal of Management Mathematics, 22(2):99–113.



                                                        25

## Page 26: Bayesian weighted discrete-time dynamic models for association football predicti

源页：第 26 页

Bayesian weighted discrete-time dynamic models for association football prediction                       Preprint


Pocock, S. J. (1976). The combination of randomized and historical controls in clinical trials. Journal of chronic
  diseases, 29(3):175–188.

R Core Team (2025). R: A Language and Environment for Statistical Computing. R Foundation for Statistical
  Computing, Vienna, Austria.

Reep, C., Pollard, R., and Benjamin, B. (1971). Skill and chance in ball games. Journal of the Royal Statistical
  Society Series A: Statistics in Society, 134(4):623–629.

Rue, H. and Øyvind Salvesen (2000). Prediction and retrospective analysis of soccer matches in a league. Journal
  of the Royal Statistical Society. Series D (The Statistician), 49(3):399–418.

Schauberger, G. and Groll, A. (2018). Predicting matches in international football tournaments with random
  forests. Statistical Modelling, 18(5-6):460–482.

Skellam, J. G. (1946). The frequency distribution of the difference between two Poisson variates belonging to
  different populations. Journal of the Royal Statistical Society Series A: Statistics in Society, 109(3):296–296.

Spiegelhalter, D. and Ng, Y.-L. (2009). One match to go! Significance, 6(4):151–153.

Zheng, H. and Wason, J. M. (2022). Borrowing of information across patient subgroups in a basket trial based
  on distributional discrepancy. Biostatistics, 23(1):120–135.




                                                       26
