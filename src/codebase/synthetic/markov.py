"""Generate sequences from a two-state Markov chain
"""

import numpy as np
import pomegranate as pm

from .synthetic import SyntheticFloodSequence

class MarkovTwoStateChain(SyntheticFloodSequence):
    """Generate a two-state Markov chain
    """

    def __init__(self, **kwargs) -> None:
        model_param = {
            'pi_1': kwargs.pop('pi_1'),
            'pi_2': kwargs.pop('pi_2'),
            'mu_1': kwargs.pop('mu_1'),
            'mu_2': kwargs.pop('mu_2'),
            'gamma_1': kwargs.pop('gamma_1'),
            'gamma_2': kwargs.pop('gamma_2'),
            'coeff_var': kwargs.pop('coeff_var'),
            'sigma_min': kwargs.pop('sigma_min')
        }
        super().__init__(**kwargs)
        self.param.update(model_param)
        self.model_name = 'Two-State Markov Chain'

    def _calculate_one(self) -> np.ndarray:
        """Run the calculation
        """

        # Get the sequence of states
        dist_1 = pm.DiscreteDistribution({'wet': 0.5, 'dry': 0.5}) # random starting point
        dist_2 = pm.ConditionalProbabilityTable(
            [['wet', 'wet', self.param['pi_1']],
             ['wet', 'dry', 1 - self.param['pi_1']],
             ['dry', 'wet', 1 - self.param['pi_2']],
             ['dry', 'dry', self.param['pi_2']]], [dist_1]
        )
        markov_chain = pm.MarkovChain([dist_1, dist_2])
        years = self._get_time('all')
        states = markov_chain.sample(years.size)

        # Get the conditional expected value
        mu_1_vec = self.param['mu_1'] + self.param['gamma_1'] * years
        mu_2_vec = self.param['mu_2'] + self.param['gamma_2'] * years
        mu_vec = mu_1_vec
        mu_vec[np.where(np.array(states) == 'wet')] = mu_2_vec[np.where(np.array(states) == 'wet')]

        # get conditional variance
        sigma_vec = self.param['coeff_var'] * mu_vec
        sigma_vec[sigma_vec < self.param['sigma_min']] = self.param['sigma_min']

        # get and the streamflow
        sflow = np.exp(np.random.normal(loc=mu_vec, scale=sigma_vec))
        return sflow
