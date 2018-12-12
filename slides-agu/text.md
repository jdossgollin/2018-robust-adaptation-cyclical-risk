# Slides

## Title

Good morning everyone.
My name is James Doss-Gollin and I'm a Ph.D. candidate in Earth and Environmental Engineering at Columbia.
Before I get started I'd like to thank my co-authors David Farnham, Scott Steinschneider, and Upmanu Lall, as well as the conveners of this session and you all for attending.

## Motivating Example

The example I put up here depicts New York's thought process in the aftermath of Hurricane Sandy, but this question could just as easily apply to Phoenix, or Sonoma County, or Bangladesh.
We're often faced with decisions between a large, permanent structure for managing water or climate risk, or implementing a sequence -- a portfolio -- of smaller, targeted, local projects.
On the one hand, large structures provide unmatched protection against some types of risk, but on the other hand a portfolio of smaller projects is likely to better meet goals of robustness and flexibility.

The question that I'm interested in is both one of scheduling, sequencing, and portfolio optimization.
How should we build a portfolio of small projects; what is the trigger which tells us to build a big project, and how can we balance robustness against performance in an economic framework?

## Table of Contents

I'm not going to perfectly answer these questions today.
Instead, I'm going to lay out three hypotheses about the world, specifically regarding the nature of water and climate risk, which I think are uncontroversial but under-appreciated.
I'll then show you some stylized experiments which probe the implications of these hypotheses, and finally I'll try to relate my experiments back to the real world.

## Hypotheses

So let's jump in.

## Idea 1

When evaluating an investment in water or climate risk management, we typically perform a cost-benefit analysis (or variant thereof).
Explicitly or implicitly, this means that we assess the net benefits of a project over a *finite* planning period, which I'll denote by the letter $M$.

This means that when we incorporate climate variability into our analysis, we need to consider climate conditions over this finite period, rather than infinitely into the future.
For our giant sea wall this might be a planning period of 50 to 100 years, while an insurance contract might have a planning period of only one to five years.

## Idea 2

This becomes relevant when we see that real-world hydroclimate systems vary on many time and space scales.
The left column here shows a \SI{100}{year} record of the American River at Folsom, California, and the right shows a paleo drought reconstruction of summer rainfall over Arizona.
The bottom column shows the global wavelet spectra for both time series.
The point here is not the specific data sets or time series, but just to remind ourselves that pronounced inter-annual to multi-decadal variability can dominate risk profiles in the near future.

## Idea 3

In the near term, this may impart some predictability.
Imagine we were walking along the river tomorrow, found a bottle, opened it, and out pops a genie.
We're AGU members, so with our first wish, we of course ask for a perfect climate model, and with our second we ask for a magical earth monitoring system to initialize our model.
In the near term we might be able to model this inter-annual to decadal variability fairly well.
However, as we look far into the future we have more intrinsic uncertainties: does Elon Musk quit Twitter tomorrow and magically solve our fossil fuel dependency, or do we burn all the rainforests and coal?
Our magic climate model can't answer these questions, and so the uncertainty associated with our mega-project is very large.

Of course, we're scientists, and so we don't believe in genies.
Instead, we use imperfect models that we have made, and we have limited information to fit them, which limits our ability to identify and predict cyclical and trend-like climate signals.

## Stylized Experiments

Now, taking these hypotheses as gospel, I'm going to conduct some stylized experiments to probe their implications.

## Research Objective

Essentially, I want to show you how well it's possible to identify and predict water or climate risk, which has both cyclical and trend-like signals, over a finite planning period, given limited information.

First, I'll look at what happens as we vary our planning period or our informational uncertainty.
My proxy for this will be a single $N$-year time series, but keep in mind that this applies to all the information that we might feed to a more complex model.

Next I'll look at what changes as we move from simple, parsimonious models to more complex ones which represent more processes but also have more parameters.

Finally I'll examine what happens when we change the form of the underlying climate signal.

I do this generating synthetic streamflow sequences.
The blue line shows just one example sequence; to the left is the first $N=50$ years and to the right the next $M=100$ years.
The gray bars indicate 50 and 95 percent confidence intervals for a statistical model which is fit on the first $N=50$ years and extrapolated over the following $M=100$ year period.
The quantity of interest is going to be flood *occurrence*, not *intensity*, so we look for bias and variance of the probability that we are above this black threshold line here, at each time step.
Interestingly, even if our statistical fit is unbiased in its estimates of flood magnitude, its large spread means that it may over-estimate the probability of flood occurrence.
This is just one sequence though, so now I'll show you what happens when we do this more systematically.

## Stationary Scenario

To do this systematic testing, we created different scenarios; in this scenario streamflow variability comes only from low-frequency variability, represented by a model for El Nino-Southern Oscillation, plus random noise.
There is no trend here.
On the top row we show the bias and on the second row the variance.
The three columns show the three example models we use to estimate risk: a hidden markov model, a linear trend model, and a stationary log-normal model.
Our results are similar with more complex and realistic models.
Within each plot, the $x$-axis shows $N$ and the y-axis shows the planning period $M$.
The results of each grid cell are computed by creating 1000 sequences, like the one shown on the previous slide, and taking expectations across all sequences.
On this plot, the largest bias occurs when we fit the most complex model -- the trend model.
Even though no trend exists, when $N$ is short we can't be sure.
As we extrapolate far into the future -- large $M$ -- the possibility of estimating a positive trend causes us to dramatically over-estimate the probability of flooding.

## Nonstationary Scenario I

Now let's repeat the experiment, but under a different scenario.
The results here are the same as for the previous slide, but now there's no variability from ENSO.
Instead, we just have a trend, plus noise.
Now we see that when we look far into the future -- large $M$ -- the models that don't account for the trend tend to seriously under-estimate our risk.
However, when $N$ is short, fitting the trend causes us to sometimes over-estimate its magnitude, leading to biased estimates of risk.
Consequently, if both $N$ and $M$ are short it might be preferable to use a simpler model which has less uncertainty.

## Nonstationary Scenario II

Now I've added the two processes together -- we have both ENSO and a trend, plus noise.
The conclusions are, in general, similar to the trend case, but note that our variance has gone up.
In other words, as our system becomes more complex, we need more data to identify different signals.

## Discussion

OK, so I hope that was interesting.

## Summary

To wrap up here, we started with the following assertions:
* that we need to evaluate investments, and their climate dependence, over a finite planning period;
* that physical hydroclimate systems vary on many scales; and
* that the physical processes which dominate our climate risk depend on the planning period $M$.

This has three key implications.

First, our ability to identify different climate signals depends on our informational uncertainty.
In order to identify complex signals, like those observed in the real world, we may need complex models, but feeding limited data sets into these can lead to large uncertainties, which are only partially represented by ensembles and scenarios.

But, this may matter more or less.
If we're looking at a project with a short planning period, we can focus on a sub-set of these processes.
On the other hand, if we are evaluating a project with a long planning period then, a greater degree of extrapolation -- and therefore uncertainty -- is therefore required.

Of course, explicit policy guidance depends on a decision-maker's risk preference.
But in general, limited data sets and low risk tolerance favor short-term investments relative to those with long planning periods.

## References

These are some references, I'm just going to flash these quickly

## The End

I'll end by saying that this work has been a bit conceptual, but I'm working on several ideas to make them more concrete.
If that sounds interesting, I'd love to discuss futher.
Here's my contact information; I'll post these slides on my page as well.
Thanks for your attention, and if I'm not too far over my time I'd be happy to take any questions.