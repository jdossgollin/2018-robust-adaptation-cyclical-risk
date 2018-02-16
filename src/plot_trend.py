import xarray as xr
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

fit = xr.open_dataset('data/trend.nc')
fit_df = fit.to_dataframe().reset_index().set_index(['M', 'N'])

# PLOT THE BIAS
fig, axes = plt.subplots(nrows=fit['gen_fun'].size, ncols=fit['fit_fun'].size, sharex=True, sharey=True, figsize=(10, 6))
for col,f in enumerate(fit['fit_fun'].values):
    for row,g in enumerate(fit['gen_fun'].values):
        sub = fit.sel(gen_fun = g, fit_fun = f).to_dataframe().reset_index().pivot('M', 'N', 'bias')
        ax=axes[row, col]
        sns.heatmap(sub, ax=ax, vmin=-0.15, vmax=0.15, cmap='PuOr', cbar=False, linewidths=0.1)
        if row == 0:
            ax.set_title(f)
        if col  == (fit['fit_fun'].size - 1):
            ax.set_ylabel(g)
            ax.yaxis.set_label_position('right')

fig.tight_layout()
fig.subplots_adjust(right=0.85)
cax = fig.add_axes([0.9, 0.1, 0.02, 0.8])
sns.heatmap(sub, ax=ax, vmin=-0.15, vmax=0.15, cmap='PuOr', cbar_ax=cax, linewidths=0.1, cbar_kws={'label': 'bias'})

fig.savefig('figs/trend_bias.pdf')



# PLOT THE VARIANCE
fig, axes = plt.subplots(nrows=fit['gen_fun'].size, ncols=fit['fit_fun'].size, sharex=True, sharey=True, figsize=(10, 6))
for col,f in enumerate(fit['fit_fun'].values):
    for row,g in enumerate(fit['gen_fun'].values):
        sub = fit.sel(gen_fun = g, fit_fun = f).to_dataframe().reset_index().pivot('M', 'N', 'variance')
        ax=axes[row, col]
        sns.heatmap(sub, ax=ax, vmin=0, vmax=0.02, cmap='viridis', cbar=False, linewidths=0.1)
        if row == 0:
            ax.set_title(f)
        if col  == (fit['fit_fun'].size - 1):
            ax.set_ylabel(g)
            ax.yaxis.set_label_position('right')

fig.tight_layout()
fig.subplots_adjust(right=0.85)
cax = fig.add_axes([0.9, 0.1, 0.02, 0.8])
sns.heatmap(sub, ax=ax, vmin=0, vmax=0.02, cmap='viridis', linewidths=0.1, cbar_kws={'label': 'bias'}, cbar_ax=cax)

fig.savefig('figs/trend_variance.pdf')