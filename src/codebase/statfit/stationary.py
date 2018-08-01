import os

from . import StatisticalModel
from ..path import data_path
from ..util import compile_model

class LN2Stationary(StatisticalModel):
    def __init__(self, **kwargs) -> None:
        self.model_file = os.path.abspath(os.path.join(data_path, 'ln2-stationary.stan'))
        model_param: dict = {
            'mu_sd': kwargs.pop('mu_sd', 1),
            'mu_mean': kwargs.pop('mu_mean', 10),
            'sigma_mean': kwargs.pop('sigma_mean', 1),
            'sigma_sd': kwargs.pop('sigma_sd', 1),
            'n_warmup': kwargs.pop('n_warmup', 1000),
            'n_chain': kwargs.pop('n_chain', 1),
        }
        super().__init__(**kwargs)
        self.param.update(model_param)
        self.model_name = 'LN2 Stationary'

    def _calculate_one(self, data):
        stan_data = {
            'y': data,
            'N': self.N,
            'M': self.M,
            'mu_sd': self.param.get('mu_sd'),
            'mu_mean': self.param.get('mu_mean'),
            'sigma_mean': self.param.get('sigma_mean'),
            'sigma_sd': self.param.get('sigma_sd'),
        }
        sm = compile_model(filename=self.model_file, model_name='LN2-Stationary')
        fit = sm.sampling(
            data=stan_data, iter=self.param.get('n_mcsim') + self.param.get('n_warmup'),
            chains=self.param.get('n_chain'), warmup=self.param.get('n_warmup')
        )
        fit_dict = fit.extract(permuted=True)
        return fit_dict['yhat']
