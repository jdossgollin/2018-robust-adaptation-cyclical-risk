"""Open the NINO3 time series and plot a sub-set of it
"""
import argparse
import os

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from floodsampling.util import get_data_path

parser = argparse.ArgumentParser()
parser.add_argument("--outfile", help="the filename of the data to save")

def main():

    args = parser.parse_args()
    data_fname = os.path.join(get_data_path(), 'ramesh2017.nc')
    enso = xr.open_dataarray(data_fname)

    # Plot Time Series
    enso.sel(year=slice(1000, 2000)).plot(
        figsize=(10, 4.5),
        c='blue',
        linewidth=0.5
    )
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Annualized NINO3 Index')

    plt.savefig(args.outfile, bbox_inches='tight')

if __name__ == '__main__':
    main()