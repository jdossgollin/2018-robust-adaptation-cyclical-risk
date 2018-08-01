"""A Hidden Markov Model implemented in Pomegranate
"""

import pomegranate as pm
import numpy as np

from . import StatisticalModel

class TwoStateHMM(StatisticalModel):
    """A Hidden Markov Model implemented in pomegranate
    """
    def __init__(self, **kwargs) -> None:
        model_param: dict = {
            'pseudocount': kwargs.pop('pseudocount', 10),
            'n_init': kwargs.pop('n_init', 25)
        }
        super().__init__(**kwargs)
        self.param.update(model_param)
        self.model_name = 'Hidden Markov Model'

    def _calculate_one(self, data) -> np.ndarray:
        """Simulate a single sequence of annual maximum flood peaks using LN2
        """
        data = np.log(data)[:, np.newaxis] # need to reshape it for pomegranate
        samples = np.nan * np.ones(shape=(self.param.get('n_mcsim'), self.M))
        model = pm.HiddenMarkovModel.from_samples(
            pm.NormalDistribution,
            n_components=2,
            X=data,
            pseudocount=self.param.get('pseudocount'),
            n_init=self.param.get('n_init'),
        )
        for j in np.arange(self.param.get('n_mcsim')):
            samples[j, :] = np.exp(np.array(model.sample(length=self.M)))

        return samples
