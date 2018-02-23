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

################################################################################
# MAKE SIMULATIONS
################################################################################

NCORES=2 # how many cores to run on

data/stationary.csv	:	src/calc_stationary.py
	$(PY_INTERP) $< --outfile $@ --n_jobs $(NCORES)

data/trend.csv	:	src/calc_trend.py
	$(PY_INTERP) $< --outfile $@ --n_jobs $(NCORES)

## Make all simulations
simulate:	dirs data/stationary.csv data/trend.csv

################################################################################
# MAKE PLOTS
################################################################################

figs/enso.pdf	:	src/plot_enso.py
	$(PY_INTERP) $< --outfile $@

figs/stationary_bias.pdf figs/stationary_variance.pdf	:	src/plot_stationary.py data/stationary.nc
	$(PY_INTERP) $<

figs/trend_bias.pdf figs/trend_variance.pdf	:	src/plot_trend.py data/trend.nc
	$(PY_INTERP) $<

figs/stationary_sequences.pdf	:	src/plot_stationary_sequences.py
	$(PY_INTERP) $<

figs/trend_sequences.pdf	:	src/plot_trend_sequences.py
	$(PY_INTERP) $<

figs/example_long.pdf	: src/plot_example_long.py
	$(PY_INTERP) $<

figs/example_short.pdf	: src/plot_example_short.py
	$(PY_INTERP) $<

plot: figs/enso.pdf figs/stationary_bias.pdf figs/trend_variance.pdf figs/trend_bias.pdf figs/trend_variance.pdf figs/stationary_sequences.pdf figs/trend_sequences.pdf figs/example_short.pdf figs/example_long.pdf

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
