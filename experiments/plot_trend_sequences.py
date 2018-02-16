"""Stationary
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sys
sys.path.insert(0, os.path.abspath('/Users/james/Documents/GitHub/floodsampling'))

from floodsampling.streamflow import CZNINO3LN2, TwoStateSymmetricMarkovLN2

time_param = {'N': 100, 'M': 50, 't0': 0, 'n_seq': 500}
plot_log = False # plot log streamflow?
n_seq_plot = 50 # how many sequences to plot
threshold = 2500
if plot_log:
    threshold = np.log(threshold)

enso_gen = CZNINO3LN2(
    N=time_param['N'], M=time_param['M'], t0=time_param['t0'], 
    mu_0=6, beta_mu=0.5, gamma=0.01,
    coeff_var=0.1, sigma_min=0.01, 
    n_seq=time_param['n_seq'],
)
markov_gen = TwoStateSymmetricMarkovLN2(
    N=time_param['N'], M=time_param['M'], t0=time_param['t0'], 
    mu_1=6.75, mu_0 = 6, gamma_1=0.01, gamma_2=0, pi=0.9,
    coeff_var = 0.1, sigma_min = 0.01,
    n_seq=time_param['n_seq'],
)
enso_seq = enso_gen.get_data()
markov_seq = markov_gen.get_data()

if plot_log:
    enso_seq = np.log(enso_seq)
    markov_seq = np.log(markov_seq)

# Setup the figure
fig, axes = plt.subplots(
    nrows=2, ncols=2, sharey=True, figsize=(11, 5),
    gridspec_kw={'width_ratios': [4, 1]},
    sharex='col'
)

ax = axes[0, 0]
for i in np.arange(n_seq_plot-1):
    enso_seq.sel(sequence=i).plot(ax=ax, linewidth=0.15, c='gray')
enso_seq.sel(sequence=n_seq_plot-1).plot(ax=ax, linewidth=1, c='blue')
ax.axvline(0, c='black', linewidth=0.6)
ax.set_xlabel('')
ax.set_title('Synthetic ENSO-Based Sequences')
if plot_log:
    ax.set_ylabel('Log Streamflow')
else:
    ax.set_ylabel('Streamflow')

ax = axes[0, 1]
hist_sequences = enso_seq.sel(year=slice(time_param['t0'] - time_param['N'], time_param['t0'])).values.flatten()
fut_sequences = enso_seq.sel(year=slice(time_param['t0'] + 1, time_param['t0'] + time_param['M'])).values.flatten()
sns.distplot(hist_sequences, vertical=True, ax=ax, label='historical')
sns.distplot(fut_sequences, vertical=True, ax=ax, label='future')
ax.legend()

ax = axes[1, 0]
for i in np.arange(n_seq_plot-1):
    markov_seq.sel(sequence=i).plot(ax=ax, linewidth=0.15, c='gray')
markov_seq.sel(sequence=n_seq_plot-1).plot(ax=ax, linewidth=1, c='blue')
ax.axvline(0, c='black', linewidth=0.6)
ax.set_title('Markov Chain-Based Sequences')
if plot_log:
    ax.set_ylabel('Log Streamflow')
else:
    ax.set_ylabel('Streamflow')

ax = axes[1, 1]
hist_sequences = markov_seq.sel(year=slice(time_param['t0'] - time_param['N'], time_param['t0'])).values.flatten()
fut_sequences = markov_seq.sel(year=slice(time_param['t0'] + 1, time_param['t0'] + time_param['M'])).values.flatten()
sns.distplot(hist_sequences, vertical=True, ax=ax, label='historical')
sns.distplot(fut_sequences, vertical=True, ax=ax, label='future')
ax.legend()

for ax in axes.flat:
    ax.axhline(threshold, c='black', linewidth=0.6)
    if not plot_log:
        ax.set_ylim([0, 7000])


fig.tight_layout()
plt.savefig('figs/trend_sequences.pdf')