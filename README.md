# Density of States (DOS) Convergence Analysis

A computational pipeline for evaluating Density of States (DOS) convergence, volume variations, and numerical data quality across major materials databases: **AFLOW**, **Materials Project (MP)**, **OQMD**, and **NOMAD**.

## Overview

Density Functional Theory (DFT) calculations across public databases can report varying electronic and structural properties for identical materials due to differences in DFT codes, k-point grid densities, and basis-set cutoffs.

This repository provides scripts and Jupyter notebooks to:
* Evaluate numerical errors and convergence quality across electronic-structure calculations.
* Compute electronic structure similarity using spectral fingerprints.
* Reproduce cross-database comparison figures (Figures 1, 4, and 5).

## Repository Structure

* **`ids/`**: Identifier mapping files for target material entries across AFLOW, MP, OQMD, and NOMAD.
  * `database_ids_to_file.py`: Utility script to parse database entry IDs.
* **`notebooks/`**: Analysis and visualization notebooks:
  * `comparing_web_databases_volumes.ipynb`: Reproduces **Figure 1** (unit-cell volume comparisons).
  * `data_quality_assessment.ipynb`: Assesses energy convergence and numerical precision.
  * `analyze_similarity_correlations.ipynb`: Reproduces **Figures 4 & 5** (similarity matrices and correlation clusters).
  * `fingerprint_tuning.ipynb`: Hyperparameter tuning for spectral DOS descriptors.
* **`requirements.txt`**: Python dependencies required to run the pipeline.

## Quick Setup & Execution

### 1. Environment Installation
Run the following commands in your terminal to create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
