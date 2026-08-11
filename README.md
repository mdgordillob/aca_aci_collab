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
| [`notebooks/aca_opt_benchmark.ipynb`](notebooks/aca_opt_benchmark.ipynb) | Clones the *pipeline* repo instead and actually **runs** three of its stages (merge/resample, baseline percentiles, anomalies) against one year of raw ERA5 fetched from Drive, timing each -- see how the pipeline performs on Colab's hardware. `ARCHITECTURE.pdf` §9 explains why no pipeline code changes were needed. |
| [`notebooks/aca_opt_full_replication.ipynb`](notebooks/aca_opt_full_replication.ipynb) | Scales the benchmark up to the real thing: fetches all 64 years of raw temperature grib, runs Stages 1-3 for real (1961-1990 baseline, 1961-2024 anomalies, ~45-90 min), and diffs the result against the official `salidas_colombia` output on Drive to confirm it actually reproduces it. |
| [`notebooks/aca_opt_multi_region_monthly.ipynb`](notebooks/aca_opt_multi_region_monthly.ipynb) | Goes further: temperature + wind + precipitation + drought (all four monthly components `calcular_anomalias_regiones.py` already orchestrates) across the 4 documented regions, sourced entirely from Drive. ~2.5-3.5 hours -- test with a narrow `YEARS` range first. |
| [`USAGE.pdf`](USAGE.pdf) | How-to: setup, full API reference, dataset naming conventions, recipes, troubleshooting (for `aci_lib`; the benchmark notebook is self-documented in its own cells). |
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

The full raw + processed data backing this pipeline -- including the raw
ERA5 `.grib` archive -- lives in a Google Drive folder shared with named
collaborators (not publicly link-shared, which is why anonymous fetching
returns HTTP 401). See `ARCHITECTURE.pdf` §4 and §9.2 for the confirmed
folder structure and where each piece fits in the data flow. `aci_lib`
itself does not read `.grib` files; it only reads `data/processed/`. The
pipeline repo's `src/drive_sync.py` (used by both benchmark notebooks
above) is what actually fetches from Drive, via a mounted
`google.colab.drive` that authenticates as whoever is logged into that
Colab session.
