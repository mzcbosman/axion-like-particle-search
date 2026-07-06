# Axion-like particle search

This repository contains a collection of small analysis and fitting workflows used for an axion-like particle search study. The folders are organized as self-contained examples for data preparation, blind analysis steps, machine-learning-style reduced datasets, and fitting/optimisation scripts.

## Repository layout

- basic/: simple reduced-data creation and basic analysis examples
- data-blind-creator/: blind-data preparation workflow
- mc-blind-creator/: blind Monte Carlo preparation workflow
- mva-blind/: blinded MVA-style analysis example
- python-true/: additional Python-based analysis pipelines for blind and unblind workflows
- s-optimiser-blind/: trigger/selection optimisation studies for blind analyses

## Getting started

Most subprojects follow the same pattern:

1. Change into the relevant project directory.
2. Source the local setup script if required:
   - `source setup.sh`
3. Run the example entrypoint:
   - `python python/runme.py`

The example data files are stored in each project's `data/` directory.

## Requirements

These workflows are built around:

- Python
- ROOT
- shell setup scripts provided in each subproject

## Notes

The repository is organized as a set of example pipelines rather than a single packaged application. For a first pass, start with the basic examples and then move to the more specialised blind/unblind workflows.
