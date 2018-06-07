# STXCluster

Welcome to the code repository for the paper "Adaptating to Spatiotemporally Clustered Risk in a Changing Environment" by James Doss-Gollin, David Farnham, and Upmanu Lall.
Running the code here will enable you to generate all the figures in our paper, including supplemental figures.

## Code and Installation

All the code except that which generates the wavelet spectrum of the NINO3 annual series is written in `python`.
You can install all the required packages in `conda`:

```
conda env create -f environment.yml
conda activate STXCluster
```

That file is written in **R**: `/src/wavelet.R`.

## Running

The code is run using GNU Make, as specified in `Makefile`.
To generate all plots, just run

```
make all
```

Please note that computation is fairly involved and you may need to run simulations on a cluster.

## To Do

This code is not in a final version, and some minor changes need to be made before it is published.
These include:

- Remove `ssh` call specific to JDG in `Makefile`
- Remove `slurm` file `make_simulate.sh`
- Provide guideline on running on a cluster (ie number of cores and hours needed)
- Can we do the wavelet analysis in **R**?
