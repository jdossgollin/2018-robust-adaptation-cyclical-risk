"""Fit models to observations
"""

import os
import warnings

import pomegranate as pm
import numpy as np
import xarray as xr
from tqdm import tqdm

from .util import compile_model, get_data_path
from .core import BaseSequence
from .streamflow import StreamflowCreator

class FloodFit(BaseSequence):
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
    sflow : StreamflowCreator
        A StreamflowCreator instance
    n_sim : int
        Number of samples to return
    model_name : str
        The name of the model

    Attributes
    ----------
    time : dict
        A dictionary that describes the time parameters of the model.
        Should have keys ``['M', 'M', t0', 'n_seq', 'n_sim']``.
    param : dict
        The parameters of _both_ the generating model and fitting model
    sflow : StreamflowCreator
        The StreamflowCreator object that creates the streamflow sequences
    """

    def __init__(self, sflow, n_sim, **kwargs):

        model_name = kwargs.pop('model_name')
        assert isinstance(model_name, str), 'model_name must be a string'
        assert isinstance(sflow, StreamflowCreator), 'sflow must be a StreamflowCreator'

        super().__init__(
            category='fit', model_name=model_name,
            N=sflow.time['N'], M=sflow.time['M'],
            t0=sflow.time['t0'], n_seq=sflow.time['n_seq']
        )
        self.time.update({'n_sim': n_sim})
        self.param.update(sflow.param)
        self.sflow = sflow

    def _calculate_one_seq(self, one_seq):
        """Simulate a single sequence of annual maximum flood peaks

        This function needs to be implemented by the child class and is not
        implemented in this parent class.

        Parameters
        ----------
        one_seq : xr.DataArray
            A single streamflow sequence, implemented as a xr.DataArray with
            one coordinate called "year"

        Returns
        -------
        xr.DataArray
            Simulated future distributions of streamflow from the fit or posterior
            distribution of the model. Indexed ['sim', 'year'].
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
        xr.DataArray
            an array indexed [sim, year, sequence]
        """

        all_sequences = self.sflow.get_data(period='historical')
        data = [None] * self.time['n_seq']
        for seq_i in tqdm(np.arange(self.time['n_seq'])):
            trials = 0
            success = False
            while not success:
                if trials > 10:
                    warnings.warn('{}: No luck on sequence {}, leaving empty'.format(self.param, seq_i))
                    years = self.get_years('all')
                    empty = xr.DataArray(
                        data=np.zeros(shape=(self.time['n_sim'], years.size)) * np.nan,
                        coords={'year': years, 'sim': np.arange(self.time['n_sim'])},
                        dims=['sim', 'year'],
                    )
                    data[seq_i] = empty
                    success = True
                try:
                    one_seq = all_sequences.sel(sequence=seq_i)
                    new_dat = self._calculate_one_seq(one_seq=one_seq)
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

        .. note:: At present, there are only two options.
            Either data is read in
            from file, or data is completely re-generated. There is not any
            incremental simulation implemented. This may change in the future.

        Parameters
        ----------
        period : {'all', 'historical', 'future'}
            The period for which to return the time (defaults to 'all')

        Returns
        -------
        xr.DataArray
            an array indexed [sim, year, sequence]
        """
        data, load_success = self.from_file()
        if not load_success:
            data = self._calculate_all_seqs()
            self.to_file(data=data)
        years_keep = self.get_years(period=period)
        data = data.sel(year=np.in1d(data['year'], years_keep))
        return data

    def decompose_variance(self, threshold):
        """Get the bias and variance of estimates

        Parameters
        ----------
        threshold : float
            the level that defines a flood

        Returns
        -------
        bias : float
            The bias of the estimates
        variance : float
            The variance of the estimates
        """
        modeled = self.get_data()
        sflow_seq = self.sflow.get_data(period='future')

        prob_estimated = (modeled > threshold).mean(dim='year')
        prob_estimated.attrs = modeled.attrs
        prob_obs = (self.sflow.get_data() > threshold).mean(dim='year')
        prob_obs.attrs = sflow_seq.attrs

        bias = np.mean(prob_estimated.values) - np.mean(prob_obs.values)
        variance = np.var(prob_estimated.values)

        return bias, variance


class StationaryLN2Stan(FloodFit):
    """A Stationary 2-Paramater Log-Normal Fit

    Parameters
    ----------
    sflow : StreamflowCreator
        A StreamflowCreator instance
    n_sim : int
        Number of samples to return
    mu_mean : float, optional
        Prior mean on mu (default 0)
    mu_sd : float, optional
        Prior standard deviation on mu (default 10)
    sigma_mean : float, optional
        Prior mean on mu (default 0)
    sigma_sd : float, optional
        Prior standard deviation on sigma (default 2)
    warmup : int, optional
        Number of warmup iterations to run in stan (default 1000)
    chains : int, optional
        Number of chains to run in stan (default 1)

    Attributes
    ----------
    time : dict
        A dictionary that describes the time parameters of the model.
        Should have keys ``['M', 'M', t0', 'n_seq', 'n_sim']``.
    param : dict
        The parameters of the model or models
    sflow : `StreamflowCreator`
        The `StreamflowCreator` object that creates the streamflow sequences
    """
    def __init__(self, sflow, n_sim, **kwargs):
        model_name = kwargs.pop('model_name', 'StationaryLN2Stan')
        super().__init__(sflow=sflow, model_name=model_name, n_sim=n_sim)
        self.param.update({
            'mu_mean': kwargs.pop('mu_mean', 0),
            'mu_sd': kwargs.pop('mu_mean', 10),
            'sigma_mean': kwargs.pop('mu_mean', 0),
            'sigma_sd': kwargs.pop('mu_mean', 2),
            'warmup': kwargs.pop('warmup', 1000),
            'chains': kwargs.pop('chains', 1)
        })

    def _calculate_one_seq(self, one_seq):
        """Simulate a single sequence of annual maximum flood peaks using LN2

        Parameters
        ----------
        one_seq : xr.DataArray
            A single streamflow sequence, implemented as a xr.DataArray with
            one coordinate called "year"

        Returns
        -------
        xr.DataArray
            Simulated future distributions of streamflow from the fit or posterior
            distribution of the model. Indexed ['sim', 'year'].
        """
        years = self.get_years(period='future')
        sim = np.arange(self.time['n_sim'])
        stan_data = {
            'N': self.sflow.time['N'],
            'M': self.sflow.time['M'],
            'y': one_seq.values,
            'mu_mean': self.param['mu_mean'],
            'mu_sd': self.param['mu_sd'],
            'sigma_mean': self.param['sigma_mean'],
            'sigma_sd': self.param['sigma_sd']
        }
        stan_file = os.path.join(get_data_path(), 'ln2-stationary.stan')
        stan_model = compile_model(filename=stan_file, model_name='')
        posterior = stan_model.sampling(
            data=stan_data,
            pars=['yhat'],
            chains=self.param['chains'],
            iter=self.param['warmup'] + self.time['n_sim'],
            warmup=self.param['warmup']
        )
        samples = posterior.extract(permuted=True)['yhat']
        samples = xr.DataArray(
            data=samples,
            coords={'sim': sim, 'year': years},
            dims=['sim', 'year']
        )

        return samples

class TrendLN2Stan(FloodFit):
    """A 2-Paramater Log-Normal Fit with Linear Time Trend

    Parameters
    ----------
    sflow : StreamflowCreator
        A StreamflowCreator instance
    n_sim : int
        Number of samples to return
    mu0_mean : float, optional
        Prior mean on mu0 (default 0)
    mu0_sd : float, optional
        Prior standard deviation on mu0 (default 10)
    sigma0_mean : float, optional
        Prior mean on sigma0 (default 0)
    sigma0_sd : float, optional
        Prior standard deviation on sigma0 (default 2)
    beta_mu_mean : float, optional
        Prior mean on beta_mu
    beta_mu_sd : float, optional
        Prior standard deviation on beta_mu
    beta_sigma_mean : float, optional
        Prior mean on sigmma
    beta_sigma_sd : float, optional
        Prior standard deviation on sigmma
    warmup : int, optional
        Number of warmup iterations to run in stan (default 1000)
    chains : int, optional
        Number of chains to run in stan (default 1)

    Attributes
    ----------
    time : dict
        A dictionary with keys ['M', 'N', 't0', 'n_seq'] that describe the time
    param : dict
        The parameters of the model or models
    sflow : StreamflowCreator
        The StreamflowCreator object that creates the streamflow sequences
    """
    def __init__(self, sflow, n_sim, **kwargs):
        model_name = kwargs.pop('model_name', 'TrendLN2Stan')
        super().__init__(sflow=sflow, model_name=model_name, n_sim=n_sim)
        self.param.update({
            'warmup': kwargs.pop('warmup', 1000),
            'chains': kwargs.pop('chains', 1),
            'mu0_mean': kwargs.pop('mu_mean', 0),
            'mu0_sd': kwargs.pop('mu_mean', 10),
            'sigma0_mean': kwargs.pop('mu_mean', 0),
            'sigma0_sd': kwargs.pop('mu_mean', 2),
            'beta_mu_mean': kwargs.pop('mu_mean', 0),
            'beta_mu_sd': kwargs.pop('mu_mean', 0.1),
            'beta_sigma_mean': kwargs.pop('mu_mean', 0),
            'beta_sigma_sd': kwargs.pop('mu_mean', 0.05),
        })

    def _calculate_one_seq(self, one_seq):
        """Simulate a single sequence of annual maximum flood peaks using LN2

        Parameters
        ----------
        one_seq : xr.DataArray
            A single streamflow sequence, implemented as a xr.DataArray with
            one coordinate called "year"

        Returns
        -------
        xr.DataArray
            Simulated future distributions of streamflow from the fit or posterior
            distribution of the model. Indexed ['sim', 'year'].
        """
        years = self.get_years(period='future')
        sim = np.arange(self.time['n_sim'])
        stan_data = {
            'N': self.sflow.time['N'],
            'M': self.sflow.time['M'],
            'y': one_seq.values,
            'mu0_mean': self.param['mu0_mean'],
            'mu0_sd': self.param['mu0_sd'],
            'sigma0_mean': self.param['sigma0_mean'],
            'sigma0_sd': self.param['sigma0_sd'],
            'beta_mu_mean': self.param['beta_mu_mean'],
            'beta_mu_sd': self.param['beta_mu_sd'],
            'beta_sigma_mean': self.param['beta_sigma_mean'],
            'beta_sigma_sd': self.param['beta_sigma_sd']
        }
        stan_file = os.path.join(get_data_path(), 'ln2-trend.stan')
        stan_model = compile_model(filename=stan_file, model_name='')
        posterior = stan_model.sampling(
            data=stan_data,
            pars=['yhat'],
            chains=self.param['chains'],
            iter=self.param['warmup'] + self.time['n_sim'],
            warmup=self.param['warmup']
        )
        samples = posterior.extract(permuted=True)['yhat']
        samples = xr.DataArray(
            data=samples,
            coords={'sim': sim, 'year': years},
            dims=['sim', 'year']
        )
        return samples

class HMM(FloodFit):
    """A Hidden Markov Model implemented in pomegranate
    Parameters
    ----------
    sflow : StreamflowCreator
        A StreamflowCreator instance
    n_sim : int
        Number of samples to return
    n_components : int, optional
        Number of latent states in HMM (default 2)
    pseudocount : int, optional
        See pomegranate documentation (default 10)
    n_init : int, optional
        See pomegranate documentation (default 25)
    Attributes
    ----------
    time : dict
        A dictionary with keys ['M', 'N', 't0', 'n_seq'] that describe the time
    param : dict
        The parameters of the model or models
    sflow : StreamflowCreator
        The StreamflowCreator object that creates the streamflow sequences
    """
    def __init__(self, sflow, n_sim, **kwargs):
        model_name = kwargs.pop('model_name', 'HMM')
        super().__init__(sflow=sflow, model_name=model_name, n_sim=n_sim)
        self.param.update({
            'n_components': kwargs.pop('n_components', 2),
            'pseudocount': kwargs.pop('pseudocount', 10),
            'n_init': kwargs.pop('n_init', 25)
        })

    def _calculate_one_seq(self, one_seq):
        """Simulate a single sequence of annual maximum flood peaks using LN2
        Parameters
        ----------
        one_seq : xr.DataArray
            A single streamflow sequence, implemented as a xr.DataArray with
            one coordinate called "year"
        Returns
        -------
        xr.DataArray
            Simulated future distributions of streamflow from the fit or posterior
            distribution of the model. Indexed ['sim', 'year'].
        """
        X = np.log(one_seq).values[:, np.newaxis]
        samples = xr.DataArray(
            np.ones(shape=(self.time['n_sim'], self.time['M'])),
            coords={
                'sim': np.arange(self.time['n_sim']),
                'year': np.arange(self.time['M'])
            }, dims=['sim', 'year']
        )
        model = pm.HiddenMarkovModel.from_samples(
            pm.NormalDistribution,
            n_components=self.param['n_components'],
            X=X,
            pseudocount=self.param['pseudocount'],
            n_init=self.param['n_init'],
        )
        for j in np.arange(self.time['n_sim']):
            samples.sel(sim=j).values += np.exp(np.array(model.sample(length=self.time['M'])))

        return samples
