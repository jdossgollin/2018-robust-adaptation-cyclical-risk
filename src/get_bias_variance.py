"""Get simulations of stationary data and save to file

This is done in parallel, but in an intelligent way.
First, the stan models are compiled -- this is not done in parallel because it should
only be done once.
Second, the synthetic streamflow sequences are generated for the longest M available.
This is done in parallel.
Finally, the statistical fitting models are used to generate replicated sequences for
the longest M available; this is also done in parallel.
For many values of M* to try, the first M* years of "true" and "fit" data are selected and
the bias and variance computed.
"""
import argparse
import itertools
from collections import OrderedDict
import numpy as np
import xarray as xr
import seaborn as sns
import pandas as pd

from joblib import Parallel, delayed

from floodsampling.streamflow import CZNINO3LN2, TwoStateSymmetricMarkovLN2
from floodsampling.fit import TrendLN2Stan, StationaryLN2Stan, HMM
from floodsampling.util import compile_model

parser = argparse.ArgumentParser()
parser.add_argument("--outfile", help="the filename of the data to save")
parser.add_argument("--n_jobs", type=int, help="number of jobs to run in parallel")
parser.add_argument("--gamma", type=float, help="the coefficient to put on time")

def get_gen_fun(fun_name, **kwargs):
    """Get a generating function as a function of the fun_name 0 or 1
    """
    N = kwargs.pop('N')
    M = kwargs.pop('M')
    n_seq = kwargs.pop('n_seq')
    t0 = kwargs.pop('t0')
    gamma = kwargs.pop('gamma')
    
    mu0 = kwargs.pop('mu0')
    beta_mu = kwargs.pop('beta_mu')
    coeff_var = kwargs.pop('coeff_var')
    sigma_min = kwargs.pop('sigma_min')

    mu_1 = kwargs.pop('mu_1')
    mu_2 = kwargs.pop('mu_2')
    pi = kwargs.pop('pi')

    if fun_name == 'NINO3':
        gen_fun = CZNINO3LN2(
            N=N, M=M, t0=t0, n_seq=n_seq,
            mu_0=mu0, beta_mu=beta_mu, gamma=gamma,
            coeff_var=coeff_var, sigma_min=sigma_min,
        )
    elif fun_name == 'Markov':
        gen_fun = TwoStateSymmetricMarkovLN2(
            N=N, M=M, t0=t0, n_seq=n_seq,
            mu_1=mu_1, mu_2 = mu_2, gamma_1=gamma, gamma_2=0, pi=0.9,
            coeff_var=coeff_var, sigma_min=sigma_min,
        )
    else:
        raise ValueError('Invalid Index')
    return gen_fun

def get_fit_fun(fun_name, gen_fun, **kwargs):
    """Get a fit function as a function of the fun_name 0 or 1 or 2
    """
    n_sim = kwargs.pop('n_sim')
    chains = kwargs.pop('chains')
    warmup = kwargs.pop('warmup')
    n_components = kwargs.pop('n_components')
    n_init = kwargs.pop('n_init')

    if fun_name == 'LN2 Stationary':
        fit_fun = StationaryLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=chains, warmup=warmup)
    elif fun_name == 'LN2 Trend':
        fit_fun = TrendLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=chains, warmup=warmup)
    elif fun_name == 'HMM':
        fit_fun = HMM(sflow=gen_fun, n_sim=n_sim, n_components=n_components, n_init=n_init)
    else:
        raise ValueError('Invalid Index')
    return fit_fun

def expand_grid(data_dict):
    """Create a dataframe from every combination of given values.
    See https://stackoverflow.com/questions/12130883/r-expand-grid-function-in-python
    """
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

def run_generate(gf_name, **kwargs):
    """Run code to generate sequences for a particular combination
    """
    N = kwargs.pop('N')
    M = kwargs.pop('M')
    n_seq = kwargs.pop('n_seq')
    t0 = kwargs.pop('t0')
    gamma = kwargs.pop('gamma')
    generating_function = get_gen_fun(fun_name=gf_name, N=N, M=M, t0=t0, n_seq=n_seq, gamma=gamma, **kwargs)
    gen_dat = generating_function.get_data()
    return True

def run_fit(M_vec, gf_name, ff_name, **kwargs):
    N = kwargs.pop('N')
    n_seq = kwargs.pop('n_seq')
    t0 = kwargs.pop('t0')
    gamma = kwargs.pop('gamma')
    n_sim = kwargs.pop('n_sim')
    threshold = kwargs.pop('threshold')
    
    # Get the full data sets
    M_max = np.max(M_vec)
    M_vec = np.sort(M_vec)
    generating_function = get_gen_fun(fun_name=gf_name, N=N, M=M_max, t0=t0, n_seq=n_seq, gamma=gamma, **kwargs)
    gen_dat = generating_function.get_data('future')
    fitting_function = get_fit_fun(fun_name=ff_name, gen_fun=generating_function, n_sim=n_sim, **kwargs)
    fit_dat = fitting_function.get_data('future')

    # Initialize results data frame
    results = pd.DataFrame({
        'M': M_vec, 
        'N': N, 
        'Generating Function': gf_name, 
        'Fitting Function': ff_name, 
        'bias': np.nan,
        'variance': np.nan
    })
    # Loop through all M
    for i,M in enumerate(M_vec):
        gen_dat_sub = gen_dat.sel(year = slice(t0+1, t0+M))
        fit_dat_sub = fit_dat.sel(year = slice(t0+1, t0+M))
        exceed_gen = gen_dat_sub > threshold
        exceed_fit = fit_dat_sub > threshold
        results.loc[i, 'bias'] = exceed_fit.mean() - exceed_gen.mean()
        results.loc[i, 'variance'] = exceed_fit.std(dim='sim').mean()

    return results

def main():
    
    args = parser.parse_args()
    
    # Compiling in parallel is a nightmare so compile separately
    compile_model('src/floodsampling/data/ln2-stationary.stan', model_name='')
    compile_model('src/floodsampling/data/ln2-trend.stan', model_name='')

    # Parameters of the model
    N_try = np.array([10, 20, 30, 40, 50, 75, 100, 150])
    M_try = np.array([3, 5, 10, 20, 30, 50, 75])
    gen_funs = np.array(['NINO3', 'Markov'])
    fit_funs = np.array(['LN2 Stationary', 'LN2 Trend', 'HMM'])
    n_jobs = args.n_jobs
    parameters = {
        't0': 0,
        'n_seq': 1000,
        'n_sim': 2000,
        'gamma': args.gamma,
        'mu0': 6,
        'beta_mu': 0.5,
        'coeff_var': 0.1,
        'sigma_min': 0.01,
        'mu_1': 6.75,
        'mu_2': 6,
        'pi': 0.9,
        'chains': 1,
        'warmup': 1000,
        'n_components': 2,
        'n_init': 50,
        'threshold': 5000,
    }

    # Parameters as data frame
    param_df = expand_grid({
        'N': N_try, 
        'gen_fun': gen_funs, 
        'fit_fun': fit_funs,
    })

    # First step is to simulate streamflow sequences
    with Parallel(n_jobs=args.n_jobs) as parallel:
        fit_success = parallel(
            delayed(run_generate)(
                N = param_df.loc[i, 'N'],
                M = np.max(M_try),
                gf_name = param_df.loc[i, 'gen_fun'],
                ff_name = param_df.loc[i, 'fit_fun'],
                **parameters
            ) for i in np.arange(param_df.shape[0])
        )
    
    # Second step is to fit each sequence to each fitting model and
    # Calculate associated bias and variance
    with Parallel(n_jobs=args.n_jobs) as parallel:
        result_list = parallel(
            delayed(run_fit)(
                M_vec = M_try,
                gf_name = param_df.loc[i, 'gen_fun'],
                ff_name = param_df.loc[i, 'fit_fun'],
                N = param_df.loc[i, 'N'],
                **parameters
            ) for i in np.arange(param_df.shape[0])
        )
    
    results_df = pd.concat(result_list, axis=0)
    results_df.set_index(['M', 'N', 'Generating Function', 'Fitting Function'], inplace=True)
    results_ds = results_df.to_xarray()
    results_ds.attrs = OrderedDict(parameters)
    results_ds.to_netcdf(path=args.outfile, mode='w', format='NETCDF4')

if __name__ == '__main__':
    main()