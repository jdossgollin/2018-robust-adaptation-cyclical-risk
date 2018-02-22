"""Get simulations of trend data and save to file
"""
import numpy as np
import xarray as xr
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from floodsampling.streamflow import CZNINO3LN2, TwoStateSymmetricMarkovLN2
from floodsampling.fit import TrendLN2Stan, StationaryLN2Stan, HMM

# Define Parameters
N_try = np.array([10, 20, 30, 40, 50, 75, 100, 150])
M_try = np.array([3, 5, 10, 20, 30, 50, 75])
n_seq = 2000
n_sim = 2000
threshold = 5000

# Initialize the bias and variance
gen_names = np.array(['NINO3', 'Markov'])
fit_names = np.array(['LN2 Stationary', 'LN2 Trend', 'HMM'])

# Indexing: [N, gen_fun, fit_fun, M]
bias = np.zeros(shape=(N_try.size, gen_names.size, fit_names.size, M_try.size)) 
variance = np.zeros(shape=(N_try.size, gen_names.size, fit_names.size, M_try.size))

def get_gen_fun(index):
    """Get a generating function as a function of the index 0 or 1
    """
    if index == 0:
        gen_fun = CZNINO3LN2(
            N=N, M=M_try.max(), t0=0, n_seq=n_seq,
            mu_0=6, beta_mu=0.5, gamma=0.01,
            coeff_var=0.1, sigma_min=0.01
        )
    elif index == 1:
        gen_fun = TwoStateSymmetricMarkovLN2(
            N=N, M=M_try.max(), t0=0, n_seq=n_seq,
            mu_1=6.75, mu_0 = 6, gamma_1=0.01, gamma_2=0, pi=0.9,
            coeff_var = 0.1, sigma_min = 0.01
        )
    else:
        raise ValueError('Invalid Index')
    return gen_fun

def get_fit_fun(index, gen_fun):
    """Get a fit function as a function of the index 0 or 1 or 2
    """
    if index == 0:
        fit_fun = StationaryLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1000)
    elif index == 1:
        fit_fun = TrendLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1001)
    elif index == 2:
        fit_fun = HMM(sflow=gen_fun, n_sim=n_sim, n_components=2, n_init=50)
    else:
        raise ValueError('Invalid Index')
    return fit_fun

# Solve this with a big for loop
for n, N in enumerate(N_try):
    for g, gen_fun_name in enumerate(gen_names):
        gen_fun = get_gen_fun(g)
        for f, fit_fun_name in enumerate(fit_names):
            fit_fun = get_fit_fun(f, gen_fun=gen_fun)
            for m, M in enumerate(M_try):
                # Loop through to get the data
                gen_dat = gen_fun.get_data('future').sel(year = slice(1, M))
                fit_dat = fit_fun.get_data('future').sel(year = slice(1, M))
                exceed_gen = gen_dat > threshold
                exceed_fit = fit_dat > threshold
                bias[n, g, f, m] = exceed_fit.mean() - exceed_gen.mean()
                variance[n, g, f, m] = exceed_fit.std(dim='sim').mean()

bias = xr.DataArray(
    bias, 
    coords={'N': N_try, 'gen_fun': gen_names, 'fit_fun': fit_names, 'M': M_try, }, 
    dims=['N', 'gen_fun', 'fit_fun', 'M']
)
variance = xr.DataArray(
    variance, 
    coords={'N': N_try, 'gen_fun': gen_names, 'fit_fun': fit_names, 'M': M_try, }, 
    dims=['N', 'gen_fun', 'fit_fun', 'M']
)

fit = xr.Dataset({'bias': bias, 'variance': variance})
fit.to_netcdf('data/trend.nc')