#!/bin/sh
#
# Run the code on a slurm server
#
#SBATCH --account=cwc           # The account name for the job.
#SBATCH --job-name=LFV-SECULAR  # The job name.
#SBATCH -N 4                    # The number of nodes to use
#SBATCH --exclusive
#SBATCH --time=18:00:00          # The time the job will take to run.

module load anaconda            # load the anaconda module
source activate STXCluster      # activate the conda environment

# run the python
python 13-Run-LFV-Secular.py

# End of script
