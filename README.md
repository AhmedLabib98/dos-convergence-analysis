# Examples for the MADAS code

This repository contains examples for the paper: 

Martin Kuban, Santiago Rigamonti, and Claudia Draxl:  
MADAS: a Python framework for assessing similarity in materials-science data  
*Digital Discovery* **3**, (2024), 2448-2457  

## Installation

Please execute:

```bash
pip install -r requirements.txt
```

## Usage

To execute the examples, run:

```bash
jupyter notebook
```

and open the notebooks in the folder `notebooks`.

Alternatively, you can generate a `pdf` version via:

```bash
jupyter nbconvert --to pdf --execute notebooks/*.ipynb
```

## Notes

To run the notebook: "comparing_web_databases_volumes.ipynb", please set an environmental variable with your API access key for the Materials Project database before starting Jupyter:

```bash
export MP_API_KEY=<YOUR_KEY>
```

## Results

Full 161-material production run: **148/161 materials fully converged** (13 incomplete).

See the [full results table](results/full_run/RESULTS_TABLE.md) for a per-material breakdown with ✅/❌ status.
