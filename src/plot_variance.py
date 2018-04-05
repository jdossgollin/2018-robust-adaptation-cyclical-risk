import xarray as xr
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import colorcet as cc

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--trend", help="the filename of the saved bias/variance data")
parser.add_argument("--stationary", help="the filename of the saved bias/variance data")
parser.add_argument("--NINO3", type=int)
parser.add_argument("--outfile", help="the filename of the figure to save")

def main():
    args = parser.parse_args()

    trend = xr.open_dataset(args.trend).to_dataframe().reset_index()
    trend['Stationarity'] = 'Trend'
    stationary = xr.open_dataset(args.stationary).to_dataframe().reset_index()
    stationary['Stationarity'] = 'Stationary'
    if args.NINO3 == 1:
        trend = trend.loc[trend['Generating Function'] == 'NINO3']
        stationary = stationary.loc[stationary['Generating Function'] == 'NINO3']
    else:
        trend = trend.loc[trend['Generating Function'] == 'Markov']
        stationary = stationary.loc[stationary['Generating Function'] == 'Markov']

    fit = pd.concat([stationary, trend], axis=0)
    fit_df = fit.reset_index().set_index(['M', 'N'])

    vmin = -5
    vmax= - 1
    cmap = cc.cm['fire']

    fig, axes = plt.subplots(
        nrows=fit['Stationarity'].unique().size, 
        ncols=fit['Fitting Function'].unique().size, 
        sharex=True, sharey=True, figsize=(10, 6)
    )
    for col,f in enumerate(fit_df['Fitting Function'].unique()):
        for row,g in enumerate(fit_df['Stationarity'].unique()):
            sub = fit_df.loc[np.logical_and(fit_df['Stationarity'] == g, fit_df['Fitting Function'] == f)].reset_index().pivot('M', 'N', 'variance')
            ax=axes[row, col]
            C = sns.heatmap(np.log(sub), ax=ax, vmin=vmin, vmax=vmax, cmap=cmap, cbar=False, linewidths=0.1)
            if row == 0:
                ax.set_title(f)            
            if col  == (axes.shape[1] - 1):
                ax.set_ylabel(g)
                ax.yaxis.set_label_position('right')

    fig.tight_layout()
    fig.subplots_adjust(right=0.85)
    cax = fig.add_axes([0.9, 0.1, 0.02, 0.8])
    sns.heatmap(np.log(sub), vmin=vmin, vmax=vmax, ax=ax, cmap=cmap, linewidths=0.1, cbar_kws={'label': 'Log of Expected Standard Deviation'}, cbar_ax=cax)
    ax.set_ylabel(g)
    ax.yaxis.set_label_position('right')
    
    fig.savefig(args.outfile)
    
if __name__ == '__main__':
    main()