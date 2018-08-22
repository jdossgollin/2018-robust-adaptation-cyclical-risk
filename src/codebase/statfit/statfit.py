"""Statistical fits
"""

from hashlib import md5
import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple
import pandas as pd

from ..path import cache_path
from ..core import BaseSequence
from ..synthetic import SyntheticFloodSequence

class StatisticalModel(BaseSequence):
    """A base class
    """

    def __init__(self, synthetic: SyntheticFloodSequence, **kwargs) -> None:
        super().__init__(M=synthetic.M, N=synthetic.N,
            category='StatisticalModel', **kwargs)
        model_param = {
            'n_mcsim': kwargs.pop('n_mcsim', 1000)
        }
        self.param.update(synthetic.param)
        self.param.update(model_param)
        self.synthetic = synthetic
        self.model_name = ''

    def _calculate_one(self, data) -> np.ndarray:
        """This *must* be implemented by a specific child class
        Should return a numpy array indexed [year, simulation]
        where simulation refers to 1, ..., n_mcsim

        Parameters
        ----------
        data : the historical data
        """
        raise NotImplementedError

    def _calculate_all(self) -> xr.DataArray:
        """Just loop through and combine
        """
        if self.synthetic.data is None:
            self.synthetic.get_data()
        
        input_data = self.synthetic.data.sel(year=self._get_time('historical'))
        sequences = 1 + np.arange(self.param.get('n_seq'))
        simulations = 1 + np.arange(self.param.get('n_mcsim'))
        fits = xr.concat([
            xr.DataArray(
                data=self._calculate_one(data = input_data.sel(sequence = seq).values),
                coords={'year': self._get_time('future'), 'simulation': simulations},
                dims=['simulation', 'year'],
                name='Statistical Monte Carlo Projection'
            ) for seq in sequences
        ], dim='sequence')
        fits['sequence'] = sequences
        fits.attrs = self._get_attributes()
        return fits
    
    def _get_filename(self) -> str:
        """Get a file name

        Uses the parameters of the model to build a dictionary of all the
        key attributes of the model. Then converts them to a string
        and hashes the output to a (shorter!) filename. Finally adds the path
        to the data directory and the appropriate file suffix.
        """

        attributes = self._get_attributes()
        _ = [attributes.pop(var) for var in ['M']]

        file_string = ''
        for key, val in attributes.items():
            file_string += '_{}={}'.format(key, val)

        file_string = md5(file_string.encode('ascii')).hexdigest()
        file_string += '.nc'

        file_dir = os.path.join(cache_path, self.category)
        file_dir = os.path.abspath(file_dir)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        
        filename = os.path.abspath(os.path.join(file_dir, file_string))
        return filename
    
    def _from_file(self) -> Tuple[xr.DataArray, bool]:
        """Get data from file

        NEEDS TO B
        """
        try:
            data = xr.open_dataarray(self._get_filename())
            attr_observed = data.attrs
            M_observed = attr_observed.pop('M')
            attr_desired = self._get_attributes()
            M_desired = attr_desired.pop('M')
            success = False # default assumption is no luck
            if (attr_desired == attr_observed) and (M_observed >= M_desired):
                data = data.sel(year=slice(1-self.N, M_desired))
                success = True # we did it!
            else:
                data = None # no luck
        
        except BaseException:
            success = False
            data = None

        return data, success

    def evaluate(self, threshold: float) -> Dict[str, float]:
        """Evaluate the sucess of predictions
        """
        if self.data is None:
            self.get_data()
        
        future_estimates = self.data.sel(year=self._get_time('future'))
        future_obs = self.synthetic.data.sel(year=self._get_time('future'))
        
        bias = (future_estimates > threshold).mean().values - (future_obs > threshold).mean().values
        stdev = (future_estimates > threshold).std(dim='simulation').mean(dim=['sequence', 'year']).values

        results = pd.DataFrame({
            'N': self.N,
            'M': self.M,
            'bias': bias  - 0,
            'stdev': stdev - 0,
            'Generating Function': self.synthetic.model_name,
            'Fitting Function': self.model_name
        }, index=[0]).set_index(['N', 'M'])

        return results
