# Response to Reviewers

We thank

## Reviewer 1

### Overall comments

I enjoyed reading this paper, which confirms that uncertainty dominates when predicting climate change over an extended lead time.

The analysis is carried out through a series of synthetic experiments.
It is interesting to see what are the limits of predictability in the presence of natural variability and secular change.

I think this paper is timely in that it confirms that particular care should be taken when making long term predictions in the presence of a changing climate.
As the analysis clearly shows, it is not easy to recognize climate signals.
Natural variability may interact with climate change therefore masking inherent behaviours.

I think the paper is well written and organized. I made some comments in the attached pdf file.
My comments are essentially minor.

I would like to point out that I missed in the paper a discussion on the Hurst effect.
There is an extended literature on it. Such effect implies the presence of low frequency variability (long term cycles) which were observed in several secular time series of environmental variables.
The Hurst effect may be difficult to distinguish from anthropogenic climate change (ACC).
This effect is ignored by several climate studies. I believe this paper would be a good opportunity to discuss the interaction of the Hurst effect with ACC.
To this end, a proper discussion should be included in the manuscript.

I would like to congratulate the authors for their interesting work.

Best regards,
Alberto Montanari

### Line comments

7: It is not clear to me what this key point means

> We have updated this key point following suggestions from reviewer 2

10: I believe these key points are not much informative. I am not sure of my opinion, but my feeling it that they should reformulated to better explain what the paper discovered.

> Working on it!

34: What do you mean exactly? I don't think mitigation efforts proved to be successful.

> We (unfortunately!) agree that mitigation efforts have not yet proven successful. We have re-phrased this sentence. It now reads "Even if future mitigation efforts are successful, existing levels of atmospheric CO2 and ocean heat content mean that novel adaptation strategies are needed."

84: I believe the impact of ACC on floods and drought is far from being well documented. It is not yet clear whether droughts like the Millenium Drought and the Californian drought have been caused by ACC. California is subjected to drought since the XIX century. Please see  https://en.wikipedia.org/wiki/Droughts_in_California and references therein.

> We agree with the reviewer that the influence of ACC on hydrological extremes is unclear and complex. We have re-worded this sentence to be more clear about this point.  It now reads "Of these processes, ACC has received the most attention in the climate adaptation literature and its influence on some river floods, droughts, hurricanes, urban flooding, and many other climate hazards has been the subject of substantial investigation..."

87: I fully agree with this sentence.

> Thank you very much

103: LFV is strictly related to the Hurst effect. There is an extended literature. I think a mention to the Hurst effect would be appropriate here.

> We have added a short paragraph here which seeks to join some disparate literatures on paleoclimate, Hurst effects, and ocean-atmosphere dynamics. These all explain similar phenomena but use different perspectives.

115: I am not sure it is appropriate to make mention to a hypothetically perfect climate model. It should be made clear that this is a VERY ideal assumption. Perfect environmental models do not exist and, as hydrologists, we should be clear on that. 

> We strongly agree with this assessment. In a presentation of this paper at the 2018 AGU Fall Meeting we referred to opening a bottle on a beach and using one of three wishes granted by a magical genie on a climate model to emphasize the ridiculousness of having a perfect model. In this slightly more formal setting we have re-worded the sentence to "Even in the idealized, and unrealistic, case of a perfect climate model, these uncertainties will be large."

118: This is why I believe we should not make reference to perfect models.

> See previous comment

231: I believe these details on the software should not be given here, in the body of the paper. These may be part of the user guide of the produced software

> We are deferring here to the editor. However, I feel that as a consumer of open source software I have an ethical responsibility to cite the primary packages that I use. Further, as a scientist committed to reproducibility I believe that describing software used is as important as describing the experiment design. However, making code accessible on GitHub partially alleviates this concern.

## Reviewer 2

### Overall comments

The authors have teased apart climatic risks that are considered for planning purposes across multiple time horizons.
It is an interesting exploration the interaction of various types of climatic variability, planning horizons, and length of time series, and how this interaction impacts the choice of instruments of climate risk mitigation.
As this paper uses the word robust in the title, the introduction needs to link the concept of robustness to their questions and methods.
Suggest citing literature on robust adaptation if you keep ‘robust’ in the title.

> See Line 39 (verify)

In Sections 2.1 and 2.2 you describe the three models of climatic change, and three ways of modeling each climate model.
Is there a way to clarify the structure of your computational experiment in these two sections, including your intent of using multiple methods of generating these types of climate variability?

> **QUESTION**: I think we just need to modify the beginning of the results section. Is there anything we can make clearer?

Please explicitly link the lognormal model with the LN2 acronym in text before using in figures.

> We have done this in section 2.2

It would be interesting to see whether there is a relationship in the results between bias and variance; e.g. can the variance inform or predict the bias in each of the three types of climate variability?

> This is certainly an interesting question. However, the precise structure of bias and variance as a function of $N$ and $M$ depends strongly on the specific model used to create nonstationarity and to estimate future climate risk. As such, we cannot expect that any answer we obtain to this question would generalize beyond the specific assumptions of our stylized computational experiment. For this reason we have determined not to address this question in this work.

The discussion needs to reference the computational results, at minimum to justify the computational experiment as opposed to solely a conceptual exploration.

> We have added some modifications to the discussion to reference our computational results more directly and clearly.

### Key points

To me, planning implies a process rather than the expected lifespan of a project.
Can you clarify which meaning you use?
If the latter, perhaps the following would be more readable: Climate risk varies over the planned lifespan of a project.
This can also be clarified in other locations of the paper, e.g. line 364 in the summary.

### Line comments

15-16: Can you restate phrase copied below, unclear terms in bold:
**the role of low-frequency variability in modulating climate extremes**

> We agree and have re-phrased this sentence. It now reads "... historical and paleo climate records emphasize interannual to multidecadal modes of variability"

23: The discount rate is given as a decision factor but this is not modeled in the paper. I suggest relegating mention of a discount rate to the introduction or discussion.

> We have removed the distracting mention of a discount rate

24: Suggest because instead of where.

> Our point here is that if variability can be identified and predicted -- which is not a given -- shorter design lives are preferred. The sentence now reads "Shorter design lives are preferred for situations where inter-annual to decadal variability can be successfully identified and predicted..."

38-39: Is this formatting of reference correct?

> Per the document "Brief Guide to AGU Style and Grammar" document available at https://publications.agu.org/brief-guide-agu-style-grammar/, "AGU’s latex template and APA style in reference management software do not include this exception. You do not need to update your manuscript with this exception; it will be applied by the production vendor during the copy-editing process."

41: perhaps a good place to insert a definition and example of operational and financial instruments? An example is given for a structural instrument and that is what people are most likely to understand already.

> This is a helpful suggestion. The sentence now reads "Rather, actors such as New York city have turned to a combination of structural (e.g., index insurance), operational (e.g., improved evacuation routes), and financial (eg, index insurance) investments for reducing vulnerability and increasing resilience to climate extremes." We note that all of these examples are contained in the City of New York report referenced. We believe that these examples are sufficient since a strict definition of different classes of instruments would substantially disrupt the structure of the paragraph.

50-51: Phrasing could be reworked; at minimum change this to these at the end of the sentence.

> The sentence now reads "In this paper we focus on the more narrow question of how the temporal structure of climate risk, and the uncertainties associated with its estimation, influence the answers to these questions."

53: comma after implications

> Added

67: perhaps a good place to define length of long-term short. Is this the interannual to multidecadal described in the abstract or the one-year term of a financial contract (line 59)?

> This is an important question, as we are certainly a bit vague here. The points are clearest in the limits of prediction at time scales less than one year or greater than a century; most real-world centuries are in between. To add some clarity, we have added another sentence with an example. This sentence reads "For example, the action that New York City can take today which best protects against uncertain hurricane risks over the 21st century could potentially be to purchase insurance and defer more permanent allocation of capital until some uncertainties are resolved." We hope that our wording does not imply that we have performed any analysis for New York City.

90-91: Phrasing is a bit obtuse.

> This sentence now reads "Secular change is not the only mechanism which can cause historical records to provide a biased view of future risk."

122: portend (singular)

> Fixed

Figure 1: Inconsistent capitalization. Can you add units?

> Working on this, but going to follow up RE units of American River

147: Recommend preserving the order you present the climate scenarios throughout the paper.

> This is reasonable. We order them (i) secular change only; (ii) LFV only; (iii) LFV plus secular change. This also mirrors the results.

185: Is the word ‘consider’ necessary in these paragraphs?

> We have changed two sentences. The first now reads "In the first case we fit a stationary model to the observed flood record, following...". The second now reads "Finally, we explicitly model LFV using a hidden Markov model (HMM)."

198: be consistent with use of acronyms (i.e. just say LFV).

> Sentence changed; see previous comment

205: suggest “log-normal distribution that is conditional only on the unobserved state
variables” (or S(t) instead of state).

> Thank you for the helpful suggestion

215 and 217: Can you say ‘that’ instead of ‘designed based on’? If these words are meaningful, can you elaborate?

> We agree that the wording was vague. The sentence now reads "An instrument whose design was based on projections with overestimated variance or positive bias will be..."

219: suggest “M, N, and

> This is helpful