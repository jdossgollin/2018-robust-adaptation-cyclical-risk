#!/bin/sh
#
# Run the code on a slurm server
#
#SBATCH --account=cwc           # The account name for the job.
#SBATCH --job-name=STATIONARY   # The job name.
#SBATCH -N 8                    # The number of nodes to use
#SBATCH --exclusive
#SBATCH --time=12:00:00          # The time the job will take to run.

module load anaconda/3-4.4.0    # load the anaconda module
source activate STXCluster      # activate the conda environment

# run the python
python 01-Run-LFV-Only.py
python 02-Run-Secular-Only.py
python 03-Run-LFV-Secular.py

# End of script
