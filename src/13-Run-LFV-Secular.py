import numpy as np
import os

from codebase.synthetic import NINO3Linear, MarkovTwoStateChain
from codebase.statfit import LN2Stationary, LN2LinearTrend, TwoStateHMM
from codebase.path import cache_path
from codebase.util import expand_grid, run_experiment

def get_generator(M, N, n_seq, model):
    """Here is where you specify the parameters of each model for creating synthetic sequences.
    This is what makes this experiment LFV Only.
    """
    if model == 'MarkovTwoStateChain':
        generator = MarkovTwoStateChain(
            M=M, N=N, n_seq=n_seq,
            pi_1=0.9, pi_2=0.9, mu_1=6.75, mu_2=6,
            gamma_1=0.015, gamma_2=0, coeff_var=0.1,
            sigma_min=0.01,
        )
    elif model == 'NINO3Linear':
        generator = NINO3Linear(
            M=M, N=N, n_seq=n_seq,
            gamma=0.015, beta=0.5, coeff_var=0.1, sigma_min=0.01, mu0=6,
        )
    else:
        raise ValueError('invalid argument for model')
    return generator

def get_fitter(n_mcsim, generator, model):
    """Here is where the parameters (particularly priors) are specified
    for each fitting model.
    """
    if model == 'LN2Stationary':
        fitter = LN2Stationary(
            synthetic=generator, n_mcsim=n_mcsim, 
            mu_sd = 1.5, mu_mean = 7, sigma_mean=1, sigma_sd=1,
        )
    elif model == 'LN2LinearTrend':
        fitter = LN2LinearTrend(
            synthetic=generator, n_mcsim=n_mcsim,
            mu0_mean=7, mu0_sd=1.5, beta_mu_mean=0, beta_mu_sd=0.1,
            cv_logmean=np.log(0.1), cv_logsd=0.1, n_warmup=1500
        )
    elif model == 'TwoStateHMM':
        fitter = TwoStateHMM(synthetic=generator, n_mcsim=n_mcsim, n_init=50)
    else:
        raise ValueError('invalid argument for model')
    return fitter

def main():
    """Here is where we run the body of the code
    """
    param_df = expand_grid({
        'N': [20, 25, 30, 50, 75, 100, 150, 250],   # these can be edited
        'M': [2, 5, 10, 20, 30, 50, 100],           # these can be edited
        'gen_fun': ['MarkovTwoStateChain', 'NINO3Linear'],
        'fit_fun': ['LN2Stationary', 'LN2LinearTrend', 'TwoStateHMM'],
    })
    param_df.sort_values(['M', 'N'], ascending=False, inplace=True)
    param_df.reset_index(inplace=True, drop=True)

    # specify more parameters here
    n_seq = 1000        # how many sequences to generate
    n_mcsim = 1000      # no reason for less
    threshold = 5000    # what constitutes a flood


    # get the actual functions for generating
    for i,row in param_df.iterrows():
        param_df.loc[i, 'generator'] = get_generator(M=row['M'], N=row['N'], model=row['gen_fun'], n_seq=n_seq)
        param_df.loc[i, 'fitter'] = get_fitter(generator=param_df.loc[i, 'generator'], model=row['fit_fun'], n_mcsim=n_mcsim)

    param_df.drop(columns=['gen_fun', 'fit_fun'], inplace=True)

    results_ds = run_experiment(
        param_df=param_df,
        n_seq=n_seq,
        n_mcsim=n_mcsim,
        threshold=threshold,
    )
   
    fn = os.path.join(cache_path, 'lfv-secular-bias-variance.nc')
    if os.path.isfile(fn):
        os.remove(fn)
    results_ds.to_netcdf(fn)

if __name__ == '__main__':
    main()