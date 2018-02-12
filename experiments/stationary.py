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
N_try = np.array([10, 30, 50, 150, 500])
M_try = np.array([5, 10, 30, 50, 100])
n_seq = 1000
n_sim = 1000
threshold = 5000

# Initialize the bias and variance
model_names = np.array(['ln2_stationary', 'ln2_trend', 'hmm'])
empty = np.zeros(shape=(N_try.size, M_try.size, model_names.size))
empty = xr.DataArray(
    data=empty,
    coords={'N': N_try, 'M': M_try, 'model': model_names},
    dims=['N', 'M', 'model']
)
fit = xr.Dataset({'bias': empty, 'variance': empty}).to_dataframe()

for M in M_try:
    for N in N_try:
        gen_fun = CZNINO3LN2(
            N=N, M=M, t0=0, mu_0=6.5, beta_mu=0.75, gamma=0,
            coeff_var=0.075, sigma_min=0.01, n_seq=n_seq,
        )

        fit_fun = StationaryLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1000)
        bias_i, variance_i = fit_fun.decompose_variance(threshold=threshold)
        fit.loc[M, N, 'ln2_stationary']['bias'] = bias_i
        fit.loc[M, N, 'ln2_stationary']['variance'] = variance_i

        fit_fun = TrendLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1000)
        bias_i, variance_i = fit_fun.decompose_variance(threshold=threshold)
        fit.loc[M, N, 'ln2_trend']['bias'] = bias_i
        fit.loc[M, N, 'ln2_trend']['variance'] = variance_i

        fit_fun = HMM(sflow=gen_fun, n_sim=n_sim, n_components=2, n_init=50)
        bias_i, variance_i = fit_fun.decompose_variance(threshold=threshold)
        fit.loc[M, N, 'hmm']['bias'] = bias_i
        fit.loc[M, N, 'hmm']['variance'] = variance_i

# make it easier to sub-set
fit = fit.to_xarray()

# make the plots
fig, axes = plt.subplots(ncols = model_names.size, nrows=2, sharex=True, sharey=True)
for i,mod_i in enumerate(model_names):
    ax = axes[0, i]
    ax.set_title(mod_i)
    df = fit.sel(model=mod_i)['bias'].to_pandas()
    sns.heatmap(df, ax=ax, cmap='PuOr', vmin=-0.01, vmax=0.01)
    ax = axes[1, i]
    df = fit.sel(model=mod_i)['variance'].to_pandas()
    sns.heatmap(df, ax=ax, cmap='viridis', vmin=0, vmax=0.05)

plt.tight_layout()
plt.show()
