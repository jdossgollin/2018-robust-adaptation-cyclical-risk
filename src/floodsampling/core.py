"""Parent class for StreamflowCreator and FloodFit
"""
import os
from hashlib import md5
from collections import OrderedDict

import numpy as np
import xarray as xr

from floodsampling.util import get_cache_path, safe_pkl_dump

class BaseSequence:
    """A parent class for streamflow sequences or monte carlo model draws

    You shouldn't call this class directly.
    It provides functionality primarily for file I/O and for repeating calculations
    for many sequences, which are shared methods which would otherwise be duplicated.

    Parameters
    ----------
    N : int
        the length of the observational record, in years
    M : int
        the length of the future project planning period, in years
    t0 : int, optional
        the "zero" time (default 0)
    n_seq : int, optional
        the number of sequences to generate (default 3)

    Attributes
    ----------
    time : dict
        A dictionary with keys ['M', 'N', 't0', 'n_seq'] that describe the time
    param : dict
        The parameters of the model or models
    """

    def __init__(self, **kwargs):
        self.time = {
            'M': int(kwargs.pop('M')),
            'N': int(kwargs.pop('N')),
            't0': int(kwargs.pop('t0', 0)),
            'n_seq': int(kwargs.pop('n_seq', 3))
        }
        self.param = {} # must be added by child class

    def _get_attributes(self):
        """Get the key parameters of the data as an ordered dictionary.

        This makes it suitable for setting a file name, and also for
        comparing the attributes of a data set read from file with the attributes
        specified by the user.

        Returns
        -------
        OrderedDict
            The parameters of the model
        """
        attributes = self.param
        attributes.update({
            'M': self.time['M'],
            'N': self.time['N'],
            't0': self.time['t0'],
            'n_seq': self.time['n_seq']
        })
        attributes = OrderedDict(attributes)
        return attributes

    def _get_filename(self):
        """Get a file name

        Uses the parameters of the model to build a dictionary of all the
        key attributes of the model. Then converts them to a string
        and hashes the output to a (shorter!) filename. Finally adds the path
        to the data directory and the appropriate file suffix.

        Returns
        -------
        str
            A full path to the filename to which the data will be saved
        """

        attributes = self._get_attributes()

        file_string = '' # initialize empty string
        for key, val in attributes.items():
            file_string += 'simulated_{}{}'.format(key, val)

        file_string = md5(file_string.encode('ascii')).hexdigest()
        file_string += '.pkl'

        file_path = os.path.join(get_cache_path(), file_string)
        return file_path

    def to_file(self, data):
        """Save the model sequences to file

        Uses the `util.safe_pkl_dump()` function to create the desired parent directory
        and delete existing file with same name, if necessary, and then dump to file.

        Parameters
        ----------
        data : xr.DataArray
            The data to save to file, will always be flood sequences.
        """
        assert isinstance(data, xr.DataArray), 'data must be data array'

        data.attrs = self._get_attributes() # force the attrs object of the xarray object
        fname = self._get_filename()
        safe_pkl_dump(data, fname=fname)

    def from_file(self):
        """Get data from file

        Tries to read in the data from file. If successful, checks the attributes
        of the data against the desired attributes of the data as given by
        `self._get_attributes()``.

        Returns
        -------
        data : xr.DataArray
            a data array  with coordinates ['year', 'sequence'] of streamflow
            sequences
        success : bool
            indicates whether data was successfully loaded and also the attributes
            matched the (user)-specified ones
        """
        try:
            fname = self._get_filename()
            data = pickle.load(open(fname, 'rb'))
            attrs_desired = self._get_attributes()
            attr_observed = data.attrs
            success = attrs_desired == attr_observed
        except BaseException:
            success = False
            data = None

        return data, success

    def get_years(self, period):
        """Get an array of years from a given N and M

        Parameters
        ----------
        period : {'all', 'historical', 'future'}
            The period for which to return the time (defaults to 'all')

        Returns
        -------
        np.ndarray
            an array of all years corresponding to the chosen time period
        """
        if period == 'all':
            syear = self.time['t0'] - self.time['N'] + 1
            eyear = self.time['t0'] + self.time['M']
        elif period == 'historical':
            syear = self.time['t0'] - self.time['N'] + 1
            eyear = self.time['t0']
        elif period == 'future':
            syear = self.time['t0'] + 1
            eyear = self.time['t0'] + self.time['M']
        else:
            raise ValueError('Invalid parameter of period: {} not recognized'.format(period))

        times = np.arange(syear, eyear + 1)
        return times
