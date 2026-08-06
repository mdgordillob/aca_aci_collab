"""Scan data/processed/ and group files into loadable datasets.

Most of data/processed/ is either a single tabular/gridded file, or a long
run of per-year or per-year-month NetCDF files that belong to one logical
time series (e.g. anomalias_colombia/anomalies_temperature_1961_1.nc ...
anomalies_temperature_2024_12.nc). This module groups the latter so they
show up as one dataset instead of ~760 separate ones -- see loaders.py for
how each kind actually gets read.
"""
import os
import re
from dataclasses import dataclass, field

_MONTHLY_RE = re.compile(r"^(?P<prefix>.+)_(?P<year>\d{4})_(?P<month>\d{1,2})$")
_YEARLY_RE = re.compile(r"^(?P<prefix>.+)_(?P<year>\d{4})$")

_TABULAR_EXT = {".csv", ".xlsx"}
_GRID_EXT = {".nc"}
_IMAGE_EXT = {".png"}

_SKIP_NAMES = {".gitkeep"}


@dataclass
class Dataset:
    name: str
    kind: str  # "tabular" | "grid" | "grid_series" | "image" | "raw"
    files: list = field(default_factory=list)
    description: str = ""

    @property
    def n_files(self):
        return len(self.files)


def _kind_for_ext(ext):
    if ext in _TABULAR_EXT:
        return "tabular"
    if ext in _GRID_EXT:
        return "grid"
    if ext in _IMAGE_EXT:
        return "image"
    return "raw"


def _join(rel_root, stem):
    if rel_root in (".", ""):
        return stem
    return f"{rel_root.replace(os.sep, '/')}/{stem}"


def build_catalog(base_dir):
    """Walk base_dir and return {dataset_name: Dataset}."""
    from .manifest import describe

    catalog = {}
    for root, _dirs, files in os.walk(base_dir):
        rel_root = os.path.relpath(root, base_dir)
        groups = {}
        singles = []

        for fname in files:
            if fname in _SKIP_NAMES:
                continue
            stem, ext = os.path.splitext(fname)
            ext = ext.lower()
            if ext in _GRID_EXT:
                m = _MONTHLY_RE.match(stem) or _YEARLY_RE.match(stem)
                if m:
                    year = int(m.group("year"))
                    month = int(m.group("month")) if "month" in m.groupdict() and m.group("month") else 0
                    groups.setdefault(m.group("prefix"), []).append((year, month, fname))
                    continue
            singles.append(fname)

        for prefix, entries in groups.items():
            if len(entries) == 1:
                # A single file that happens to match _YYYY[_MM]$ (e.g. a
                # "..._1961_1990.nc" baseline range) isn't really a series --
                # keep its full original name instead of the stripped prefix.
                singles.append(entries[0][2])
                continue
            name = _join(rel_root, prefix)
            # Sort chronologically (year, month), not by filename string --
            # filenames sort "_1, _10, _11, ..., _2" lexicographically.
            paths = [os.path.join(root, fname) for _, _, fname in sorted(entries)]
            catalog[name] = Dataset(name, "grid_series", paths, describe(name))

        for fname in singles:
            stem, ext = os.path.splitext(fname)
            ext = ext.lower()
            name = _join(rel_root, stem)
            catalog[name] = Dataset(name, _kind_for_ext(ext), [os.path.join(root, fname)], describe(name))

    return catalog
