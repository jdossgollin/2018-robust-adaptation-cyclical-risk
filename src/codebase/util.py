"""Utility Functions

These are broadly useful for the rest of the package
"""
from typing import Any
import itertools
import os
import pickle
import stat
from hashlib import md5
from pystan import StanModel
from joblib import Parallel, delayed
import pandas as pd

from .path import data_path, cache_path

def compile_model(filename: str, model_name: str='') -> StanModel:
    """Compile a stan model only if it hasn't already been compiled

    This will automatically cache models - great if you're just running a
    script on the command line.

    Parameters
    ----------
    filename : the path to the .stan file
    model_name : the name of the model
    """

    with open(filename) as file:
        model_code = file.read()
        code_hash = md5(model_code.encode('ascii')).hexdigest()
        cache_fn = 'cached-{}-{}.pkl'.format(model_name, code_hash)
        cache_fn = os.path.join(cache_path, 'stan', cache_fn)
        try:
            smodel = pickle.load(open(cache_fn, 'rb'))
        except BaseException:
            smodel = StanModel(model_code=model_code)
            safe_pkl_dump(obj=smodel, fname=cache_fn)

    return smodel

def clear_cache() -> None:
    """Delete cached files and stan models.

    This function completely clears the cache off data simulations and
    stan models.
    """
    for root, dirs, files in os.walk(cache_path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(cache_path)

def safe_pkl_dump(obj: Any, fname: str) -> None:
    """Dump a file to `pickle`.

    If a file is saved with that same name, it is overwritten.
    If the parent directory does not exist, it is created.

    Parameters
    ----------
    obj : The object to be saved to file
    fname : The full filename, including path
    """
    # If the directory doesn't exist, try to make it
    par_dir = os.path.dirname(fname)
    if not os.path.isdir(par_dir):
        os.makedirs(par_dir)

    # dump the object to file
    with open(fname, 'wb') as file:
        pickle.dump(obj, file)

def expand_grid(data_dict):
    """Create a dataframe from every combination of given values.
    See https://stackoverflow.com/questions/12130883/r-expand-grid-function-in-python
    """
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

def get_bias_variance(generator, fitter, threshold):
    """Helpful for running experiments
    """
    N = generator.N
    M = generator.M
    generator.get_data()
    fitter.get_data()
    df = fitter.evaluate(threshold=threshold)
    df['Generating_Function'] = generator.model_name
    df.drop(columns='Generating Function', inplace=True)
    df.rename(columns={'Fitting Function': 'Fitting_Function'}, inplace=True)
    return df

def run_experiment(param_df, n_jobs, n_seq, n_mcsim, threshold):
    """Run in parallel
    """
    with Parallel(n_jobs=n_jobs) as parallel:
        result_list =  parallel(
            delayed(get_bias_variance)(
                generator = row['generator'],
                fitter = row['fitter'],
                threshold=threshold
            ) for i,row in param_df.iterrows()
        )
    
    results_df = pd.concat(result_list, axis=0)
    results_df.reset_index(inplace=True)
    results_df.set_index(['M', 'N', 'Generating_Function', 'Fitting_Function'], inplace=True)
    results_ds = results_df.to_xarray()
    
    return results_ds