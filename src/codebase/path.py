"""Path variables
"""
import os

def get_data_path() -> str:
    """Get the directory of the data 
    """
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(cur_dir, 'data'))
    return data_dir

def get_cache_path() -> str:
    """Get the folder where cached simulations are saved
    """
    data_dir = get_data_path()
    cache_dir = os.path.join(data_dir, 'cached')
    cache_dir = os.path.abspath(cache_dir)
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    return cache_dir

# get the paths as importable values
data_path = get_data_path()
cache_path = get_cache_path()
