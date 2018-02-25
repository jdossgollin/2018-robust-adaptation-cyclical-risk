"""Get simulations of stationary data and save to file
"""
import argparse
import itertools
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

def get_gen_fun(fun_name, N, M, t0, n_seq):
    """Get a generating function as a function of the fun_name 0 or 1
    """
    if fun_name == 'NINO3':
        gen_fun = CZNINO3LN2(
            N=N, M=M, t0=0, n_seq=n_seq,
            mu_0=6, beta_mu=0.5, gamma=0.015,
            coeff_var=0.1, sigma_min=0.01
        )
    elif fun_name == 'Markov':
        gen_fun = TwoStateSymmetricMarkovLN2(
            N=N, M=M, t0=0, n_seq=n_seq,
            mu_1=6.75, mu_0 = 6, gamma_1=0.015, gamma_2=0, pi=0.9,
            coeff_var = 0.1, sigma_min = 0.01
        )
    else:
        raise ValueError('Invalid Index')
    return gen_fun

def get_fit_fun(fun_name, gen_fun, n_sim):
    """Get a fit function as a function of the fun_name 0 or 1 or 2
    """
    if fun_name == 'LN2 Stationary':
        fit_fun = StationaryLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1000)
    elif fun_name == 'LN2 Trend':
        fit_fun = TrendLN2Stan(sflow=gen_fun, n_sim=n_sim, chains=1, warmup=1000)
    elif fun_name == 'HMM':
        fit_fun = HMM(sflow=gen_fun, n_sim=n_sim, n_components=2, n_init=50)
    else:
        raise ValueError('Invalid Index')
    return fit_fun

def expand_grid(data_dict):
    """Create a dataframe from every combination of given values.
    See https://stackoverflow.com/questions/12130883/r-expand-grid-function-in-python
    """
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

def calc_bias_variance(N, M, gf_name, ff_name, **kwargs):
    """Calculate bias and variance as a function of input parameters
    These input parameters are passed as the row of a pandas data frame
    """
    n_seq = kwargs.pop('n_seq', 1000)
    n_sim = kwargs.pop('n_sim', 2000)
    M_max = kwargs.pop('M_max', 150)
    threshold = kwargs.pop('threshold', 5000)
    t0 = kwargs.pop('t0', 0)
    if M > M_max:
        raise ValueError('M cannot be greater than M_max')

    generating_function = get_gen_fun(fun_name=gf_name, N=N, M=M_max, t0=t0, n_seq=n_seq)
    gen_dat = generating_function.get_data('future').sel(year = slice(1, M))

    fitting_function = get_fit_fun(fun_name=ff_name, gen_fun=generating_function, n_sim=n_sim)
    fit_dat = fitting_function.get_data('future').sel(year = slice(1, M))
    
    exceed_gen = gen_dat > threshold
    exceed_fit = fit_dat > threshold
    
    bias = exceed_fit.mean() - exceed_gen.mean()
    variance = exceed_fit.std(dim='sim').mean()

    return bias.values, variance.values

def main():
    
    args = parser.parse_args()
    
    # Compiling in parallel --> nightmare so compile separately
    compile_model('src/floodsampling/data/ln2-stationary.stan', model_name='StationaryLN2Stan')
    compile_model('src/floodsampling/data/ln2-trend.stan', model_name='TrendLN2Stan')

    # Parameters of the model
    N_try = np.array([10, 20, 30, 40, 50, 75, 100, 150])
    M_try = np.array([3, 5, 10, 20, 30, 50, 75])
    gen_funs = np.array(['NINO3', 'Markov'])
    fit_funs = np.array(['LN2 Stationary', 'LN2 Trend', 'HMM'])

    # First step is to run the *simulations* in parallel, using only the
    # largest value of M
    simulation_df = expand_grid({'N': N_try, 'gen_fun': gen_funs, 'fit_fun': fit_funs,})
    with Parallel(n_jobs=args.n_jobs) as parallel:
        bv_tuple = parallel(
            delayed(calc_bias_variance)(
                N=row[1]['N'], 
                M=M_try.max(), 
                gf_name=row[1]['gen_fun'], 
                ff_name=row[1]['fit_fun'], 
                M_max = M_try.max()
            ) for row in simulation_df.iterrows()
        )
    
    # Second step is to go through and calculate bias and variance in 
    # parallel for many values of M
    param_df = expand_grid({
        'N': N_try, 'M': M_try,
        'gen_fun': gen_funs, 'fit_fun': fit_funs,
    })
    with Parallel(n_jobs=args.n_jobs) as parallel:
        bv_tuple = parallel(
            delayed(calc_bias_variance)(
                N=row[1]['N'], 
                M=row[1]['M'], 
                gf_name=row[1]['gen_fun'], 
                ff_name=row[1]['fit_fun'], 
                M_max = M_try.max()
            ) for row in param_df.iterrows()
        )
    param_df['bias'] = [tup[0] for tup in bv_tuple]
    param_df['variance'] = [tup[1] for tup in bv_tuple]

    param_df.to_csv(args.outfile)

if __name__ == '__main__':
    main()