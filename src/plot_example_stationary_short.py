import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, os.path.abspath('/Users/james/Documents/GitHub/floodsampling'))

from floodsampling.streamflow import CZNINO3LN2, TwoStateSymmetricMarkovLN2
from floodsampling.fit import TrendLN2Stan, StationaryLN2Stan, HMM

M = 20
N = 30
n_seq = 1
n_sim = 100

def get_gen_fun(index):
    """Get a generating function as a function of the index 0 or 1
    """
    if index == 0:
        gen_fun = CZNINO3LN2(
            N=N, M=M, t0=0, n_seq=n_seq,
            mu_0=6, beta_mu=0.5, gamma=0,
            coeff_var=0.1, sigma_min=0.01
        )
    elif index == 1:
        gen_fun = TwoStateSymmetricMarkovLN2(
            N=N, M=M, t0=0, n_seq=n_seq,
            mu_1=6.75, mu_0 = 6, gamma_1=0, gamma_2=0, pi=0.9,
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

# Initialize the bias and variance
gen_names = np.array(['enso', 'markov'])
fit_names = np.array(['ln2_stationary', 'ln2_trend', 'hmm'])

fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 7), sharex=True, sharey=True)
for g, gen_fun_name in enumerate(gen_names):
    gen_fun = get_gen_fun(g)
    for f, fit_fun_name in enumerate(fit_names):
        fit_fun = get_fit_fun(f, gen_fun=gen_fun)
        gen_dat = gen_fun.get_data('all')
        fit_dat = fit_fun.get_data('future')
        ax = axes[f, g]
        for i in np.arange(n_sim):
            ax.plot(fit_dat['year'], fit_dat.sel(sim=i).values.ravel(), c='gray', linewidth=0.5)
        ax.plot(gen_dat['year'], gen_dat.values.ravel(), c='blue')
        ax.set_ylim([10, 100000])
        ax.semilogy()
        if f == 0:
            ax.set_title(gen_fun_name)
        if g == len(gen_names)-1:
            ax.set_ylabel(fit_fun_name)
            ax.yaxis.set_label_position('right')

fig.tight_layout()
plt.savefig('figs/example_stationary_short.pdf')