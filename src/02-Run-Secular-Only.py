import itertools
import numpy as np
import pandas as pd
import os

from codebase.synthetic import NINO3Linear, MarkovTwoStateChain
from codebase.statfit import LN2Stationary, LN2LinearTrend, TwoStateHMM
from codebase.path import cache_path

def expand_grid(data_dict):
    """Create a dataframe from every combination of given values.
    See https://stackoverflow.com/questions/12130883/r-expand-grid-function-in-python
    """
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

def get_generator(M, N, n_seq, model):
    if model == 'MarkovTwoStateChain':
        generator = MarkovTwoStateChain(
            M=M, N=N, n_seq=n_seq,
            pi_1=0.9, pi_2=0.9, mu_1=6.5, mu_2=6.5,
            gamma_1=0.015, gamma_2=0.015, coeff_var=0.1,
            sigma_min=0.01,
        )
    elif model == 'NINO3Linear':
        generator = NINO3Linear(
            M=M, N=N, n_seq=n_seq,
            gamma=0.015, beta=0, coeff_var=0.1, sigma_min=0.01, mu0=6.5,
        )
    else:
        raise ValueError('invalid argument for model')
    return generator

def get_fitter(n_mcsim, generator, model):
    if model == 'LN2Stationary':
        fitter = LN2Stationary(synthetic=generator, n_mcsim=n_mcsim)
    elif model == 'LN2LinearTrend':
        fitter = LN2LinearTrend(synthetic=generator, n_mcsim=n_mcsim)
    elif model == 'TwoStateHMM':
        fitter = TwoStateHMM(synthetic=generator, n_mcsim=n_mcsim, n_init=50)
    else:
        raise ValueError('invalid argument for model')
    return fitter

def get_bias_variance(N, M, gen_fun, fit_fun, n_seq, n_mcsim, threshold):
    generator = get_generator(N=N, M=M, model=gen_fun, n_seq=n_seq)
    generator.get_data()
    fitter = get_fitter(generator=generator, model=fit_fun, n_mcsim=n_mcsim)
    df = fitter.evaluate(threshold=threshold)
    df['Generating_Function'] = gen_fun
    df.drop(columns='Generating Function', inplace=True)
    df.rename(columns={'Fitting Function': 'Fitting_Function'}, inplace=True)
    return df

def main():
    param_df = expand_grid({
        'N': [10, 30, 50, 100, 500],
        'M': [2, 5, 10, 30, 50, 100],
        'gen_fun': ['MarkovTwoStateChain', 'NINO3Linear'],
        'fit_fun': ['LN2Stationary', 'LN2LinearTrend', 'TwoStateHMM'],
    })
    param_df.sort_values(['M', 'N'], ascending=False, inplace=True)

    n_seq = 100
    n_mcsim = 1000
    threshold = 5000
    n_jobs = 4 # set >1 for parallel computing

    result_list = [get_bias_variance(
        M = param_df.loc[i, 'M'],
        N = param_df.loc[i, 'N'],
        gen_fun = param_df.loc[i, 'gen_fun'],
        fit_fun = param_df.loc[i, 'fit_fun'],
        n_seq=n_seq, n_mcsim=n_mcsim, threshold=threshold
    ) for i in np.arange(param_df.shape[0])]

    results_df = pd.concat(result_list, axis=0)
    results_df.reset_index(inplace=True)
    results_df.set_index(['M', 'N', 'Generating_Function', 'Fitting_Function'], inplace=True)
    results_ds = results_df.to_xarray()
    fn = os.path.join(cache_path, 'secular-only-bias-variance.nc')
    if os.path.isfile(fn):
        os.path.remove(fn)
    results_ds.to_netcdf(fn)

if __name__ == '__main__':
    main()