"""Utility functions for floodfit

This module provides some functions which are useful to the entire project and
whose utility is not limited to a single sub-module.
"""

import os
import pickle
from hashlib import md5
import stat
import pystan

def compile_model(filename, model_name=''):
    """Compile a stan model only if it hasn't already been compiled

    This will automatically cache models - great if you're just running a
    script on the command line. This code was taken nearly verbatim from
    `Pystan` documentation.

    Parameters
    ----------
    model_code : str
        the model code
    filename : str
        the path to the .stan file

    Returns
    -------
    pystan.StanModel
        the compiled model object

    See Also
    --------
    - `Pystan Documentation <http://pystan.readthedocs.io/en/latest/avoiding_recompilation.html/>`_
    - `Aki Vehtari's Stan Utilities <https://github.com/avehtari/BDA_py_demos/blob/new_pystan_demos/utilities_and_data/stan_utility.py>`
    """

    cache_dir = get_cache_path()

    with open(filename) as file:
        model_code = file.read()
        code_hash = md5(model_code.encode('ascii')).hexdigest()
        cache_fn = 'cached-{}-{}.pkl'.format(model_name, code_hash)
        cache_fn = os.path.join(cache_dir, 'stan', cache_fn)
        try:
            smodel = pickle.load(open(cache_fn, 'rb'))
        except BaseException:
            smodel = pystan.StanModel(model_code=model_code)
            safe_pkl_dump(obj=smodel, fname=cache_fn)

    return smodel

def get_data_path():
    """Get the folder where all data is saved

    Returns
    -------
    str
        The full path to the directory where the data is stored.
    """
    data_dir = os.path.abspath(os.path.join('.', 'data'))
    if not os.path.isdir(data_dir):
        raise ValueError('Uh Oh there is a path error')
    return data_dir

def get_cache_path():
    """Get the folder where cached simulations are saved

    Returns
    -------
    str
        The full path to the directory where the cache is stored.
    """
    data_dir = get_data_path()
    cache_dir = os.path.join(data_dir, 'cached')
    cache_dir = os.path.abspath(cache_dir)
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    return cache_dir

def clear_cache():
    """Delete cached files and stan models.

    This function completely clears the cache off data simulations and
    stan models.
    """
    for root, dirs, files in os.walk(get_cache_path(), topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(get_cache_path())

def safe_pkl_dump(obj, fname):
    """Dump a file to `pickle`.

    If a file is saved with that same name, it is overwritten.
    If the parent directory does not exist, it is created.

    Parameters
    ----------
    obj :
        The object to be saved to file
    fname : str
        The full filename, including path
    """
    # If the directory doesn't exist, try to make it
    par_dir = os.path.dirname(fname)
    if not os.path.isdir(par_dir):
        os.makedirs(par_dir)

    # Make sure there isn't anything else there
    if os.path.isfile(fname):
        os.remove(fname)

    # dump the object to file
    with open(fname, 'wb') as file:
        pickle.dump(obj, file)