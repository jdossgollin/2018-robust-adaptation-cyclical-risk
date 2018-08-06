"""A set of base classes which provide the skeleton for the streamflow and fit classes
"""

from collections import OrderedDict
from typing import Tuple
import os
import numpy as np
import xarray as xr
import pandas as pd

class BaseSequence:

    def __init__(self, M: int, N: int, category: str, **kwargs) -> None:
        """A base class for synthetic streamflow data or statistical fits

        Parameters
        ----------
        M : the project planning period, in years
        N : the length of the historical record, in years
        category : what kind of sequence is this?
        """
        self.param: dict = {} # initialize
        self.M = np.int(M)
        self.N = np.int(N)
        self.category = category
        self.data = None

    def _get_time(self, period: str) -> np.ndarray:
        """Get an array of years from a given N and M

        Parameters
        ----------
        period : either 'all', 'historical', or 'future'
        """
        if period == 'all':
            syear = - self.N + 1
            eyear = self.M
        elif period == 'historical':
            syear = - self.N + 1
            eyear = 0
        elif period == 'future':
            syear = 1
            eyear = self.M
        else:
            raise ValueError('Invalid parameter of period: {} not recognized'.format(period))    
        return np.arange(start=syear, stop=eyear+1)

    def _get_attributes(self) -> OrderedDict:
        """Get the key parameters of the data as an ordered dictionary.

        This makes it suitable for setting a file name, and also for
        comparing the attributes of a data set read from file with the attributes
        specified by the user.
        """
        attributes = self.param
        attributes.update({
            'M': self.M,
            'N': self.N,
        })
        attributes = OrderedDict(attributes)
        return attributes
    
    def _get_filename(self) -> str:
        """Get a file name

        Uses the parameters of the model to build a dictionary of all the
        key attributes of the model. Then converts them to a string
        and hashes the output to a (shorter!) filename. Finally adds the path
        to the data directory and the appropriate file suffix.
        """
        raise NotImplementedError # implemented slightly differently for each sub class

    def _to_file(self, data: xr.DataArray) -> None:
        """Save the model sequences to file

        Create the desired parent directory and delete existing file with same name, if necessary, and then dump to file.
        """
        assert isinstance(data, xr.DataArray), 'data must be data array'

        data.attrs = self._get_attributes() # save all the model parameters
        if os.path.isfile(self._get_filename()):
            os.remove(self._get_filename())
        data.to_netcdf(self._get_filename(), mode='w', format='netCDF4')

    def _from_file(self) -> Tuple[xr.DataArray, bool]:
        """Get data from file

        NEEDS TO B
        """
        raise NotImplementedError # needs to be implemented slightly differently

    def _calculate_all(self) -> xr.DataArray:
        """Need to implement in child class
        """
        raise NotImplementedError

    def get_data(self) -> xr.DataArray:
        """Get the data
        """
        try:
            data, success = self._from_file()
        except BaseException:
            success = False

        if not success:
            data = self._calculate_all()
            self._to_file(data=data)
            success = True

        self.data = data