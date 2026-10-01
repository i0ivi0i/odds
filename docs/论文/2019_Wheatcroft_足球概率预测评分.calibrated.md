# Evaluating probabilistic forecasts of football

> 重建说明：模式 transcribe；来源 `2019_Wheatcroft_足球概率预测评分.pdf`；共 29 页；原图逐页查看 2/29 页。
>
> 补充：正文按 PDF 文字层原样转写，未改写、未翻译、未凭看图补字。公式和上下标若在文字层里已经乱，保留原样，以 PDF 原页为准，不许猜。 已对原图：第3、29页。未列入的页只核对了文字层与页码，未打开原图。

## Page 01: Evaluating probabilistic forecasts of football

源页：第 1 页

Evaluating probabilistic forecasts of football
                                             matches: The case against the Ranked
arXiv:1908.08980v1 [stat.AP] 23 Aug 2019




                                                        Probability Score
                                                                     Edward Wheatcroft

                                           London School of Economics and Political Science, Houghton
                                                 Street, London, United Kingdom, WC2A 2AE.

                                                                       August 27, 2019


                                                                              Abstract
                                                  A scoring rule is a function of a probabilistic forecast and a cor-
                                              responding outcome that is used to evaluate forecast performance. A
                                              wide range of scoring rules have been defined over time and there is
                                              some debate as to which are the most appropriate for evaluating the
                                              performance of forecasts of sporting events. This paper focuses on
                                              forecasts of the outcomes of football matches. The ranked probability
                                              score (RPS) is often recommended since it is ‘sensitive to distance’,
                                              that is it takes into account the ordering in the outcomes (a home win
                                              is ‘closer’ to a draw than it is to an away win, for example). In this
                                              paper, this reasoning is disputed on the basis that it adds nothing in
                                              terms of the actual aims of using scoring rules. A related property
                                              of scoring rules is locality. A scoring rule is local if it only takes the
                                              probability placed on the outcome into consideration. Two simula-
                                              tion experiments are carried out in the context of football matches
                                              to compare the performance of the RPS, which is non-local and sen-
                                              sitive to distance, the Brier score, which is non-local and insensitive
                                              to distance, and the ignorance score, which is local and insensitive to
                                              distance. The ignorance score is found to outperform both the RPS
                                              and the Brier score, casting doubt on the value of non-locality and
                                              sensitivity to distance as properties of scoring rules in this context.

                                                                                  1

## Page 02: 1 Introduction

源页：第 2 页

1    Introduction
Probabilistic forecasting of sporting events such as football matches has be-
come an area of considerable interest in recent years. One reason for this
is that forecasting can help inform gambling decisions and therefore has the
potential to support the identification of profitable betting strategies. Prob-
abilistic forecasting has also grown in popularity in the sports media. In
some media outlets, for example, estimated probabilities are routinely dis-
seminated in match previews and even in-play. An obvious implication of
the growth of probabilistic forecasting in sport is the need for effective meth-
ods of forecast evaluation. This is particularly true in the case of gambling
where ‘beating the bookmaker’ is a difficult task which typically requires
highly informative predictions. However, even when the forecasts are used
for purposes other than gambling, there is often still an incentive for the
forecasts to be informative, or at least to be perceived as such. There is
therefore a need for objective measures of forecast performance. This paper
is concerned with the question of how to evaluate probabilistic forecasts of
events such as football matches with three or more possible outcomes.
    Evaluation of probabilistic forecasts is typically performed using scoring
rules, functions of the forecast and corresponding outcome aimed at assessing
forecast performance. A large number of scoring rules have been defined
over the years and there is considerable debate surrounding which are the
most appropriate. A common approach with which to differentiate candidate
scoring rules is to identify desirable properties and favour scores that have
them. There is often debate, however, surrounding which properties are
(most) desirable and hence a lack of consensus remains. As a result, in
fields such as weather forecasting, a wide range of different scores are often
presented.
    One property of scoring rules that is perhaps the most widely agreed
upon is called propriety. A score is proper if, in expectation, it favours a
forecast that consists of the distribution from which the outcome is drawn,
i.e a perfect probabilistic forecast. This paper is concerned primarily with
two more contentious properties. One of those properties is locality. A score
is local if it only considers the probability at the outcome and disregards
the rest of the distribution. A non-local score therefore takes at least some
of the rest of the forecast distribution into account. The other property of
interest concerns whether a scoring rule takes ordering into account. Events
with discrete outcomes can be divided into two categories: nominal and

                                       2

## Page 03: ordinal. Ordinal events have a natural ordering. For example, a question on

源页：第 3 页

ordinal. Ordinal events have a natural ordering. For example, a question on
a survey asking an interviewee to rate a service might have a set of potential
responses ranging from ‘very poor’ to ‘very good’. It is clear that ‘very good’
ranks higher than ‘good’, whilst ‘good’ ranks higher than ‘poor’. Nominal
events, on the other hand, have no natural ordering. For example, there
is no obvious way to rank a set of colours or nationalities. The outcomes
of football matches can be considered to be ordinal (along with matches in
other sports in which a draw is allowed). A home win is closer to a draw than
it is to an away win. As such, there is a question of whether a scoring rule
should take into account this ordering. A paper by Constantinou and Fenton
argues that forecast probability placed on potential outcomes close to the
actual outcome should be rewarded and therefore ordering should be taken
into account (Constantinou and Fenton [2012]). Therefore, if the match
outcome is a home win, probability placed on a draw should be rewarded
more than probability on an away win. Scoring rules that have this property
are referred to as being ‘sensitive to distance’. One scoring rule that has this
property is the ranked probability score (RPS). Constantinou and Fenton
therefore argue that the RPS is the appropriate score for the evaluation of
probabilistic forecasts of football matches. As a result, the RPS has become
perhaps the most popular and widely used scoring rule for this purpose. In
this paper, the view that sensitivity to distance in a scoring rule is beneficial
is disputed along with Constantinou and Fenton’s suggestion that the RPS
should be widely used to evaluate football forecasts.
    Three scoring rules are considered in this paper: the RPS, which is both
non-local and sensitive to distance, the Brier score, which is non-local but
insensitive to distance and the ignorance score, which is local and therefore
also insensitive to distance. It is argued that the ignorance score is the most
appropriate out of these three candidate scores and evidence is presented in
the form of two experiments demonstrating that the ignorance score is able
to identify a set of perfect forecasts quicker than the other two scoring rules.
    The question of how probabilistic forecasts of discrete events should be
evaluated is one with a long history. An early contribution to the literature
was the introduction of the Brier score (Brier [1950]). The Brier score con-
siders the squared distance between the forecast probability and the outcome
for each possible category in which the outcome could fall (the category in
which the outcome falls is represented with a one and all other categories
with a zero). Whilst the Brier score is most commonly applied to binary
events, it was originally formulated more generally such that it can be ex-

                                       3

## Page 04: tended to events with more than two possible outcomes. The ignorance score

源页：第 4 页

tended to events with more than two possible outcomes. The ignorance score
(Good [1992]; Roulston and Smith [2002]), often referred to as the logarith-
mic score, takes a different approach by simply taking the logarithm of the
probability placed on the outcome. The rationale behind the ignorance score
is in information theory and is closely related to other information measures
such as the Kullback-Leibler Divergence (Bröcker and Smith [2007]). The
ranked probability score (Epstein [1969]) is closely related to the Brier score
but compares the cumulative distribution function of the forecast and the
outcome rather than the probability mass function. Other proposed scor-
ing rules include the spherical score, which combines the probability placed
on the outcome with a correction term to ensure that it is proper (Friedman
[1983]) and the quadratic score which simply takes the mean squared distance
between the forecast and the outcome (Selten [1998]). This paper, however,
is concerned only with the ignorance score, Brier score and RPS. These scor-
ing rules were chosen because we are principally interested in the properties
of locality and sensitivity to distance. The RPS is both non-local and sensi-
tive to distance, the Brier score is non-local and insensitive to distance and
the ignorance score is local and insensitive to distance (the ignorance score
is in fact the only local and proper scoring rule (Bernardo [1979]).
    A range of other properties of scoring rules have been proposed, many
of which have been suggested as desirable in some way. Propriety, as men-
tioned above is perhaps the most well known property and it stipulates that,
in expectation, a scoring rule should favour the distribution from which the
outcome was drawn over all others (Bröcker and Smith [2007]). Another
property is locality. A score is local if only the probability at the outcome
is taken into account (Parry et al. [2012]). Other properties of scoring rules
include those that are equitable, defined as those that ascribe the same score,
in expectation, to constant forecasts as they do to a random forecast, reg-
ular, those that only ascribe an infinite score to a forecast that places zero
probability on the outcome (Gneiting and Raftery [2007]), and feasible, those
that assign bad scores to forecasts that give material probability to events
that are highly unlikely (Maynard [2016]).
    A number of authors have commented on the value of sensitivity to dis-
tance in scoring rules. Jose et al. [2009] recommended the use of scoring rules
that are sensitive to distance, including for forecasts of football matches.
They provide generalisations of existing scoring rules to make them sensitive
to distance. Staël von Holstein [1970] also recommended that scoring rules
should be sensitive to distance and suggest a family of scoring rules based

                                      4

## Page 05: on the RPS that also have this property. Murphy [1970] compared the for-

源页：第 5 页

on the RPS that also have this property. Murphy [1970] compared the for-
mulation of the RPS and the Brier score and recommended that the RPS
should at least be used alongside the Brier score when the event of interest
is ordered. Bernardo [1979], on the other hand commented that “when as-
sessing the worthiness of a scientist’s final conclusions, only the probability
he attaches to a small interval containing the true value should be taken into
account.” arguing for locality as a desirable property.
    There is a steadily increasing literature describing methodology for the
construction of probabilistic forecasts of sporting events such as football
matches (Diniz et al. [2019]). In many of these, scoring rules have been
deployed to attempt to assess the quality of those forecasts. For example,
Forrest et al. [2005] use the Brier score to compare probabilistic forecasts
derived from bookmakers’ odds and from a statistical model. Spiegelhalter
and Ng [2009] use the Brier score to assess the performance of their Premier
League match predictions. The ranked probability score has also been widely
used. For example, Koopman and Lit [2019] use the RPS to evaluate their
dynamic multivariate model of football matches, Baboota and Kaur [2019]
use the RPS to evaluate their machine learning approach to football predic-
tion and Schauberger et al. [2016] use the RPS alongside cross-validation to
select a tuning parameter in their model. The ignorance score appears to be
less widely used than the Brier score and the RPS. Diniz et al. [2019] compare
the performance of a number of predictive models using the ignorance score
alongside the Brier score and the spherical score whilst it also has been used
by Schmidt et al. [2008] alongside the Brier score to assess the probabilistic
performance of a prediction market for the 2002 World Cup.
    This paper is organised as follows. In section 2, formal definitions of the
scoring rules and their properties are given. In section 3, the arguments of
Constantinou and Fenton are presented and disputed. In section 4, the ques-
tion of how scoring rules are used in practice is discussed. The philosophical
difference between a perfect and imperfect model scenario is discussed in
section 5. The performance of the Brier score, Ignorance score and RPS are
compared in a model selection experiment using examples from Constantinou
and Fenton’s paper in section 6. A similar experiment is performed in sec-
tion 7 using forecast probabilities derived from bookmakers’ odds of actual
matches. Finally, section 8 is used for discussion and conclusions.




                                      5

## Page 06: 2 Background

源页：第 6 页

2     Background
2.1    Definitions of Scoring Rules
The three scoring rules considered in this paper are defined as follows. For
an event with r possible outcomes, let pj and oj be the forecast probability
and outcome at position j where the ordering of the positions is preserved.
The Brier score, generalised for forecasts of events with r possible outcomes,
is defined as                         r
                                     X
                            Brier =     (pi − oi )2 .                      (1)
                                      i=1
The ranked probability score is defined as
                                    r−1 X
                                    X   i
                          RPS =           (pj − oj )2 .                     (2)
                                    i=1 j=1

The ignorance score is defined as
                             IGN = − log2 (p(Y ))                           (3)
where p(Y ) is the probability placed on the outcome Y .

2.2    Properties of Scoring Rules
Throughout a long history of research, a large number of properties of scoring
rules have been defined. Here, those that are relevant to the arguments and
experiments in this paper are described.
    Perhaps the most well known property of scoring rules is propriety. A
score is proper if it is optimised, in expectation, with the distribution from
which the outcome was drawn. As such, a proper scoring rule always favours
a perfect probabilistic forecast in expectation. It is widely held that scoring
rules that do not have this property should be dismissed (Bröcker and Smith
[2007]). Each of the scoring rules described above are proper. A perfect
probabilistic forecast is rarely, if ever, expected to be possible to achieve in
practice. Therefore, in expectation, whilst a proper scoring rule will always
rank a perfect forecast more favourably than an imperfect one, different
proper scores will often rank pairs of imperfect forecasts differently.
    Another property of scoring rules is locality. A score is local if it only
takes into account the probability at the outcome. If any of the rest of the

                                        6

## Page 07: distribution is taken into account by the score, it is non-local. The ignorance

源页：第 7 页

distribution is taken into account by the score, it is non-local. The ignorance
score is local whilst the Brier Score and RPS are both non-local.
    For discrete events, another property concerns whether the score takes
into account the ordering of a set of potential outcomes. Scores that do this
are defined as sensitive to distance. For sporting events, for example, a draw
and a home win can be considered to be closer together than a home win
and an away win. An scoring rule that is sensitive to distance will therefore
reward probability placed on an event closer to the actual outcome. Whilst
the RPS is sensitive to distance, the ignorance and Brier Scores are not since
they do not take into account the ordering of the possible outcomes.


3    A Rebuttal of Arguments in Favour of the
     RPS
The popularity of the RPS for evaluating probabilistic forecasts of football
matches is largely due to a paper written by Constantinou and Fenton, pub-
lished in the Journal of Quantitative Analysis in Sports in 2012 (Constantinou
and Fenton [2012]). The crux of the argument in that paper is that prob-
ability placed on potential outcomes ‘close’ to the actual outcome should
be rewarded more than probability placed on those that are ‘further away’.
If the home team is currently winning by one goal, it would take the away
team to score one more goal for the match to end in a draw and two more
goals for it to end in an away win and, therefore, the potential outcomes are,
in a sense, ordered. The authors claim that, in light of this, only scoring
rules that are sensitive to distance should be considered. A natural choice is
therefore argued to be the RPS.
    With the aim of presenting further evidence towards the suitability of the
RPS, Constantinou and Fenton define five hypothetical football matches,
each with a specified outcome (i.e. a home win, a draw or an away win).
For each match, they define a competing pair of probabilistic forecasts and
use general reasoning to argue that, given the defined outcome, one is more
informative than the other. They then show that the RPS is the only scoring
rule out of a number of candidates that assigns the best score to their favoured
forecast in each case, and argue that this provides evidence of its suitability.
We dispute the validity of this reasoning. We argue that the approach by
which the performance of the scores is compared under a specific outcome of


                                       7

## Page 08: Match Forecast p(H) p(D) p(A) Result ‘Best’ Forecast

源页：第 8 页

Match Forecast      p(H)   p(D)    p(A)   Result ‘Best’ Forecast
 1     α             1      0       0      H      α
       β             0.9    0.1     0
 2     α             0.8    0.1     0.1    H        α
       β             0.5    0.25    0.25
 3     α             0.35   0.3     0.35   D        α
       β             0.6    0.3     0.1
 4     α             0.6    0.25    0.15   H        α
       β             0.6    0.15    0.25
 5     α             0.57   0.33    0.1    H        α
       β             0.6    0.2     0.2

Table 1: Match examples defined by Constantinou and Fenton. In each case,
forecast α is described as superior to forecast β by the authors.

the match is flawed. Instead, scores should be compared by considering the
underlying probability of each possible outcome, thereby taking into account
the underlying probability distribution of the match. This is a much more
difficult task.
    To provide a setting with which to illustrate the arguments of Constanti-
nou and Fenton and to provide counterarguments, details of the five hy-
pothetical matches used as examples in that paper are reproduced. The
outcome of each match, the two forecasts and an indicator of Constantinou
and Fenton’s favoured forecast (α or β) are shown in table 3.
    The reasoning given by the authors for favouring each forecast is as fol-
lows. For match one, forecast α predicts a home win with total certainty
and must outperform any other forecast (including β). For match two, fore-
cast α places more probability on the outcome than forecast β and therefore
provides the most informative forecast. For match three, the only match in
which the outcome is defined to be a draw, it is argued that, although both
forecasts place the same probability on the outcome, forecast α should be
favoured because the probability placed on a home win and an away win
are evenly distributed and therefore ‘more indicative of a draw’. For match
four, it is argued that forecast α should be favoured because, although both
forecasts place the same probability on the outcome, α places more proba-
bility ‘close’ to the home win, i.e. on a draw, than β and therefore is more
favourable. Finally, for match five, which is described as the most contentious


                                      8

## Page 09: case, whilst β places more probability on the outcome than α, the authors

源页：第 9 页

case, whilst β places more probability on the outcome than α, the authors
argue that forecast α is, in fact, more desirable than β because it is ‘more
indicative of a home win’ due to the greater probability placed on the draw.
To provide further justification for favouring forecast α, they give an example
in which a gambler uses the forecast to inform a bet on the binary event of
whether the match ends with any outcome other than an away win (com-
monly known as a lay bet). Since the sum of the probabilities on the home
win and the draw are higher for forecast α than for forecast β, they suggest
that α is more desirable for that purpose.
    Our main counterargument to the reasoning of Constantinou and Fenton
concerns their assertion that forecast α outperforms forecast β in each case.
In fact, it is impossible to say which of the two forecasts should be preferred
in each case without considering the underlying probability distribution of
the match (which is unknown in practice). Consider match one. Here, they
argue that forecast α should be rewarded more than any other forecast since
it predicts the outcome with absolute certainty. This seems entirely rea-
sonable since no forecast is able to place more probability on the outcome.
However, it does not follow from this that α is the best forecast. To illustrate
this, consider the case in which β represents the true underlying probability
distribution of the match; i.e. the match will end with a home win with prob-
ability 0.9, a draw with probability 0.1 and an away win with probability 0.
It is not contentious to state that β is the best forecast in this setting and we
argue that it would be deeply flawed to claim otherwise. Forecast α should
not be considered to be the best forecast simply because the match happened
to end in a home win (which would happen with 90 percent probability in this
case). In a succession of football matches in which the underlying probabil-
ity is represented by β and the forecast is α, a draw would eventually occur,
with forecast α placing zero probability on that event. The same logic can be
applied if the underlying probability distribution is represented by forecast
α, in which case, α can objectively be considered to be the best forecast.
In summary, without knowing the underlying probability distribution of the
match, the answer to the question of which forecast is best can only be ‘it
depends’. In practice, of course, it is never possible to know the underlying
distribution and therefore we cannot distinguish the performance of the two
forecasts on the basis of a single match.
    The effect of the probability distribution of the match on the favoured
forecast under each score is now demonstrated. For a given probability distri-
bution, the expected score of each of forecasts α and β are calculated, in order

                                       9

## Page 10: Colour Ignorance RPS Brier

源页：第 10 页

Colour      Ignorance RPS Brier
 Green           α      β   β
 Blue            β      α   β
 Red             β      β   α
 Turquoise       α      α   β
 Brown           α      β   α
 Purple          β      α   α
 Yellow          β      β   β
 Black           α      α   α

                Table 2: Colour scheme for figures 1 and 2.

to determine which is preferred by each scoring rule. This is repeated for a
large number of randomly selected underlying probability distributions. This
is demonstrated for match five in figure 1. Here, each dot represents a differ-
ent probability distribution of the match with the probability of a home win
and a draw on the x and y axes respectively. Each dot is coloured according
to which of the two candidate forecasts is preferred under the three scoring
rules. The colour scheme is defined in table 3. For example, if a point is
coloured blue, the RPS prefers α whilst the ignorance and Brier scores prefer
β under that distribution. Whilst the colour scheme might seem difficult to
interpret at first, it becomes much clearer when it is considered that points
coloured green, blue and red represent distributions in which only the ig-
norance, RPS and Brier score prefer α and that the colours of overlapping
regions are defined by mixing those colours. Note that, for this particular
match, there are no green areas, that is there are no underlying distributions
in which the ignorance score prefers α and the RPS and Brier score prefer β.
    The first conclusion to be drawn from figure 1 is that, clearly, as previ-
ously discussed, the forecast favoured by each scoring rule depends on the
underlying probability distribution. Moreover, the choice of scoring rule im-
pacts which of the two forecasts is preferred. We can look at each of the
regions and try to understand how and why the three scoring rules differ.
Consider the blue region in the bottom right of the figure. A point located
in the very bottom right represents a probability distribution which places
a probability of one on a home win and therefore zero on both a draw and
an away win. Here, the RPS is the only score that favours α over β. This
seems somewhat counterintuitive and can be argued to be a weakness of the
scoring rule. Here, the RPS rewards probability placed on a draw, regardless

                                      10

## Page 11: of the fact that that outcome cannot happen. The cost of doing this is that,

源页：第 11 页

of the fact that that outcome cannot happen. The cost of doing this is that,
out of the two forecasts, the one that places less probability on the outcome
is favoured.




Figure 1: Randomly chosen probability distributions of match five coloured
according to which forecast (α or β) is preferred by each of the three scoring
rules. The colour scheme is described in table 3.

    The same information as shown in figure 1 for match five is shown for
matches one to four in figure 2. This reinforces the importance of the under-
lying probability distribution and how the choice of forecast depends heavily
on the scoring rule.
    In practice, scoring rules are usually used to assess the performance of
forecasting systems rather than individual forecasts. A forecasting system is
a set of rules that is used to generate forecasts of different events in some
common way. For example, a forecasting system might be built on the basis of

                                     11

## Page 12: Figure 2: Randomly chosen probability distributions of matches one to four

源页：第 12 页

Figure 2: Randomly chosen probability distributions of matches one to four
coloured according to which forecast (α or β) is preferred by each of the three
scoring rules. The colour scheme is described in table 3.

an individual model, a combination of models or the judgement of a particular
person and can be applied to generate forecasts of a range of events (e.g.
football matches). Forecasting systems are then evaluated by taking the
average score over many events according to some scoring rule. This provides
a basis with which to select a forecasting system for the prediction of future
events.
    Before moving on, it is of interest to address two particular points made
by Constantinou and Fenton in favour of forecast α for match five. Firstly,
they describe a situation in which the forecasts are used to inform a ‘lay’
bet on an away win. They argue that, since the combined probability placed


                                      12

## Page 13: on a home win or a draw is higher for forecast α than for forecast β, α is a

源页：第 13 页

on a home win or a draw is higher for forecast α than for forecast β, α is a
better forecast, given this outcome. There is a simple counterargument to
this. If a gambler intends to use the forecasts to make lay bets such as the
one described, the resulting binary forecasts formed by adding the home win
and draw probabilities should be evaluated separately. This is because the
new binary forecasts take a different form and have a different aim. It does
not makes sense during evaluation to attempt to pre-empt how the forecasts
might be used to create other forecasts of a different nature. In fact, the
original match outcome forecasts and the binary forecasts might even favour
a different forecasting system. For example, one forecasting system might be
poor at distinguishing a home win from a draw but good at estimating the
probability of an away win. Tying one’s hands to create and use a one size
fits all forecast seems unnecessary and counterproductive in this case.
    The second point of contention regards the ‘indicativeness of a home win’
in match five. The authors argue that despite the fact that forecast β places
more probability on the outcome than forecast α, forecast α is more indicative
of a home win, due to the increased probability placed on the draw. It should
be noted here that, were the probability on the draw reduced to 0.3 and the
probability on the away win increased to 0.23, the RPS would favour forecast
β and thus the ‘indicativeness’ of a home win is somewhat arbitrary.
    The primary claim of Constantinou and Fenton is that probability placed
on possible outcomes that are ‘close’ to the actual outcome should be re-
warded more than probability placed on outcomes that are ‘further away’.
Furthermore, they argue that the RPS provides a scoring rule that does this
and is therefore suitable for evaluating forecasts of football matches. How-
ever, as described above, by not considering the underlying distribution of
the match, it is not possible to state that one forecast is better than another
and therefore the reasoning given in support of the RPS does not provide a
compelling argument. We therefore consider the question of which forecast
is assigned the best score, when conditioned on a single outcome, to be moot
and we do not consider it further. Instead, we define potential goals of using
scoring rules and ask whether the sensitivity to distance property offered by
the RPS has any value in achieving them.




                                      13

## Page 14: 4 What are Scoring Rules For?

源页：第 14 页

4     What are Scoring Rules For?
The principle intention of this paper is to assess the value of scoring rules that
are non-local and sensitive to distance in the context of forecasts of football
matches. In order to attempt to assess the merits of these properties, it is
useful to consider the aims behind the deployment of scoring rules. For the
properties of interest to have value, there should be some practical benefit
in terms of achieving those aims. Here, we discuss the aims behind the
application of scoring rules with a view to assessing whether the non-local
and sensitivity to distance properties help to achieve them.
    One obvious aim of scoring rules is to provide a means of comparison
between competing forecasting systems. There are many contexts in which
one might want to make such comparisons. One might have a finite set of
competing probabilistic forecasts of the same events and be looking to deter-
mine which is the most informative. For example, a broadcaster may want
to decide which forecasts are most useful to show in its sports coverage or
a gambler may wish to decide which forecasting service to subscribe to in
order to aid their betting decisions. A means of comparison can also be im-
portant in the context of model development. A forecaster looking to improve
the performance of their forecasting system by, for example, increasing the
number of factors included in the model, may want to assess whether these
changes result in improved forecasts. Parameter selection also falls under
the umbrella of forecast comparison since each set of parameter values will
lead to a different set of forecasts. Since parameters usually take continuous
values, parameter selection can be considered to be a comparison between
an infinite number of sets of forecasts.
    Whilst selecting one of two or more sets of forecasts may be considered
to be important in a range of settings, this alone does not give an indication
of the magnitude of the difference in skill. An additional question of inter-
est concerns how much more informative one set of forecasts is over another
and whether this difference is significant. Typically, two sets of forecasts
are compared using the difference in their mean score (Wheatcroft [2019]).
Resampling techniques can then be used to determine if that difference is
significant. An interesting question concerns whether the difference in scores
has an interpretation in terms of the relative performance of the forecast-
ing systems of interest. In fact, to our knowledge, only one of the scoring
rules considered in this paper has a useful interpretation when considered in
this way and that is the ignorance score. The difference between the mean

                                       14

## Page 15: ignorance scores of two forecasting systems represents the difference in infor-

源页：第 15 页

ignorance scores of two forecasting systems represents the difference in infor-
mation provided by each one expressed in bits. This means that calculating
2 to the power of the mean relative ignorance between forecasting systems
one and two yields the mean increase in probability density placed on the
outcome by the former over the latter.
    Whilst scoring rules are useful tools for evaluating and comparing fore-
casting systems, it is important to acknowledge their limitations. Often, a set
of forecasts are used with a specific purpose in mind. In sports forecasting,
this might be to aid a decision whether to place a bet on a certain outcome,
whether to select a certain player for a match or which play to make during
a game. It is therefore crucial to determine whether the forecasts are fit for
that specific purpose. For example, a set of forecasts may successfully in-
corporate important information and therefore score better than alternative
forecasts that do not incorporate this information yet still not be fit for a
specific purpose. For example, using a set of forecasts to choose whether to
place bets may result in a substantial loss which would have been avoided
had the bets not been placed at all.


5    Perfect and imperfect model scenarios
Philosophical approaches to the comparison of scoring rules typically consider
two distinct settings: the perfect model scenario, in which one of the candi-
date forecasting systems coincides with the probability distribution that gen-
erated the outcome (often referred to as the data generating model (DGM))
and the imperfect model scenario, in which each candidate forecasting system
is imperfect (Judd and Smith [2001, 2004]). In the perfect model scenario,
there should be no ambiguity as to which set of forecasts is most desirable;
a perfect forecasting system is always better than an imperfect one. In the
latter, on the other hand, the ‘best’ forecasting system is subjective and the
question of which one is the most desirable is also subjective.
    In the perfect model setting, there are two directly linked questions of
interest. Firstly, ‘does the scoring rule always favour the perfect forecasting
system in expectation?’ Scoring rules that do this are called proper and it
is generally considered that a chosen scoring rule should have this property
(Bröcker and Smith [2007]). As discussed in section 2.2, each of the three
scoring rules considered in this paper are proper and thus they cannot be
distinguished in this way. A closely linked means of comparison for scoring


                                      15

## Page 16: rules assumes that each one is proper and assesses how many past forecasts

源页：第 16 页

rules assumes that each one is proper and assesses how many past forecasts
and outcomes are required to have a given probability of selecting the perfect
forecasting system. Requiring fewer forecasts and outcomes to do this means
that the information is used more efficiently and therefore that there is a
better chance of selecting the best forecasting system for future events. This
observation forms the basis of the experiments presented in this paper.
    In practice, one can never expect any of the candidate forecasting sys-
tems to be perfect and therefore the perfect model case is generally accepted
to be only a theoretical construct. It can nonetheless be argued that the
performance of scoring rules in this context is important. If, in expectation,
a scoring rule does not favour a perfect forecasting system over all others,
one should be uneasy about the ability of that scoring rule to favour useful
imperfect forecasting systems over misleading ones. Similarly, the efficiency
in which a scoring rule uses the information in past forecasts and outcomes
ought to tell us something about the way in which each scoring rule uses the
information provided to it. For example, in the context of non-local scoring
rules that are sensitive to distance, if these properties are truely useful, we
might expect that that extra information should be capable of distinguishing
perfect and imperfect forecasting systems more quickly.
    In practical situations, since none of the candidate forecasting systems are
expected to be perfect, all exercises in forecasting system selection fall into
the imperfect category. In this setting, unlike the perfect model case, proper
scores will often favour different imperfect forecasting systems. Distinguish-
ing the scoring rules is then a question of identifying which type of imperfect
forecasts should be preferred. Other than the analysis demonstrated in fig-
ures 1 and 2, this question is left as future work.


6    Experiment one - Repeated outcomes of
     the same match
In this experiment, the five pairs of forecasts defined by Constantinou and
Fenton and shown in table 3 are used to assess the probability that each of the
three candidate scoring rules identifies a perfect forecasting system over an
imperfect one for a given number of past forecasts and outcomes. For a given
pair of forecasts, define the outcomes of a series of n matches by drawing from
forecast α or forecast β with equal probability 0.5. Define two forecasting


                                      16

## Page 17: systems as follows. The perfect forecasting system always knows which of

源页：第 17 页

systems as follows. The perfect forecasting system always knows which of
the two distributions from which the outcome is drawn and therefore always
defines the correct distribution as the forecast. The imperfect forecasting
system, on the other hand, always issues the alternative distribution as the
forecast. A scoring rule is defined to ‘select’ a forecasting system if it is
assigned the lowest mean score over n forecasts. The probability that each
scoring will select the perfect forecasting system is calculated for different
values of n and the experiment is carried out using each of the forecast pairs
in table 3.

6.1    Results
Perhaps the most interesting of the five examples defined by Constantinou
and Fenton is match five. Here, both forecast α and forecast β place similar
probability on a home win but forecast α places more probability on the
draw. The probability of each scoring rule identifying the perfect forecasting
system in this case is shown as a function of n in figure 3. Here, the ignorance
score outperforms both the Brier score and the RPS for almost every tested
value of n, whilst there is little difference in the performance of the Brier
score and RPS.
    The results for matches one to four are shown in figure 3. For match
one, the ignorance score clearly outperforms both the Brier score and the
RPS for relatively large values of n, whilst the difference is minimal for
lower values. The non monotonic nature of the probabilities under the RPS
and Brier scores may seem surprising at first but, in fact, can easily be
explained. All three scoring rules punish the imperfect forecasting system
when the outcome is a draw, since the forecast in this case predicts a home
win with certainty. The overall probability of a draw for a given realisation
is 0.05 since the probability that the outcome is drawn from β is 0.5 and the
probability of a draw given β is 0.1. For all values of n less than 20, once
a draw has occurred, no combinations of other outcomes can result in the
imperfect forecasting system being assigned a better mean score than the
perfect forecasting system. When n is greater than 20, on the other hand,
the imperfect forecasting system can still ‘recover’ from such a situation as
long as there is only one such occurrence. The probability for the ignorance
score, on the other hand, is monotonic and this is because the ignorance score
assigns an infinitely bad score to a forecast that places zero probability on
an outcome. Therefore, once such a case has been observed, the imperfect

                                      17

## Page 18: forecasting system cannot achieve a better score than the perfect forecasting

源页：第 18 页

forecasting system cannot achieve a better score than the perfect forecasting
system and, since the probability of observing such a case increases with n,
the probability is monotonically increasing.
    For match two, whilst the probabilities of selecting the perfect forecasting
system are similar for each score, the ignorance score slightly outperforms
the other two scores for all values of n. In terms of the Brier score and the
RPS, neither appears to be systematically better than the other.
    For match three, the ignorance score tends to outperform the other two
scores for all n greater than three, whilst, again, there is no obvious system-
atic difference between the performance of the RPS and Brier scores. For
very small n, the ignorance score achieves a lower probability of selecting the
perfect forecasting system. However, caution should be applied in such cases
since scoring rules are designed with a relatively large number of forecast
pairs in mind, that is, if the aim were to apply them to small n, they might
be designed differently.
    Match four provides perhaps the most interesting results. In this case,
α and β differ only in the probabilities placed on a draw and an away win.
There is therefore only a small difference between the perfect and imperfect
forecasting systems. This is reflected in the fact that the probability of
choosing the perfect forecasting system increases relatively slowly with n.
Here, whilst the ignorance and Brier scores perform similarly well, there is a
distinct advantage for both over the RPS. Whilst the RPS performs relatively
well for low n, the value of increasing n is far lower than for the ignorance and
Brier scores, i.e. the RPS does not make good use of the extra information
provided by increasing the number of forecasts and outcomes.
    Overall, from these results, there is no evidence that the RPS outper-
forms either the Brier or ignorance scores and, in fact, there is some evidence
that the opposite is true. The RPS does not typically make good use of
additional sample members in comparison to the other two scores. Looking
more closely at the results, the stark difference in performance in match four,
and to some extent match five, suggests that the biggest difference in perfor-
mance might be in cases in which the difference between the two candidate
forecasts is relatively small and this observation provides a motivation for
the design of experiment two. Experiment one considers only a case with re-
peated forecasts from one of two candidate distributions. In practice, there
is usually interest in forecasts of different events rather than a large number
of realisations of the same event. In experiment two, the performance of the
three candidate scoring rules is compared in the context of forecasts of a wide

                                       18

## Page 19: range of different football matches generated from actual bookmakers’ odds.

源页：第 19 页

range of different football matches generated from actual bookmakers’ odds.




Figure 3: Probability of each scoring rule selecting the perfect forecasting
system as a function of n for match 5.



7     Experiment two - forecasts based on match
      odds
In experiment two, the aim is to assess the effectiveness of each scoring rule in
terms of distinguishing a ‘perfect’ forecasting system from an ‘imperfect’ one
in a more realistic setting in which each match has a different probability
distribution. To do this, artificial pairs of forecasts are created in which
one represents the true distribution and the other is imperfect. The aim is
then to estimate the probability that each scoring rule selects the set of true
distributions.
    To obtain sets of forecasts that are realistic in terms of actual football
matches, bookmakers’ odds on past matches are used which are converted

                                       19

## Page 20: Figure 4: Probability of each scoring rule selecting the perfect forecasting

源页：第 20 页

Figure 4: Probability of each scoring rule selecting the perfect forecasting
system as a function of n for matches 1 to 4.

into probabilistic forecasts. These are taken from the repository of foot-
ball data at football-data.co.uk which supplies free-to-access data from
a range of European leagues. Details of the data and how the odds are used
to generate probabilistic forecasts are given in the appendix. Odds from a
total of 39,343 matches are available and form the basis of a set of candidate
probability distributions.
    We seek n pairs of forecasts such that one represents the true distribution
of the outcome, and therefore a perfect forecast, whilst the other represents
an imperfect forecast. In order to test the effect of different levels of imper-
fection, we define a method of controlling it. To create a perfect forecast
and corresponding outcome, a distribution is randomly drawn from the can-
didate set and defined to be the perfect forecast. A random draw from that
distribution is then taken and defined to be the outcome. Next, we seek
an alternative, imperfect forecast from the candidate set. Here, we apply a
condition on the similarity of the candidate forecasts with the perfect fore-


                                      20

## Page 21: cast. Let the perfect forecast be defined by {ph , pd , pa } where ph , pd and p

源页：第 21 页

cast. Let the perfect forecast be defined by {ph , pd , pa } where ph , pd and pa
represents the forecast probability of a home win, draw and away win respec-
tively. For each forecast in the candidate set, define the ‘distance’ from the
true probability distribution to be
                      1
                    = (|p̃h − ph | + |p̃d − pd | + |p̃a − pa |).            (4)
                      3
We define some threshold value δ, find all forecasts for which  is less than
δ (excluding the perfect forecast itself) and randomly draw the imperfect
forecast from that set. This process is repeated n times such that there are
a total of n pairs of forecasts. We define the ‘perfect forecasting system’
to be the system that always issues the perfect forecast from the pair and
the ‘imperfect forecasting system’ to be such that the alternative, imperfect
forecast is always issued. The experiment is repeated for multiple values of
n and different levels of the parameter δ, which governs the imperfection.

7.1    Results
The effect of different levels of imperfection, governed by the selected value
of δ, is demonstrated in figure 5. Each blue dot represents a perfect forecast,
with the x and y axes representing the probability of a home win and a
draw respectively. The grey line links each of these with the corresponding
imperfect forecast. Increasing the value of δ tends to result in more distinct
pairs of forecasts and therefore a higher level of imperfection.
    The proportion of forecast pairs in which the perfect forecasting system
is selected over the imperfect forecasting system is shown for each score and
value of δ as a function of log2 (n) in figure 6. The red, blue and green lines
represent this proportion for the Brier score, Ignorance score and RPS respec-
tively for the stated value of δ. For higher levels of imperfection, that is when
δ is high, there does not appear to be much difference in the performance
of the scoring rules. However, for the lowest level of imperfection, in which
δ = 0.1, there appears to be a notable difference with the RPS outperformed
by both the ignorance and Brier scores. From this graph alone, however, it
is not clear whether these differences are statistically significant. Given that
each of the scores are calculated on the same sets of forecast pairs, the scoring
rules can be compared pairwise with a total of three different comparisons
(ignorance vs RPS, ignorance vs Brier and RPS vs Brier). These differences
are shown as a function of log2 (n) in figure 7, with each panel representing a

                                        21

## Page 22: different value of δ. The error bars represent 95 percent resampling intervals

源页：第 22 页

different value of δ. The error bars represent 95 percent resampling intervals
of the mean difference and hence, if the intervals do not contain zero, there
is a significant difference in the performance of that pair of scoring rules.
    For the two lowest levels of imperfection (δ = 0.01 and δ = 0.025), there
is a clear hierarchy in terms of the efficacy of each score in identifying the
perfect forecasting system. The ignorance score tends to outperform the
Brier score which tends to outperform the RPS. This difference is most stark
for larger values of n. For the two larger levels of imperfection (δ = 0.05 and
δ = 0.1), the difference is less clear and, in general, there is no significant
difference between the Brier score and the RPS. The ignorance score, on
the other hand, still tends to perform significantly better than both other
scores. These results therefore provide clear support for the ignorance score
and little support for the RPS.




Figure 5: Examples of forecast pairs for different levels of imperfection. The
probability placed on a home win and a draw is represented by the x and y
axes respectively. The grey lines join pairs of forecasts for the purpose of the
experiment.


                                      22

## Page 23: Figure 6: The proportion of cases in which the perfect forecasting system

源页：第 23 页

Figure 6: The proportion of cases in which the perfect forecasting system
is selected by each scoring rule system as a function of log2 (n) for different
values of δ.

8    Discussion
The aim of this paper is to reopen the debate surrounding the use of scor-
ing rules for evaluating the performance of probabilistic forecasts of football
matches. The reasoning presented by Constantinou and Fenton supporting
the use of the RPS over other scoring rules has been shown to be oversim-
plistic and the conclusion questionable. With this in mind, two experiments
have been conducted with the aim of assessing the performance of each scor-
ing rule in the context of identifying a perfect forecasting system using a
finite number of past forecasts and outcomes. The ignorance score has been
found to outperform both the RPS and the Brier scores whilst, to a lesser
extent, the Brier score has been shown to perform better than the RPS in
this context.
    The results in this paper may seem surprising at first. After all, both
the Brier score and the RPS are non-local and take into account the entire

                                      23

## Page 24: Figure 7: Pairwise differences in the proportion of cases in which the perfect

源页：第 24 页

Figure 7: Pairwise differences in the proportion of cases in which the perfect
forecasting system is selected between the ignorance and RPS (blue), igno-
rance and Brier score (red) and Brier score and RPS (yellow) as a function
of log2 (n) with 95 percent resampling intervals of the mean.

forecast distribution rather than just the probability at the outcome whilst
the RPS is sensitive to distance and therefore also takes into account the
ordering of the potential outcomes. It would be easy to conclude from this
that, since both scores take more of the distribution into account, they are
more informative. However, it should be stressed that this would only be
the case if those extra aspects are genuinely useful in terms of assessing the
performance of the forecasts. In practice, we only ever gain limited knowledge
regarding the true distribution, even once the outcome is revealed. If, for
example, the outcome is a home win, this tells us little or nothing about
the probability of a draw or an away win. In fact, knowing the outcome
reveals relatively little about its probability, other than it is greater than zero.
Given this, we argue that the probability placed on potential outcomes that
didn’t happen are irrelevant. We know nothing about the true probabilities


                                        24

## Page 25: and therefore cannot reward probability placed on such outcomes. On the

源页：第 25 页

and therefore cannot reward probability placed on such outcomes. On the
other hand, we know that the actual outcome occurred. Moreover, the more
likely that event was deemed by the forecast, the better prepared we could
have been for the occurrence of that outcome. We therefore argue that
the probability placed on the outcome can be the only aspect of interest in
evaluating probabilistic forecasts. Given that the ignorance score is the only
proper and local score (Bröcker and Smith [2007]), this leads to it being a
natural preference.
    In summary, this paper has both argued for and provided empirical evi-
dence in favour of the ignorance score over both the Brier score and RPS. It
should be noted, however, that this paper has only touched upon the ques-
tion of which types of imperfect forecasts are favoured by different scores.
Useful future work would be to attempt to understand better where different
scoring rules favour different types of forecasts. A preference for the types of
forecasts favoured by the Brier score or RPS would then need to be weighed
up against the unfavourable results demonstrated in this paper. Regardless,
we hope that the arguments and results in this paper are successful in reopen-
ing the debate surrounding the choice of scoring rule for evaluating forecasts
of football matches. From the evidence presented in this paper, we strongly
recommend the ignorance score for this purpose.




                                      25

## Page 26: Experiment two makes use of bookmakers’ odds on actual football matches

源页：第 26 页

A      Data
Experiment two makes use of bookmakers’ odds on actual football matches
to form probabilistic forecasts. These odds are taken from the data set avail-
able at www.football-data.co.uk which supplies free-to-access match-by-
match data on 22 European Leagues dating back as far back as the 1993/1994
season. Here, data from the top five English leagues are used and are sum-
marised in table 3.
    League                      First available season Number of matches
    English Premier League            2005/2006             6460
    English Championship              2005/2006             6624
    English League One                2005/2006             6624
    English League Two                2005/2006             6624
    English National League           2005/2006             6488

             Table 3: Football league data used in this paper.




B      Match probabilities from odds
Let Oh , Od and Oa be the decimal odds on a home win, draw and away
win respectively for a given match. The multiplicative inverse of the odds on
each outcome represents the ‘implied’ probability. However, due to the profit
margin of the bookmakers, the implied probabilities will generally sum to a
value greater than one. To remove the profit margin, the implied probabilities
are divided through by their sum and therefore a probabilistic forecast is
formed by
                                     1/Oh
                         ph =                    ,
                              1/Oh + 1/Od + 1/Oa
                                     1/Od
                         pd =                    ,                        (5)
                              1/Oh + 1/Od + 1/Oa
                                     1/Oa
                         pa =                    .
                              1/Oh + 1/Od + 1/Oa
Forecasts are formed using the maximum odds (over all bookmakers given)
in each case.

                                      26

## Page 27: References

源页：第 27 页

References
Baboota, R., and H. Kaur, Predictive analysis and modelling football results
  using machine learning approach for english premier league, International
  Journal of Forecasting, 35 (2), 741–755, 2019.

Bernardo, J. M., Expected information as expected utility, the Annals of
  Statistics, pp. 686–690, 1979.

Brier, G. W., Verification of forecasts expressed in terms of probability,
  Monthly weather review, 78 (1), 1–3, 1950.

Bröcker, J., and L. A. Smith, Scoring probabilistic forecasts: The importance
  of being proper, Weather and Forecasting, 22 (2), 382–388, 2007.

Constantinou, A. C., and N. E. Fenton, Solving the problem of inadequate
  scoring rules for assessing probabilistic football forecast models, Journal
  of Quantitative Analysis in Sports, 8 (1), 2012.

Diniz, M. A., R. Izbicki, D. Lopes, and L. E. Salasar, Comparing probabilistic
  predictive models applied to football, Journal of the Operational Research
  Society, 70 (5), 770–782, 2019.

Epstein, E. S., A scoring system for probability forecasts of ranked categories,
  Journal of Applied Meteorology, 8 (6), 985–987, 1969.

Forrest, D., J. Goddard, and R. Simmons, Odds-setters as forecasters: The
  case of english football, International journal of forecasting, 21 (3), 551–
  564, 2005.

Friedman, D., Effective scoring rules for probabilistic forecasts, Management
  Science, 29 (4), 447–454, 1983.

Gneiting, T., and A. E. Raftery, Strictly proper scoring rules, prediction,
 and estimation, Journal of the American Statistical Association, 102 (477),
 359–378, 2007.

Good, I. J., Rational decisions, in Breakthroughs in statistics, pp. 365–377,
 Springer, 1992.




                                      27

## Page 28: Jose, V. R. R., R. F. Nau, and R. L. Winkler, Sensitivity to distance and

源页：第 28 页

Jose, V. R. R., R. F. Nau, and R. L. Winkler, Sensitivity to distance and
  baseline distributions in forecast evaluation, Management Science, 55 (4),
  582–590, 2009.

Judd, K., and L. A. Smith, Indistinguishable states i: The perfect model
  scenario, Physica D: nonlinear phenomena, 151 (2-4), 125–141, 2001.

Judd, K., and L. A. Smith, Indistinguishable states ii: The imperfect model
  scenario, Physica D: nonlinear phenomena, 196 (3-4), 224–242, 2004.

Koopman, S. J., and R. Lit, Forecasting football match results in national
 league competitions using score-driven time series models, International
 Journal of Forecasting, 35 (2), 797–809, 2019.

Maynard, T., Extreme insurance and the dynamics of risk, Ph.D. thesis,
 London School of Economics and Political Science, 2016.

Murphy, A. H., The ranked probability score and the probability score: A
 comparison, weather, 81, 82, 1970.

Parry, M., A. P. Dawid, S. Lauritzen, et al., Proper local scoring rules, The
  Annals of Statistics, 40 (1), 561–592, 2012.

Roulston, M. S., and L. A. Smith, Evaluating probabilistic forecasts using
  information theory, Monthly Weather Review, 130 (6), 1653–1660, 2002.

Schauberger, G., A. Groll, and G. Tutz, Modeling football results in the
  german bundesliga using match-specific covariates, 2016.

Schmidt, C., M. Strobel, and H. O. Volkland, Accuracy, certainty and sur-
  prise: a prediction market on the outcome of the 2002 fifa world cup, 2008.

Selten, R., Axiomatic characterization of the quadratic scoring rule, Experi-
  mental Economics, 1 (1), 43–61, 1998.

Spiegelhalter, D., and Y.-L. Ng, One match to go!, Significance, 6 (4), 151–
  153, 2009.

Staël von Holstein, C.-A. S., A family of strictly proper scoring rules which
  are sensitive to distance, Journal of Applied Meteorology, 9 (3), 360–364,
  1970.


                                     28

## Page 29: Wheatcroft, E., Interpreting the skill score form of forecast performance met-

源页：第 29 页

Wheatcroft, E., Interpreting the skill score form of forecast performance met-
 rics, International Journal of Forecasting, 35 (2), 573–579, 2019.




                                     29
