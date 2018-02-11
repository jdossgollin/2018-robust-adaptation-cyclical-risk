#!/bin/bash

#SBATCH --account=cwc
#SBATCH -J notebook
#SBATCH --time=6:00:00


# Setup Environment
module load anaconda
source activate floodsampling

export XDG_RUNTIME_DIR=""

jupyter notebook --no-browser --ip "*" --notebook-dir $HOME
