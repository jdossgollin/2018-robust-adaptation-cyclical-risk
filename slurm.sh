#!/bin/sh
#
# Run the code on a slurm server
#
# Replace <ACCOUNT> with your account name before submitting.
#
#SBATCH --account=cwc           # The account name for the job.
#SBATCH --job-name=JDGMN01      # The job name.
#SBATCH -N 1                    # The number of nodes to use
#SBATCH --exclusive
#SBATCH --time=10:00:00         # The time the job will take to run.

module load anaconda            # load the anaconda module
make environment                # create the conda env (comment if not 1st time)
source activate floodsampling   # activate the conda environment
make simulate                   # run the make command specified in the Makefile

# End of script