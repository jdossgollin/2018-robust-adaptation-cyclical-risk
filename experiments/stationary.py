"""Stationary
"""
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, os.path.abspath('/Users/james/Documents/GitHub/floodsampling'))

from floodsampling.streamflow import CZNINO3LN2
from floodsampling.fit import TrendLN2Stan
from floodsampling.util import get_data_path

# Define Parameters
N_try = np.array([10, 50, 250])
M_try = np.array([5, 10, 50])
n_seq = 250
n_sim = 100
threshold = 2500

# Initialize the bias and variance
empty = np.zeros(shape=(N_try.size, M_try.size)) # indexed (N, M)
bias = xr.DataArray(data=empty, coords={'N': N_try, 'M': M_try}, dims=['N', 'M'])
variance = xr.DataArray(data=empty, coords={'N': N_try, 'M': M_try}, dims=['N', 'M'])

M = 50
N = 100

gen_fun = CZNINO3LN2(
    N=N, M=M, t0=0, mu_0=6.5, beta_mu=0.75, gamma=0,
    coeff_var=0.075, sigma_min=0.01, n_seq=n_seq,
)
fit_fun = TrendLN2Stan(
    sflow=gen_fun, n_sim=n_sim,
    chains=1, warmup=1000
)
print(fit_fun.get_data())
