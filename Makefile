################################################################################
# GLOBAL VARIABLES
#
# This section lays out some global and high-level commands for the Makefile;
# you can edit them if you like
################################################################################

# commands to run
PY_INTERP = python
PDF_VIEWER = Preview
TEX_INTERP = latexmk -cd -e -f -pdf -interaction=nonstopmode

## Get data, process it, and create plots
output	: simuulate plot

## View all figures
viewfigs:
	open -a $(PDF_VIEWER) figs/*

## create everything in the analysis
all: dirs simulate plot

################################################################################
# MAKE SETUP
#
# This section defines commands to create the desired conda environment
# and to create all required folders
################################################################################

## Create all directories that the system expects
dirs	:
	mkdir -p figs data

## Create and activate a conda environment pyfloods
environment	:
	conda update -y conda;\
	conda env create --file environment.yml;\
	conda activate floodsampling

## Pull data from habanero
pull	:
	rsync -avz -e ssh jwd2136@habanero.rcs.columbia.edu:/rigel/cwc/users/jwd2136/MNPaper/data ./

################################################################################
# MAKE SIMULATIONS
################################################################################

NCORES=8 # how many cores to run on

data/stationary.nc	:	src/get_bias_variance.py
	$(PY_INTERP) $< --outfile $@ --n_jobs $(NCORES) --gamma 0

data/trend.nc	:	src/get_bias_variance.py
	$(PY_INTERP) $< --outfile $@ --n_jobs $(NCORES) --gamma 0.015

data/nino3.csv	:	src/nc_to_csv.py
	$(PY_INTERP) $< --infile src/floodsampling/data/ramesh2017.nc --outfile $@

## Make all simulations
simulate:	dirs data/stationary.nc data/trend.nc data/nino3.csv

################################################################################
# MAKE PLOTS
################################################################################

figs/bias_nino.pdf	:	src/plot_bias.py data/stationary.nc
	$(PY_INTERP) $< --stationary data/stationary.nc --trend data/trend.nc --NINO3 1 --outfile $@

figs/bias_markov.pdf	:	src/plot_bias.py data/stationary.nc
	$(PY_INTERP) $< --stationary data/stationary.nc --trend data/trend.nc --NINO3 0 --outfile $@

figs/variance_nino.pdf	:	src/plot_variance.py data/stationary.nc
	$(PY_INTERP) $< --stationary data/stationary.nc --trend data/trend.nc --NINO3 1 --outfile $@

figs/variance_markov.pdf	:	src/plot_variance.py data/stationary.nc
	$(PY_INTERP) $< --stationary data/stationary.nc --trend data/trend.nc --NINO3 0 --outfile $@

figs/variance_stationary.pdf	:	src/plot_variance.py data/stationary.nc
	$(PY_INTERP) $< --infile data/stationary.nc --outfile $@

figs/bias_trend.pdf	:	src/plot_bias.py data/trend.nc
	$(PY_INTERP) $< --infile data/trend.nc --outfile $@

figs/variance_trend.pdf	:	src/plot_variance.py data/trend.nc
	$(PY_INTERP) $< --infile data/trend.nc --outfile $@

figs/example_long.pdf	: src/plot_example.py
	$(PY_INTERP) $< --N 150 --outfile $@

figs/example_short.pdf	: src/plot_example.py
	$(PY_INTERP) $< --N 50 --outfile $@

figs/example_markov_long.pdf	:	src/plot_example_markov.py
	$(PY_INTERP) $< --N 150 --outfile $@

figs/example_markov_short.pdf	:	src/plot_example_markov.py
	$(PY_INTERP) $< --N 50 --outfile $@

figs/sequences_stationary.pdf	:	src/plot_sequences.py
	$(PY_INTERP) $< --gamma 0 --outfile $@

figs/sequences_trend.pdf	:	src/plot_sequences.py
	$(PY_INTERP) $< --gamma 0.015 --outfile $@

figs/case_study.pdf	:	src/case_study.py
	$(PY_INTERP) $< --outfile $@ --N_sites 5000 --N_years 2000

plot: figs/example_short.pdf figs/example_long.pdf figs/sequences_stationary.pdf figs/sequences_trend.pdf figs/case_study.pdf figs/example_markov_long.pdf figs/example_markov_short.pdf figs/bias_nino.pdf figs/bias_markov.pdf figs/variance_markov.pdf figs/variance_nino.pdf

################################################################################
# Self-Documenting Help Commands
#
# This section contains codes to build automatic help in the makefile
# Copied nearly verbatim from cookiecutter-data-science, in turn taken from
# <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
################################################################################

.DEFAULT_GOAL := help
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
