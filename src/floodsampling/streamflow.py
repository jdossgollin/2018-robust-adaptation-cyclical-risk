"""Generate synthetic streamflow sequences conditional on climate variables.

Some recent literature has considered statistical-dynaimcal models for fitting
flood time series where the flood or hydrological quantity of interest depends
on some (fully observed) climate covariates. This module provides some classes
for generating sequences that reverse-engineer this approach and in which the
observed annual-maximum streamflow depends on some climate covariates, plus
(optionally) time.
"""

import warnings
import os
from tqdm import tqdm
import xarray as xr
import numpy as np
import pandas as pd
import pomegranate as pm

from .core import BaseSequence
from .util import get_data_path

class StreamflowCreator(BaseSequence):
    """A parent class for creating multiple synthetic streamflow sequences.

    To implement your own method for creating streamflow sequences, create a child
    class. Otherwise, you shouldn't call this class directly.

    It is built on `floodfit.core.BaseSequence`, which you should also not plan
    on calling directly.

    .. note:: Time Indexing
        The time is indexed so that the "historical record" is defined as
        the period from time_0 - n_years + 1 to time_0, inclusive. The "future period"
        is defined as the period from time_0 + 1 to time_0 + m_years, inclusive.

    Parameters
    ----------
    N : int
        the length of the observational record, in years
    M : int
        the length of the future project planning period, in years
    t0 : int, optional
        the "zero" time (default 0)
    model_name : str, optional
        A name for the model used to generate the sequences (default None)
    n_seq : int, optional
        the number of sequences to generate (default 1)

    Attributes
    ----------
    time : dict
        A dictionary that describes the time parameters of the model.
        Should have keys ``['M', 'M', t0', 'n_seq']``.
    param : dict
        The parameters of the model or models
    """

    def __init__(self, **kwargs):

        model_name = kwargs.pop('model_name')
        assert isinstance(model_name, str), 'model_name must be a string'
        super().__init__(category='sequence', model_name=model_name, **kwargs)

    def _calculate_one_seq(self):
        """Simulate a single sequence of annual maximum flood peaks

        This function needs to be implemented by the child class and _is not_
        implemented in this parent class.

        Returns
        -------
        array_like
            a one-dimensional numpy array with shape (M+N, ).
        """
        raise NotImplementedError

    def _calculate_all_seqs(self):
        """Loop through calculations for all sequences

        Builds on the `_calculate_one_seq()` method, which _must_ be implemented in
        the child class. Loops through all requested sequences and concatenates
        the results from each along a new axis called "sequence".

        Each `_calculate_one_seq` call must return a `xr.DataArray` object.

        The loop is somewhat robust, so if you have failure on a single
        sequence the algorithm will try up to 5 before giving up.

        Parameters
        ----------
        period : {'all', 'historical', 'future'}
            The period for which to return the time (defaults to 'all')

        Returns
        -------
        np.ndarray
            an array of all years corresponding to the chosen time period
        """
        data = [None] * self.time['n_seq']
        for seq_i in tqdm(np.arange(self.time['n_seq'])):
            trials = 0
            success = False
            while not success:
                if trials > 5:
                    warnings.warn('No luck on sequence {}, leaving empty'.format(seq_i))
                    years = self.get_years('all')
                    empty = xr.DataArray(
                        data=np.zeros(shape=(years.size, )) * np.nan,
                        coords={'year': years}, dims='year',
                        name='Synthetic Streamflow Sequence'
                    )
                    data[seq_i] = empty
                    success = True
                try:
                    new_dat = self._calculate_one_seq()
                    assert isinstance(new_dat, xr.DataArray), \
                        '_calculate_one_seq must return xr.DataArray'
                    data[seq_i] = new_dat
                    success = True
                except BaseException:
                    trials += 1

        data = xr.concat(data, 'sequence')
        data['sequence'] = np.arange(self.time['n_seq'])

        return data

    def get_data(self, period='all'):
        """Get all the streamflow sequences.

        Tries to load from file, but if it is not successful will re-generate the
        sequences.

        .. note:: At present, there are only two options. Either data is read in
            from file, or data is completely re-generated. There is not any
            incremental simulation implemented. This may change in the future.

        Parameters
        ----------
        period : {'all', 'historical', 'future'}
            The period for which to return the time (defaults to 'all')

        Returns
        -------
        xr.DataArray
            an array indexed [year, sequence]
        """
        data, load_success = self.from_file()
        if not load_success:
            data = self._calculate_all_seqs()
            self.to_file(data=data)
        years_keep = self.get_years(period=period)
        data = data.sel(year=years_keep)
        return data

class CZNINO3LN2(StreamflowCreator):
    """Create sequences of streamflow conditional on a synthetic NINO3 Index.

    A 100 000 year sequences of the Cane-Zebiak model was run with stationary
    forcing to generate a monthly NINO3 time series which was reduced to annual
    time steps. Then calculate the parameters.

    The model data is an annualized version of the data described in Ramesh et al [1]_
    and is provided courtesy of Nandini Ramesh (Columbia University).

    If we denote this index by :math:`X(t)`, then we have the streamflow  :math:`Q(t)` given by

      .. math::

        \\log Q(t) \\sim \\mathcal{N} \\left( \\mu(t), \\sigma(t), \\right)

        \\mu(t) = \\mu_0 + \\beta_\\mu  X(t) + \\gamma  (t - t_0)

        \\sigma(t) = \\alpha \\mu(t)

      where :math:`\\alpha` is the coefficient of variation specifying a constant of
      proportionality between the mean and standard deviation parameters.
      Note that becuase :math:`\\mu` is allowed to be negative, an additional
      parameter **sigma_min** specifies the minimum allowable value of :math:`\\sigma`,
      with a default of 0.01.

    .. rubric:: Footnotes

    .. [1] Ramesh, N., Cane, M. A., Seager, R., & Lee, D. E. (2017).
        Predictability and prediction of persistent cool states of the Tropical Pacific Ocean.
        Climate Dynamics, 49(7–8), 2291–2307. https://doi.org/10.1007/s00382-016-3446-3

    Parameters
    ----------
    N : int
        the length of the observational record, in years
    M : int
        the length of the future project planning period, in years
    t0 : int, optional
        the "zero" time (default 0)
    mu_0 : float, optional
        the intercept term for mu (default 6)
    beta_mu : float, optional
        The coefficient for mu on the synthetic NINO3 data (default 1)
    gamma : float, optional
        The coefficeient for mu on time (default 0)
    coeff_var : float, optional
        The coefficient of variance (default 0.1)
    sigma_min : float, optional
        The lowest allowed value of sigma; must be greater than 0. Default 0.01.
    n_seq : int, optional
        the number of sequences to generate (default 1)

    Attributes
    ----------
    time : dict
        A dictionary with keys ['M', 'N', 't0', 'n_seq'] that describe the time
    param : dict
        The parameters of the model
    """
    def __init__(self, **kwargs):
        model_name = kwargs.pop('model_name', 'CZNINO3LN2')
        super().__init__(model_name=model_name, **kwargs)
        self.param.update({
            'mu_0': kwargs.pop('mu_0', 6),
            'beta_mu': kwargs.pop('beta_mu', 1),
            'gamma': kwargs.pop('gamma', 0),
            'coeff_var': kwargs.pop('coeff_var', 0.1),
            'sigma_min': kwargs.pop('sigma_min', 0.01),
        })

        # Read in the NINO3 data
        data_fname = os.path.join(get_data_path(), 'ramesh2017.nc')
        self.NINO3 = xr.open_dataarray(data_fname)

    def _calculate_one_seq(self):
        """Override the parent method to calculate streamflow sequences.
        """
        # get the NINO 3 data
        n_yrs_data = 100000 # OK to hard-code this, it doesn't change
        possible_years = np.arange(self.time['N'] - 1, n_yrs_data - self.time['M'])
        start_year = np.random.choice(possible_years)
        end_year = start_year + self.time['N'] + self.time['M'] - 1
        nino_3 = self.NINO3.sel(year=slice(start_year, end_year))

        # Get the model time
        years = self.get_years(period='all')

        # get mu and sigma
        mu_vec = self.param['mu_0'] + self.param['gamma'] * (years - self.time['t0'])
        mu_vec += self.param['beta_mu'] * nino_3
        sigma_vec = self.param['coeff_var'] * mu_vec
        sigma_vec[sigma_vec < self.param['sigma_min']] = self.param['sigma_min']

        # get the streamflow as a xr data array
        log_streamflow = np.random.normal(loc=mu_vec, scale=sigma_vec)
        streamflow = xr.DataArray(
            data=np.exp(log_streamflow),
            coords={'year': years},
            dims='year',
            name='Synthetic Streamflow Sequence'
        )
        return streamflow

class TwoStateSymmetricMarkovLN2(StreamflowCreator):
    """Create sequences of streamflow based on a Markov Chain.

    For each sequence of streamflow, generate a set of states based on an input transition matrix.
    Then, use the state sequence to generate data from a conditional log-normal distribution with
    specified parameters, including a time trend (which can be set zero for stationarity).

    Parameters
    ----------
    N : int
        the length of the observational record, in years
    M : int
        the length of the future project planning period, in years
    t0 : int, optional
        the "zero" time (default 0)
    pi : float
        The [symmetric] probability of persistence.
        Once the  model is in a given state it will remain in that same state with
        probability `pi` and switch with probability `(1-pi)`.
    mu_1 : float, optional
        the intercept term for mu in state 1 (default 6.5)
    mu_2 : float, optional
        the intercept term for mu in state 1 (default 6)
    gamma_1 : float, optional
        The coefficeient for mu on time in state 1 (default 0)
    gamma_2 : float, optional
        The coefficeient for mu on time in state 2 (default 0)
    coeff_var : float, optional
        The coefficient of variance (default 0.1)
    sigma_min : float, optional
        The lowest allowed value of sigma; must be greater than 0. Default 0.01.
    n_seq : int, optional
        the number of sequences to generate (default 1)

    Attributes
    ----------
    time : dict
        A dictionary with keys ['M', 'N', 't0', 'n_seq'] that describe the time
    param : dict
        The parameters of the model
    """
    def __init__(self, **kwargs):
        model_name = kwargs.pop('model_name', 'TwoStateSymmetricMarkovLN2')
        model_param = {
            'pi': kwargs.pop('pi'),
            'mu_1': kwargs.pop('mu_1', 6.5),
            'mu_2': kwargs.pop('mu_2', 6),
            'gamma_1': kwargs.pop('gamma_1', 0),
            'gamma_2': kwargs.pop('gamma_2', 0),
            'coeff_var': kwargs.pop('coeff_var', 0.1),
            'sigma_min': kwargs.pop('sigma_min', 0.01)
        }

        super().__init__(model_name=model_name, **kwargs)
        self.param.update(model_param)

    def _calculate_one_seq(self):
        """Override the parent method to calculate streamflow sequences.
        """

        # Get the sequence of states
        d1 = pm.DiscreteDistribution({'wet': 0.5, 'dry': 0.5})
        d2 = pm.ConditionalProbabilityTable(
            [['wet', 'wet', self.param['pi']],
            ['wet', 'dry', 1 - self.param['pi']],
            ['dry', 'wet', 1 - self.param['pi']],
            ['dry', 'dry', self.param['pi']]], [d1]
        )
        mc = pm.MarkovChain([d1, d2])
        years = self.get_years('all')
        states = mc.sample(years.size)

        # Get the conditional expected value
        mu_1_vec = self.param['mu_1'] + self.param['gamma_1'] * (years - self.time['t0'])
        mu_2_vec = self.param['mu_2'] + self.param['gamma_2'] * (years - self.time['t0'])
        mu_vec = mu_1_vec
        mu_vec[np.where(np.array(states) == 'wet')] = mu_2_vec[np.where(np.array(states) == 'wet')]

        # get conditional variance
        sigma_vec = self.param['coeff_var'] * mu_vec
        sigma_vec[sigma_vec < self.param['sigma_min']] = self.param['sigma_min']

        # get the streamflow as a xr data array
        log_sflow = np.random.normal(loc=mu_vec, scale=sigma_vec)
        sflow = xr.DataArray(
            data=np.exp(log_sflow),
            coords={'year': years},
            dims='year',
            name='Synthetic Streamflow Sequence'
        )
        return sflow