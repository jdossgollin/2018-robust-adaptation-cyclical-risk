# Slides for AGU Talk

## Title

Good morning everyone.
My name is James Doss-Gollin and I'm a Ph.D. candidate in Earth and Environmental Engineering at Columbia.
Before I get started I'd like to thank my co-authors: David Farnham, Scott Steinschneider, and Upmanu Lall, and also the NSF and Columbia University for funding my work.

## Motivating Example

The example here depicts a decision that New York City faced in the aftermath of Hurricane Sandy, but this question could just as easily apply to Phoenix, or Sonoma County, or Bangladesh.
Decision-makers often have tradeoffs between a large, permanent structure and a sequence -- or portfolio -- of smaller, local projects.
On the one hand, large structures -- like a sea wall to block storm surges -- provide unmatched protection against some types of risk.
However, they lock in funds and are difficult to modify should requirements change.
On the other hand, a portfolio of smaller projects may be more robust, and is certainly more flexible and adaptive.

With this in mind, the questions that I hope to work towards today involve scheduling, sequencing, and portfolio optimization.
In other words, how should we build a portfolio of small projects, and what is the trigger which might tell us when we need to invest in a permanent structural solution?

## Table of Contents

These are deep questions.
My approach today will be to lay out three interesting hypotheses about the world, which might seem obvious, but which are under-appreciated.
I'll then show you some stylized experiments which probe the implications of these hypotheses, and which I think are of interest if you're wrestling with these deep questions.

## Hypotheses

So let's jump in.

## Idea 1

When evaluating an investment in water or climate risk management, we typically perform cost-benefit analysis (or some variant thereof).
Explicitly or implicitly, this means that we assess the net benefits of a project over a *finite* planning period, which I'll denote by the letter $M$.

This means that when we incorporate climate into our analysis, we need to consider climate conditions over this finite period, rather than infinitely into the future.
For our giant sea wall this might be a planning period of 50 to 100 years.
Alternatively, an insurance contract might have a planning period of only one to five years.

## Idea 2

This becomes important when we see that real-world hydroclimate systems vary on many timescales.
This top row of this figure shows the American River at Folsom, California, and a paleo drought reconstruction over Arizona.
The second row shows their respective wavelet spectra; you can see significant peaks well above 10 years for both data sets.
The point I want to make is not the specific data sets or time series, but just to remind ourselves that pronounced inter-annual to multi-decadal variability can dominate risk profiles over the next several decades.

## Idea 3

Though we've often considered this background noise, it may be useful!
Imagine we go for a walk tomorrow along the coast, find a bottle, open it, and out pops a genie.
We're AGU members, so with our first wish, we of course ask for a perfect climate model, and with our second we ask for a magical earth monitoring system to initialize our model.
In the near term we might be able to model this inter-annual to decadal variability fairly well.
However, as we look far into the future we have more intrinsic uncertainties: does Elon Musk quit Twitter and solve our fossil fuel dependency, or do we burn all the rainforests and coal?
Our magic climate model can't answer these questions, and so the uncertainty associated with our investment grows as we look further into the future.

Of course, we're scientists, and so we don't believe in genies.
Instead, we use imperfect, non-magical, models that we have made, and we have limited information to fit them.
This limits our ability to identify and predict different climate signals.

## Stylized Experiments

These points may seem obvious, but they have some interesting implications.

## Research Objective

Essentially, I want to show you how well it's possible to identify and predict water or climate risk, which has both cyclical and trend-like signals, over a finite planning period, given limited information.

I'm going to do this by generating synthetic streamflow sequences for three different idealized climate scenarios.
Then I fit the first $N$ years to a statistical model, and use this model to project $M$ years forward.
Then, repeating this many times, I evaluate the bias and variance of this statistical fit.
As this risk premium equation highlights, both the bias and the variance of our risk estimate map onto the insurance premium that we would pay.
If we're instead considering a structural solution, this insurance premium can be interpreted as a risk factor which would affect our over- or under-design.

In these experiments, I'll consider three scenarios for what the underlying climate signal might be.
In each, I look at what happens as we vary our planning period and our informational uncertainty.
I'll also consider changes as we move from simple, parsimonious models for risk estimation to more complex ones which represent more processes but also have more parameters and therefore more uncertainty.

## Stationary Scenario

In this first scenario, there is no trend -- our synthetic streamflow sequences depend only on a model for ENSO.
On the top row we show the bias and on the second row the variance of our flood occurrence probabilities.
The three columns show the three toy models we use to estimate risk: a hidden markov model, a linear trend model, and a stationary log-normal model.
I chose these models for their interpretability, not because I recommend them, but results are similar with more complex models.
Within each plot, the $x$-axis shows $N$ and the $y$-axis shows the planning period $M$.
In this figure, the largest bias occurs when we fit the most complex model -- the trend model.
Even though no trend exists, when $N$ is short (left) we can't be sure.
Identifiability is low.
As we extrapolate far into the future -- large $M$ (top) -- the possibility of estimating a positive trend causes us to dramatically over-estimate the probability of flooding, hence the positive bias.

## Nonstationary Scenario I

Now let's repeat the experiment, but under a different scenario.
Where before we had dependence on ENSO, here there is none -- there is just a trend, plus noise.
Now we see that when we look far into the future -- large $M$ -- the stationary models, which don't account for the trend, dramatically under-estimate our risk.
However, when $N$ is short, meaning we don't have much data, fitting the trend still causes us to sometimes over-estimate its magnitude, again leading to biased estimates of risk.
Consequently, if both $N$ and $M$ are short it might be preferable to use a simpler model which has less informational uncertainty.

## Nonstationary Scenario II

Finally, I've added the two processes together -- we have both ENSO and a trend, plus noise.
The conclusions are, in general, similar to the trend case, but note that our variance has gone up.
In other words, as our system becomes more complex, we need more data to identify different signals.

## Discussion

OK, so I hope that was interesting.

## Summary

To wrap up here, we started with a few observations, or assertions, about the world.

By running some stylized experiments, we probed their implications.

First, our ability to identify different climate signals depends on the information available to us.
In order to identify complex signals, like those observed in the real world, we may need complex models.
However, feeding limited data sets into complex models can lead to large biases and uncertainties, and if we're being honest with ourselves, we recognize that these are only partially represented by ensemble and scenario techniques.

The types of signals that we care about may vary.
If we're looking at a project with a short planning period, we don't need to model all relevant processes, and so we both *can* and *should* use simpler models which have lower uncertainties.
On the other hand, if we are evaluating a project with a long planning period, then complex models -- with greater uncertainties -- may be required.

This informs our choice of strategy.
Though the details will be project-specific, we can say that in general, limited data sets and low risk tolerance favor short-term investments relative to those with long planning periods.

## References

These are some references, I'm just going to flash these quickly

## The End

I'll end by saying that this work has been a bit conceptual, but I'm working on techniques for identifying, predicting, and managing risk.
If that sounds interesting, I'd love to discuss further.
Here's my contact information; I'll post these slides on my page as well.
Thanks for your attention, and if I'm not too far over my time I'd be happy to take any questions.