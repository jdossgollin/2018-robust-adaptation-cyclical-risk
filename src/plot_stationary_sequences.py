"""Stationary
"""
import numpy as np
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, os.path.abspath('/Users/james/Documents/GitHub/floodsampling'))

from floodsampling.streamflow import CZNINO3LN2, TwoStateSymmetricMarkovLN2

time_param = {'N': 100, 'M': 50, 't0': 0, 'n_seq': 500}
n_seq_plot = 50 # how many sequences to plot
threshold = 2500

enso_gen = CZNINO3LN2(
    N=time_param['N'], M=time_param['M'], t0=time_param['t0'], 
    mu_0=6, beta_mu=0.5, gamma=0,
    coeff_var=0.1, sigma_min=0.01, 
    n_seq=time_param['n_seq'],
)
markov_gen = TwoStateSymmetricMarkovLN2(
    N=time_param['N'], M=time_param['M'], t0=time_param['t0'], 
    mu_1=6.55, mu_0=5.7, gamma_1=0, gamma_2=0, pi=0.9,
    coeff_var = 0.1, sigma_min = 0.01,
    n_seq=time_param['n_seq'],
)
enso_seq = enso_gen.get_data()
markov_seq = markov_gen.get_data()

# Setup the figure
fig, axes = plt.subplots(nrows=2, ncols=1, sharey=True, figsize=(12, 5), sharex='col')

ax = axes[0]
for i in np.arange(n_seq_plot-1):
    enso_seq.sel(sequence=i).plot(ax=ax, linewidth=0.05, c='gray', alpha=0.5)
enso_seq.sel(sequence=n_seq_plot-1).plot(ax=ax, linewidth=1, c='blue')
ax.axvline(0, c='black', linewidth=0.6)
ax.set_xlabel('')
ax.set_title('{} Synthetic ENSO-Based Sequences'.format(n_seq_plot))

ax = axes[1]
for i in np.arange(n_seq_plot-1):
    markov_seq.sel(sequence=i).plot(ax=ax, linewidth=0.05, c='gray', alpha=0.5)
markov_seq.sel(sequence=n_seq_plot-1).plot(ax=ax, linewidth=1, c='blue')
ax.axvline(0, c='black', linewidth=0.6)
ax.set_title('{} Markov Chain-Based Sequences'.format(n_seq_plot))


for ax in axes.flat:
    ax.axhline(threshold, c='black', linewidth=0.6)
    ax.semilogy()
    ax.set_ylabel('Streamflow')
    ax.grid(True)

fig.tight_layout()
plt.savefig('figs/stationary_sequences.pdf', bbox_inches='tight')

p_T_enso = (enso_seq > threshold).values.mean()
p_T_markov = (markov_seq > threshold).values.mean()
print('p_T for ENSO: {}'.format(p_T_enso))
print('p_T for Markov: {}'.format(p_T_markov))