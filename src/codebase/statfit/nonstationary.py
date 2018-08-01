"""Nonstationary (linear trend) flood frequency analysis stan
"""

import os
import numpy as np

from . import StatisticalModel
from ..path import data_path
from ..util import compile_model

class LN2LinearTrend(StatisticalModel):
    """Lognormal Model with linear trend and constant CV
    """
    def __init__(self, **kwargs) -> None:
        self.model_file = os.path.abspath(os.path.join(data_path, 'ln2-trend.stan'))
        model_param: dict = {
            'mu0_mean': kwargs.pop('mu0_mean', 10),
            'mu0_sd': kwargs.pop('mu0_sd', 1),
            'beta_mu_mean': kwargs.pop('beta_mu_mean', 0),
            'beta_mu_sd': kwargs.pop('beta_mu_sd', 0.5),
            'cv_logmean': kwargs.pop('cv_logmean', np.log(0.1)),
            'cv_logsd': kwargs.pop('cv_logsd', 0.5),
            'n_warmup': kwargs.pop('n_warmup', 1000),
            'n_chain': kwargs.pop('n_chain', 1),
        }
        super().__init__(**kwargs)
        self.param.update(model_param)
        self.model_name = 'LN2 Linear Trend'

    def _calculate_one(self, data) -> np.ndarray:
        stan_data = {
            'y': data,
            'N': self.N,
            'M': self.M,
        }
        for param in ['mu0_mean', 'mu0_sd', 'beta_mu_mean', 'beta_mu_sd', 'cv_logmean', 'cv_logsd']:
            stan_data.update({'{}'.format(param): self.param.get(param)})
        stan_mod = compile_model(filename=self.model_file, model_name='LN2-Linear-Trend')
        n_iter: int = self.param.get('n_mcsim') + self.param.get('n_warmup')
        fit = stan_mod.sampling(
            data=stan_data, iter=n_iter,
            chains=self.param.get('n_chain'), warmup=self.param.get('n_warmup')
        )
        fit_dict = fit.extract(permuted=True)
        return fit_dict['yhat']
