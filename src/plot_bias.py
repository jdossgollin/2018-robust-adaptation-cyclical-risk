import xarray as xr
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("--infile", help="the filename of the saved bias/variance data")
parser.add_argument("--outfile", help="the filename of the figure to save")

def main():
    args = parser.parse_args()

    fit = xr.open_dataset(args.infile)
    fit_df = fit.to_dataframe().reset_index().set_index(['M', 'N'])

    fig, axes = plt.subplots(
        nrows=fit['Generating Function'].size, 
        ncols=fit['Fitting Function'].size, 
        sharex=True, sharey=True, figsize=(10, 6)
    )
    for col,f in enumerate(fit['Fitting Function'].values):
        for row,g in enumerate(fit['Generating Function'].values):
            sub = fit_df.loc[np.logical_and(fit_df['Generating Function'] == g, fit_df['Fitting Function'] == f)].reset_index().pivot('M', 'N', 'bias')
            ax=axes[row, col]
            sns.heatmap(sub, ax=ax, vmin=-0.025, vmax=0.025, cmap='PuOr', cbar=False, linewidths=0.1)
            if row == 0:
                ax.set_title(f)
            if col  == (fit['Fitting Function'].size - 1):
                ax.set_ylabel(g)
                ax.yaxis.set_label_position('right')

    fig.tight_layout()
    fig.subplots_adjust(right=0.85)
    cax = fig.add_axes([0.9, 0.1, 0.02, 0.8])
    sns.heatmap(sub, ax=ax, vmin=-0.025, vmax=0.025, cmap='PuOr', cbar_ax=cax, linewidths=0.1, cbar_kws={'label': 'Expected Bias'})

    fig.savefig(args.outfile)

if __name__ == '__main__':
    main()