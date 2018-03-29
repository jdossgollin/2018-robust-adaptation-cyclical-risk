import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string

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
    threshold = sflow.quantile(0.99, dim='time')
    exceedances = (sflow > threshold).mean(dim='location')

    exceedances_iid = np.random.binomial(n=N_sites, p=0.01, size=N_years) / N_sites
    exceedances_iid = xr.DataArray(exceedances_iid, coords=exceedances.coords, dims=['time'])
    print(exceedances_iid.max().values)
    print(exceedances_iid.min().values)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 4), gridspec_kw={'width_ratios': [4.5, 1]}, sharey=True)
    
    ax = axes[0]
    sub_ex = exceedances.sel(time=slice(0, 250))
    sub_iid = exceedances_iid.sel(time=slice(0, 250))
    ax.plot(sub_ex['time'], sub_ex.values, label='Simulated')
    ax.plot(sub_iid['time'], sub_iid.values, label='IID')
    ax.set_xlabel('Year')
    ax.set_ylabel('Proportion of Sites Experiencing 100-Year Flood'.format(N_sites))
    ax.grid()
    ax.axhline(0.01, c='gray')

    ax = axes[1]
    sns.distplot(exceedances, vertical=True, label='Simulated')
    sns.distplot(exceedances_iid, vertical=True, label='IID')
    ax.set_xticks([])
    ax.axhline(0.01, c='gray')
    ax.grid()
    ax.legend()

    letters = string.ascii_lowercase
    for i, ax in enumerate(axes.flat):
        label = '({})'.format(letters[i])
        t = ax.text(0.075, 0.925, label, fontsize=14, transform=ax.transAxes)
        t.set_bbox(dict(facecolor='white', edgecolor='black'))

    fig.tight_layout()
    fig.savefig(args.outfile, bbox_inches='tight')
    
if __name__ == '__main__':
    main()