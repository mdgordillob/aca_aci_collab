"""Read a dataset named by aci_lib.list_datasets() into memory."""
import os

from .catalog import build_catalog
from .config import get_data_dir


def _resolve(name, base_dir):
    base = base_dir or get_data_dir()
    catalog = build_catalog(base)
    if name not in catalog:
        raise KeyError(f"No dataset named {name!r}. See aci_lib.list_datasets() for valid names.")
    return catalog[name]


def load(name, base_dir=None):
    """Load a dataset by name.

    Returns a pandas.DataFrame for "tabular" datasets (csv/xlsx), an
    xarray.Dataset for "grid"/"grid_series" datasets (single/multi-file
    NetCDF), and a file path string for "image"/"raw" datasets.
    """
    ds = _resolve(name, base_dir)

    if ds.kind == "tabular":
        import pandas as pd
        path = ds.files[0]
        if path.lower().endswith(".xlsx"):
            return pd.read_excel(path)
        return pd.read_csv(path)

    if ds.kind == "grid":
        import xarray as xr
        return xr.open_dataset(ds.files[0])

    if ds.kind == "grid_series":
        import xarray as xr
        try:
            return xr.open_mfdataset(ds.files, combine="by_coords")
        except (ValueError, KeyError):
            # No shared "time" coordinate to auto-sort by -- ds.files is
            # already in chronological (year, month) order (see catalog.py),
            # so concatenate in that order rather than by filename string.
            return xr.open_mfdataset(ds.files, combine="nested", concat_dim="file")

    if ds.kind in ("image", "raw"):
        return ds.files[0]

    raise ValueError(f"Unknown dataset kind {ds.kind!r} for {name!r}")
