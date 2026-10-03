# Tests of Conditional Predictive Ability

> 重建说明：模式 transcribe；来源 `2006_Giacomini_条件预测能力检验.pdf`；共 34 页；原图逐页查看 34/34 页。
> 核图证据：对照 `.ky-md-work/2006_Giacomini_条件预测能力检验/pages/` 下 page-01.png 至 page-34.png 全量 34 页原图，重构 Table I-V 全量标准 Markdown 管道表格，全保真修复条件预测能力检验定理 1-4 (公式 1-8)、预测组合与最优决策规则 (公式 9-12)、实证模型 (公式 14) 与附录渐近分布证明。

## Page 01: Econometrica, Vol. 74, No. 6 (November, 2006), 1545–1578

源页：第 1 页

Econometrica, Vol. 74, No. 6 (November, 2006), 1545–1578

             TESTS OF CONDITIONAL PREDICTIVE ABILITY

               BY RAFFAELLA GIACOMINI AND HALBERT WHITE1
       We propose a framework for out-of-sample predictive ability testing and forecast
    selection designed for use in the realistic situation in which the forecasting model is
    possibly misspecified, due to unmodeled dynamics, unmodeled heterogeneity, incor-
    rect functional form, or any combination of these. Relative to the existing literature
    (Diebold and Mariano (1995) and West (1996)), we introduce two main innovations:
    (i) We derive our tests in an environment where the finite sample properties of the
    estimators on which the forecasts may depend are preserved asymptotically. (ii) We
    accommodate conditional evaluation objectives (can we predict which forecast will be
    more accurate at a future date?), which nest unconditional objectives (which forecast
    was more accurate on average?), that have been the sole focus of previous literature.
    As a result of (i), our tests have several advantages: they capture the effect of estima-
    tion uncertainty on relative forecast performance, they can handle forecasts based on
    both nested and nonnested models, they allow the forecasts to be produced by general
    estimation methods, and they are easy to compute. Although both unconditional and
    conditional approaches are informative, conditioning can help fine-tune the forecast
    selection to current economic conditions. To this end, we propose a two-step decision
    rule that uses current information to select the best forecast for the future date of inter-
    est. We illustrate the usefulness of our approach by comparing forecasts from leading
    parameter-reduction methods for macroeconomic forecasting using a large number of
    predictors.

       KEYWORDS: Forecast evaluation, out-of-sample, hypothesis test.


                                     1. INTRODUCTION
FORECASTING IS CENTRAL to economic decision-making. Government insti-
tutions and regulatory authorities often base policy decisions on forecasts of
major economic variables, and firms rely on forecasting for inventory man-
agement and production planning decisions. A problem economic forecasters
often face is how to evaluate the relative merit of two or more forecast alterna-
tives. One answer to this problem is to develop out-of-sample tests to compare
the predictive ability of competing forecasts, given a general loss function. This
literature was initiated by Diebold and Mariano (1995) and further formalized
by West (1996), McCracken (2000), Clark and McCracken (2001), Corradi,
Swanson, and Olivetti (2001), and Chao, Corradi, and Swanson (2001), among

   1
     Discussions with Clive Granger, Graham Elliott, and Andrew Patton were essential to the
paper. Useful comments from a co-editor and three anonymous referees led to a considerably
improved version of the paper. We also thank Lutz Kilian for insightful suggestions and Farshid
Vahid, Matteo Iacoviello, Mike McCracken, and seminar participants at UCSD, Nuffield Col-
lege, LSE, University of Exeter, University of Warwick, University of Manchester, Cass Business
School, North Carolina State University, Boston College, Texas A&M, University of Chicago
GSB, the International Finance Division of the Federal Reserve Board, University of Houston,
UCLA, Harvard/MIT, and the 2002 EC2 conference in Bologna, Italy for helpful comments. We
thank Vince Crawford for the use of the UCSD Experimental and Computational Lab.

                                               1545

## Page 02: 1546 R. GIACOMINI AND H. WHITE

源页：第 2 页

1546                         R. GIACOMINI AND H. WHITE

others. This work represents a generalization of previous evaluation tech-
niques that restricted attention to a particular loss function (e.g., Granger and
Newbold (1977), Leitch and Tanner (1991), West, Edison, and Cho (1993),
Harvey, Leybourne, and Newbold (1997)).
   In this paper, we develop a framework for out-of-sample predictive ability
testing and forecast selection designed for use when the forecasting model may
be misspecified. It applies to multistep point, interval, probability, or density
forecast evaluation for a general loss function. Our tests are a complement to
the existing approach to predictive ability testing (which in the remainder of
the paper we consider to be represented by Diebold and Mariano (1995) and
West (1996), henceforth referenced as DMW), and at the same time they can
be viewed as extending the DMW tests because they apply in all cases in which
those tests are applicable and in many more besides.
   We introduce two main methodological innovations: (i) motivated by the
consequences of misspecification, we consider forecasts based on limited mem-
ory estimators, whose finite sample properties are preserved asymptotically;
and (ii) we formulate the problem of forecast evaluation as a problem of infer-
ence about conditional expectations of forecasts and forecast errors that nests
the unconditional expectations that are the sole focus of the existing literature.
We accordingly propose two tests: a general test of equal conditional predictive
ability of two competing forecasts and, as a special case, a test of equal uncon-
ditional predictive ability. Although the latter coincides with the test proposed
by Diebold and Mariano (1995), we provide primitive conditions that ensure
its validity and extend it to an environment that permits parameter estimation.
   Regardless of whether we take a conditional or an unconditional perspec-
tive, preserving the finite sample behavior of the estimators in our evaluation
procedure has a number of consequences that give our tests some appealing
properties. First, they directly reflect the effect of estimation uncertainty on
relative forecast performance, whereas the DMW tests do not, for example,
take into account differing model complexities unless they are explicitly incor-
porated into the loss function (e.g., Akaike information criterion and Bayesian
information criterion (BIC)).2 As a result, our object of evaluation is not sim-
ply the forecasting model as in the DMW approach, but what we call the fore-
casting method. This includes the forecasting model along with a number of
choices that must be made by the forecaster at the time of the prediction and
that can affect future forecast performance, such as which estimation proce-
dure to choose and what data to use for estimation. A second advantage is
that our framework permits a unified treatment of nested and nonnested mod-
els, whereas the tests of West (1996) are not applicable to nested models. The
comparison between nested models is important because it is often of inter-
est to test whether forecasts from a given model can outperform those from

  2
    A recent paper by Clark and West (2005) suggests an alternative way to overcome this prob-
lem in the context of testing the martingale difference hypothesis.

## Page 03: TESTS OF PREDICTIVE ABILITY 1547

源页：第 3 页

TESTS OF PREDICTIVE ABILITY                          1547

a nested benchmark model. Third, we can accommodate general estimation
procedures in the derivation of the forecasts, including Bayesian and semi- and
nonparametric estimation methods that are excluded from the DMW frame-
work. A final, practical advantage of our tests is that they are easily computed
using standard regression software, whereas the existing tests can be difficult
to compute or have limiting distributions that are context-specific (e.g., the
nested test of Clark and McCracken (2001)).
   Concerning our second innovation, we emphasize that we are not recom-
mending the conditional over the unconditional approach. Rather we provide
a framework in which both make sense, and it is up to the researcher to de-
cide which is more appropriate given her objectives. The unconditional ap-
proach asks which forecast was more accurate, on average, in the past; it may
thus be appropriate for making recommendations about which forecast may
be better for an unspecified future date. The conditional approach asks in-
stead whether we can use available information—above and beyond past av-
erage behavior—to predict which forecast will be more accurate for a specific
future date. A simple analogy may be helpful in understanding this distinction.
Viewing the difference in forecast performance (e.g., squared prediction er-
ror) as the dependent variable in a regression that contains only a constant,
the unconditional approach is like a test for whether the regression intercept
is zero, whereas the conditional approach is like a test for serial correlation in
the regression errors.
   In applications, one rarely has sufficient knowledge to guarantee correct
specification of one’s forecasting model. Instead, misspecification is common,
as a result of inadequately modeled dynamics, inadequately modeled hetero-
geneity, incorrect functional form, or any combination of these. To accommo-
date each of these possible sources of misspecification, we permit but do not
require the underlying data-generating process (DGP) to be heterogeneous.
For example, the DGP can have structural shifts at unknown dates. When the
forecasting model is misspecified, it is often the case that forecasts based on
estimators using an expanding data window can be less reliable than forecasts
based on estimators with a limited memory. For example, when there is inad-
equately modeled heterogeneity, observations from the more distant past may
lose their predictive relevance. Alternatively, when dynamics are inadequately
modeled, a limited memory estimator can better track a series of interest. To
illustrate this last point, consider predicting an AR(1) process using a regres-
sion model that is misspecified by omitting the lagged dependent variable and
including only a constant. The expanding window forecast is just the sample
mean. A simple equal-weight finite moving average (MA) of the preceding
data values provides a limited memory forecasting method based on the same
model. Both forecasts are unbiased, but the MA predictor can often track the
target of interest well, whereas the sample mean performs essentially no track-
ing. The simplicity of this example is not crucial. Any dynamic misspecification
yields the same essential features.

## Page 04: 1548 R. GIACOMINI AND H. WHITE

源页：第 4 页

1548                     R. GIACOMINI AND H. WHITE

   Similarly, when the prediction model functional form is misspecified and the
target series exhibits memory (e.g., is autocorrelated), a limited memory es-
timator can provide more reliable forecasts than an expanding window-based
forecast, because the limited memory estimator can provide a local approx-
imation to the prediction relationship (and therefore potentially more accu-
rate prediction, given the memory of the target series), whereas the expanding
memory estimator provides a global approximation (and therefore potentially
less accurate prediction).
   Accordingly, we focus on limited memory forecasting methods. One class of
well known and widely applied limited memory forecasts is “rolling window”
forecasts, such as those introduced by Fama and MacBeth (1973) and Gonedes
(1973). Not only are these methods familiar, but they also afford considerable
analytical convenience. For these reasons, our primary focus will be on rolling
window methods. As straightforward as rolling window methods are, they nev-
ertheless permit a rich variety of possibilities. For example, two rolling window
methods can have different estimation windows and apply different weight-
ing schemes within those windows. The choice of estimation window can even
be data driven, as in the procedure suggested by Pesaran and Timmermann
(2006), so that two competing forecasting methods can use different data-
driven window choice procedures. In any given application, it is an empirical
matter as to whether a limited memory or an expanding memory method pro-
vides better forecasts. Our methods can provide direct evidence on this point,
as demonstrated in our empirical example in Section 7, where we see numer-
ous examples of limited memory predictors outperforming expanding window
predictors.
   Although our main focus is on rolling window methods, our results are also
valid for a “fixed estimation sample” forecasting scheme, which involves esti-
mating the models’ parameters only once over the in-sample data and using
these to produce all out-of-sample forecasts.
   A final, important implication of our approach is that it provides a basis to
make forecast selection decisions in cases where equal (conditional) predictive
ability is rejected. As an example, we propose a simple decision rule for fore-
cast selection based on the idea that, because rejection means that the relative
performance of the competing forecasts is predictable, we should exploit cur-
rent information to predict which forecast will be more accurate in the future.
   To illustrate the usefulness of our approach, we consider, from both the con-
ditional and the unconditional perspectives, the problem of macroeconomic
forecasting using a large number of predictors and compare multistep fore-
casts of four macroeconomic variables (two measures of real activity and two
price indexes) obtained by leading methods for parameter reduction: a simpli-
fied version of the general-to-specific model selection approach of Hoover and
Perez (1999), the “diffusion indexes” approach of Stock and Watson (2002),
and the use of Bayesian shrinkage estimators (Litterman (1986)). These fore-
casts cannot be compared using any previous method. We conclude that for

## Page 05: TESTS OF PREDICTIVE ABILITY 1549

源页：第 5 页

TESTS OF PREDICTIVE ABILITY                           1549

the price indexes, these methods are no better than a simple autoregres-
sion, whereas for the real variables, Bayesian shrinkage is the best perform-
ing method. The simplified general-to-specific method is characterized by an
overall poor performance.

   2. A NEW APPROACH TO OUT-OF-SAMPLE PREDICTIVE ABILITY TESTING
  In this section, we set forth our approach and discuss the main differences
between our approach and previous approaches to out-of-sample predictive
ability testing.

                2.1. Null Hypothesis and Asymptotic Framework
  Suppose one wants to compare the accuracy of competing forecasts ft (β1 )
and gt (β2 ) for the τ-steps-ahead variable Yt+τ , using a loss function Lt+τ (·).
The DMW approach tests
                                                                
$$H_0 : \mathbb{E}[L_{t+\tau}(Y_{t+\tau}, f_t(\beta_1^*)) - L_{t+\tau}(Y_{t+\tau}, g_t(\beta_2^*))] = 0 \tag{1}$$ 

where β∗1 and β∗2 are population values (i.e., probability limits of the parameter
estimates). This makes (1) a statement about the forecasting models: H0 says
that the models are equally accurate on average. A key feature of West’s (1996)
test of H0 is the recognition and accommodation of the fact that, although H0
concerns population values, the actual forecasts that appear in the test statistic
depend on estimated parameters.
  Our central idea is to test a null hypothesis that differs from the DMW null in
two respects: (i) the losses depend on estimates β̂1t and β̂2t , rather than on their
probability limits; and (ii) the expectation is conditional on some information
set Gt :
                                                                      
$$H_0 : \mathbb{E}[L_{t+\tau}(Y_{t+\tau}, f_t(\hat{\beta}_{1t})) - L_{t+\tau}(Y_{t+\tau}, g_t(\hat{\beta}_{2t})) \mid \mathcal{G}_t] = 0 \tag{2}$$

The focus on parameter estimates makes (2) a statement about the forecasting
methods, which include the models as well as the estimation procedures and
the possible choices of estimation window (note that the two forecasts may
use different estimation windows). Our null says that one cannot predict which
forecasting method will be more accurate at the forecast target date t + τ using
the information in Gt .
   Regardless of the choice of Gt , expressing the null in terms of parameter es-
timates is useful because it allows us to capture the impact of estimation uncer-
tainty on relative forecast performance. For example, by comparing expected
estimated mean squared forecast errors (MSE), rather than their population
counterparts, we accommodate the possibility of a bias–variance trade-off such
that forecasts from a small, misspecified model (biased with low variance)

## Page 06: 1550 R. GIACOMINI AND H. WHITE

源页：第 6 页

1550                      R. GIACOMINI AND H. WHITE

are as accurate as forecasts from a large, correctly specified model (unbi-
ased with high variance). Because of its focus on the forecasting model rather
than the forecasting method, the DMW approach cannot accommodate such
a trade-off. This emphasizes the distinction between evaluation of a forecast-
ing method, which is a practical matter, and evaluation of a forecasting model,
which may be appropriate for obtaining economic insight, but is less informa-
tive for prediction purposes.
   An implication of testing different null hypotheses is that the tests of
(1) and (2) are analyzed in different out-of-sample asymptotic environments.
Whereas the test of West (1996) is analyzed in an environment where parame-
ter estimates converge to their population values, we operate in an environ-
ment with asymptotically nonvanishing estimation uncertainty. This ensures
that our tests capture the impact of estimation uncertainty on forecast perfor-
mance. Furthermore, as we discuss in detail in Section 3.2, this has the impor-
tant advantage that our tests can handle nested and nonnested models in a
unified framework.
   We achieve nonvanishing estimator uncertainty by considering estimators
with limited memory, in particular, rolling window estimators, a method pop-
ular among practitioners ever since its influential use by Fama and MacBeth
(1973) and Gonedes (1973). Limited memory estimators are especially appro-
priate in the misspecified predictor environments considered here, because
they discount or exclude older data that may either no longer be informative
about the predictive relationships of current interest or prevent a dynamically
misspecified model from tracking well. Other relevant limited memory estima-
tors are recursive estimators of the exponential smoothing type or, as suggested
by a referee, expanding window weighted least squares estimators with weights
that more heavily discount less recent observations. We work explicitly with
rolling window estimators, not only because of their popularity among practi-
tioners, but also for two further reasons: first, this approach affords significant
generality, because it imposes no restrictions on the estimators other than fi-
nite memory, whereas the alternatives are comparatively specific; second, the
analysis required for this approach is straightforward, whereas that for the al-
ternatives is more involved, but has no compensating increase in insight.
   Regarding the choice of the conditioning set Gt , a leading case of interest
is Gt = Ft , the time-t information set. Another possibility is Gt = {∅,  Ω}, the
trivial σ-field, which yields a test of equal unconditional predictive ability. The
choice of the relevant conditioning set will depend on the objectives of the
evaluator. Letting Gt = {∅,  Ω} seems appropriate if the goal is to provide a
forecast for an unspecified date in the future, in which case it makes sense to
base recommendations on which forecast may be better on average. If, on the
other hand, the goal is to produce a forecast for a specific date τ periods in
the future, choosing Gt = Ft may be more appropriate, because it allows us
to ask whether there is additional current information that can help predict
which forecast will be more accurate for that date. Conditioning (i.e., letting

## Page 07: TESTS OF PREDICTIVE ABILITY 1551

源页：第 7 页

TESTS OF PREDICTIVE ABILITY                                   1551

Gt , = {∅,  Ω}) when testing relative forecast performance is important, because
it is plausible with misspecification to expect some predictability in future loss
differences. For example, the relative performance may be characterized by
persistence, so that if a forecast outperforms its competitor today, it may be
likely to do so tomorrow. In this case, past loss differences may predict fu-
ture loss differences. We may also expect the performance of certain models
to depend on the state of the economy, so that a business cycle indicator may
tell us which forecast is preferable for a future date, given current economic
conditions.
   Even though our framework nests both conditional and unconditional ob-
jectives, for succinctness we refer to a test of (2) as a test of equal conditional
predictive ability.

                                  2.2. Data Assumptions
   One of the conclusions of Clements and Hendry (1998, 1999) is that the main
explanation for systematic forecast failure in economics is the use of mod-
els that are inadequate to handle the nonconstant data-generating processes
that govern real-world economic data. Specific sources of heterogeneity in
economic series are several, including changes in the measurement process,
changes in laws, and changes in technology. Any failure to model this hetero-
geneity will result in misspecification. As previously remarked, incorrect func-
tional form or omission of lags (either own lags or lags of predictively relevant
variables) also yields a misspecified prediction model. To accommodate each
of these possible sources of misspecification, we operate in a data environment
that permits but does not require data heterogeneity.3

                                         3. THEORY
                          3.1. Description of the Environment
   Consider a stochastic process W ≡ {Wt : Ω → Rs+1 ,  s ∈ N,  t = 1,  2,  . . . } de-
fined on a complete probability space (Ω,  F ,  P). We partition the observed
vector Wt as Wt ≡ (Yt ,  Xt' )' , where Yt : Ω → R is the variable of interest
and Xt : Ω → Rs is a vector of predictor variables, and we define Ft =
σ(W1' ,  . . . ,  Wt ' )' (cf., White (1994, p. 96)).
   We focus for simplicity on univariate forecasts. Suppose two alternative
models are used to forecast the variable of interest τ steps ahead, Yt+τ . The
(point, interval, probability, or density) forecasts formulated at time t are based
on the information set Ft and are denoted by fˆt, mf ≡ f (Wt ,  Wt−1 ,  . . . ,  Wt−mf +1 ;

  3
   The type of nonstationarity we consider here is that induced by distributions that change over
time. We also assume short memory, thus ruling out nonstationarity due to the presence of unit
roots.

## Page 08: 1552 R. GIACOMINI AND H. WHITE

源页：第 8 页

1552                           R. GIACOMINI AND H. WHITE

β̂t, m ) and ĝt, mg ≡ g(Wt ,  Wt−1 ,  . . . ,  Wt−mg +1 ; β̂t, m ), where f and g are measur-
able functions. The subscripts indicate that the time-t forecasts are measur-
able functions of a sample of size mf for f and of size mg for g. If the forecasts
are based on parametric models, the parameter estimates from the two mod-
els are collected in the k × 1 vector β̂t, m , where m ≡ max(mf ,  mg ). Other-
wise, β̂t, m represents whatever semiparametric or nonparametric estimators
are used to construct the forecasts. We allow general estimation procedures.
We only require that the estimation window size is bounded.
   We view mf and mg as either method-specific constants or as possibly
time-dependent random integers determined by the forecasting method. For
technical convenience, we require that m ≤ m̄, a finite constant (this can be
relaxed, but at the cost of an explosion of technicality). For example, data-
driven choices for mf and mg are given by the procedure suggested by Pesaran
and Timmermann (2006). The requirement that m̄ be finite rules out an ex-
panding window forecasting scheme. In principle, however, our framework can
also handle expanding estimation window procedures with observation weights
that suitably discount older observations, such as exponential smoothers, with
smoothing parameter bounded away from zero.
   We produce the forecasts using a rolling window estimation scheme. Let
T be the total sample size and let m1 be the maximum size of the first estima-
tion window.4 We formulate the first τ-step-ahead forecasts at time m1 using
data indexed 1,  . . . ,  m1 and compare these forecasts to the realization ym1 +τ .
At time m1 + 1, we formulate the second set of forecasts using the previous m2
observations (m2 can be different from m1 ) and compare them to the realiza-
tion ym1 +1+τ . Iterating this procedure yields n ≡ T − τ − m1 + 1 out-of-sample
forecasts and relative forecast errors.
   Note that the requirement that m̄ be finite is also compatible with a fixed es-
timation sample forecasting scheme, where the parameters are estimated only
once on the first m1 observations and used to produce all n out-of-sample fore-
casts (in which case β̂t, m = β̂m1 , m1 , m1 ≤ t ≤ T − 1).
   The preceding elements—the model, the estimation procedure, the size of
estimation window, and any applied observation weights—are part of each
forecasting method under evaluation.
   We evaluate the sequence of out-of-sample forecasts by a loss function
Lt+τ (Yt+τ ,  fˆt, mf ) that is either an economically meaningful criterion, such as
utility or profits (e.g., Leitch and Tanner (1991), West, Edison, and Cho
(1993)), or a statistical measure of accuracy. Examples of loss functions for
point forecasts considered in the literature and covered by our theory are
squared error loss, absolute error loss, lin–lin loss, linex loss, direction-of-
change loss, and predictive log-likelihood. Loss functions for quantile, prob-

  4
    If mf and mg are time dependent, say mf = {mf t } and mg = {mgt }, then m1 = max(mf 1 ,  mg1 ),
m2 = max(mf 2 ,  mg2 ), etc., and we write m = max(m1 ,  m2 ,  . . . ).

## Page 09: TESTS OF PREDICTIVE ABILITY 1553

源页：第 9 页

TESTS OF PREDICTIVE ABILITY                         1553

ability, and density forecasts are discussed, e.g., in Diebold and Lopez (1996), Giacomini and Komunjer (2005), and Amisano and Giacomini (2006).

For a given loss function and $\sigma$-field $\mathcal{G}_t$, we write the null hypothesis of equal conditional predictive ability of forecasts $f$ and $g$ for the target date $t + \tau$ as:

$$H_0 : \mathbb{E}[L_{t+\tau}(Y_{t+\tau}, \hat{f}_{t, m_f}) - L_{t+\tau}(Y_{t+\tau}, \hat{g}_{t, m_g}) \mid \mathcal{G}_t] \equiv \mathbb{E}[\Delta L_{m, t+\tau} \mid \mathcal{G}_t] = 0 \quad \text{a.s. } t = 1, 2, \dots \tag{3}$$

In writing (3), we are adopting the convention that $\hat{f}_{t, m_f}$ and $\hat{g}_{t, m_g}$ are measurable-$\mathcal{F}_t$. Note that we do not require $\mathcal{G}_t = \mathcal{F}_t$, although this is a leading case of interest that we analyze in the next two sections. We separately address the case $\mathcal{G}_t = \{\emptyset, \Omega\}$ in a subsequent section.

### 3.2. One-Step Conditional Predictive Ability Test

When $\tau = 1$ and $\mathcal{G}_t = \mathcal{F}_t$, the null hypothesis (3) claims that $\{\Delta L_{m, t}, \mathcal{F}_t\}$ is a martingale difference sequence (MDS). In this case, the conditional moment restriction (3) is equivalent to stating that $\mathbb{E}[\tilde{h}_t \Delta L_{m, t+1}] = 0$ for all $\mathcal{F}_t$-measurable functions $\tilde{h}_t$. We restrict attention to a given subset of such functions, which we denote by the $q \times 1$ $\mathcal{F}_t$-measurable vector $h_t$ and follow Stinchcombe and White (1998) by referring to this as the test function. For a given choice of test function $h_t$, we construct a test that exploits the consequence of the MDS property that $H_{0, h} : \mathbb{E}[h_t \Delta L_{m, t+1}] = 0$.

Standard asymptotic normality arguments suggest using a Wald-type test statistic of the form:

$$T_{m, n}^h = n \left( n^{-1} \sum_{t=m}^{T-1} h_t \Delta L_{m, t+1} \right)' \hat{\Omega}_n^{-1} \left( n^{-1} \sum_{t=m}^{T-1} h_t \Delta L_{m, t+1} \right) = n \bar{Z}_{m, n}' \hat{\Omega}_n^{-1} \bar{Z}_{m, n} \tag{4}$$

where $\bar{Z}_{m, n} \equiv n^{-1} \sum_{t=m}^{T-1} Z_{m, t+1}$, $Z_{m, t+1} \equiv h_t \Delta L_{m, t+1}$, and $\hat{\Omega}_n \equiv n^{-1} \sum_{t=m}^{T-1} Z_{m, t+1} Z_{m, t+1}'$ is a $q \times q$ matrix that consistently estimates the variance of $Z_{m, t+1}$.

A level $\alpha$ test can be conducted by rejecting the null hypothesis of equal conditional predictive ability whenever $T_{m, n}^h > \chi_{q, 1-\alpha}^2$, where $\chi_{q, 1-\alpha}^2$ is the $(1 - \alpha)$ quantile of a $\chi_q^2$ distribution. The asymptotic justification for the test is provided in the following theorem, which characterizes the behavior of the test statistic (4) under the null hypothesis.

**THEOREM 1 (One-Step Conditional Predictive Ability Test)**: For forecast horizon $\tau = 1$, (maximum) estimation window size $m \le \bar{m} < \infty$, and $q \times 1$ test function sequence $\{h_t\}$, suppose:
(i) $\{W_t\}$ and $\{h_t\}$ are mixing with $\phi$ of size $-r/(2r - 1)$, $r \ge 1$, or $\alpha$ of size $-r/(r - 1)$, $r > 1$;
(ii) $\mathbb{E}|Z_{m, t+1, i}|^{2(r+\delta)} < \infty$ for some $\delta > 0$, $i = 1, \dots, q$ and for all $t$;
(iii) $\Omega_n \equiv n^{-1} \sum_{t=m}^{T-1} \mathbb{E}[Z_{m, t+1} Z_{m, t+1}']$ is uniformly positive definite.

Then, under $H_0$ in (3), $T_{m, n}^h \xrightarrow{d} \chi_q^2$ as $n \to \infty$.

## Page 10: 1554 R. GIACOMINI AND H. WHITE

源页：第 10 页

1554                      R. GIACOMINI AND H. WHITE

**COMMENT 1**: Assumption (i) is mild, allowing the data to be characterized by considerable heterogeneity as well as dependence. In particular, we allow the data to be characterized by arbitrary structural changes at unknown dates.

**COMMENT 2**: The asymptotic distribution is obtained for the number of out-of-sample observations $n$ going to infinity, whereas the maximum estimation sample size $m$ is finite. This leads to asymptotically nonvanishing estimation uncertainty. In contrast, in the framework of West (1996), both the in-sample and the out-of-sample sizes grow, causing estimation uncertainty to vanish asymptotically.

**COMMENT 3**: Expanding window forecasting schemes are ruled out by assumption.

**COMMENT 4**: Assumption (iii), which imposes positive definiteness of the asymptotic variance of the test statistic, is related to a similar requirement made in the existing predictive ability testing literature, but it differs in a fundamental way. Here, the nonvanishing estimation uncertainty prevents singularity and makes our tests applicable to both nested and nonnested models.

**COMMENT 5**: In the construction of the test statistic, we exploit the simplifying feature that the null hypothesis imposes the time dependence structure of a MDS, which implies that the asymptotic variance can be consistently estimated by the sample variance.

## Page 11: TESTS OF PREDICTIVE ABILITY 1555

源页：第 11 页

TESTS OF PREDICTIVE ABILITY                           1555

**COMMENT 6**: As pointed out by a referee, the same theory outlined in Theorem 1 can be applied to testing for conditional bias, efficiency, and encompassing, provided the assumptions of the theorem are satisfied. One simply replaces $\Delta L_{m, t+1}$ with a suitable function of $Y_{t+1}$ and the forecasts.

**COMMENT 7**: It is easy to show that the test statistic $T_{m, n}^h$ can be alternatively computed as $n R^2$, where $R^2$ is the uncentered squared multiple correlation coefficient for the artificial regression of the constant unity on $(h_t \Delta L_{m, t+1})'$.

#### 3.2.1. Alternative hypothesis

We now analyze the behavior of the test statistic $T_{m, n}^h$ under a form of global alternative to $H_0$. Because we do not require identical distributions, our test is consistent against:

$$H_{A, h} : \mathbb{E}[\bar{Z}_{m, n}]' \mathbb{E}[\bar{Z}_{m, n}] \ge \delta > 0 \quad \text{for all } n \text{ sufficiently large} \tag{5}$$

**THEOREM 2**: Given assumptions (i), (ii), and (iii) of Theorem 1, under $H_{A, h}$ in (5) and for any constant $c \in \mathbb{R}$,

$$P[T_{m, n}^h > c] \to 1 \quad \text{as } n \to \infty$$

## Page 12: 1556 R. GIACOMINI AND H. WHITE

源页：第 12 页

1556                       R. GIACOMINI AND H. WHITE

### 3.3. Multistep Conditional Predictive Ability Test

For a forecast horizon $\tau > 1$ and with $\mathcal{G}_t = \mathcal{F}_t$, the null hypothesis (3) implies that for all $\mathcal{F}_t$-measurable test functions $h_t$, the sequence $\{h_t \Delta L_{m, t+\tau}\}$ is 'finitely correlated', so that $\text{cov}(h_t \Delta L_{m, t+\tau}, h_{t-j} \Delta L_{t+\tau-j}) = 0$ for all $j \ge \tau$.

Using reasoning that mirrors the development of the test for the one-step horizon, we consider the test statistic:

$$T_{m, n, \tau}^h = n \bar{Z}_{m, n}' \tilde{\Omega}_n^{-1} \bar{Z}_{m, n} \tag{6}$$

where $h_t$ is a $q \times 1$ $\mathcal{F}_t$-measurable test function, $\bar{Z}_{m, n} \equiv n^{-1} \sum_{t=m}^{T-\tau} Z_{m, t+\tau}$, $Z_{m, t+\tau} \equiv h_t \Delta L_{m, t+\tau}$, and

$$\tilde{\Omega}_n \equiv n^{-1} \sum_{t=m}^{T-\tau} Z_{m, t+\tau} Z_{m, t+\tau}' + n^{-1} \sum_{j=1}^{\tau-1} w_{n, j} \sum_{t=m+j}^{T-\tau} [Z_{m, t+\tau} Z_{m, t+\tau-j}' + Z_{m, t+\tau-j} Z_{m, t+\tau}']$$

where $w_{n, j}$ is a weight function such that $w_{n, j} \to 1$ as $n \to \infty$ for each $j = 1, \dots, \tau - 1$ (e.g., Newey and West (1987) and Andrews (1991)).

A level $\alpha$ test rejects the null hypothesis of equal conditional predictive ability whenever $T_{m, n, \tau}^h > \chi_{q, 1-\alpha}^2$.

**THEOREM 3 (Multistep Conditional Predictive Ability Test)**: For given forecast horizon $\tau > 1$, (maximum) estimation window size $m \le \bar{m} < \infty$, and a $q \times 1$ test function sequence $\{h_t\}$, suppose:
(i) $\{W_t\}$ and $\{h_t\}$ are mixing with $\phi$ of size $-r/(2r - 2)$, $r \ge 2$, or $\alpha$ of size $-r/(r - 2)$, $r > 2$;
(ii) $\mathbb{E}|Z_{m, t+\tau, i}|^{r+\delta} < \infty$ for some $\delta > 0$, $i = 1, \dots, q$ and for all $t$;
(iii) $\Omega_n$ is uniformly positive definite.

Then:
(a) under $H_0$ in (3), $T_{m, n, \tau}^h \xrightarrow{d} \chi_q^2$ as $n \to \infty$, and
(b) under $H_{A, h}$ in (5), for any constant $c \in \mathbb{R}$, $P[T_{m, n, \tau}^h > c] \to 1$ as $n \to \infty$.

## Page 13: TESTS OF PREDICTIVE ABILITY 1557

源页：第 13 页

TESTS OF PREDICTIVE ABILITY                             1557

### 3.4. Multistep Unconditional Predictive Ability Test

When $\mathcal{G}_t$ is the trivial $\sigma$-field $\mathcal{G}_t = \{\emptyset, \Omega\}$ and for forecast horizon $\tau \ge 1$, the null hypothesis (3) can be viewed as a test of equal unconditional predictive ability of forecasting methods $f$ and $g$, $H_0 : \mathbb{E}[\Delta L_{m, t+\tau}] = 0$, $t = 1, 2, \dots$, against the alternative:

$$H_A : |\mathbb{E}[\Delta \bar{L}_{m, n}]| \ge \delta > 0 \quad \text{for all } n \text{ sufficiently large} \tag{7}$$

where $\Delta \bar{L}_{m, n} \equiv n^{-1} \sum_{t=m}^{T-\tau} \Delta L_{m, t+\tau}$. The test is based on the statistic:

$$t_{m, n, \tau} = \frac{\Delta \bar{L}_{m, n}}{\hat{\sigma}_n / \sqrt{n}} \tag{8}$$

where $\hat{\sigma}_n^2$ is a suitable HAC estimator of the asymptotic variance $\sigma_n^2 = \text{var}[\sqrt{n} \Delta \bar{L}_{m, n}]$, for example:

$$\hat{\sigma}_n^2 \equiv n^{-1} \sum_{t=m}^{T-\tau} \Delta L_{m, t+\tau}^2 + 2 n^{-1} \sum_{j=1}^{p_n} w_{n, j} \sum_{t=m+j}^{T-\tau} \Delta L_{m, t+\tau} \Delta L_{m, t+\tau-j}$$

A level $\alpha$ test rejects the null hypothesis whenever $|t_{m, n, \tau}| > z_{\alpha/2}$. The test statistic $t_{m, n, \tau}$ coincides with that proposed by Diebold and Mariano (1995).

**THEOREM 4 (Unconditional Predictive Ability Test)**: For given forecast horizon $\tau \ge 1$ and (maximum) estimation window size $m \le \bar{m} < \infty$, suppose:
(i) $\{W_t\}$ is mixing with $\phi$ of size $-r/(2r - 2)$, $r \ge 2$, or $\alpha$ of size $-r/(r - 2)$, $r > 2$;
(ii) $\mathbb{E}|\Delta L_{m, t+\tau}|^{2r} < \infty$ for all $t$;
(iii) $\sigma_n^2 \equiv \text{var}[\sqrt{n} \Delta \bar{L}_{m, n}] > 0$ for all $n$ sufficiently large.

Then:
(a) under $H_0$ in (3), $t_{m, n, \tau} \xrightarrow{d} N(0, 1)$ as $n \to \infty$, and
(b) under $H_A$ in (7), for any constant $c \in \mathbb{R}$, $P[|t_{m, n, \tau}| > c] \to 1$ as $n \to \infty$.

## Page 14: 1558 R. GIACOMINI AND H. WHITE

源页：第 14 页

1558                          R. GIACOMINI AND H. WHITE

Mariano (1995) test (see, e.g., Clark (1999)).5 Our simulations in Section 5
provide additional evidence on this point.


                  4. A DECISION RULE FOR FORECAST SELECTION
  In this section, we consider the implications of rejecting equal conditional
predictive ability and describe a method for adaptively selecting at time T a
forecasting method for T + τ. The basic idea is that rejection occurs because
the test functions {ht } can predict the loss differences {'Lm, t+τ } out of sample,
which suggests using hT to predict which method will yield lower loss at T + τ.
We propose the following two-step procedure:

  STEP 1: Regress 'Lm, t+τ = Lt+τ (Yt+τ ,  fˆt, mf ) − Lt+τ (Yt+τ ,  ĝt, mg ) on ht over the
out-of-sample period t = m,  . . . ,  T − τ and let δ̂n denote the regression coeffi-
cient. Apply one of the tests from Section 3 and, in case of rejection, proceed
to Step 2.

  STEP 2: The approximation δ̂'n hT ≈ E['Lm, t+τ |FT ] motivates the decision
rule: use g if δ̂'n hT > c and use f if δ̂'n hT < c, with c a user-specified threshold
(e.g., c = 0).

   This procedure is a simple example of how our tests can be used in forecast
selection. More sophisticated approaches immediately suggest themselves, but
the subject of forecast selection is a significant topic that deserves extensive
attention beyond that possible in the space available here.
   In general, the plot of out-of-sample period predicted loss differences
   '       −τ
{δ̂n ht }Tt=m is useful for assessing the relative performance of f and g at differ-
ent times. One can further summarize relative out-of-sample performance by
computing the proportion of times the foregoing decision rule chooses g, i.e.,
              -T −τ
In, c = n−1 t=m 1{δ̂'n ht > c}, where 1{A} equals 1 if A is true and 0 otherwise.
We report these proportions for our empirical application in Section 6.


                              5. MONTE CARLO EVIDENCE
   We investigate the size and power properties of the tests of conditional and
unconditional predictive ability in finite samples of the sizes typically available
in macroeconomic forecasting applications.

  5
    Diebold and Mariano (1995) also acknowledge that τ-step-ahead errors may not be (τ − 1)
dependent, but find that the assumption of (τ − 1) dependence works well in practical applica-
tions and suggest using it as a benchmark. In the remainder of the paper, we adopt this approach.

## Page 15: TESTS OF PREDICTIVE ABILITY 1559

源页：第 15 页

TESTS OF PREDICTIVE ABILITY                                          1559

### 5.1. Size Properties

The goal of our first Monte Carlo experiment is twofold: first, to consider a situation where our null hypothesis of equal forecasting method accuracy is satisfied when comparing nested models and, second, to contrast our test with tests for equal forecasting model accuracy previously available (McCracken (1999) and Clark and McCracken (2001)).

Let the data-generating process be:

$$Y_t = c + \text{CPI}_t + \varepsilon_t, \quad \varepsilon_t \sim \text{i.i.d. } N(0, \sigma^2) \tag{9}$$

where $\text{CPI}_t$ is the second log difference of the monthly U.S. consumer price index over the period 1959:1–1998:12. The two competing forecasting models are $M_1 : Y_t = \beta \text{CPI}_t + u_{1t}$ and $M_2 : Y_t = \delta + \gamma \text{CPI}_t + u_{2t}$. Note that $M_1$ is misspecified in that it omits the intercept. The one-step-ahead forecasts of $Y_{t+1}$ implied by the two models are, respectively:

$$\hat{f}_{t, m}^{(1)} = \hat{\beta}_{t, m} \text{CPI}_{t+1}, \quad \hat{f}_{t, m}^{(2)} = \hat{\delta}_{t, m} + \hat{\gamma}_{t, m} \text{CPI}_{t+1} \tag{10}$$

estimated by ordinary least squares (OLS) over a sample of size $m$. For each $m$ and $n$ pair in the range $(25, 75, 125, 150)$, we find values of $c$ in (9) such that the two forecasting methods have equal expected MSE, using the following result:

**PROPOSITION 5**: Let $X_t \equiv \text{CPI}_t$, $\bar{X} \equiv \frac{1}{m} \sum_{j=t-m+1}^t X_j$, $S_{xx} \equiv \sum_{j=t-m+1}^t X_j^2 - m \bar{X}^2$. If:

$$c = \sigma \left[ \frac{\sum_{t=m}^{T-1} \left( \frac{\sum_{j=t-m+1}^t X_j^2}{m S_{xx}} + \frac{X_{t+1}^2}{S_{xx}} - 2 \frac{\bar{X}}{S_{xx}} X_{t+1} - \frac{X_{t+1}^2}{\sum_{j=t-m+1}^t X_j^2} \right)}{\sum_{t=m}^{T-1} \left( 1 - \frac{\sum_{j=t-m+1}^t X_j}{\sum_{j=t-m+1}^t X_j^2} X_{t+1} \right)^2} \right]^{1/2} \tag{11}$$

then $\mathbb{E}[\frac{1}{n} \sum_{t=m}^{T-1} L(Y_{t+1}, \hat{f}_{t, m}^{(1)})] = \mathbb{E}[\frac{1}{n} \sum_{t=m}^{T-1} L(Y_{t+1}, \hat{f}_{t, m}^{(2)})]$ for quadratic loss $L(Y_{t+1}, f) = (Y_{t+1} - f)^2$.

## Page 16: 1560 R. GIACOMINI AND H. WHITE

源页：第 16 页

1560                                R. GIACOMINI AND H. WHITE

To examine the robustness of the size properties of our test to the choice of loss function and to illustrate the flexibility of our method, we further consider a linex loss function $L(Y_{t+1}, f) = e^{Y_{t+1} - f} - (Y_{t+1} - f) - 1$.

**PROPOSITION 6**: Using the notation of Proposition 5, if $c$ solves $F(c) = 0$, where:

$$F(c) \equiv \sum_{t=m}^{T-1} \left[ \exp\left( c \left( 1 - \frac{\sum_j X_j}{\sum_j X_j^2} X_{t+1} \right) + \frac{\sigma^2}{2} \left( 1 + \frac{X_{t+1}^2}{\sum_j X_j^2} \right) \right) - c \left( 1 - \frac{\sum_j X_j}{\sum_j X_j^2} X_{t+1} \right) - \exp\left( \frac{\sigma^2}{2} \left( 1 + \frac{\sum_j X_j^2}{m S_{xx}} + \frac{X_{t+1}^2}{S_{xx}} - 2 \frac{\bar{X}}{S_{xx}} X_{t+1} \right) \right) \right] \tag{12}$$

then $\mathbb{E}[\frac{1}{n} \sum_{t=m}^{T-1} L(Y_{t+1}, \hat{f}_{t, m}^{(1)})] = \mathbb{E}[\frac{1}{n} \sum_{t=m}^{T-1} L(Y_{t+1}, \hat{f}_{t, m}^{(2)})]$ for linex loss.

We find values of $c$ that solve the equation in Proposition 6 by numerical techniques.

## Page 17: TESTS OF PREDICTIVE ABILITY 1561

源页：第 17 页

TESTS OF PREDICTIVE ABILITY                                             1561
                                                        ### TABLE I: REJECTION FREQUENCIES OF UNCONDITIONAL PREDICTIVE ABILITY AND MCCRACKEN'S (1999) TESTS

| Estimation Window ($m$) | Uncond. (Quadratic) $n=25$ | $n=75$ | $n=125$ | $n=150$ | McCracken (Quadratic) $n=25$ | $n=75$ | $n=125$ | $n=150$ | Uncond. (Linex) $n=25$ | $n=75$ | $n=125$ | $n=150$ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **25** | 0.053 | 0.037 | 0.035 | 0.024 | 0.087 | 0.360 | 0.481 | 0.525 | 0.060 | 0.055 | 0.046 | 0.046 |
| **75** | 0.062 | 0.048 | 0.040 | 0.037 | 0.147 | 0.070 | 0.256 | 0.279 | 0.069 | 0.065 | 0.064 | 0.058 |
| **125** | 0.073 | 0.054 | 0.044 | 0.042 | 0.120 | 0.146 | 0.063 | 0.199 | 0.072 | 0.070 | 0.075 | 0.077 |
| **150** | 0.061 | 0.056 | 0.048 | 0.046 | 0.091 | 0.134 | 0.204 | 0.058 | 0.075 | 0.075 | 0.077 | 0.073 |

> *Notes: Rejection frequencies of the test of Theorem 6 and of McCracken's (1999) test in the Monte Carlo experiment described in Section 5.1, for nominal size 0.05: $m$ is the estimation window size and $n$ is the out-of-sample size.*

The table reveals that our test is generally well sized, particularly when the
estimation window m is small relative to the out-of-sample size n (for given m,
the size tends to improve as n increases). This is true for both quadratic and
linex loss functions, although for the linex loss the test is slightly oversized.
Before discussing the rejection frequencies of the CM test, we emphasize that
these do not represent the empirical size of the CM test, because this tests a dif-
ferent null hypothesis: for CM the losses are functions of population values of
the parameters rather than parameter estimates, so the CM test is focused on
the forecasting model rather than the forecasting method. Table I shows that
in our scenario the CM test rejects the hypothesis that the forecasting mod-
els are equally accurate in favor of the larger model7 more often than our test
rejects its null hypothesis. In other words, by rejecting its null hypothesis rel-
atively more frequently, the CM test signals that the larger forecasting model
is superior in cases where the forecasting method based on the larger model
is not superior. The disparity of conclusions between the two tests is greater
when m is small relative to n (our test rejects 5% of the time, whereas the CM
test rejects up to 50% of the time). Interestingly, the two tests have comparable
rejection frequencies when m is equal to n.


                                               5.2. Power Properties
  We next investigate the power of our unconditional and conditional tests in
two directions: (i) against serially correlated loss differences; and (ii) against
different performance in different states of the economy. Again, solely for sim-
plicity and brevity, we take m = mf = mg .

    7
        The alternative hypothesis for the CM test is that the larger model is more accurate.

## Page 18: 1562 R. GIACOMINI AND H. WHITE

源页：第 18 页

1562                         R. GIACOMINI AND H. WHITE

5.2.1. Power against serial correlation in relative performance
 Here we consider the alternative that the loss differences 'Lm, t+1 follow an
AR(1) process:
(13)       'Lm, t+1 = µ(1 − ρ) + ρ'Lm, t + εt+1 ,            εt+1 ∼ i.i.d. N(0,  1).
For each of 5,000 Monte Carlo replications, we use (13) to generate a sequence
of loss differences of length n = 150 starting from an initial value 'Lm, m that
equals the difference in squared errors for forecasts of CPI1998:12 implied by
(i) a white noise and (ii) an AR(1) model for CPI estimated over a window of
size m = 150 using data up to 1998:11. We consider two scenarios: (I) the loss
differences are not serially correlated (ρ = 0) but have nonzero unconditional
mean; (II) the loss differences have zero unconditional mean (µ = 0) but are
serially correlated (and thus the unconditional null hypothesis is still satisfied).
The corresponding parameterizations are (i) ρ = 0, µ = (0,  0.05,  . . . ,  1) and
(ii) µ = 0, ρ = (0,  0.05,  . . . ,  0.9).
   Figure 1 shows the power curves of the tests of Theorems 1 (conditional)
and 6 (unconditional) in scenarios (I) and (II) computed as the proportion of
rejections of the null hypotheses H0, cond and H0, unc at the 5% nominal level.
In all cases, we let ht = (1,  'Lm, t )' for the conditional test and pn = 0 for the
unconditional test.
   The left panel of Figure 1 reveals that using the conditional rather than the
unconditional test, even though there is no serial correlation in the loss differ-
ences, involves only a small loss of power. From the right panel of Figure 1,
on the other hand, we see that the conditional test has appealing power prop-
erties but that the unconditional test suffers severe size distortions as the loss




  FIGURE 1.—Power curves for the conditional test of Theorem 1 and the unconditional test of
Theorem 6. The DGP in the left panel is such that E['Lm, t+1 |Ft ] = µ and the DGP in the right
panel is such that E['Lm, t+1 ] = 0, but E['Lm, t+1 |Ft ] = ('Lm, t ).

## Page 19: TESTS OF PREDICTIVE ABILITY 1563

源页：第 19 页

TESTS OF PREDICTIVE ABILITY                                 1563

differences become more serially correlated (the power curve is upward slop-
ing, whereas it should be flat because H0, unc is satisfied), a possible consequence
of not using a more involved method for choosing pn .

5.2.2. Power against different performance in different states
  We next consider a situation where the two forecasts have equal predictive
ability unconditionally, but each forecast is more accurate in a given state of the
economy. For each of 5,000 Monte Carlo replications, we generate a sequence
of loss differences of length n = 150 as
                           µ
           'Lm, t+1 =             (St − p) + εt+1 ,        εt+1 ∼ i.i.d. N(0,  1), 
                        p(1 − p)
where St = 1 with probability p and St = 0 with probability 1 − p. We thus have
E['Lm, t+1 ] = 0, but
                           
                             µ/p,           if St = 1
         E['Lm, t+1 |St ] =
                             −µ/(1 − p),  if St = 0,
so that the second forecast is more accurate in the first state and the first
forecast is more accurate in the second state. Figure 2 shows the rejection
frequencies of the null hypotheses H0, cond and H0, unc at the 5% nominal level us-
ing the tests of Theorems 1 and 6. The power curves are obtained for p = 0.5
and d ≡ p(1−p)
            µ
                 = (0,  0.1,  . . . ,  1) (d represents the difference in expected loss
between the two states). We let ht = (1,  St )' for the conditional test and let
pn = 0 for the unconditional test.
   As expected, the conditional test has power to detect different performance
in the different states, whereas the rejection frequencies for the unconditional




   FIGURE 2.—Power curves for the conditional test of Theorem 1 and the unconditional test of
Theorem 6. The DGP is such that E['Lm, t+1 ] = 0, but E['Lm, t+1 |Ft ] = d(St − p), where St = 1
with probability p and is 0 otherwise.

## Page 20: 1564 R. GIACOMINI AND H. WHITE

源页：第 20 页

1564                         R. GIACOMINI AND H. WHITE

test remain constant at the empirical size. Unlike the previous case, the uncon-
ditional test does not suffer size distortion.

       6. APPLICATION: COMPARING PARAMETER-REDUCTION METHODS
   A problem that often arises in macroeconomic forecasting is how to select
a manageable subset of predictors from a large number of potentially use-
ful variables. In this situation, one key determinant of the resulting forecast
performance is the trade-off between the information content of each series
and the estimation uncertainty that is introduced. The goal of our application
is to analyze and compare the forecast performance, both conditionally and
unconditionally, of three leading methods for parameter reduction: a sequen-
tial model-selection approach based on a simplified general-to-specific mod-
eling strategy (Hoover and Perez (1999)), the “diffusion indexes” approach
of Stock and Watson (2002), and the use of Bayesian shrinkage estimation
(Litterman (1986)). We also compare each method to autoregressive and ran-
dom walk benchmark forecasts. The DMW testing framework cannot be used
here because some of the comparisons are between nested models and, fur-
thermore, that framework does not easily accommodate Bayesian estimation
or the presence of estimated regressors. In contrast, our approach is well suited
for comparing methods based on nested models or on different modeling and
estimation techniques.
   We consider the “balanced panel” subset of the data set of Stock and Watson
(2002) (henceforth SW), including 146 monthly economic time series mea-
sured over the period 1959:1–1998:12, and apply the same transformations
as those documented in Appendix B of SW. We use the different parameter-
reduction methods to construct multistep forecasts for four8 U.S. macroeco-
nomic variables: two real variables (industrial production and real personal
income less transfers) and two price indexes (consumer price index and pro-
ducer price index).

                        6.1. Parameter-Reduction Methods
                                                                        τ
  All forecasting models project the τ-step-ahead variable Yt+τ            onto time-t
predictors Xt and lags of the variable of interest Yt , Yt−1 ,  . . . . We consider the
following forecasting methods.
  The sequential model selection method (denoted Seq.) considers the model

(14)        τ
          Yt+τ = α + β' Xt + γ1 Yt + · · · + γ6 Yt−5 + εt+τ , 

where Xt contains the 145 predictors, and applies a simplified version of the
algorithm described by Hoover and Perez (1999, p. 175), which reduces the

  8
    Results for additional   series   are   available   at   http://www.econ.ucla.edu/giacomin/
CPAappendix.pdf.

## Page 21: TESTS OF PREDICTIVE ABILITY 1565

源页：第 21 页

TESTS OF PREDICTIVE ABILITY                                    1565

number of regressors by performing a sequence of stability tests, residual au-
tocorrelation tests, and t- and F -tests of significance.9 The significance level
for all tests is α = 0.01. A complete algorithm description is available upon
request.
    The diffusion indexes method (denoted DI) first uses principal component
analysis to estimate k factors F̂t from the predictors Xt (1 ≤ k ≤ 12) and then
considers the model Yt+τ      τ
                                 = α + β' F̂t + γ1 Yt + · · · + γp Yt−p+1 + εt+τ,  where both
k and p are selected by BIC.
    The Bayesian shrinkage method (denoted Bay) considers the full model (14)
and applies Bayesian estimation of its coefficients using the Litterman (1986)
prior. For variables in differences, the variance V for the prior distribution
of θ ≡ (α,  β' ,  γ ' )' is diagonal, with α ∼ N(0,  108 ), βi ∼ N(0,  (w · λ · σ̂y /σ̂xi )2 ),
i = 1,  . . . ,  145, and γj ∼ N(0,  (λ/j))2 ), j = 1,  . . . ,  6. As in Litterman (1986),
we set w = 0.2 and λ = 0.2, but the results were robust to a number of
different choices for w and λ. The Bayesian estimate of θ is θB = (X ' X +
σ̂ 2 V −1 )−1 (X ' Y τ ), where X is m × 152 (m is the size of the estimation sample)
with rows (1,  Xt' ,  Yt ,  Yt−1 ,  . . . ,  Yt−5 ), Y τ is m × 1 with elements Yt+τ  τ
                                                                                   , and σ̂ is
the estimated standard error of the residuals in a univariate autoregression
        τ
for Yt+τ   .
    The benchmark methods are an autoregressive (denoted AR) model Yt+τ                 τ
                                                                                            =
α + γ1 Yt + · · · + γp Yt−p+1 + εt+τ , where p is selected by BIC with 0 ≤ p ≤ 6,
and a random walk (denoted RW) in levels, corresponding to the forecasting
model in differences Yt+τ      τ
                                 = α + εt+τ .

                         6.2. Real-Time Forecasting Experiment
  We use the preceding five methods to produce sequences of τ-step-ahead
forecasts for τ = 1,  6,  12 using a rolling window estimation procedure with m =
mf = mg = 150 + τ. The first estimation sample is from 1960:1–1972:6 + τ
(the first 12 data were used as initial observations), the total sample has size
T = 468, and the out-of-sample size is n = 318 − τ.
  At the outset, we described how limited memory estimators can have ad-
vantages relative to expanding memory procedures, especially in the presence
of inadequately modeled heterogeneity, inadequately modeled dynamics, or
incorrect functional form. To gain quantitative insight, one can compare the
estimated loss from using a limited memory estimator (e.g., a rolling window
estimator) to that of an expanding data window procedure. We do not provide
a formal test based on this comparison here. Instead, however, we examine
the relative performance of these different approaches by comparing the per-
formance of forecasts of industrial production and consumer price index for

   9
     We overcome multicollinearity in Xt by replacing the groups of variables whose correlation is
greater than 0.98 with their average. The new Xt contains 130 regressors.

## Page 22: 1566 R. GIACOMINI AND H. WHITE

源页：第 22 页

1566                                 R. GIACOMINI AND H. WHITE

                                                      ### TABLE II: RELATIVE MSE OF ROLLING AND EXPANDING WINDOW FORECASTS

| Horizon ($\tau$) | IP: Seq. | IP: DI | IP: Bay | IP: AR | IP: RW | CPI: Seq. | CPI: DI | CPI: Bay | CPI: AR | CPI: RW |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 month | 3.38 | 0.79 | 0.75 | 1.02 | 0.84 | 0.15 | 1.02 | 0.96 | 1.04 | 1.00 |
| 6 months | 0.02 | 0.85 | 0.53 | 1.01 | 0.41 | 0.02 | 1.04 | 0.15 | 1.03 | 1.00 |
| 12 months | 0.03 | 0.66 | 0.12 | 1.07 | 0.26 | 0.01 | 1.00 | 0.11 | 1.04 | 1.01 |

> *Notes: Ratios of MSEs of $\tau$-steps-ahead forecasts for the methods in the column estimated over either a rolling window of size $m = 150$ or an expanding window with the same initial size. IP = Industrial Production, CPI = Consumer Price Index.*

all models, and comparing forecast horizons based on rolling window methods
to forecasts based on an expanding window of data from 1960:1 onward. Ta-
ble II reports the relative MSEs of the rolling window and expanding window
forecasts.
   The table shows that MSEs for rolling window forecasts are often much
smaller than those for expanding window forecasts (ratios are as small as 0.01).
In the remaining cases, the MSEs for the two procedures are virtually identical
(with one exception, ratios are no greater than 1.07).10 We see that the rolling
window procedure can result in substantial forecast accuracy gains relative to
an expanding window for important economic time series.

                               6.3. Results of Predictive Ability Tests
  For each forecast series we conduct pairwise tests of equal conditional pre-
dictive ability of the five forecasting methods using a squared error loss (results
for absolute error loss are available on request). For τ = 1,  6, and 12, we test
H0 : E[(Yt+τ − fˆt, mf )2 − (Yt+τ − ĝt, mg )2 |Gt ] ≡ E['Lt+τ |Gt ] = 0 for Gt = Ft (con-
ditional test) and Gt = {∅,  Ω} (unconditional test).
  For the case Gt = Ft , we use the test function ht = (1,  'Lt )' . Table III shows
the results of conditional predictive ability tests for real variables and price in-
dexes. Table IV shows the results for the unconditional case. The entries in the
tables are the p-values of pairwise tests of equal conditional and unconditional
predictive ability, using the tests of Theorems 5 and 6. In Table III, the num-
bers within parentheses below each entry are the indicators In, c discussed in
Section 4, for c = 0. A plus (minus) sign indicates rejection of the null hypoth-
esis at the 10% level and signals that the method in the column would have
been chosen more (less) often than the method in the row, as suggested by an
entry In, c greater (less) than 0.5. In Table IV, the numbers within parentheses
are the ratios of MSEs for the method in the column relative to the method in

  10
     Note that these results are for a fixed choice of estimation window. Optimizing the estimation
window size could produce even greater improvements.

## Page 23: TABLE III: CONDITIONAL PREDICTIVE ABILITY TESTS

源页：第 23 页

### TABLE III: CONDITIONAL PREDICTIVE ABILITY TESTS

*Pairwise tests of equal conditional predictive ability for forecast methods. Entries are p-values of Theorem 3; numbers in parentheses are the proportion of times the column method outperforms the row method over the out-of-sample period. A plus (minus) indicates rejection at 10% level where column outperforms (is outperformed by) row >50% of the time. Rows labeled 'Bound' report Hochberg-Bonferroni (HB) multiple hypothesis bounds. Square brackets [ ] report joint panel HB bounds.*

#### Panel A: Horizon = 1 Month

**1. Industrial Production (Joint HB Bound = [0.010])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.043 | 0.080 | 0.004 | 0.004 | 0.016 |
| **DI** | 0.026- (0.00) | - | - | - | - |
| **Bay** | 0.020- (0.00) | 0.080- (0.02) | - | - | - |
| **AR** | 0.034- (0.00) | 0.040+ (0.91) | 0.001+ (0.93) | - | - |
| **RW** | 0.043- (0.00) | 0.049+ (0.81) | 0.004+ (0.84) | 0.163 (0.78) | - |

**2. Personal Income (Joint HB Bound = [0.020])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.016 | 0.008 | 0.012 | 0.054 | 0.008 |
| **DI** | 0.004- (0.02) | - | - | - | - |
| **Bay** | 0.006- (0.02) | 0.731 (0.90) | - | - | - |
| **AR** | 0.027- (0.03) | 0.018+ (0.97) | 0.199 (0.93) | - | - |
| **RW** | 0.108 (0.07) | 0.002+ (0.86) | 0.003+ (0.83) | 0.023+ (0.80) | - |

**3. Consumer Price Index (CPI) (Joint HB Bound = [1.00])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.193 | 0.496 | 0.584 | 0.496 | 0.452 |
| **DI** | 0.175 (0.00) | - | - | - | - |
| **Bay** | 0.146 (0.01) | 0.644 (0.99) | - | - | - |
| **AR** | 0.192 (0.00) | 0.124 (0.74) | 0.721 (0.18) | - | - |
| **RW** | 0.193 (0.00) | 0.385 (0.84) | 0.389 (0.78) | 0.452 (0.80) | - |

**4. Producer Price Index (PPI) (Joint HB Bound = [0.009])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.003 | 0.004 | 0.134 | 0.004 | 0.327 |
| **DI** | 0.001- (0.02) | - | - | - | - |
| **Bay** | 0.046- (0.01) | 0.067+ (0.99) | - | - | - |
| **AR** | 0.001- (0.02) | 0.161 (0.22) | 0.047- (0.01) | - | - |
| **RW** | 0.240 (0.01) | 0.109 (1.00) | 0.578 (0.76) | 0.098+ (0.98) | - |

---

#### Panel B: Horizon = 6 Months

**1. Industrial Production (Joint HB Bound = [0.030])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.012 | 0.040 | 0.012 | 0.228 | 0.152 |
| **DI** | 0.010- (0.05) | - | - | - | - |
| **Bay** | 0.003- (0.01) | 0.432 (0.00) | - | - | - |
| **AR** | 0.885 (0.01) | 0.167 (0.98) | 0.057+ (0.98) | - | - |
| **RW** | 0.654 (0.30) | 0.154 (0.98) | 0.038+ (0.99) | 0.193 (0.97) | - |

**2. Personal Income (Joint HB Bound = [0.140])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.035 | 0.072 | 0.037 | 0.080 | 0.096 |
| **DI** | 0.018- (0.00) | - | - | - | - |
| **Bay** | 0.014- (0.00) | 0.037- (0.00) | - | - | - |
| **AR** | 0.031- (0.00) | 0.098+ (0.93) | 0.020+ (1.00) | - | - |
| **RW** | 0.035- (0.00) | 0.124 (1.00) | 0.024+ (0.99) | 0.591 (0.90) | - |

**3. Consumer Price Index (CPI) (Joint HB Bound = [0.009])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.364 | 0.004 | 0.008 | 0.004 | 0.003 |
| **DI** | 0.091- (0.00) | - | - | - | - |
| **Bay** | 0.261 (0.00) | 0.002+ (0.99) | - | - | - |
| **AR** | 0.146 (0.00) | 0.082+ (0.82) | 0.055- (0.02) | - | - |
| **RW** | 0.935 (0.00) | 0.001+ (1.00) | 0.004+ (0.96) | 0.001+ (1.00) | - |

**4. Producer Price Index (PPI) (Joint HB Bound = [0.007])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.003 | 0.003 | 0.003 | 0.003 | 0.009 |
| **DI** | 0.001- (0.00) | - | - | - | - |
| **Bay** | 0.493 (0.51) | 0.001+ (0.99) | - | - | - |
| **AR** | 0.001- (0.00) | 0.809 (0.82) | 0.001- (0.01) | - | - |
| **RW** | 0.554 (0.95) | 0.003+ (1.00) | 0.404 (0.97) | 0.003+ (1.00) | - |

---

#### Panel C: Horizon = 12 Months

**1. Industrial Production (Joint HB Bound = [0.010])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.004 | 0.012 | 0.004 | 0.116 | 0.124 |
| **DI** | 0.003- (0.00) | - | - | - | - |
| **Bay** | 0.001- (0.00) | 0.201 (0.00) | - | - | - |
| **AR** | 0.029- (0.02) | 0.202 (0.96) | 0.088+ (0.99) | - | - |
| **RW** | 0.031- (0.05) | 0.174 (1.00) | 0.073+ (1.00) | 0.873 (0.01) | - |

**2. Personal Income (Joint HB Bound = [0.030])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.012 | 0.024 | 0.012 | 0.112 | 0.164 |
| **DI** | 0.006- (0.00) | - | - | - | - |
| **Bay** | 0.003- (0.00) | 0.044- (0.01) | - | - | - |
| **AR** | 0.028- (0.00) | 0.314 (0.94) | 0.095+ (1.00) | - | - |
| **RW** | 0.041- (0.00) | 0.227 (0.92) | 0.113 (0.99) | 0.096+ (0.85) | - |

**3. Consumer Price Index (CPI) (Joint HB Bound = [0.008])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.200 | 0.003 | 0.004 | 0.004 | 0.003 |
| **DI** | 0.050- (0.00) | - | - | - | - |
| **Bay** | 0.271 (0.00) | 0.001+ (0.98) | - | - | - |
| **AR** | 0.224 (0.00) | 0.059+ (0.98) | 0.634 (0.06) | - | - |
| **RW** | 0.557 (0.03) | 0.001+ (1.00) | 0.005+ (0.99) | 0.001+ (0.99) | - |

**4. Producer Price Index (PPI) (Joint HB Bound = [0.005])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.003 | 0.002 | 0.003 | 0.002 | 0.003 |
| **DI** | 0.001- (0.00) | - | - | - | - |
| **Bay** | 0.367 (0.00) | 0.001+ (1.00) | - | - | - |
| **AR** | 0.001- (0.00) | 0.152 (0.83) | 0.001- (0.01) | - | - |
| **RW** | 0.484 (0.08) | 0.001+ (1.00) | 0.187 (0.96) | 0.001+ (1.00) | - |


## Page 24: TABLE IV: UNCONDITIONAL PREDICTIVE ABILITY TESTS

源页：第 24 页

### TABLE IV: UNCONDITIONAL PREDICTIVE ABILITY TESTS

*Pairwise tests of equal unconditional predictive ability (Theorem 4 / Diebold-Mariano). Entries are p-values; numbers in parentheses are ratios of MSEs for the column method relative to the row method. A plus (minus) indicates rejection at 10% level where column has smaller (larger) MSE than row. Truncation lag is $\tau - 1$.*

#### Panel A: Horizon = 1 Month

**1. Industrial Production (Joint HB Bound = [0.020])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.065 | 0.072 | 0.008 | 0.008 | 0.116 |
| **DI** | 0.036- (3.82) | - | - | - | - |
| **Bay** | 0.029- (4.22) | 0.028- (1.10) | - | - | - |
| **AR** | 0.046- (3.37) | 0.027+ (0.88) | 0.002+ (0.80) | - | - |
| **RW** | 0.065- (2.97) | 0.083+ (0.78) | 0.029+ (0.70) | 0.227 (0.88) | - |

**2. Personal Income (Joint HB Bound = [0.100])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.160 | 0.040 | 0.174 | 0.040 | 0.156 |
| **DI** | 0.055- (1.83) | - | - | - | - |
| **Bay** | 0.054- (1.79) | 0.554 (0.98) | - | - | - |
| **AR** | 0.099 (1.64) | 0.010- (0.89) | 0.091+ (0.91) | - | - |
| **RW** | 0.160 (1.50) | 0.039+ (0.82) | 0.058+ (0.84) | 0.184 (0.92) | - |

**3. Consumer Price Index (CPI) (Joint HB Bound = [1.00])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.229 | 0.472 | 0.635 | 0.635 | 0.362 |
| **DI** | 0.181 (3.45) | - | - | - | - |
| **Bay** | 0.196 (3.19) | 0.472 (0.93) | - | - | - |
| **AR** | 0.186 (3.36) | 0.287 (0.97) | 0.635 (1.05) | - | - |
| **RW** | 0.229 (2.81) | 0.301 (0.81) | 0.261 (0.88) | 0.362 (0.84) | - |

**4. Producer Price Index (PPI) (Joint HB Bound = [0.036])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.012 | 0.016 | 0.063 | 0.016 | 0.120 |
| **DI** | 0.004- (1.71) | - | - | - | - |
| **Bay** | 0.054- (1.31) | 0.019+ (0.77) | - | - | - |
| **AR** | 0.004- (1.75) | 0.462 (1.03) | 0.021- (1.34) | - | - |
| **RW** | 0.030- (1.29) | 0.108 (0.75) | 0.823 (0.98) | 0.102 (0.73) | - |

---

#### Panel B: Horizon = 6 Months

**1. Industrial Production (Joint HB Bound = [0.010])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.004 | 0.044 | 0.004 | 0.232 | 0.240 |
| **DI** | 0.011- (1.67) | - | - | - | - |
| **Bay** | 0.001- (1.83) | 0.294 (1.10) | - | - | - |
| **AR** | 0.680 (1.11) | 0.175 (0.67) | 0.058+ (0.61) | - | - |
| **RW** | 0.921 (1.03) | 0.156 (0.62) | 0.060+ (0.56) | 0.145 (0.93) | - |

**2. Personal Income (Joint HB Bound = [0.100])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.039 | 0.040 | 0.040 | 0.100 | 0.156 |
| **DI** | 0.026- (6.23) | - | - | - | - |
| **Bay** | 0.022- (7.37) | 0.010- (1.18) | - | - | - |
| **AR** | 0.037- (4.78) | 0.149 (0.77) | 0.025+ (0.65) | - | - |
| **RW** | 0.039- (4.62) | 0.196 (0.74) | 0.057+ (0.63) | 0.655 (0.97) | - |

**3. Consumer Price Index (CPI) (Joint HB Bound = [0.007])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.392 | 0.003 | 0.003 | 0.004 | 0.002 |
| **DI** | 0.098- (2.67) | - | - | - | - |
| **Bay** | 0.306 (1.65) | 0.001+ (0.62) | - | - | - |
| **AR** | 0.145 (2.27) | 0.143 (0.85) | 0.001+ (0.43) | - | - |
| **RW** | 0.742 (1.15) | 0.003- (1.37) | 0.001+ (0.70) | 0.001+ (0.51) | - |

**4. Producer Price Index (PPI) (Joint HB Bound = [0.007])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.003 | 0.003 | 0.003 | 0.003 | 0.012 |
| **DI** | 0.001- (2.30) | - | - | - | - |
| **Bay** | 0.988 (1.00) | 0.001+ (0.43) | - | - | - |
| **AR** | 0.001- (2.24) | 0.801 (0.98) | 0.004+ (0.37) | - | - |
| **RW** | 0.476 (0.84) | 0.001- (2.25) | 0.188 (0.84) | 0.003+ (0.37) | - |

---

#### Panel C: Horizon = 12 Months

**1. Industrial Production (Joint HB Bound = [0.009])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.003 | 0.004 | 0.004 | 0.105 | 0.108 |
| **DI** | 0.001- (3.77) | - | - | - | - |
| **Bay** | 0.001- (4.03) | 0.442 (1.07) | - | - | - |
| **AR** | 0.035- (1.80) | 0.064+ (0.48) | 0.034+ (0.45) | - | - |
| **RW** | 0.036- (1.83) | 0.063+ (0.49) | 0.032+ (0.46) | 0.772 (1.02) | - |

**2. Personal Income (Joint HB Bound = [0.009])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.003 | 0.004 | 0.004 | 0.068 | 0.102 |
| **DI** | 0.001- (2.97) | - | - | - | - |
| **Bay** | 0.001- (3.42) | 0.009- (1.15) | - | - | - |
| **AR** | 0.017- (2.08) | 0.076+ (0.70) | 0.025+ (0.61) | - | - |
| **RW** | 0.034- (1.95) | 0.083+ (0.65) | 0.033+ (0.57) | 0.212 (0.93) | - |

**3. Consumer Price Index (CPI) (Joint HB Bound = [0.007])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.180 | 0.003 | 0.003 | 0.004 | 0.002 |
| **DI** | 0.045- (3.63) | - | - | - | - |
| **Bay** | 0.095- (2.48) | 0.001+ (0.68) | - | - | - |
| **AR** | 0.068- (2.79) | 0.110 (0.77) | 0.001+ (0.42) | - | - |
| **RW** | 0.344 (1.52) | 0.001+ (0.42) | 0.389 (1.12) | 0.001+ (0.61) | - |

**4. Producer Price Index (PPI) (Joint HB Bound = [0.007])**

| Benchmark | Seq. | DI | Bay | AR | RW |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Bound** | 0.003 | 0.003 | 0.003 | 0.003 | 0.012 |
| **DI** | 0.001- (2.76) | - | - | - | - |
| **Bay** | 0.339 (1.22) | 0.001+ (0.44) | - | - | - |
| **AR** | 0.001- (2.52) | 0.516 (0.91) | 0.004+ (0.32) | - | - |
| **RW** | 0.642 (0.88) | 0.001- (2.07) | 0.075+ (0.72) | 0.003+ (0.35) | - |


## Page 25: TESTS OF PREDICTIVE ABILITY 1569

源页：第 25 页

TESTS OF PREDICTIVE ABILITY                              1569

the row and a plus (minus) sign indicates that the method in the column out-
performs (underperforms) the method in the row at the 10% significance level,
as evidenced by a relative MSE less (greater) than 1. The rows labeled “Bound”
contain Hochberg’s (1988) modified Bonferroni p-value bounds for testing the
multiple hypothesis that all pairwise comparisons are zero for a given column
reference method.11 The square brackets contain Hochberg’s (1988) p-value
bound for the hypothesis that all pairwise comparisons are zero for that panel.
   A sharp result that emerges from the tables is that the sequential model-
selection method is characterized by the worst performance, likely due to its
tendency to select overparameterized models (cases with 40 or more predic-
tors in the final model were not uncommon). A second observation is that the
predictors seem less useful for forecasting price indexes than real variables. For
price indexes, the parameter-reduction methods do not generally outperform
the AR benchmark. For real variables, both Bayesian shrinkage and the dif-
fusion indexes methods mostly outperform the benchmarks. Bayesian shrink-
age, however, often outperforms the diffusion indexes, thus emerging as the
best forecasting method for real variables. Note that the use of Hochberg–
Bonferroni modified p-values does not, in general, change the conclusions that
emerge from the pairwise tests.
   Finally, we draw two conclusions from the comparison of the results for the
conditional and the unconditional tests. First, in some of the comparisons there
is evidence of superior conditional performance even though we cannot reject
equal unconditional performance (e.g., diffusion indexes versus AR forecasts
of CPI). This suggests that in those cases, even though the two methods per-
formed on average equally well, their relative performance could have been
predicted by lagged relative performance. A second conclusion is that even
though rejection of the unconditional hypothesis should imply rejection of the
conditional hypothesis, in some cases the unconditional tests reject equal per-
formance while the conditional tests fail to do so. This could be due either
to the unconditional test being oversized or to the conditional test having low
power. Our Monte Carlo simulations suggest that the more plausible expla-
nations are the mild size distortions of the unconditional test and the test’s
sensitivity to lag length selection for the HAC estimator.


                           6.4. Decision Rule Assessment
  To assess the effectiveness of the decision rule proposed in Section 4, we
evaluate the performance of the “hybrid” forecast obtained by recursively
applying the decision rule to select the best forecast for the next period.
We consider the sequence of quadratic out-of-sample losses for 1-, 6-, and

   11
      Hochberg’s (1988) method involves ordering the p-values from testing r hypotheses as
p(1) ,  . . . ,  p(r) and computing the bound as Bound = minj=1, ..., r (r − j + 1)p(j) .

## Page 26: 1570 R. GIACOMINI AND H. WHITE

源页：第 26 页

1570                                 R. GIACOMINI AND H. WHITE

                                                      ### TABLE V: DECISION RULE ASSESSMENT: PERFORMANCE OF THE "HYBRID" FORECAST OF INDUSTRIAL PRODUCTION

| Benchmark | Horizon = 1m: Seq. | DI | Bay | AR | Horizon = 6m: Seq. | DI | Bay | AR | Horizon = 12m: Seq. | DI | Bay | AR |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **DI** | 1 | — | — | — | 0 | — | — | — | 1 | — | — | — |
| **Bayes** | 1 | 1 | — | — | 1 | 1 | — | — | 1 | 1 | — | — |
| **AR** | 1 | 1 | 0 | — | 1 | 1 | 1 | — | 1 | 1 | 1 | — |
| **RW** | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

> *Notes: Entries equal 1 if the MSE of the hybrid forecast (see Section 6.4) is less than or equal to the MSEs of both the method in the row and the method in the column, and they equal 0 otherwise.*

12-months-ahead forecasts of industrial production obtained by the five fore-
casting methods, as described in Section 6.2. For each pair of forecasting meth-
ods and for each forecast horizon, we derive the hybrid forecast sequence by
applying the two-step decision rule (using ht = (1,  'Lt )' ) on a rolling window
of size 200, except that we proceed to Step 2 regardless of the test outcome.
We evaluate the performance of the hybrid forecast and contrast it to that of
the forecasts in the pair by (i) comparing the MSE of the hybrid forecast to the
MSE of the individual forecasts and (ii) testing the optimality of each forecast
for quadratic loss. The entries in Table V equal 1 if the MSE of the switching
forecast is less than or equal to both the MSEs of the individual forecasts. We
see that in 26 of 30 cases, the switching forecast is at least as accurate.
  Overall, we observe that our simple decision rule behaves reasonably and
adds useful information, suggesting that the model-selection implications of
our testing approach may be a promising direction for future research.

                                              7. CONCLUSION
  We propose a general framework for out-of-sample predictive ability test-
ing and forecast selection designed for use when the forecasting model may
be misspecified. Our method can be applied to evaluation of point, interval,
probability, and density forecasts for a general loss function.
  We depart from the approach to predictive ability testing of Diebold and
Mariano (1995) and West (1996) by evaluating the accuracy of a particular
forecasting method, rather than the accuracy of the forecasting model. Because
we consider forecasts based on estimators whose estimation uncertainty does
not vanish asymptotically, our tests have a number of appealing properties:
they directly capture the effect of estimation uncertainty on relative forecast
performance, they can handle comparison of forecasts based on both nested
and nonnested models, and they allow the forecasts to be produced by general
parametric, semiparametric, and nonparametric estimation techniques.

## Page 27: TESTS OF PREDICTIVE ABILITY 1571

源页：第 27 页

TESTS OF PREDICTIVE ABILITY                         1571

   Our framework can accommodate both unconditional objectives (which
forecasting method was more accurate on average?), which have been the sole
focus of the literature up to this point, as well as conditional objectives (can
we predict which forecasting method will be more accurate at a specific future
date?), which can help fine-tune the forecast selection decision to current eco-
nomic conditions. We accordingly propose two tests: a test of equal conditional
predictive ability and a test of equal unconditional predictive ability, which is
the Diebold and Mariano (1995) test extended to an environment that permits
parameter estimation.
   Our Monte Carlo simulations suggest that our conditional tests have good
finite-sample size and power properties. For the unconditional test, we show
that when we compare nested models, our test correctly recognizes that fore-
casts from a misspecified but parsimonious model may be as accurate as
forecasts from a correctly specified but less parsimonious model. Previously
available tests (McCracken (1999) and Clark and McCracken (2001)) instead
focus on the model rather than the forecasting method, and thus tend to fa-
vor the less parsimonious model. The disparity between the two approaches
is greater the smaller is the ratio of in-sample to out-of-sample sizes. A draw-
back of the unconditional test implemented here is that it tends to falsely reject
equal performance when the loss differences have zero mean but are highly se-
rially correlated. This may be possible to remedy by more careful selection of
HAC covariance estimators. On the other hand, the conditional tests emerge
as useful tools for detecting persistence in the relative performance of the fore-
casts, as well as cases where the relative performance may depend on the state
of the economy.
   We explore the model-selection implications of adopting a conditional per-
spective by proposing and illustrating a simple two-step decision rule for fore-
cast selection that tests for equal performance of the competing forecasts and
then—in case of rejection—uses currently available information to select the
best forecast for the future date of interest.
   One useful application of our tests is the evaluation of different parameter-
reduction methods for forecasting with a large number of predictors. We con-
sider three popular methods: a sequential model selection approach, the dif-
fusion indexes approach of Stock and Watson (2002), and Bayesian shrinkage
estimation. Previous techniques are not capable of comparing these forecasting
methods. We find that the sequential model-selection method performs worst,
probably due to its tendency to select large models. A second result is that
the predictors are less useful for price indexes than real variables. For these
variables, Bayesian shrinkage is the best method.
   Much work remains to be done. A significant area for future research is
the exploration of procedures for selecting the best forecasting method or for
optimally combining the methods in case of rejection of equal conditional pre-
dictive ability. A further generalization of our tests is to consider multiple com-
parison methods that are more sophisticated than the Hochberg–Bonferroni

## Page 28: 1572 R. GIACOMINI AND H. WHITE

源页：第 28 页

1572                            R. GIACOMINI AND H. WHITE

bounds of Section 6, for example, by adapting the “reality check” approach
of White (2000) to the conditional framework. Finally, it may be possible
to obtain asymptotic refinements of the tests presented here by using boot-
strap resampling techniques; for example, by establishing whether the results
of Andrews (2002) can be extended to heterogeneous data.
  Dept. of Economics, University of California, at Los Angeles, 405 Hilgard Av-
enue, Box 951477, CA 90095, U.S.A.; giacomin@econ.ucla.edu
                                     and
  Dept. of Economics, University of California at San Diego, 9500 Gilman Drive,
La Jolla, CA 92093-0508, U.S.A.; hwhite@weber.ucsd.edu.
                 Manuscript received April, 2003; final revision received April, 2006.

                                    APPENDIX: PROOFS

   PROOF OF THEOREM 1: Under H0 , {Zm, t ,  Ft } is a MDS and we can ap-
                                                                         √          d
ply a MDS central limit theorem (CLT) to show that Ω̂−1/2              n    nZ̄m, n → N(0,  I)
                                                          d
as n → ∞, from which it follows that Tm, n             h
                                                         → χ2q as n → ∞. The MDS CLT
                                                             p                       √
we use requires conditions such that Ω̂n − Ωn → 0, where Ωn = var[ nZ̄m, n ].
                  '
Write Zm, t+1 Zm, t+1     = f (ht ,  Wt+1 ,  . . . ,  Wt−m ), where f (·) is a measurable func-
tion. Since {Wt } and {ht } are mixing by (i), and f is a function of only a finite
number of leads and lags of Wt and ht , it follows from Lemma 2.1 of White
                                               '
and Domowitz (1984) that {Zm, t+1 Zm, t+1             } is also mixing of the same size as Wt .
                                                                     '
To apply the law of large numbers (LLN) to Zm, t+1 Zm, t+1                  , we further need
to ensure that each of its elements has absolute r + δ moment bounded uni-
formly in t. By the Cauchy–Schwarz inequality and (ii), E|Zm, t+1, i Zm, t+1, j |r+δ ≤
[E|Zm, t+1, i
      2
            |r+δ ]1/2 [E|Zm, t+1, j
                          2
                                  |r+δ ]1/2 < '1/2 '1/2 < ∞, i,  j = 1,  . . . ,  q and for all t.
                  p
That Ω̂n −Ωn → 0 then follows from McLeish’s (1975) LLN as in Corollary 3.48
of White (2001). The variable Ωn is finite by (ii) and it is uniformly positive
definite by (iii). We apply the Cramér–Wold device (e.g., Proposition 5.1 of
                                                                  √         d
White (2001)) and show that for all λ ∈ Rq , λ' λ = 1, λ' Ω−1/2     nZ̄m, n → N(0,  1),
                            √         d
                                                              n
                                                                    √
which implies that Ω−1/2      nZ̄m, n → N(0,  I). Consider λ' Ω−1/2     nZ̄m, n = n−1/2 ×
-T −1 ' −1/2            n
                                      ' −1/2
                                                     -  q
                                                                n

    t=m λ Ωn     Zm, t+1 and write λ Ωn Zm, t+1 = i=1 λ̃i Zm, t+1, i . The variable
λ̃i Zm, t+1, i is measurable with respect to Ft , and we have that E[λ' Ω−1/2    Zm, t+1 |
        -q                                                                  n
Ft ] = i=1 λ̃i E[Zm, t+1, i |Ft ] = 0, given (3). Hence {λ Ωn Zm, t+1 ,  Ft } is a MDS.
                                                        ' −1/2
                                                 √                         √
The asymptotic variance is σ̄n2 = var[λ' Ω−1/2n    nZ̄m, n ] = λ' Ω−1/2
                                                                  n    var[ nZ̄m, n ] ×
Ω−1/2
   n   λ = 1 for all n sufficiently large. We have
                 .
                 T −1

           n−1          λ' Ω−1/2
                            n
                                         '
                                 Zm, t+1 Zm, t+1 Ω−1/2
                                                n    λ−1
                 t=m
                                                                                         p
              = λ' Ω−1/2
                    n    Ω̂n Ω−1/2
                              n    λ − λ' Ω−1/2
                                           n    Ωn Ω−1/2
                                                    n    λ = g(Ω̂n ) − g(Ωn ) → 0, 

## Page 29: TESTS OF PREDICTIVE ABILITY 1573

源页：第 29 页

TESTS OF PREDICTIVE ABILITY                                  1573
                    p
because Ω̂n − Ωn → 0 and by using Proposition 2.30 of White (2001). Further-
more, by Minkowski’s inequality,
                                      q               2+δ
                                     .                
                                                      
         E|λ' Ω−1/2 Z m, t+1 |2+δ
                                 = E    λ̃i Z m, t+1, i 
               n
                                                      
                                       i=1
                                      q                                  2+δ
                                      .
                                 ≤          λ̃i (E|Zm, t+1, i |
                                                            2+δ 1/(2+δ)
                                                                )                < ∞, 
                                      i=1

the last inequality following from (ii). Hence, the sequence {λ' Ω−1/2
                                                                  n    Zm, t+1 ,  Ft }
satisfies the conditions of Corollary 5.26 of White (2001) (CLT for MDS),
                             √         d
which implies that λ' Ω−1/2     nZ̄m, n → N(0,  1). By the Cramér–Wold device,
      √         d
                          n
Ω−1/2
  n     nZ̄m, n → N(0,  I), from which the desired result follows by consistency
of Ω̂n for Ωn .                                                           Q.E.D.

  PROOF OF THEOREM 2: By arguments similar to those used in the proof
of Theorem 1, {Zm, t+1 } is mixing of the same size as Wt . Furthermore, each
element of Zm, t+1 is bounded uniformly in t by (ii). McLeish’s (1975) LLN (cf.
                                                             p
White (2001, Cor. 3.48)) then implies Z̄m, n − E[Z̄m, n ] → 0. Under HA, h there
                             '
exists ε > 0 such that E[Z̄m, n ]E[Z̄m, n ] > 2ε for all n sufficiently large. Then
               '
                                 '                '
                                                                        
(15)      P[Z̄m, n Z̄m, n > ε] ≥ P Z̄m, n Z̄m, n − E[Z̄m, n ]E[Z̄m, n ] > −ε
                                 '                  '
                                                                       
                             ≥ P |Z̄m, n Z̄m, n − E[Z̄m, n ]E[Z̄m, n ]| < ε → 1.
                                                                          '
By arguments identical to those used in the proof of Theorem 1, {Zm, t+1 Zm, t+1 }
is mixing of the same size as Wt by (i) and each of its elements is bounded
                                                                            p
uniformly in t by (ii). McLeish’s (1975) LLN then implies that Ω̂n − Ωn → 0,
with Ωn uniformly positive definite by (iii). The conditions of Theorem 8.13 of
White (1994) are then satisfied, and the theorem implies that for any constant
c ∈ R, P[Tm, n
           h
              > c] → 1 as n → ∞.                                        Q.E.D.
                                                                  √           d
   PROOF OF THEOREM 3: (a) Under H0 , we show that Ω̃−1/2     n      nZ̄m, n → N(0,  I)
as n → ∞, from which (a) follows. First, we apply the Cramér–Wold de-
                                                         √          d
vice and show that for all λ ∈ Rq , λ' λ = 1, λ' Ω−1/2      nZ̄m, n → N(0,  1), where
           √                                         n
Ωn = var[ nZ̄m, n ], using the fact that E[Zm, t+τ |Ft ] = 0. The variable Ωn is fi-
                                                                            √
nite by (ii) and it is uniformly positive definite by (iii). Write λ' Ω−1/2     nZ̄m, n =
  −1/2
       -T −τ ' −1/2                                                      n
n        t=m λ Ωn    Zm, t+τ . We verify that {λ Ωn Zm, t+τ } satisfies the condi-
                                                 ' −1/2

tions of the Wooldridge and White (1988) CLT for mixing processes. By ar-
guments identical to those used in the proof of Theorem 1, {λ' Ω−1/2             Zm, t+τ }
                                                                           √n
is mixing of the same size as Wt . Furthermore, σ̄n2 = var[λ' Ω−1/2           n Z̄ m, n ] =
              √                                                        n
λ' Ω−1/2
     n   var[  nZ̄ m, n ]Ω−1/2
                         n    λ = 1 > 0  for all  n sufficiently   large.  Finally,     by

## Page 30: 1574 R. GIACOMINI AND H. WHITE

源页：第 30 页

1574                        R. GIACOMINI AND H. WHITE

Minkowski’s inequality,
                                      q             2+δ
                                     .              
                                                    
          E|λ' Ω−1/2 Zm, t+τ |2+δ = E    λ̃i Zm, t+τi 
                n
                                                    
                                            i=1
                                       q                                   2+δ
                                       .
                                 ≤            λ̃i (E|Zm, t+τi |2+δ 1/(2+δ)
                                                                 )                 < ∞, 
                                        i=1

the last inequality following from (ii). Hence, {λ' Ω−1/2n  Zm, t+τ } satisfies the
conditions of Corollary 3.1 of Wooldridge and White (1988), which implies
              √        d
that λ' Ω−1/2   nZ̄m, n → N(0,  1). By the Cramér–Wold device, we then have
      √  n
               d                                           p
Ω−1/2
  n     nZ̄m, n → N(0,  I). It remains to show that Ω̃n − Ωn → 0, which completes
the proof. We have
          Ω̃n − Ωn
                   .
                   T −τ

             = n−1               '
                        [Zm, t+τ Zm, t+τ             '
                                       − E(Zm, t+τ Zm, t+τ )]
                    t=m

                               .
                               τ−1
                                            .
                                            T −τ
                                                 
                       + n−1         wn, j                   '
                                                    Zm, t+τ Zm, t+τ−j             '
                                                                    − E(Zm, t+τ Zm, t+τ−j )
                               j=1          t=m+j

                                                                 '                   '
                                                                                            
                                                     + Zm, t+τ−j Zm, t+τ − E(Zm, t+τ−j Zm, t+τ ).
                                   '
For j = 0,  . . . ,  τ − 1, {Zm, t+τ Zm, t+τ−j } is mixing of the same size as Wt and each
of its elements is bounded uniformly in t by (ii). Applying McLeish’s (1975)
LLN (e.g., Corollary 3.48 of White (2001)) and using the fact that wn, j → 1 for
                                     -T −τ                                           p
n → ∞, it follows that n−1 wn, j t=m+j [Zm, t+τ Zm, t+τ−j '                   '
                                                              − E(Zm, t+τ Zm, t+τ−j )] → 0
                                                                             p
for each j = 0,  . . . ,  τ − 1 (with wn, 0 ≡ 1), implying Ω̃n − Ωn → 0.
   (b) Using the same arguments as in the proof of Theorem 1, {Zm, t+τ } is mix-
ing of the same size as Wt . Furthermore, each element of Zm, t+τ is bounded uni-
                                                                                     p
formly in t by (ii). McLeish’s (1975) LLN then implies that Z̄m, n − E[Z̄m, n ] → 0.
                                                                   '
By definition, under HA, h there exists ε > 0 such that E[Z̄m, n        ]E[Z̄m, n ] > 2ε for
all n sufficiently large. We then have
               '
                                    '               '
                                                                          
(16)       P[Z̄m, n Z̄m, n > ε] ≥ P Z̄m, n  Z̄m, n − E[Z̄m, n ]E[Z̄m, n ] > −ε
                                    '                 '
                                                                         
                               ≥ P |Z̄m, n Z̄m, n − E[Z̄m, n ]E[Z̄m, n ]| < ε → 1.
By arguments identical to those used in part (a), which for this particular re-
sult do not require the time dependence structure imposed under the null
                                      p
hypothesis, it follows that Ω̃n − Ωn → 0 with Ωn uniformly positive definite
by (iii). Theorem 8.13 of White (1994) then implies that for any constant c ∈ R,
     h
P[Tm, n, τ  > c] → 1 as n → ∞.                                            Q.E.D.

## Page 31: TESTS OF PREDICTIVE ABILITY 1575

源页：第 31 页

TESTS OF PREDICTIVE ABILITY                           1575
                                                                        √
  PROOF OF THEOREM 4: (a) We separately show that under H0 , n('L̄m, n /
     d                            √                                 p
σn ) → N(0,  1), where σn2 = var[ n'L̄m, n ], and that σ̂n − σn → 0, from which
the result follows. The variable σn2 is finite by (ii) and it is positive for all n
                                   √                          -T −τ
sufficiently large by (iii). Write n('L̄m, n /σn ) = n−1/2 t=m σn−1 'Lm, t+τ . We
verify that the sequence {σn−1 'Lm, t+τ } satisfies the conditions of Wooldridge
and White’s (1988) CLT for mixing processes. By arguments similar to those
used in the proof of Theorem 1, {σn−1 'Lm, t+τ } is mixing of the same size as Wt .
Furthermore, by (ii), E|σn−1 'Lm, t+τ |2+δ < ∞. Hence, {σn−1 'Lm, t+τ } satisfies the
conditions of Corollary 3.1 of Wooldridge and White (1988), which implies that
√                d
  n('L̄m, n /σn ) → N(0,  1). By arguments similar to the preceding, {'Lm, t+τ } is
mixing of the same size as Wt , which implies that {'Lm, t+τ } is also mixing with φ
of size −r/(r − 1) or α of size −2r/(r − 2). This, together with assumption (ii)
and with the fact that E('Lm, t+τ ) = 0 under H0 , implies that the conditions of
                                                                    p
Theorem 6.20 of White (2001) are satisfied, and thus σ̂n − σn → 0.
  (b) As shown in (a), {'Lm, t+τ } is mixing of the same size as Wt . Furthermore,
'Lm, t+τ is bounded uniformly in t by (ii). McLeish’s (1975) LLN (as in Corol-
                                                                      p
lary 3.48 of White (2001)) then implies that 'L̄m, n − E['L̄m, n ] → 0. Under HA
there exists ε > 0 such that (E['L̄m, n ])2 > 2ε for all n sufficiently large. We
then have
                                                           
(17)      P['L̄2m, n > ε] ≥ P 'L̄2m, n − (E['L̄m, n ])2 > −ε
                                                          
                         ≥ P |'L̄2m, n − (E['L̄m, n ])2 | < ε → 1.
                                                             p
By arguments identical to those used in part (a), σ̂n2 −σn2 → 0 and by (iii), σn2 > 0
for all n sufficiently large. From Theorem 8.13 of White (1994), it follows that
for any constant c ∈ R, P[n'L̄2m, n /σ̂n2 > c 2 ] = P[tm, n, τ
                                                       2
                                                            > c 2 ] → 1 as n → ∞,
which implies that P[|tm, n, τ | > c] → 1 as n → ∞.                            Q.E.D.

  PROOF OF PROPOSITION 5: We have
                               
           1.
       E       (Yt+1 − fˆt, m
                          (i) 2
                             )
           n t
                1 .                                        
            =       (E[Yt+1 − fˆt, m ]) + Var(Yt+1 − fˆt, m
                                 (i) 2                 (i)
                                                           ) ,      i = 1,  2.
                n t

For i = 1, the bias term is
                                                             2
          (E[Yt+1 − β̂t, m Xt+1 ])2 = c − Xt+1 (E[β̂t, m ] − 1)
                                        '   -              2
                                               j Xj
                                   =c 1−
                                      2
                                           -      2
                                                    Xt+1
                                               j Xj

## Page 32: 1576 R. GIACOMINI AND H. WHITE

源页：第 32 页

1576                              R. GIACOMINI AND H. WHITE

and the variance term is
                                                  '
                                                          X2
          Var(Yt+1 − β̂t, m Xt+1 ) = σ         2
                                                      1 + - t+1 2 .
                                                           j Xj


For i = 2, the bias term is

          (E[Yt+1 − δ̂t, m − γ̂t, m Xt+1 ])2 = 0

and the variance term is

          Var(Yt+1 − δ̂t, m − γ̂t, m Xt+1 )
                = σ 2 + Var(δ̂t, m ) + Xt+1
                                       2
                                           Var(γ̂t, m ) + 2Xt+1 cov(δ̂t, m ,  γ̂t, m )
                     '    - 2
                             j Xj     X2        X̄
                = σ2 1 +            + t+1 − 2        Xt+1 .
                           mSxx        Sxx      Sxx
                -                                -
Letting E[ n1       t   (Yt+1 − fˆt, m ) ] = E[ n1 t (Yt+1 − fˆt, m
                                   (1) 2
                                                                  ) ] gives c in (11) as a solu-
                                                               (2) 2

tion.                                                                                    Q.E.D.

  PROOF OF PROPOSITION 6: Given the assumption of normality, we have
                                 
          1.
       E       L(Yt+1 ,  fˆt, m
                           (i)
                               )
          n t
                  1 .                                                
                =      E[exp(Yt+1 − fˆt, m
                                       (i)
                                           )] − E[Yt+1 − fˆt, m
                                                            (i)
                                                                ]−1
                  n t
                       '
                  1.                            1
                =      exp E[Yt+1 − fˆt, m(i)
                                             ] + Var(Yt+1 − fˆt, m(i)
                                                                     )
                  n t                           2

                              − E[Yt+1 − fˆt, m
                                            (i)
                                                ]−1 .


Substituting the expressions for E[Yt+1 − fˆt, m
                                             (i)
                                                 ] and Var(Yt+1 − fˆt, m
                                                                     (i)
                                                                         ), i = 1,  2,
                                                             -
from the proof of Proposition 5 and letting F(c) = E[ n1 t L(Yt+1 ,  fˆt, m     (1)
                                                                                  )] −
   1
     -           ˆ(2)
E[ n t L(Yt+1 ,  ft, m )] gives (12).                                           Q.E.D.

                                           REFERENCES
AMISANO, G., AND R. GIACOMINI (2006): “Comparing Density Forecasts via Weighted Likeli-
 hood Ratio Tests,” Journal of Business & Economic Statistics, in press. [1553]
ANDREWS, D. W. K. (1991): “Heteroskedasticity and Autocorrelation Consistent Covariance Ma-
 trix Estimation,” Econometrica, 59, 817–858. [1554,1556,1557,1560]

## Page 33: TESTS OF PREDICTIVE ABILITY 1577

源页：第 33 页

TESTS OF PREDICTIVE ABILITY                                  1577

           (2002): “Higher-Order Improvements of a Computationally Attractive k-Step Boot-
  strap for Extremum Estimators,” Econometrica, 70, 119–162. [1572]
BIERENS, H. B. (1990): “A Consistent Conditional Moment Test of Functional Form,” Economet-
  rica, 58, 1443–1458. [1556]
CHAO, J. C., V. CORRADI, AND N. R. SWANSON (2001): “An Out-of-Sample Test for Granger
  Causality,” Macroeconomic Dynamics, 5, 598–620. [1545]
CLARK, T. E. (1999): “Finite-Sample Properties of Tests of Equal Forecast Accuracy,” Journal of
  Forecasting, 18, 489–504. [1558]
CLARK, T. E., AND M. W. MCCRACKEN (2001): “Tests of Equal Forecast Accuracy and Encom-
  passing for Nested Models,” Journal of Econometrics, 105, 85–110. [1545,1547,1559,1560,1571]
CLARK, T. E., AND K. D. WEST (2005): “Using Out-of-Sample Mean Squared Prediction Errors
  to Test the Martingale Difference Hypothesis,” NBER Technical Working Paper #305. [1546]
CLEMENTS, M. P., AND D. F. HENDRY (1998): Forecasting Economic Time Series. Cambridge,
  U.K.: Cambridge University Press. [1551]
          (1999): Forecasting Non-Stationary Economic Time Series. Cambridge, MA: MIT Press.
  [1551]
CORRADI, V., N. R. SWANSON, AND C. OLIVETTI (2001): “Predictive Ability with Cointegrated
  Variables,” Journal of Econometrics, 104, 315–358. [1545]
DIEBOLD, F. X., AND R. S. MARIANO (1995): “Comparing Predictive Accuracy,” Journal of Busi-
  ness & Economic Statistics, 13, 253–263. [1545,1546,1557,1558,1570,1571]
DIEBOLD, F. X., AND J. A. LOPEZ (1996): “Forecast Evaluation and Combination,” in Handbook
  of Statistics, Vol. 14: Statistical Methods in Finance, ed. by G. S. Maddala and C. R. Rao.
  Amsterdam: North-Holland, 241–268. [1553]
FAMA, E. F., AND J. D. MACBETH (1973): “Risk, Return, and Equilibrium: Empirical Tests,”
  Journal of Political Economy, 81, 607–636. [1548,1550]
GIACOMINI, R., AND I. KOMUNJER (2005): “Evaluation and Combination of Conditional Quan-
  tile Forecasts,” Journal of Business & Economic Statistics, 23, 416–431. [1553,1555]
GONEDES, N. (1973): “Evidence on the Information Content of Accounting Massages:
  Accounting-Based and Market-Based Estimate of Systematic Risk,” Journal of Financial and
  Quantitative Analysis, 8, 407–444. [1548,1550]
GRANGER, C. W. J., AND P. NEWBOLD (1977): Forecasting Economic Time Series. London: Acad-
  emic Press. [1546]
HARVEY, D. I., S. J. LEYBOURNE, AND P. NEWBOLD (1997): “Testing the Equality of Prediction
  Mean Squared Errors,” International Journal of Forecasting, 13, 281–291. [1546]
HOCHBERG, Y. (1988): “A Sharper Bonferroni Procedure for Multiple Tests of Significance,”
  Biometrika, 75, 800–802. [1569]
HOOVER, K. D., AND S. J. PEREZ (1999): “Data Mining Reconsidered: Encompassing and
  the General-to-Specific Approach to Specification Search,” Econometrics Journal, 2, 167–191.
  [1548,1564]
LEITCH, G., AND J. E. TANNER (1991): “Economic Forecast Evaluation: Profits versus the Con-
  ventional Error Measures,” American Economic Review, 81, 580–590. [1546,1552]
LITTERMAN, R. B. (1986): “Forecasting with Bayesian Vector Autoregressions—Five Years of
  Experience,” Journal of Business & Economic Statistics, 4, 25–38. [1548,1564,1565]
MCCRACKEN, M. W. (1999): “Asymptotics for Out-of-Sample Tests of Granger Causality,” Work-
  ing Paper, University of Missouri, Columbia. [1559-1561,1571]
          (2000): “Robust Out-of-Sample Inference,” Journal of Econometrics, 99, 195–223. [1545,
  1554]
MCLEISH, D. L. (1975): “A Maximal Inequality and Dependent Strong Laws,” The Annals of
  Probability, 3, 826–836. [1572-1575]
NEWEY, W. K., AND K. D. WEST (1987): “A Simple, Positive Semidefinite, Heteroskedasticity and
  Autocorrelation Consistent Covariance Matrix,” Econometrica, 55, 703–708. [1556]
PESARAN, M. H., AND A. TIMMERMANN (2006): “Selection of Estimation Window in the Pres-
  ence of Breaks,” Journal of Econometrics, forthcoming. [1548,1552]

## Page 34: 1578 R. GIACOMINI AND H. WHITE

源页：第 34 页

1578                         R. GIACOMINI AND H. WHITE

STINCHCOMBE, M. B., AND H. WHITE (1998): “Consistent Specification Testing with Nuisance
  Parameters Present Only under the Alternative,” Econometric Theory, 14, 295–325. [1556]
STOCK, J. H., AND M. W. WATSON (2002): “Macroeconomic Forecasting Using Diffusion In-
  dexes,” Journal of Business & Economic Statistics, 20, 147–162. [1548,1564,1571]
WEST, K. D. (1996): “Asymptotic Inference about Predictive Ability,” Econometrica, 64,
  1067–1084. [1545,1546,1549,1550,1554,1570]
WEST, K. D., H. J. EDISON, AND D. CHO (1993): “A Utility-Based Comparison of Some Models
  of Exchange Rate Volatility,” Journal of International Economics, 35, 23–45. [1546,1552]
WHITE, H. (1994): Estimation, Inference and Specification Analysis. New York: Cambridge Uni-
  versity Press. [1551,1573-1575]
          (2000): “A Reality Check for Data Snooping,” Econometrica, 68, 1097–1126. [1572]
         (2001): Asymptotic Theory for Econometricians. San Diego: Academic Press. [1572-1575]
WHITE, H., AND I. DOMOWITZ (1984): “Nonlinear Regression with Dependent Observations,”
  Econometrica, 52, 143–162. [1572]
WOOLDRIDGE, J. M., AND H. WHITE (1988): “Some Invariance Principles and Central Limit The-
  orems for Dependent Heterogeneous Processes,” Econometric Theory, 4, 210–230. [1573-1575]
