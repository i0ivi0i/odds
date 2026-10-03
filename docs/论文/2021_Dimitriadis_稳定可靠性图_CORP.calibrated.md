# Stable Reliability Diagrams Using CORP and Isotonic Recalibration

> 重建说明：模式 transcribe；来源 `2021_Dimitriadis_稳定可靠性图_CORP.pdf`；共 10 页；原图逐页查看 10/10 页。
> 核图证据：对照 `.ky-md-work/2021_Dimitriadis_稳定可靠性图_CORP/pages/` 下 page-01.png 至 page-10.png 全量 10 页原图，重构 Table 1 评分规则解析式表与 Table 2 CORP 评分分解表（失准度 MCB、辨别力 DSC、不确定性 UNC）为标准 Markdown 管道表格，全保真修复保序回归 (Pool-Adjacent-Violators) 与一致性分解方程。

## Page 01: Stable reliability diagrams for probabilistic classifiers

源页：第 1 页

Stable reliability diagrams for probabilistic classifiers
                                              Timo Dimitriadisa,b,1 , Tilmann Gneitingb,c , and Alexander I. Jordanb
                                              a
                                               Alfred Weber Institute of Economics, Heidelberg University, 69115 Heidelberg, Germany; b Computational Statistics Group, Heidelberg Institute for
                                              Theoretical Studies, 69118 Heidelberg, Germany; and c Institute for Stochastics, Karlsruhe Institute of Technology, 76131 Karlsruhe, Germany

                                              Edited by Bin Yu, University of California, Berkeley, CA, and approved January 13, 2021 (received for review August 5, 2020)

                                              A probability forecast or probabilistic classifier is reliable or cal-           cipitation forecasts at Niamey, Niger, in July–September 2016.
                                              ibrated if the predicted probabilities are matched by ex post                    They concern three competing forecasting methods, including
                                              observed frequencies, as examined visually in reliability diagrams.              the world-leading, 52-member ensemble system run by the Euro-
                                              The classical binning and counting approach to plotting reliability              pean Center for Medium-Range Weather Forecasts [ENS (6)],
                                              diagrams has been hampered by a lack of stability under unavoid-                 a reference forecast called extended probabilistic climatology
                                              able, ad hoc implementation decisions. Here, we introduce the                    (EPC), and a purely data-driven statistical forecast (Logistic), as
                                              CORP approach, which generates provably statistically consis-                    described by Vogel et al. (ref. 7, figure 2).
                                              tent, optimally binned, and reproducible reliability diagrams in                    Not surprisingly, the classical approach to plotting reliability
                                              an automated way. CORP is based on nonparametric isotonic                        diagrams is highly sensitive to the specification of the bins, and
                                              regression and implemented via the pool-adjacent-violators (PAV)                 the visual appearance may change drastically under the slight-
                                              algorithm—essentially, the CORP reliability diagram shows the                    est change. We show an example in Fig. 2 A–C for a fourth type
                                              graph of the PAV-(re)calibrated forecast probabilities. The CORP                 of forecast at Niamey, namely, a statistically postprocessed ver-
                                              approach allows for uncertainty quantification via either resam-                 sion of the ENS forecast called ensemble model output statistics
                                              pling techniques or asymptotic theory, furnishes a numerical                     (EMOS), for which choices of m = 9, 10, or 11 equidistant bins
                                              measure of miscalibration, and provides a CORP-based Brier-score                 yield drastically distinct reliability diagrams. This is a discon-
                                              decomposition that generalizes to any proper scoring rule. We                    certing state of affairs for a widely used data-analytic tool and
                                              anticipate that judicious uses of the PAV algorithm yield improved               contrary to well-argued recent pleas for reproducibility (8) and




                                                                                                                                                                                                                             STATISTICS
                                              tools for diagnostics and inference for a very wide range of                     stability (9).
                                              statistical and machine learning methods.                                           A simple and seemingly effective enhancement is to use evenly
                                                                                                                               populated bins, as opposed to equidistantly spaced bins. Perhaps
                                              calibration | discrimination ability | probability forecast |                    surprisingly, instability remains a major issue, typically caused by
                                              score decomposition | weather prediction                                         multiple occurrences of the same forecast value at bin breaks.
                                                                                                                               Furthermore, the instabilities carry over to associated numer-
                                                                                                                               ical measures of calibration, such as the Brier-score reliability
                                              C   alibration or reliability is a key requirement on any prob-
                                                  ability forecast or probabilistic classifier. In a nutshell, a
                                              probabilistic classifier assigns a predictive probability to a binary
                                                                                                                               component (10–14) and the Hosmer–Lemeshow statistic (15–
                                                                                                                               19). These issues have been well documented in both research
                                              event. The classifier is calibrated or reliable if, when looking                 papers (16–20) and textbooks (21–23) and may occur even when
                                              back at a series of extant forecasts, the conditional event fre-                 the size n of the dataset is large. See SI Appendix, sections S1 and
                                              quencies match the predictive probabilities. For example, if                     S2 for illustrations on meteorological, geophysical, social science,
                                              we consider all cases with a predictive probability of about                     and economic forecast datasets.
                                              0.80, the observed event frequency ought to be about 0.80
                                              as well. While for many decades, researchers and practition-                          Significance
                                              ers have been checking calibration in myriads of applications
                                              (1, 2), the topic is subject to a surge of interest in machine                        Probabilistic classifiers assign predictive probabilities to binary
                                              learning (3), spurred by the recent recognition that “modern                          events, such as rainfall tomorrow, a recession, or a personal
                                              neural networks are uncalibrated, unlike those from a decade                          health outcome. Such a system is reliable or calibrated if
                                              ago” (4).                                                                             the predictive probabilities are matched by the observed fre-
                                                                                                                                    quencies. In practice, calibration is assessed graphically in
                                              Reliability Diagrams: Binning and Counting
                                                                                                                                    reliability diagrams and quantified via the reliability com-
                                              The key diagnostic tool for checking calibration is the reliability                   ponent of mean scores. Extant approaches rely on binning
                                              diagram, which plots the observed event frequency against the                         and counting and have been hampered by ad hoc imple-
                                              predictive probability. In discrete settings, where there are only                    mentation decisions, a lack of reproducibility, and inefficiency.
                                                                                                1             9
                                              a few predictive probabilities, such as, e.g., 0, 10 , . . . , 10 , 1, this is        Here, we introduce the CORP approach, which uses the pool-
                                              straightforward. However, even in discrete settings, there might                      adjacent-violators algorithm to generate optimally binned,
                                              be many such values. Furthermore, statistical and machine-                            reproducible, and provably statistically consistent reliability
                                              learning approaches to binary classification generate continuous                      diagrams, along with a numerical measure of miscalibration
                                              predictive probabilities that can take any value between zero                         based on a revisited score decomposition.
                                              and one, and typically the forecast values are pairwise distinct.
                                              In these settings, researchers have been using the “binning and                  Author contributions: T.D., T.G., and A.I.J. designed research; T.D., T.G., and A.I.J. per-
                                              counting” approach, which starts by selecting a certain, typi-                   formed research; T.D. and A.I.J. contributed new reagents/analytic tools; T.D. and A.I.J.
                                              cally arbitrary, number of bins for the forecast values. Then,                   analyzed data; and T.D., T.G., and A.I.J. wrote the paper.y
                                              for each bin, one plots the respective conditional event fre-                    The authors declare no competing interest.y
                                              quency versus the midpoint or average forecast value in the bin.                 This article is a PNAS Direct Submission.y
                                              For calibrated or reliable forecasts, the two quantities ought to                This open access article is distributed under Creative Commons Attribution License 4.0
                                              match, and so the points plotted ought to lie on, or close to, the               (CC BY).y
                                              diagonal (2, 5).                                                                 1
                                                                                                                                   To whom correspondence may be addressed. Email: timo.dimitriadis@h-its.org.y
Downloaded at KIT Library on March 19, 2021




                                                 In Fig. 1 A, C and E, we show reliability diagrams based on                   This article contains supporting information online at https://www.pnas.org/lookup/suppl/
                                              the binning and counting approach with a choice of m = 10                        doi:10.1073/pnas.2016191118/-/DCSupplemental.y
                                              equally spaced bins for 24-h-ahead daily probability of pre-                     Published February 17, 2021.



                                              PNAS 2021 Vol. 118 No. 8 e2016191118                                                                             https://doi.org/10.1073/pnas.2016191118 | 1 of 10

## Page 02: ENS / Binning and Counting ENS / CORP

源页：第 2 页

ENS / Binning and Counting                                      ENS / CORP
                                                                     A                                                               B
                                                                           1.00                                                            1.00
                                                                                                                                                      MCB = .066
                                                                                                                                                      DSC = .044
                                                                                                                                                      UNC = .244
                                                                           0.75                                                            0.75


                                                                     CEP




                                                                                                                                     CEP
                                                                           0.50                                                            0.50




                                                                           0.25                                                            0.25




                                                                           0.00                                                            0.00

                                                                                  0.00        0.25         0.50        0.75   1.00                 0.00        0.25        0.50        0.75         1.00
                                                                                                     Forecast value                                                   Forecast value


                                                                     C            EPC / Binning and Counting                         D EPC / CORP
                                                                           1.00                                                            1.00
                                                                                                                                                     MCB = .022
                                                                                                                                                     DSC = .032
                                                                                                                                                     UNC = .244
                                                                           0.75                                                            0.75
                                                                     CEP




                                                                                                                                     CEP




                                                                           0.50                                                            0.50




                                                                           0.25                                                            0.25




                                                                           0.00                                                            0.00

                                                                                   0.00       0.25         0.50        0.75   1.00                0.00         0.25        0.50        0.75         1.00
                                                                                                      Forecast value                                                  Forecast value


                                                                     E            Logistic / Binning and Counting                    F            Logistic / CORP
                                                                           1.00                                                            1.00
                                                                                                                                                     MCB = .017
                                                                                                                                                      DSC = .056
                                                                                                                                                      UNC = .244
                                                                           0.75                                                            0.75
                                                                     CEP




                                                                                                                                     CEP




                                                                           0.50                                                            0.50




                                                                           0.25                                                            0.25




                                                                           0.00                                                            0.00

                                                                                   0.00       0.25         0.50        0.75   1.00                0.00         0.25        0.50        0.75         1.00
                                                                                                      Forecast value                                                  Forecast value

                                              Fig. 1. Reliability diagrams for probability of precipitation forecasts over Niamey, Niger (7), in July–September 2016 under ENS (A and B), EPC (C and D),
                                              and Logistic (E and F) methods. (A, C, and E) We show reliability diagrams under the binning and counting approach with a choice of 10 equally spaced bins.
                                              (B, D, and F) We show CORP reliability diagrams with uncertainty quantification through 90% consistency bands. The histograms at the bottom illustrate
                                              the distribution of the n = 92 forecast values.

[图已对原图] Fig. 1 六幅可靠性图（A–F）。点值和柱高未抄数字。


                                                While alternative methods for the choice of the binning have                           grams and report associated measures of calibration based on ad
                                              been proposed in the literature (5, 24, 25), extant approaches                           hoc choices. In this light, Stephenson et al. (ref. 26, p. 757) call for
                                              exhibit similar instabilities, lack theoretical justification, are elab-                 the development of “nonparametric approaches for estimating
Downloaded at KIT Library on March 19, 2021




                                              orate, and have not been adopted by practitioners. Instead,                              the reliability curves (and hence the Brier score components),
                                              researchers across disciplines continue to craft reliability dia-                        which also include[d] point-wise confidence intervals.”


                                              2 of 10 | PNAS                                                                                                                                                   Dimitriadis et al.
                                                        https://doi.org/10.1073/pnas.2016191118                                                                           Stable reliability diagrams for probabilistic classifiers

## Page 03: A EMOS / 9 Equidistant Bins B EMOS / 10 Equidistant Bins

源页：第 3 页

A            EMOS / 9 Equidistant Bins                          B EMOS / 10 Equidistant Bins
                                                                                     1.00                                                           1.00




                                                                                     0.75                                                           0.75




                                                                               CEP




                                                                                                                                              CEP
                                                                                     0.50                                                           0.50




                                                                                     0.25                                                           0.25




                                                                                     0.00                                                           0.00

                                                                                            0.00        0.25        0.50        0.75   1.00                0.00        0.25        0.50        0.75         1.00
                                                                                                               Forecast value                                                 Forecast value




                                                                               C EMOS / 11 Equidistant Bins                                    D EMOS / CORP
                                                                                     1.00                                                           1.00
                                                                                                                                                              MCB = .018
                                                                                                                                                              DSC = .030
                                                                                                                                                              UNC = .244
                                                                                     0.75                                                           0.75




                                                                                                                                                                                                                                                STATISTICS
                                                                               CEP




                                                                                                                                              CEP



                                                                                     0.50                                                           0.50




                                                                                     0.25                                                           0.25




                                                                                     0.00                                                           0.00

                                                                                            0.00        0.25        0.50        0.75   1.00                0.00        0.25        0.50        0.75         1.00
                                                                                                               Forecast value                                                 Forecast value


                                              Fig. 2. Reliability diagrams for probability of precipitation forecasts over Niamey, Niger (7), in July–September 2016 with the EMOS method, using the
                                              binning and counting approach with a choice of 9 (A), 10 (B), and 11 (C) equidistant bins, together with the CORP reliability diagram (D), for which we
                                              provide uncertainty quantification through 90% consistency bands.

[图已对原图] Fig. 2 四幅 EMOS 图（A–D）。点值和柱高未抄数字。



                                                 Here, we introduce an approach to reliability diagrams and                                     Reproducibility. The CORP approach does not require any tun-
                                              score decompositions, which resolves these issues in a theo-                                      ing parameters or implementation decision, thus yielding well-
                                              retically optimal and readily implementable way, as illustrated                                   defined and readily reproducible reliability diagrams and score
                                              on the forecasts at Niamey in Figs. 1 B, D, and F and 2D.                                         decompositions.
                                              In a nutshell, we use nonparametric isotonic regression and
                                              the pool-adjacent-violators (PAV) algorithm to estimate condi-                                    PAV Algorithm-Based. CORP is based on nonparametric isotonic
                                              tional event probabilities (CEPs), which yields a fully automated                                 regression and implemented via the PAV algorithm, a classical
                                              choice of bins that adapts to both discrete and continuous set-                                   iterative procedure with linear complexity only (33, 34). Essen-
                                              tings, without any need for tuning parameters or implementation                                   tially, the CORP reliability diagram shows the graph of the
                                              decisions. We equip the diagram with quantitative measures                                        PAV-(re)calibrated forecast probabilities.
                                              of (mis)calibration (MCB), discrimination ability (DSC), and                                         In the remainder of the article, we provide the details of CORP
                                              uncertainty (UNC), which improve upon the classical Brier-score                                   reliability diagrams and score decompositions, and we substanti-
                                              decomposition in terms of stability. We call this stable approach                                 ate the above claims via mathematical analysis and simulation
                                              CORP, as its novelty and power include the following four                                         experiments.
                                              properties.
                                                                                                                                                The CORP Approach: Optimal Binning via the PAV Algorithm
                                              Consistency. The CORP reliability diagram and the MCB mea-                                        The basic idea of CORP is to use nonparametric isotonic
                                              sure of (mis)calibration are consistent in the classical statistical                              regression to estimate a forecast’s CEPs as a monotonic, non-
                                              sense of convergence to population characteristics. We lever-                                     decreasing function of the original forecast values. Fortunately,
                                              age existing asymptotic theory (27–29) to demonstrate that the                                    in this simple setting, there is one, and only one, kind of non-
                                              rate of convergence is best possible and to generate large sample                                 parametric isotonic regression, for which the PAV algorithm
                                              consistency and confidence bands for uncertainty quantification.                                  provides a simple algorithmic solution (33, 34). To each origi-
                                                                                                                                                nal forecast value, the PAV algorithm assigns a (re)calibrated
                                              Optimality. The CORP reliability diagram is optimally binned, in                                  probability under the regularizing constraint of isotonicity, as
                                              that no other choice of bins generates more skillful (re)calibrated                               illustrated in textbooks (ref. 35, figures 2.13 and 10.7), and
Downloaded at KIT Library on March 19, 2021




                                              forecasts, subject to regularization via isotonicity (ref. 30,                                    this solution is optimal under a very broad class of loss func-
                                              theorem 1.10, and refs. 31 and 32).                                                               tions (ref. 30, theorem 1.10). In particular, the PAV solution


                                              Dimitriadis et al.                                                                                                                                                              PNAS | 3 of 10
                                              Stable reliability diagrams for probabilistic classifiers                                                                                               https://doi.org/10.1073/pnas.2016191118

## Page 04: constitutes both the nonparametric isotonic least squares and operate in the dis

源页：第 4 页

constitutes both the nonparametric isotonic least squares and          operate in the discrete setting, and else in the continuous one.
                                              the nonparametric isotonic maximum-likelihood estimate of              The CORP reliability diagrams in Figs. 1–3 also display measures
                                              the CEPs.                                                              of (most importantly, and hence highlighted) (mis)calibration
                                                 The CORP reliability diagram plots the PAV-calibrated prob-         (MCB), discrimination (DSC), and uncertainty (UNC), dis-
                                              ability versus the original forecast value, as illustrated on the      cussed in detail later on as we introduce the CORP score
                                              Niamey data in Figs. 1 B, D, and F and 2D. The PAV algorithm           decomposition.
                                              assigns calibrated probabilities to the individual unique forecast
                                              values, and we interpolate linearly in between, to facilitate com-     Uncertainty Quantification
                                              parison with the diagonal that corresponds to perfect calibration.     Bröcker and Smith (39) convincingly advocate the need for
                                              If a group of (one or more) forecast values are assigned identi-       uncertainty quantification, so that structural deviations of the
                                              cal PAV-calibrated probabilities, the CORP reliability diagram         estimated CEP from the diagonal can be distinguished from
                                              displays a horizontal segment. The horizontal sections can be          deviations that merely reflect noise. They employ a resampling
                                              interpreted as bins, and the respective PAV-calibrated probabil-       technique for the binning and counting method in order to
                                              ities are simply the bin-specific empirical event frequencies. For     find consistency bands under the assumption of calibration. For
                                              example, we see from Fig. 1B that the PAV algorithm assigns a          CORP, we extend this approach in two crucial ways, by gener-
                                              calibrated probability of 0.125 to ENS forecast values between         ating either consistency or confidence bands and by using either
                                               9
                                              52
                                                  and 2052
                                                            and a calibrated probability of 0.481 to ENS values      a resampling technique or asymptotic distribution theory, where
                                              between 21  52
                                                             and 42
                                                                  52
                                                                     . The PAV algorithm guarantees that both        we leverage existing theory for nonparametric isotonic regression
                                              the number and the positions of the horizontal segments (and,          estimates (27–29).
                                              hence, the bins) in the CORP reliability diagram are determined           Consistency bands are generated under the assumption that
                                              in a fully automated, optimal way.                                     the probability forecasts are calibrated, and so they are posi-
                                                 The assumption of nondecreasing CEPs is natural, as decreas-        tioned around the diagonal. There is a close relation to the
                                              ing estimates are counterintuitive, routinely being dismissed as       classical interpretation of statistical tests and P values: Under
                                              artifacts by practitioners. Furthermore, the constraint provides       the hypothesized perfect calibration, how much do reliability
                                              an implicit regularization, serving to stabilize the estimate and      diagrams vary, and how (un)likely is the outcome at hand?
                                              counteract overfitting, despite the method being entirely non-         In contrast, confidence bands cluster around the CORP esti-
                                              parametric. Under the binning and counting approach, small or          mate and follow the classical interpretation of frequentist con-
                                              sparsely populated bins are subject to overfitting and large esti-     fidence intervals: If one repeats the experiment numerous times,
                                              mation uncertainty, as exemplified by the sharp upward spike in        the fraction of confidence intervals that contain the true CEP
                                              Fig. 2B. The assumption of isotonicity in CORP stabilizes the          approaches the nominal level. The two methods are illustrated
                                              estimate and avoids artifacts; see the examples in Fig. 2D and SI      in Fig. 3, where the diagrams in Fig. 3 B and D feature con-
                                              Appendix, Figs. S2–S5.                                                 fidence bands and in Fig. 3 A and C show consistency bands,
                                                 In contrast to the binning and counting approach, which             as do the CORP reliability diagrams in Figs. 1 B, D, and F
                                              has not been subject to asymptotic analysis, CORP reliability          and 2D.
                                              diagrams are provably statistically consistent: If the predictive         In our adaptation of the resampling approach, for each iter-
                                              probabilities and event realizations are samples from a fixed,         ation, the resampled CORP reliability diagram is computed,
                                              joint distribution, then the graph of the diagram converges to         and confidence or consistency bands are then specified by
                                              the respective population equivalent, as a direct consequence of       using resampling percentiles, in customary ways. For consistency
                                              existing large sample theory for nonparametric isotonic regres-        bands, the resampling is based on the assumption of calibrated
                                              sion estimates (27–29). Furthermore, CORP is asymptotically            original forecast values, whereas PAV-calibrated probabilities
                                              efficient, in the sense that its automated choice of binning results   are used to generate confidence bands. While resampling works
                                              in an estimate that is as accurate as possible in the large sample
                                                                                                                     well in small to medium samples, the use of asymptotic theory
                                              limit. In Appendix B, we formalize these arguments and report on
                                                                                                                     suits cases where the sample size n of the dataset is large—
                                              a simulation study, for which we give details in Appendix A, and
                                                                                                                     exactly when the computational cost of resampling-based proce-
                                              which demonstrates that the efficiency of the CORP approach
                                                                                                                     dures becomes prohibitive. Existing asymptotic theory is readily
                                              also holds in small samples.
                                                                                                                     applicable and operates under weak conditions on the marginal
                                                 Traditionally, reliability diagrams have been accompanied by
                                                                                                                     distribution of the forecast values and (strict) monotonicity and
                                              histograms or bar plots of the marginal distribution of the pre-
                                                                                                                     smoothness of (true) CEPs (27–29).
                                              dictive probabilities, on either standard or logarithmic scales
                                                                                                                        The distinction between discretely and continuously dis-
                                              (e.g., ref. 36). Under the binning and counting approach, the
                                                                                                                     tributed forecasts becomes critical here, as the asymptotic theory
                                              histogram bins are typically the same as the reliability bins.
                                                                                                                     differs between these cases. For discrete forecasts, results of
                                              In plotting CORP reliability diagrams, we distinguish discretely
                                                                                                                     El Barmi and Mukerjee (27) imply that the difference between
                                              and continuously distributed classifiers or forecasts. Intuitively,
                                              the discrete case refers to forecast values that only take on a        the estimated and the true CEP, scaled by n 1/2 , converges to
                                              finite and sufficiently small number of distinct values. Then,         a (mixture of) normal distribution(s). For continuous forecasts,
                                              we show the PAV-calibrated probabilities as dots, interpolate          following Wright (28), the difference between the estimated
                                              linearly in between, and visualize the marginal distribution of        and the true CEP, magnified by n 1/3 , converges to Chernoff’s
                                              the forecast values in a bar diagram, as illustrated in Fig. 3 A       distribution (40). The distinct scaling laws imply that the con-
                                              and B. For continuously distributed forecasts, essentially every       vergence is faster in the discrete than in the continuous case,
                                              forecast takes on a different value, whence the choice of bin-         since in the former, the CORP binning stabilizes as it captures
                                              ning becomes crucial. The CORP reliability diagram displays            the discrete forecast values, and, thereafter, the amount of sam-
                                              the bin-wise constant PAV-calibrated probabilities in horizon-         ples per bin increases linearly, in accordance with the standard
                                              tal segments, which are linearly interpolated in between, and          n 1/2 rate. In either setting, asymptotic consistency and confi-
                                              we use the Freedman–Diaconis rule (37) to generate a his-              dence bands can be obtained from quantiles of the asymptotic
                                              togram estimate of the marginal density of the forecast values,        distributions in customary ways. See SI Appendix, section S3 for
Downloaded at KIT Library on March 19, 2021




                                              as exemplified in Fig. 3 C and D. In our software implemen-            details on both the resampling algorithm and asymptotic theory.
                                              tation (38), a simple default is used: If the smallest distance        As a caveat, these techniques operate under the assumption of
                                              between any two distinct forecast values is 0.01 or larger, we         independent, or at least exchangeable, forecast cases, which may

                                              4 of 10 | PNAS                                                                                                                     Dimitriadis et al.
                                                        https://doi.org/10.1073/pnas.2016191118                                             Stable reliability diagrams for probabilistic classifiers

## Page 05: 1.00 1.00

源页：第 5 页

A                                                              B
                                                                                     1.00                                                           1.00
                                                                                               MCB = .042                                                     MCB = .042
                                                                                               DSC = .055                                                     DSC = .055
                                                                                               UNC = .218                                                     UNC = .218
                                                                                     0.75                                                           0.75




                                                                               CEP




                                                                                                                                              CEP
                                                                                     0.50                                                           0.50




                                                                                     0.25                                                           0.25




                                                                                     0.00                                                           0.00

                                                                                            0.00        0.25        0.50        0.75   1.00                0.00        0.25        0.50         0.75          1.00
                                                                                                               Forecast value                                                 Forecast value


                                                                               C                                                              D
                                                                                     1.00                                                           1.00
                                                                                               MCB = .039                                                     MCB = .039
                                                                                               DSC = .061                                                     DSC = .061
                                                                                               UNC = .224                                                     UNC = .224
                                                                                     0.75                                                           0.75
                                                                              CEP




                                                                                                                                              CEP
                                                                                     0.50                                                           0.50




                                                                                                                                                                                                                                                  STATISTICS
                                                                                     0.25                                                           0.25




                                                                                     0.00                                                           0.00

                                                                                            0.00        0.25        0.50        0.75   1.00                0.00        0.25        0.50          0.75         1.00
                                                                                                               Forecast value                                                 Forecast value


                                              Fig. 3. CORP reliability diagrams in the setting of discretely (A and B) and continuously (C and D), uniformly distributed, simulated predictive prob-
                                                                                            √
                                              abilities x with a true, miscalibrated CEP of x, with uncertainty quantification via consistency (A and C) and confidence (B and D) bands at the
                                              90% level.

[图已对原图] Fig. 3 四幅模拟可靠性图（A–D）。点值和柱高未抄数字。


                                              or may not be warranted in practice. We encourage follow-up                                       proper. In practice, for a given sample (x1 , y1 ), . . . , (xn , yn ) of
                                              work in dependent data settings, as recently tackled for related                                  forecast-realization pairs, the empirical score
                                              types of data-science tools (41).
                                                                                                                                                                                                    n
                                                 In our software implementation (38), we use the following                                                                                     1X
                                              default choices. Suppose that the sample size is n, and there are                                                                      S̄X =           S(xi , yi ),                          [1]
                                                                                                                                                                                               n i=1
                                              k unique forecast values. For consistency bands, if n ≤ 1,000
                                              or if n ≤ 5,000 and n ≤ 50k , we use resampling; else we rely
                                              on asymptotic theory. In the latter case, we employ the discrete                                  is used for forecast ranking. Table 1 presents examples of proper
                                              asymptotic distribution if n ≥ 8k 2 , while otherwise we use the                                  and strictly proper scoring rules. The Brier score and logarithmic
                                              continuous one. For confidence bands, the current default uses                                    score are strictly proper. In contrast, the misclassification error
                                              resampling throughout, as the asymptotic theory depends on the                                    is proper, but not strictly proper—all that matters is whether or
                                              assumption of a true CEP with strictly positive derivative. In the                                not a classifier probability is on the correct side of 12 .
                                              simulation examples in Fig. 3, which are based on n = 1,024                                          Under any proper scoring rule, the mean score S̄X consti-
                                              observations, this implies the use of resampling in Fig. 3 B–D and                                tutes a measure of overall predictive performance. For several
                                              of discrete asymptotic theory in Fig. 3A. Fig. 4 shows coverage                                   decades, researchers have been seeking to decompose S̄X into
                                              rates of 90% consistency and confidence bands in the simulation                                   intuitively appealing components, typically thought of as reli-
                                              settings described in Appendix A, based on the default choices.                                   ability (REL), resolution (RES), and uncertainty (UNC) terms.
                                              The coverage rates are generally accurate, or slightly conserva-                                  The REL component measures how much the conditional event
                                              tive, especially in large samples. In SI Appendix, section S4A, we                                frequencies deviate from the forecast probabilities, while RES
                                              qualitatively confirm these results in simulation settings driven                                 quantifies the ability of the forecasts to discriminate between
                                              by datasets from meteorology, astrophysics, social science, and                                   events and nonevents. Finally, UNC measures the inherent dif-
                                              economics.                                                                                        ficulty of the prediction problem, but does not depend on the
                                                                                                                                                forecast under consideration. While there is a consensus on
                                              CORP Score Decomposition: MCB, DSC, and UNC Components                                            the character and intuitive interpretation of the decomposition
                                              Scoring rules provide a numerical measure of the quality of a                                     terms, their exact form remains subject to debate, despite a
                                              classifier or forecast by assigning a score or penalty S(x , y), based                            half-century quest in the wake of Murphy’s (11) Brier-score
                                              on forecast value x ∈ [0, 1] for a dichotomous event y ∈ {0, 1}.                                  decomposition. In particular, Murphy’s decomposition is exact in
Downloaded at KIT Library on March 19, 2021




                                              A scoring rule is proper (42) if it assigns the minimal penalty                                   the discrete case, but fails to be exact under continuous forecasts,
                                              in expectation when x equals the true underlying event prob-                                      which has prompted the development of increasingly complex
                                              ability. If the minimum is unique, the scoring rule is strictly                                   types of decompositions (13, 26).

                                              Dimitriadis et al.                                                                                                                                                                PNAS | 5 of 10
                                              Stable reliability diagrams for probabilistic classifiers                                                                                                 https://doi.org/10.1073/pnas.2016191118

## Page 06: Here, we adopt the general score decomposition introduced n1 , . . . , nk times,

源页：第 6 页

Here, we adopt the general score decomposition introduced                                                            n1 , . . . , nk times, with o1 , . . . , ok of these cases being events, is
                                              by Dawid (12), advocated forcefully by Siegert (14), and dis-                                                          “calibrated” if
                                              cussed by various other authors as well (e.g., refs. 13 and 43).                                                                                 oj
                                              Specifically, let S̄X ,                                                                                                                     zj =        for all j = 1, . . . , k .            [4]
                                                                                                                                                                                               nj
                                                                                         n                                               n
                                                                                    1X                                            1X                                 We posit that in the score decomposition of Eq. 3 the
                                                                           S̄C =          S(x̂i , yi ),        and        S̄R =         S(r , yi )         [2]       (re)calibrated values x̂1 , . . . x̂n ought to be the PAV-transformed
                                                                                    n i=1                                         n i=1
                                                                                                                                                                     probabilities, as displayed in the CORP reliability diagram,
                                                                                                                                                                     whereas the referencePforecast r ought to be the marginal
                                              denote the mean score for the original forecast values of                                                              event frequency ȳ = n1 ni=1 yi . These forecasts both satisfy the
                                              Eq. 1, the mean score for suitably (re)calibrated probabilities                                                        calibration condition of Eq. 4.
                                              x̂1 , . . . , x̂n , and the mean score for a constant reference forecast                                                 We refer to the resulting decomposition as the CORP score
                                              r , respectively. Then, S̄X decomposes as                                                                              decomposition, which enjoys the following properties:
                                                                                                                                                                  • MCB ≥ 0 with equality if the original forecast is calibrated.
                                                                                       S̄X = S̄X − S̄C − S̄R − S̄C + S̄R ,                                 [3]      • DSC ≥ 0 with equality if the PAV-(re)calibrated forecast is
                                                                                            | {z } | {z } |{z}
                                                                                                    MCB                 DSC         UNC                               constant.
                                                                                                                                                                    • The decomposition is exact.
                                              where we adopt, in part, terminology proposed by Ehm and                                                                  In particular, the CORP score decomposition never yields
                                              Ovcharov (44) and Pohle (45). As defined in Eq. 3, the miscal-                                                         counterintuitive negative values of the components, contrary to
                                              ibration component MCB is the difference of the mean scores                                                            choices in the extant literature. The cases of vanishing compo-
                                              of the original and the (re)calibrated forecasts. Similarly, the                                                       nents (MCB = 0 or DSC = 0) support the intuitive interpretation
                                              DSC component quantifies discrimination ability via the dif-                                                           of CORP reliability diagrams, in that parts away from the diag-
                                              ference between the mean score for the reference and the                                                               onal indicate lack of calibration, whereas extended horizontal
                                              (re)calibrated forecast, while the classical measure of uncer-                                                         segments are indicative of diminished discrimination ability. For
                                              tainty (UNC) is simply the mean score for the reference                                                                refined technical statements, proofs, and a demonstration that
                                              forecast.                                                                                                              under (re)calibration methods other than isotonic regression
                                                 In the extant literature, it has been assumed implicitly or                                                         these properties may fail, see Appendix C and SI Appendix,
                                              explicitly that the (re)calibrated and reference forecasts can be                                                      section S5.
                                              chosen at researchers’ discretion (e.g., refs. 14 and 45), without                                                        If S is the Brier score, then in the special case of discrete fore-
                                              considering whether or not the transformed probabilities are cal-                                                      casts with nondecreasing CEPs, the MCB, DSC, and UNC terms
                                              ibrated in the classical technical sense. Specifically, a probability                                                  in Eq. 3 agree with the REL, RES, and UNC components, respec-
                                              forecast with unique forecast values z1 < · · · < zk that are issued                                                   tively, in the classical Murphy decomposition, as we demonstrate


                                                                                                   Uniform                                                       Linear                                                   Beta Mixture
                                                                   1.00




                                                                   0.95




                                                                                                                                                                                                                                                            Consistency Bands
                                                                   0.90




                                                                   0.85
                                              Empirical Coverage




                                                                   0.80


                                                                   1.00




                                                                   0.95
                                                                                                                                                                                                                                                            Confidence Bands




                                                                   0.90




                                                                   0.85




                                                                   0.80

                                                                                 128              512            2048             8192        128             512            2048          8192            128             512           2048        8192
                                                                                                                                                              Sample Size

                                                                          Uncertainty Quantification via     continuous asymptotic theory    discrete asymptotic theory     resampling   Number k of Distinct Forecast Values    10      20     50   Inf


                                              Fig. 4. Empirical coverage, averaged equally over the forecast values, of 90% uncertainty bands for CORP reliability diagrams under default choices for
Downloaded at KIT Library on March 19, 2021




                                              1,000 simulation replicates. Upper concerns consistency bands, and Lower confidence bands. The columns correspond to three types of marginal distributions
                                              for the forecast values, and colors distinguish discrete and continuous settings, as described in Appendix A. Different symbols denote reliance of the bands
                                              on resampling, discrete, or continuous asymptotic distribution theory.


                                              6 of 10 | PNAS                                                                                                                                                                              Dimitriadis et al.
                                                        https://doi.org/10.1073/pnas.2016191118                                                                                                      Stable reliability diagrams for probabilistic classifiers

## Page 07: Table 1: Scoring Rules & CORP Decomposition (Table 2)

源页：第 7 页

### Table 1: Scoring Rules for Probability Forecasts of Binary Events

| Scoring Rule | Propriety | Analytic Form $S(x, y)$ |
|:---|:---:|:---|
| **Brier Score** | Strictly proper | $S(x, y) = (x - y)^2$ |
| **Logarithmic Score** | Strictly proper | $S(x, y) = -y \log x - (1 - y) \log(1 - x)$ |
| **Misclassification Error (0-1)** | Nonstrictly proper | $S(x, y) = \mathbb{I}(x < 0.5, y = 1) + \mathbb{I}(x > 0.5, y = 0) + 0.5 \mathbb{I}(x = 0.5)$ |

### Table 2: CORP Brier Score Decomposition for Probability Forecasts

*Under the CORP framework, the mean score decomposes into Miscalibration (MCB), Discrimination (DSC), and Uncertainty (UNC):*

$$\bar{S} = \text{MCB} - \text{DSC} + \text{UNC}$$

| Forecast Model | Mean Brier Score ($\bar{S}$) | Miscalibration (MCB $\downarrow$) | Discrimination (DSC $\uparrow$) | Uncertainty (UNC) |
|:---|:---:|:---:|:---:|:---:|
| **Logistic Regression Forecast** | 0.169 | 0.018 | **0.056** | 0.207 |
| **EMOS Benchmark Forecast** | 0.194 | 0.017 | 0.030 | 0.207 |
| **Difference (Gain)** | -0.025 | +0.001 | **+0.026** | 0.000 |

*Note: While both forecasts are well-calibrated (MCB near 0.017-0.018), the Logistic forecast achieves superior overall accuracy primarily due to significantly higher discrimination ability (DSC = 0.056 vs 0.030).*

## Page 08: and associated realizations y1 , . . . , yn ∈ {0, 1} from an order n α for α ∈ (

源页：第 8 页

and associated realizations y1 , . . . , yn ∈ {0, 1} from an                   order n α for α ∈ (0, 1), we obtain a consistent estimate with an
                                              underlying population, with the true CEP being nondecreasing.                  estimation variance that decays like n α−1 and a squared bias that
                                                 In the case of discretely distributed forecasts that attain a               decays like n −2α . Consequently, the MSE of the estimates is of
                                              small number k of distinct values only, results of El Barmi                    order n β , where β = max(α − 1, −2α). The optimal choice of
                                              and Mukerjee (27) imply that the MSE of the estimates in a                     the exponent, α = 13 , results in an MSE of order n −2/3 . While
                                              CORP reliability diagram decays at the standard rate of n −1 . If              this asymptotic rate is the same as under the CORP approach,
                                              the binning and counting approach separates the distinct fore-                 the CORP reliability diagram is preferable in finite samples, as
                                              cast values, the traditional reliability diagram and the CORP                  we now demonstrate.
                                              reliability diagram are asymptotically the same, and so are the                   In Fig. 6, we detail a comparison of CORP reliability diagrams
                                              respective asymptotic distributions. However, under the CORP                   to the binning and counting approach with either a fixed num-
                                              approach, the unique forecast values are always correctly iden-                ber m of bins, or m = m(n) = [n α ] empirical-quantile dependent
                                              tified as the sample size increases, while under the binning and               bins, where [x ] denotes the smallest integer less than or equal
                                              counting approach, this may or may not be the case, depending                  to x ∈ R. For this, we plot the empirical MSE of the various
                                              on implementation decisions.                                                   CEP estimates against the sample size n, using settings described
                                                 Large-sample theory for the continuously distributed case is                in Appendix A. Across columns, the distributions of the fore-
                                              more involved and generally assumes that the CEP is differ-                    cast values differ in shape, across rows, we are in the discrete
                                              entiable with strictly positive derivative. Asymptotic results of              setting with k = 10 and 50 unique forecast values, and in the con-
                                              Wright (28) for the variance and of Dai et al. (52) for the bias               tinuous setting, respectively. Throughout, the CORP reliability
                                              imply that the MSE of the CORP estimates decays like n −2/3 .                  diagrams exhibit the smallest MSE, uniformly over all sample
                                              We now compare to the binning and counting approach, either                    sizes and against all alternative methods, with the superiority
                                              using m fixed, equidistant bins or using m = m(n) empirical                    being the most pronounced under nonuniform forecast distribu-
                                              quantile-based bins. For a general sequence of m(n) bins, the                  tions with many unique forecast values, as frequently generated
                                              magnitudes of the asymptotic variance and squared bias are gov-                by statistical or machine-learning techniques. The data-driven
                                              erned by the most sparsely populated bin, at a disadvantage                    simulation experiments in SI Appendix, section S4B confirm the
                                              relative to the quantile-based case.                                           superiority of the CORP approach in terms of estimation effi-
                                                 The classical reliability diagram relies on a fixed number m                ciency. Only for simulation settings with nearly horizontal true
                                              of bins, finds the respective bin-averaged event frequencies, and              CEPs, the efficiency of the CORP approach is slightly inferior
                                              plots them against the bin midpoints or bin-averaged forecast                  to binning and counting with very small numbers of bins—
                                              values. Any such approach fails asymptotically, with estimates                 exactly the choices that perform particularly poorly in almost any
                                              that are, in general, biased and inconsistent. More adequately,                other setting.
                                              a flexible number m(n) of bins can be used, with boundaries
                                              defined via empirical quantiles of x1 , . . . , xn . Specifically, m(n)
                                              bins can be bracketed by zero, the empirical quantiles at level                Appendix C: Properties of CORP Score Decomposition
                                              j /m(n) for j = 1, . . . , m(n) − 1, and one. Then, for n sufficiently         Consider data (x1 , y1 ), . . . , (xn , yn ) in the form of probabil-
                                              large, each bin covers about n/m(n) data points, and the bin-                  ity forecasts and binary outcomes, so that x1 , . . . , xn ∈ [0, 1],
                                              averaged CEPs converge to the true CEPs at the respective true                 and y1 , . . . , yn ∈ {0, 1}. Let S̄X , S̄C , and S̄R denote the mean
                                              quantiles with an estimation variance that decays like m(n)/n                  scores for the original forecast values, (re)calibrated probabil-
                                              and a squared bias that decays like m(n)−2 . When m(n) is of                   ities, and a reference forecast, as defined in Eqs. 1 and 2,



                                              A            EMOS                                                              B           Logistic



                                                    1.00                                                                          1.00
                                                            MCB = .018                                                                     MCB = .017
                                                            DSC = .030                                                                     DSC = .056
                                                            UNC = .244                                                                     UNC = .244
                                                    0.75                                                                          0.75
                                              CEP




                                                                                                                            CEP




                                                    0.50                                                                          0.50




                                                    0.25                                                                          0.25




                                                    0.00                                                                          0.00

                                                           0.00     0.25         0.50         0.75        1.00                           0.00       0.25           0.50           0.75           1.00
                                                                           Forecast value                                                                   Forecast value
Downloaded at KIT Library on March 19, 2021




                                              Fig. 5. CORP discrimination diagrams for probability of precipitation forecasts over Niamey, Niger (7), in July–September 2016 with the EMOS (A) and
                                              Logistic (B) methods. The histograms at the top show the marginal distribution of the original forecast values, and the histograms at the right are for the
                                              PAV-recalibrated probabilities.


                                              8 of 10 | PNAS                                                                                                                                    Dimitriadis et al.
                                                        https://doi.org/10.1073/pnas.2016191118                                                            Stable reliability diagrams for probabilistic classifiers

## Page 09: Uniform Linear Beta Mixture

源页：第 9 页

Uniform                                            Linear                                         Beta Mixture
                                                    0.0300


                                                    0.0100




                                                                                                                                                                                                                   Discrete: k = 10
                                                    0.0030


                                                    0.0010


                                                    0.0003


                                                     0.100




                                                                                                                                                                                                                   Discrete: k = 50
                                                     0.010
                                              MSE




                                                     0.001



                                                     0.100




                                                                                                                                                                                                                   Continuous
                                                     0.010




                                                     0.001




                                                                                                                                                                                                                                      STATISTICS
                                                               128           512           2048           8192    128        512            2048           8192      128          512           2048        8192
                                                                                                                            Sample Size n

                                                                                                                 CORP   5    10       50    n1 6   n1 3    n1 2


                                              Fig. 6. MSE of the CEP estimates in CORP reliability diagrams for samples of size n, in comparison to the binning and counting approach with m = 5, 10,
                                              or 50 fixed bins, or m(n) = [nα ] quantile-based bins, where α = 16 , 31 , or 12 . Note the log–log scale. The simulation settings are described in Appendix A, and
                                              MSE values are averaged over 1,000 replicates.

[图已对原图] Fig. 6 九幅 MSE 曲线（对数坐标）。曲线数值未抄。



                                              and recall the definition of a calibrated forecast from Eq. 4.                        Then, forecast-value-wise recalibration is prone to overfitting,
                                              With the specific choices of the PAV-calibrated probabilities                         and, as already noted by Dawid (12), smoothing methods are
                                              as the (re)calibrated forecasts  x̂1 , . . . , x̂n , and the marginal                 required to render the approach useable.
                                              event frequency ȳ = n1 ni=1 yi as the constant reference fore-
                                                                     P
                                                                                                                                        As before, let us assume that the unique forecast values z1 <
                                              cast r , the score decomposition in Eq. 3 enjoys the following                        · · · < zk are issued n1 , . . . , nk times, with o1 , . . . , ok of these cases
                                              properties.                                                                           being events, so that n1 + · · · + nk = n and o1 + · · · + ok = n ȳ.
                                                                                                                                    The classical Brier-score decomposition then becomes
                                              Theorem 1. Given any set of original forecast values and associ-
                                              ated binary events, suppose that we apply the PAV algorithm to                                       k             2     k             2
                                              generate a (re)calibrated forecast and use the marginal event fre-                               1X          oj        1X          oj
                                                                                                                                       S̄X =          nj      − zj −        nj      − ȳ + ȳ (1 − ȳ),
                                              quency as reference forecast. Then, for every proper scoring rule S,                             n j =1      nj        n j =1      nj        | {z }
                                              the decomposition defined by Eqs. 2 and 3 satisfies the following:                               |         {z        } |         {z        }     UNC
                                                                                                                                                          REL                       RES
                                              1) MCB = S̄X − S̄C ≥ 0 with equality if the original forecast itself is
                                                 calibrated.                                                                        where the UNC component is the same as in the CORP decom-
                                              2) MCB > 0 if the score is strictly proper and the original forecast is               position in Eq. 3. Furthermore, subject to conditions that in
                                                 not calibrated.                                                                    genuinely discrete settings may be mild, the decompositions
                                              3) DSC = S̄R − S̄C ≥ 0 with equality if the (re)calibrated forecast is                agree in full.
                                                 constant.
                                              4) DSC > 0 if the score is strictly proper and the (re)calibrated                     Theorem 2. Under the Brier score, if the sequence o1 /n1 , . . . , ok /
                                                 forecast is not constant.                                                          nk is nondecreasing, then MCB = REL and DSC = RES, respectively.
                                              5) The decomposition is exact.
                                                                                                                                    Data Availability. The probability of precipitation forecast data at Niamey,
                                                 For further discussion see SI Appendix, section S5, where part                     Niger, are from the paper by Vogel et al. (ref. 7, figure 2), where the original
                                              A provides the proofs of Theorems 1 and 2, and part B illustrates                     data sources are acknowledged. Precipitation forecasts and realizations data
                                              that the properties 1–4 generally do not hold if recalibration                        have been deposited at GitHub (https://github.com/TimoDimi/replication
                                              methods other than isotonic regression are used. Dawid (12)                           DGJ20). Additional data analyses, simulation studies, technical discussion,
                                              introduced the score decomposition in Eq. 3 with the subtle,                          and the proofs of Theorems 1 and 2 have been relegated to SI Appendix.
                                              but important, difference that the recalibrated probabilities are                     Reproduction material for both the main article and SI Appendix, including
                                              obtained as the (unique) forecast-value-wise empirical event fre-                     data and code in the R software environment (51), are available online (38,
                                              quencies. Then, properties 1–5 of Theorem 1 are satisfied as                          53). Open-source code for the implementation of the CORP approach in the
                                                                                                                                    R language and environment for statistical computing (51) is available on
                                              well, and if the sequence of (unique) forecast-value-wise event
                                                                                                                                    CRAN (38).
Downloaded at KIT Library on March 19, 2021




                                              frequencies is isotonic, Dawid’s decomposition and the CORP
                                              decomposition coincide. However, isotonicity is frequently vio-                       ACKNOWLEDGMENTS. We thank two referees, Andreas Fink, Peter
                                              lated, especially for datasets with many unique forecast values.                      Knippertz, Benedikt Schulz, Peter Vogel, and seminar participants at the


                                              Dimitriadis et al.                                                                                                                                    PNAS | 9 of 10
                                              Stable reliability diagrams for probabilistic classifiers                                                                     https://doi.org/10.1073/pnas.2016191118

## Page 10: Luminy workshop on Mathematical Methods of Modern Statistics 2 and the Tschira F

源页：第 10 页

Luminy workshop on Mathematical Methods of Modern Statistics 2 and the                              Tschira Foundation, the University of Hohenheim and Heidelberg University,
                                              virtual International Symposium on Forecasting 2020 for providing data, dis-                        the Helmholtz Association, and Deutsche Forschungsgemeinschaft (German
                                              cussion, and encouragement. Our work has been supported by the Klaus                                Research Foundation) Project ID 257899354 TRR 165.


                                               1. D. J. Spiegelhalter, Probabilistic prediction in patient management and clinical trials.        28. F. T. Wright, The asymptotic behavior of monotone regression estimates. Ann. Stat. 9,
                                                  Stat. Med. 5, 421–433 (1986).                                                                       443–448 (1981).
                                               2. A. H. Murphy, R. L. Winkler, Diagnostic verification of probability forecasts. Int. J.          29. A. Mösching, L. Dümbgen, Montone least squares and isotonic quantiles. El. J. Stat.
                                                  Forecast. 7, 435–455 (1992).                                                                        14, 24–49 (2020).
                                               3. P. A. Flach, “Classifier calibration” in Encyclopedia of Machine Learning and Data              30. R. E. Barlow, D. J. Bartholomew, J. M. Bremner, H. D. Brunk, Statistical Inference
                                                  Mining, C. Sammut, G. I. Webb, Eds. (Springer, New York, 2016), pp. 210–217.                        under Order Restrictions (Wiley, Hoboken, NJ, 1972).
                                               4. C. Guo, G. Pleiss, Y. Sun, K. Q. Weinberger, “On calibration of modern neutral net-             31. T. Fawcett, A. Niculescu-Mizil, PAV and the ROC convex hull. Mach. Learn. 68, 97–106
                                                  works” in ICML’17: Proceedings of the 34th International Conference on Machine                      (2007).
                                                  Learning, D. Precup, Y. W. Teh, Eds. (PMLR, Cambridge, MA, 2017), pp. 1321–1330.                32. N. Brümmer, J. Du Preez, The PAV algorithm optimizes binary proper scoring rules.
                                               5. J. Bröcker, Some remarks on the reliability of categorical probability forecasts. Mon.             arXiv [Preprint] (2013). https://arxiv.org/abs/1304.2331 (Accessed 2 February 2021).
                                                  Weather Rev. 136, 4488–4502 (2008).                                                             33. M. Ayer, H. D. Brunk, G. M. Ewing, W. T. Reid, E. Silverman, An empirical distribution
                                               6. ECMWF Directorate, Describing ECMWF’s forecasts and forecasting system. ECMWF                       function for sampling with incomplete information. Ann. Math. Stat. 26, 641–647
                                                  Newsl 133, 11–13 (2012).                                                                            (1955).
                                               7. P. Vogel, P. Knippertz, T. Gneiting, A. H. Fink, M. Klar, A. Schlueter, Statistical forecasts   34. J. de Leeuw, K. Hornik, P. Mair, Isotone optimization in R: Pool-adjacent-violators
                                                  for the occurrence of precipitation outperform global models over northern tropical                 algorithm (PAVA) and active set methods. J. Stat. Softw., 10.18637/jss.v032.i05
                                                  Africa. Geophys. Res. Lett. 48, e2020GL091022 (2021).                                               (2009).
                                               8. V. Stodden et al., Enhancing reproducibility for computational methods. Science 354,            35. P. Flach, Machine Learning: The Art and Science of Algorithms That Make Sense of
                                                  1240–1241 (2016).                                                                                   Data (Cambridge University Press, Cambridge, UK, 2012).
                                               9. B. Yu, K. Kumbier, Veridical data science. Proc. Natl. Acad. Sci. U.S.A. 117, 3920–3929         36. T. H. Hamill, R. Hagedorn, J. S. Whitaker, Probabilistic forecast calibration using
                                                  (2020).                                                                                             ECMWF and GFS ensemble reforecasts. Mon. Weather Rev. 136, 2620–2632
                                              10. G. W. Brier, Verification of forecasts expressed in terms of probability. Mon. Weather              (2008).
                                                  Rev. 78, 1–3 (1950).                                                                            37. D. Freedman, P. Diaconis, On the histogram as a density estimator: L2 theory. Z.
                                              11. A. H. Murphy, A new vector partition of the probability score. J. Appl. Meteorol. 12,               Wahrscheinlichkeitsth. Verw. Geb. 57, 453–476 (1981).
                                                  595–600 (1973).                                                                                 38. T. Dimitriadis, A. I. Jordan, reliabilitydiag: Reliability diagrams using isotonic
                                              12. A. P. Dawid, “Probability forecasting” in Encyclopedia of Statistical Sciences, S. Kotz,            regression. R package version 0.1.3. https://cran.r-project.org/package=reliabilitydiag.
                                                  N. L. Johnson, C. B. Read, Eds. (Wiley-Interscience, Hoboken, NJ, 1986), vol. 7, pp.                Accessed 2 February 2021.
                                                  210–218.                                                                                        39. J. Bröcker, L. A. Smith, Increasing the reliability of reliability diagrams. Weather
                                              13. M. Kull, P. Flach, “Novel decompositions of proper scoring rules for classification:                Forecast. 22, 651–661 (2007).
                                                  Score adjustment as precursor to calibration” in ECML PKDD 2015: Machine Learn-                 40. P. Groeneboom, J. A. Wellner, Computing Chernoff’s distribution. J. Computat. Graph.
                                                  ing and Discovery in Databases, A. Appice et al., Eds. (Springer, Cham, Switzerland,                Stat. 10, 388–400 (2001).
                                                  2015), pp. 68–85.                                                                               41. J. Bröcker, Z. Ben Bouallègue, Stratified rank histograms for ensemble forecast
                                              14. S. Siegert, Simplifying and generalising Murphy’s Brier score decomposition. Q. J. R.               verification under serial dependence. Q. J. R. Meteorol. Soc. 146, 1976–1990
                                                  Meteorol. Soc. 143, 1178–1183 (2017).                                                               (2020).
                                              15. D. W. Hosmer, S. Lemeshow, Goodness-of-fit tests for the multiple logistic regression           42. T. Gneiting, A. E. Raftery, Strictly proper scoring rules, prediction, and estimation. J.
                                                  Model. Commun. Stat. A 9, 1043–1069 (1980).                                                         Am. Stat. Assoc. 102, 359–379 (2007).
                                              16. G. Bertolini, R. D’Amico, D. Nardi, A. Tinazzi, G. Apolone, One model, several results:         43. J. Bröcker, Reliability, sufficiency, and the decomposition of proper scores. Q. J. R.
                                                  The paradox of the Hosmer–Lemeshow goodness-of-fit test for the logistic regression                 Meteorol. Soc. 135, 1512–1519 (2009).
                                                  model. J. Epidemiol. Biostat. 5, 251–253 (2000).                                                44. W. Ehm, E. Y. Ovcharov, Bias-corrected score decomposition for generalized quantiles.
                                              17. O. Kuss, Global goodness-of-fit tests in logistic regression with sparse data. Stat. Med.           Biometrika 104, 473–480 (2017).
                                                  21, 3789–3801 (2002).                                                                           45. M.-O. Pohle, The Murphy decomposition and the calibration–resolution principle:
                                              18. J. Bröcker, Estimating reliability and resolution of probability forecasts through                 A new perspective on forecast evaluation. arXiv [Preprint] (2020). https://arxiv.
                                                  decomposition of the empirical score. Clim. Dyn. 39, 655–667 (2012).                                org/abs/2005.01835 (Accessed 2 February 2021).
                                              19. P. D. Allison, “Measures of fit for logistic regression” (Paper 1485-2014, SAS Global           46. W. Ehm, T. Gneiting, A. Jordan, F. Krüger, Of quantiles and expectiles: Consistent
                                                  Forum, Washington DC, 2014).                                                                        scoring functions, Choquet representations and forecast rankings (with discussion). J.
                                              20. A. Kumar, P. Liang, T. Ma, “Verified uncertainty calibration” in Proceedings of                     R. Stat. Soc. Ser. B 78, 505–562 (2016).
                                                  the 33rd Conference on Neural Information Processing Systems (NeurIPS 2019),                    47. T. Fawcett, An introduction to ROC analysis. Pattern Recogn. Lett. 8, 861–874
                                                  H. Wallach et al., Eds. (NeurIPS Foundation, San Diego, CA, 2019).                                  (2006).
                                              21. G. Tutz, Regression for Categorical Data (Cambridge University Press, Cambridge, UK,            48. G. Barnes et al., A comparison of flare forecasting methods. I. Results from the “all-
                                                  2011).                                                                                              clear” Workshop. Astrophys. J. 829, 89 (2016).
                                              22. A. Agresti, Categorical Data Analysis, (Wiley Series in Probability and Statistics, Wiley,      49. A. I. Jordan, A. Mühlemann, J. F. Ziegel, Optimal solutions to the isotonic regres-
                                                  Hoboken, NJ, ed. 3, 2013).                                                                          sion problem. arXiv [Preprint] (2019). https://arxiv.org/abs/1904.04761 (Accessed 2
                                              23. F. E. Harrell, Jr, Regression Modeling Strategies: With Applications to Linear Models,              February 2021).
                                                  Logistic Regression, and Survival Analysis (Springer Series in Statistics, Springer, Cham,      50. S. Bentzien, P. Friederichs, Decomposition and graphical portrayal of the quantile
                                                  Switzerland, 2015).                                                                                 score. Q. J. R. Meteorol. Soc. 140, 1924–1934 (2014).
                                              24. J. B. Copas, Plotting p against x. Appl. Stat. 32, 25–31 (1983).                                51. R Core Team, R: A language and environment for statistical computing (R Version
                                              25. F. Atger, Estimation of the reliability of ensemble-based probabilistic forecasts. Q. J.            4.0.3, R Foundation for Statistical Computing, Vienna, Austria, 2020). https://www.r-
                                                  R. Meteorol. Soc. 130, 627–646 (2004).                                                              project.org/. Accessed 2 February 2021.
                                              26. D. B. Stephenson, C. A. S. Coelho, I. T. Jolliffe, Two extra components in the Brier score      52. R. Dai, H. Song, R. F. Barber, G. Raskutti, The bias of isotonic regression. El. J. Stat. 14,
                                                  decomposition. Weather Forecast. 23, 752–757 (2008).                                                801–834 (2020).
                                              27. H. El Barmi, H. Mukerjee, Inferences under a stochastic ordering constraint. J. Am.             53. T. Dimitriadis, A. I. Jordan, Replication material. GitHub. https://github.com/
                                                  Stat. Assoc. 100, 252–261 (2005).                                                                   TimoDimi/replication DGJ20. Deposited 13 November 2020.
Downloaded at KIT Library on March 19, 2021




                                              10 of 10 | PNAS                                                                                                                                                             Dimitriadis et al.
                                                         https://doi.org/10.1073/pnas.2016191118                                                                                     Stable reliability diagrams for probabilistic classifiers
