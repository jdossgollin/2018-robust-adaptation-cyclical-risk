import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("--outfile", help="the filename of the figure to save")
parser.add_argument("--N_sites", type=int, help="number of sites to create")
parser.add_argument("--N_years", type=int, help="number of years")

def main():
    
    args = parser.parse_args()
    N_sites = args.N_sites
    N_years = args.N_years

    start_year = 5432
    enso = xr.open_dataarray('./src/floodsampling/data/ramesh2017.nc').sel(year = slice(start_year, start_year + N_years - 1))
    coefficients = np.random.normal(size=N_sites)
    intercepts = 7
    mu = intercepts + np.multiply.outer(enso, coefficients)
    sigma = 0.075 * mu
    sigma[np.where(sigma < 0.01)] = 0.01
    log_sflow = np.random.normal(loc=mu, scale=sigma)
    sflow = xr.DataArray(
        np.exp(log_sflow), 
        coords = {'location': np.arange(1, N_sites + 1), 'time': np.arange(1, N_years + 1)},
        dims = ['time', 'location']
    )
    threshold = sflow.quantile(0.99).values

    (sflow > threshold).mean(dim='location').plot(figsize=(12, 6))
    plt.xlabel('Year')
    plt.ylabel('Proportion of {} Sites Experiencing Flood'.format(N_sites))
    plt.grid()
    plt.savefig(args.outfile, bbox_inches='tight')
    
if __name__ == '__main__':
    main()