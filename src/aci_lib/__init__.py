"""Read-only access layer over data/processed/, for notebooks (e.g. Colab).

This repository ships code only -- it does not include data/processed/
(too large for git; see the source project's ARCHITECTURE.tex, Section 8.2).
Point this library at a copy of the data (a mounted Drive folder, an
unzipped upload, ...) before calling load():

    import sys
    sys.path.insert(0, "/content/aca_aci_collab/src")
    import aci_lib

    aci_lib.set_data_dir("/content/drive/MyDrive/aca_data/processed")
    aci_lib.list_datasets()                       # browse what's available
    df = aci_lib.load("anomalias_colombia/anomalies_temperature_combined")
    grid = aci_lib.load("anomalias_colombia/anomalies_temperature")  # multi-file NetCDF series

Run locally (inside the repo checkout) set_data_dir() is not needed --
get_data_dir() finds data/processed/ on its own.
"""
import pandas as pd

from .catalog import Dataset, build_catalog
from .config import get_data_dir, set_data_dir
from .loaders import load

__all__ = ["set_data_dir", "get_data_dir", "list_datasets", "describe", "load", "Dataset"]


def list_datasets(base_dir=None, kind=None):
    """Return a DataFrame with one row per loadable dataset (name/kind/n_files/description)."""
    base = base_dir or get_data_dir()
    catalog = build_catalog(base)
    rows = [
        {"name": d.name, "kind": d.kind, "n_files": d.n_files, "description": d.description}
        for d in catalog.values()
    ]
    df = pd.DataFrame(rows, columns=["name", "kind", "n_files", "description"])
    df = df.sort_values("name").reset_index(drop=True)
    if kind:
        df = df[df["kind"] == kind].reset_index(drop=True)
    return df


def describe(name, base_dir=None):
    """Return the Dataset record (name/kind/files/description) for a given dataset name."""
    base = base_dir or get_data_dir()
    catalog = build_catalog(base)
    if name not in catalog:
        raise KeyError(f"No dataset named {name!r}. See aci_lib.list_datasets().")
    return catalog[name]
