"""Stationary
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sys
sys.path.insert(0, os.path.abspath('/Users/james/Documents/GitHub/floodsampling'))

from floodsampling.streamflow import CZNINO3LN2

gen_fun = CZNINO3LN2(
    N=50, M=50, t0=0, mu_0=6.5, beta_mu=0.5, gamma=0.01,
    coeff_var=0.075, sigma_min=0.01, n_seq=500,
)
sequences = np.log(gen_fun.get_data())

n_seq_plot = 50
threshold = 5000

fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(10, 4),
    gridspec_kw={'width_ratios': [4, 1]})
ax = axes[0]
for i in np.arange(n_seq_plot-1):
    sequences.sel(sequence=i).plot(ax=ax, linewidth=0.15, c='gray')
sequences.sel(sequence=n_seq_plot-1).plot(ax=ax, linewidth=1, c='blue')
ax.set_ylabel('Log Streamflow')
ax.set_title('')
ax.axhline(np.log(threshold), c='black', linewidth=0.6)
ax.axvline(0, c='black', linewidth=0.6)

ax = axes[1]
hist_sequences = np.log(gen_fun.get_data('historical').values.flatten())
fut_sequences = np.log(gen_fun.get_data('future').values.flatten())
sns.distplot(hist_sequences, vertical=True, ax=ax, label='historical')
sns.distplot(fut_sequences, vertical=True, ax=ax, label='future')
ax.axhline(np.log(threshold), c='black', linewidth=0.4)
ax.set_xticks([])
ax.legend()

fig.tight_layout()
fig.subplots_adjust(top=0.9)
fig.suptitle('{} Synthetic Streamflow Sequences'.format(n_seq_plot))
plt.savefig('figs/trend_sequences.pdf')
