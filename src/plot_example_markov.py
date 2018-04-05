import argparse
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

from floodsampling.streamflow import CZNINO3LN2, TwoStateSymmetricMarkovLN2
from floodsampling.fit import TrendLN2Stan, StationaryLN2Stan, HMM

parser = argparse.ArgumentParser()
parser.add_argument("--outfile", help="the filename of the data to save")
parser.add_argument("--N", type=int, help="the filename of the data to save")

def get_gen_fun(index, N, M, t0, n_seq):
    """Get a generating function as a function of the index 0 or 1
    """
    if index == 0:
        gen_fun = TwoStateSymmetricMarkovLN2(
            N=N, M=M, t0=t0, n_seq=n_seq,
            mu_1=6.75, mu_2 = 6, gamma_1=0., gamma_2=0, pi=0.9,
            coeff_var=0.1, sigma_min=0.01,
        )
    elif index == 1:
        gen_fun = TwoStateSymmetricMarkovLN2(
            N=N, M=M, t0=t0, n_seq=n_seq,
            mu_1=6.75, mu_2 = 6, gamma_1=0.01, gamma_2=0, pi=0.9,
            coeff_var=0.1, sigma_min=0.01,
        )
    else:
        raise ValueError('Invalid Index')
    return gen_fun

def get_fit_fun(index, gen_fun, n_sim):
    """Get a fit function as a function of the index 0 or 1 or 2
    """
    if index == 0:
        fit_fun = StationaryLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1000)
    elif index == 1:
        fit_fun = TrendLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1001)
    elif index == 2:
        fit_fun = HMM(sflow=gen_fun, n_sim=n_sim, n_components=2, n_init=50)
    else:
        raise ValueError('Invalid Index')
    return fit_fun

def main():
    
    args = parser.parse_args()

    M = 150
    n_seq = 1
    n_sim = 5000

    # Initialize the bias and variance
    gen_names = np.array(['Markov Chain Stationary', 'Markov Chain Trend'])
    fit_names = np.array(['LN2 Stationary', 'LN2 Trend', 'HMM'])

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 7), sharex=True, sharey=True)
    for g, gen_fun_name in enumerate(gen_names):
        gen_fun = get_gen_fun(g, N=args.N, M=M, t0=0, n_seq=n_seq)
        for f, fit_fun_name in enumerate(fit_names):
            fit_fun = get_fit_fun(f, gen_fun=gen_fun, n_sim=n_sim)
            gen_dat = gen_fun.get_data('all')
            fit_dat = fit_fun.get_data('future')
            ax = axes[f, g]
            year = fit_dat['year']

            c50l = fit_dat.quantile(0.25, dim='sim').values.ravel()
            c50u = fit_dat.quantile(0.75, dim='sim').values.ravel()
            c80u = fit_dat.quantile(0.90, dim='sim').values.ravel()
            c80l = fit_dat.quantile(0.10, dim='sim').values.ravel()
            c99u = fit_dat.quantile(0.995, dim='sim').values.ravel()
            c99l = fit_dat.quantile(0.005, dim='sim').values.ravel()
            
            ax.fill_between(year, c99l, c99u, color='gray', alpha=0.33, label='99% CI')
            ax.fill_between(year, c80l, c80u, color='gray', alpha=0.33, label='80% CI')
            ax.fill_between(year, c50l, c50u, color='gray', alpha=0.33, label='50% CI')
            
            ax.plot(gen_dat['year'], gen_dat.values.ravel(), c='blue', linewidth=1)
            ax.semilogy()
            ax.grid()
            ax.set_ylim([np.power(10, 1.5), np.power(10, 4.5)])
            if f == 0:
                ax.set_title(gen_fun_name)
            if g == len(gen_names)-1:
                ax.set_ylabel(fit_fun_name)
                ax.yaxis.set_label_position('right')
            
            ax.axhline(5000, c='black')

    fig.tight_layout()
    plt.savefig(args.outfile)

if __name__ == '__main__':
    main()