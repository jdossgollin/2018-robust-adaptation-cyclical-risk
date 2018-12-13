# Slides for AGU Talk

## Title

Good morning everyone.
My name is James Doss-Gollin and I'm a Ph.D. candidate in Earth and Environmental Engineering at Columbia.
Before I get started I'd like to thank my co-authors: David Farnham, Scott Steinschneider, and Upmanu Lall, and also the NSF and Columbia University for funding my work.

## Motivating Example

I'm going to start by thinking about a decision that New York City faced in the aftermath of Hurricane Sandy, but really I could just as easily apply to Phoenix, or Sonoma County, or Bangladesh.
Since hurricanes will return, and since the sea level is rising, how should the City manage future flood damages?
On the one hand, large structures -- like a sea wall to block storm surges shown in the top left -- provide unmatched protection against some types of risk.
However, this project would lock in funds and be difficult to modify should future climatic or societal conditions change unexpectedly.
Alternatively, a portfolio of smaller projects may be more robust, and is certainly more flexible and adaptive.
These measures might be smaller structures, financial instruments, or policy and operational shifts.

With this in mind, I'm going to ask about how we ought to build a portfolio of small projects, how to maintain adaptability, and what, if any, is the trigger trigger which might tell us when we need to invest in a permanent structural solution.

## Hypotheses

These are deep questions which I won't fully answer.
My approach today will be to lay out a few interesting hypotheses about the world, which might seem obvious, but which are also under-appreciated.
Then, I'll show you some stylized experiments which probe some implications of these hypotheses.

## Idea 1

When evaluating an investment in water or climate risk management, we typically perform cost-benefit analysis (or some variant thereof).
Explicitly or implicitly, this means that we assess the net benefits of a project over a *finite* planning period.

This means that when we incorporate climate into our analysis, we need to consider climate conditions over this finite period, rather than infinitely into the future.
For our giant sea wall this might be a planning period of 50 to 100 years.
Alternatively, an insurance contract might have a planning period of only one to five years.

## Idea 2

This becomes important when we see that real-world hydroclimate systems vary on many timescales.
This top row of this figure shows the American River at Folsom, California, and a paleo drought reconstruction over Arizona.
The second row shows their respective wavelet spectra; you can see significant peaks well above 10 years for both data sets.
The point I want to make is not the specific data sets or time series, but just to remind ourselves that pronounced inter-annual to multi-decadal variability can dominate risk profiles over the next several decades.

## Idea 3

In the climate and hydrology spaces we often consider this a background noise, but it can be useful!
Given a magically perfect climate model, we might be able to model this inter-annual to decadal variability quite successfully.
However, as we look far into the future, our uncertainties grow.
We're familiar with chaos in the climate, but there are more intrinsic uncertainties: does Elon Musk quit Twitter and solve our fossil fuel dependency, or do we burn all the rainforests and coal?
Our magic climate model can't answer these questions, and so the uncertainty associated with our investment grows as we look further into the future.

Of course, we're scientists, and so we don't want to depend on magic.
Instead, we use imperfect  models, and we have limited information to fit them.
This limits our ability to identify and predict different climate signals.

## Stylized Experiments

These points may seem obvious, but they have some interesting implications.

## Research Objective

Essentially, I want to show you how well it's possible to identify and predict water or climate risk, which has both cyclical and trend-like signals, over a finite planning period, given limited information.
To measure our ability to identify and predict these signals, I'm going to show you the expected bias and variance of estimated flood occurrence.
As this risk premium equation highlights, both the bias and the variance of our risk estimate map onto the insurance premium that we would pay; if we're instead considering a structural solution, this insurance premium can be interpreted as a risk factor which would affect our over- or under-design.

This figure on the left here shows how we do this.
First, we generate a synthetic streamflow sequence, as shown in blue.
Next, we fit the first $N$ years to a statistical model, use this model to project $M$ years forward, as shown in gray.
By repeating this many times, we can evaluate the expected bias and variance of our estimates.
Using this framework, we explore what happens as we vary the planning period, the informational record, and the structure of the climate signal.
We also look at what happens as we move from simple, parsimonious models for risk estimation to complex models with more parameters and thus greater uncertainty.

## Stationary Scenario

In this first scenario, there is no trend -- our synthetic streamflow sequences depend only on a model for ENSO.
On the top row we show the bias and on the second row the variance of our flood occurrence probabilities.
The three columns show the three toy models we use to estimate risk: a hidden markov model, a linear trend model, and a stationary log-normal model.
I want to highlight that I chose these models for their interpretability, not because I recommend them, but results are similar with more complex models.
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

To wrap up here, we started with a few observations, or really assertions, about the world.

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