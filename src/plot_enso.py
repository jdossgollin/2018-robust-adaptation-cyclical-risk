"""Open the NINO3 time series and plot a sub-set of it
"""
import argparse
import os

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

from floodsampling.util import get_data_path

parser = argparse.ArgumentParser()
parser.add_argument("--outfile", help="the filename of the data to save")

def main():

    args = parser.parse_args()
    data_fname = os.path.join(get_data_path(), 'ramesh2017.nc')
    enso = xr.open_dataarray(data_fname)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 4), gridspec_kw={'width_ratios': [2, 1]})
    enso.sel(year=slice(1000, 2000)).plot(
        c='blue',
        linewidth=0.5,
        ax=axes[0],
    )
    axes[0].grid(True)
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Annualized NINO3 Index')

    # get the spectrum
    x = enso.values
    fs = 1
    f, Pxx_den = signal.periodogram(x, fs)
    periodogram = pd.Series(Pxx_den, index=f)
    smoothed = periodogram.rolling(100, win_type='hamming').mean()

    smoothed.plot(ax=axes[1], label='smoothed')
    axes[1].set_xlabel('frequency [Year$^{-1}$]')
    axes[1].set_ylabel('Power Spectral Density')
    axes[1].grid()

    plt.savefig(args.outfile, bbox_inches='tight')

if __name__ == '__main__':
    main()