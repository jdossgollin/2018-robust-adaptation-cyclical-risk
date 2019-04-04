# STXCluster

Welcome to the code repository for the paper "Adaptating to Spatiotemporally Clustered Risk in a Changing Environment" by James Doss-Gollin, David Farnham, and Upmanu Lall.
Running the code in the `src` directory will enable you to generate all the figures in our paper, including supplemental figures.
You can also view original versions of several presentations of (early versions of) this work.


## Code and Installation

All the code except that which generates the wavelet spectrum of the NINO3 annual series is written in `python` and lives in the `src` directory.
You can install all the required packages in `conda`:

```
conda env create -f environment.yml
conda activate robust-adaptation-cyclical-risk
```

## Running

There are two steps to running the codes.
The first step is to run the computational experiments.
The relevant files are called `slurm-LFV-Only.sh`, `slurm-LFV-Secular.sh`, and `slurm-Secular-Only.sh`.
These files are currently written to be run on Columbia's Habanero cluster, but you can easily run them elsewhere.
Simply replace the comments at the top of each file (these are for a slurm scheduler) and replace

```
module load anaconda
source activate STXCluster
```

with

```
conda activate robust-adaptation-cyclical-risk
```

This will take a long time and will generate a lot of data, so be prepared!
Once the experiments have run, you can use `jupyter` notebooks to visualize results.
These also live in the `src` directory and are numbered.
