"""Generate synthetic streamflow sequences based on a NINO3 sequence
"""

import os
import numpy as np
import pandas as pd
import xarray as xr

from .synthetic import SyntheticFloodSequence
from ..path import data_path

class NINO3Linear(SyntheticFloodSequence):
    """Draw streamflow sequences based on a linear relationship with a NINO3 index/
    NINO3 data from Ramesh et al (2017)
    """

    def __init__(self, **kwargs) -> None:
        model_param = {
            'mu0': kwargs.pop('mu0'),
            'gamma': kwargs.pop('gamma', 0),
            'beta': kwargs.pop('beta', 0.5),
            'coeff_var': kwargs.pop('coeff_var', 0.1),
            'sigma_min': kwargs.pop('sigma_min', 0.01),
        }
        super().__init__(**kwargs)
        self.param.update(model_param)
        self.model_name = 'NINO3'

    def _calculate_one(self) -> np.ndarray:
        """Run the calculation
        """
        filename = os.path.join(data_path, 'ramesh2017.csv')
        nino3 = pd.read_csv(filename, index_col='year')
        syear = np.random.choice(np.arange(0, nino3.index.max() - (self.M + self.N)))
        nino3_sub = nino3.loc[syear:(syear + self.M + self.N - 1)].nino3.values
        
        mu = self.param.get('mu0') + self.param.get('gamma') * self._get_time(period='all') + self.param.get('beta') * nino3_sub
        sigma = self.param.get('coeff_var') * mu
        sigma[np.where(sigma < self.param.get('sigma_min'))] = self.param.get('sigma_min')
        sflow = np.exp(np.random.normal(loc=mu, scale=sigma))
        return sflow
