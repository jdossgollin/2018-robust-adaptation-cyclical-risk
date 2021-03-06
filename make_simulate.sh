#!/bin/sh
#
# Run the code on a slurm server
#
# Replace <ACCOUNT> with your account name before submitting.
#
#SBATCH --account=cwc           # The account name for the job.
#SBATCH --job-name=STATIONARY   # The job name.
#SBATCH -N 1                    # The number of nodes to use
#SBATCH --exclusive
#SBATCH --time=3:59:00          # The time the job will take to run.

module load anaconda/3-4.4.0    # load the anaconda module
source activate gcm-lfv   # activate the conda environment
make simulate		        # run the make command specified in the Makefile

# End of script
