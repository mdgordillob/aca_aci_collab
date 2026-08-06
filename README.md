# aca_aci_collab

Read-only data-access toolkit for outputs of the **Colombian Actuarial
Climate Index (ACI-CO)** pipeline, plus a Google Colab notebook built on
top of it.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mdgordillob/aca_aci_collab/blob/main/notebooks/aci_lib_quickstart.ipynb)

## What's here

| Path | Contents |
|---|---|
| [`src/aci_lib/`](src/aci_lib/) | The library: catalogs `data/processed/` and loads any entry into a `pandas.DataFrame` or `xarray.Dataset` with one function call. |
| [`notebooks/aci_lib_quickstart.ipynb`](notebooks/aci_lib_quickstart.ipynb) | Runs end-to-end in Colab: clone this repo, point `aci_lib` at your data, browse the catalog, load and plot two example datasets. |
| [`USAGE.pdf`](USAGE.pdf) | How-to: setup, full API reference, dataset naming conventions, recipes, troubleshooting. |
| [`ARCHITECTURE.pdf`](ARCHITECTURE.pdf) | Why: the ACI-CO methodology and the pipeline that produced the data this repo reads. |

**Not here:** the data itself. `data/processed/` from the source ACI-CO
project is ~13GB across 8,000+ files -- too large for git -- so every
workflow below starts by pointing `aci_lib` at a copy you supply yourself
(Drive mount, upload, or a local checkout of the source pipeline). See
`USAGE.pdf` §3 for all four options.

## Quickstart

```python
# In Colab:
!git clone --depth 1 https://github.com/mdgordillob/aca_aci_collab.git
import sys
sys.path.insert(0, "/content/aca_aci_collab/src")
import aci_lib

# Point at your data (see USAGE.pdf for Drive-mount / upload alternatives)
aci_lib.set_data_dir("/content/drive/MyDrive/aca_data/processed")

aci_lib.list_datasets()  # browse everything that's loadable

df = aci_lib.load("anomalias_colombia/anomalies_temperature_combined")   # -> pandas.DataFrame
grid = aci_lib.load("anomalias_colombia/anomalies_temperature")          # -> xarray.Dataset
```

Full walkthrough: open the notebook badge above, or read `USAGE.pdf`.

## Source project

This repo is a lightweight companion to the full ACI-CO pipeline (ERA5-Land
reanalysis, ENSO calibration, bootstrap uncertainty bands, UNGRD disaster
validation). `ARCHITECTURE.pdf` documents that pipeline in detail; the
pipeline's own repository is where `data/processed/` and the scripts that
produce it actually live.
