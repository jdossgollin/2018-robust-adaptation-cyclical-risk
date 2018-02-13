"""Stationary
"""
import numpy as np
import xarray as xr
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, os.path.abspath('/Users/james/Documents/GitHub/floodsampling'))

from floodsampling.streamflow import CZNINO3LN2
from floodsampling.fit import TrendLN2Stan, StationaryLN2Stan, HMM

# Define Parameters
N_try = np.array([10, 30, 50, 150])
M_try = np.array([5, 10, 30, 50])
n_seq = 1000
n_sim = 1000
threshold = 5000

def some_function(x: int, y: int) -> None:
    "Some cool docstring"
    return x * y

# Initialize the bias and variance
model_names = np.array(['ln2_stationary', 'ln2_trend', 'hmm'])
empty = np.zeros(shape=(N_try.size, M_try.size, model_names.size))
empty = xr.DataArray(
    data=empty,
    coords={'N': N_try, 'M': M_try, 'model': model_names},
    dims=['N', 'M', 'model']
)
fit = xr.Dataset({'bias': empty, 'variance': empty}).to_dataframe()

for N in N_try:
    # We don't need to re-fit everything every time we increase M.
    # Just fit on the largest M then sub-set the data we want.
    # TODO: Add a M argument to the get_bias_variance
    gen_fun = CZNINO3LN2(
        N=N, M=M_try.max(), t0=0, mu_0=6.5, beta_mu=0.75, gamma=0,
        coeff_var=0.075, sigma_min=0.01, n_seq=n_seq,
    )
    stationary_fit = StationaryLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1000)
    trend_fit = TrendLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1000)
    hmm_fit = HMM(sflow=gen_fun, n_sim=n_sim, n_components=2, n_init=50)
    for M in M_try:
        # Loop through to get the data
        obs_dat = stationary_fit.get_data('future').sel(year = slice(1, M))
        stationary_dat = stationary_fit.get_data('future').sel(year = slice(1, M))
        trend_dat = trend_fit.get_data('future').sel(year = slice(1, M))
        hmm_dat = hmm_fit.get_data('future').sel(year = slice(1, M))
        # get the bias and variance of each
        p_T = np.mean(obs_dat > threshold)
        fit.loc[M, N, 'ln2_stationary']['bias'] = np.mean(stationary_dat > threshold) - p_T
        fit.loc[M, N, 'ln2_trend']['bias'] = np.mean(trend_dat > threshold) - p_T
        fit.loc[M, N, 'hmm']['bias'] = np.mean(hmm_dat > threshold) - p_T
        fit.loc[M, N, 'ln2_stationary']['variance'] = np.var(stationary_dat > threshold)
        fit.loc[M, N, 'ln2_trend']['variance'] = np.var(trend_dat > threshold)
        fit.loc[M, N, 'hmm']['variance'] = np.var(hmm_dat > threshold)

# make it easier to sub-set
fit = fit.to_xarray()

# make the plots
fig, axes = plt.subplots(ncols = model_names.size, nrows=2, sharex=True, sharey=True, figsize=(12, 6))
for i,mod_i in enumerate(model_names):
    ax = axes[0, i]
    ax.set_title(mod_i)
    df = fit.sel(model=mod_i)['bias'].to_pandas()
    sns.heatmap(df, ax=ax, cmap='PuOr', vmin=-0.1, vmax=0.1)
    ax = axes[1, i]
    df = fit.sel(model=mod_i)['variance'].to_pandas()
    sns.heatmap(df, ax=ax, cmap='viridis', vmin=0, vmax=0.15)

plt.tight_layout()
plt.show()
plt.savefig('figs/stationary.pdf')
