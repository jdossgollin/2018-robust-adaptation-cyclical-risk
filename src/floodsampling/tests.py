import numpy as np
import pytest

from .streamflow import CZNINO3LN2
from .fit import StationaryLN2Stan, TrendLN2Stan, HMM
from .util import clear_cache

clear_cache()

def assert_get_sequences(sflow):
    """Make sure we are getting data of the right shape
    """
    data = sflow.get_data()
    n_seq = sflow.time['n_seq']
    n_years = sflow.time['M'] + sflow.time['N']
    assert data['year'].size == n_years
    assert data['sequence'].size == n_seq

def assert_get_fits(fitted):
    """Make sure we can get fits
    """
    data = fitted.get_data()
    n_seq = fitted.time['n_seq']
    n_sim = fitted.time['n_sim']
    n_years = fitted.time['M']
    assert data['year'].size == n_years
    assert data['sequence'].size == n_seq
    assert data['sim'].size == n_sim

def assert_bias(fitted):
    """Make sure we can get fits
    """
    bias, _ = fitted.decompose_variance(threshold=2000)
    assert np.abs(bias) < 1, 'bias cannot be greater than 1'

def test_loop():
    """For each possible combination, run the assertion.

    The idea here is to try many different combinations of generating model,
    fitting model, and parameters.
    In particular, try different values of T_0
    """
    M_vec = [20, 50, 20, 50]
    N_vec = [50, 20, 50, 20]
    t0_vec = [0, 10, -10, 0]
    all_gen_fun = [CZNINO3LN2]
    all_fit_fun = [StationaryLN2Stan, TrendLN2Stan, HMM]
    for (M, N, t0) in zip(M_vec, N_vec, t0_vec):
        for gen_fun in all_gen_fun:
            for fit_fun in all_fit_fun:
                sflow = gen_fun(N=N, M=M, n_seq=3, t0=t0)
                assert_get_sequences(sflow)
                fitted = fit_fun(sflow=sflow, n_sim=10)
                assert_get_fits(fitted)
                assert_bias(fitted)
