"""Locate the data/processed/ directory that aci_lib reads from.

This repository ships code only -- a plain `git clone` (e.g. in Google
Colab) never contains data/processed/, it's too large for git. Call
set_data_dir() with wherever the data actually lives (a mounted Drive
folder, an unzipped upload, ...) before using the rest of aci_lib. Running
against a local checkout of the source project (which does have
data/processed/ on disk, just gitignored), get_data_dir() finds it on its
own by walking up from this file to the nearest repo root.
"""
import os

_ENV_VAR = "ACI_DATA_DIR"
_ROOT_MARKERS = (".git", "CLAUDE.md")

_data_dir = None


def _find_repo_root(start):
    path = os.path.abspath(start)
    while True:
        if any(os.path.exists(os.path.join(path, m)) for m in _ROOT_MARKERS):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def set_data_dir(path):
    """Point aci_lib at a data/processed directory for the rest of the session."""
    global _data_dir
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Not a directory: {path}")
    _data_dir = path


def get_data_dir():
    """Return the currently configured data/processed directory.

    Resolution order: an explicit set_data_dir() call, the ACI_DATA_DIR
    environment variable, then an auto-detected repo-relative data/processed/.
    """
    if _data_dir is not None:
        return _data_dir

    env = os.environ.get(_ENV_VAR)
    if env:
        return env

    here = os.path.dirname(os.path.abspath(__file__))
    root = _find_repo_root(here)
    if root:
        candidate = os.path.join(root, "data", "processed")
        if os.path.isdir(candidate):
            return candidate

    raise FileNotFoundError(
        "Could not find data/processed/. This repository does not include "
        "it (too large for git). In Colab: upload or mount the data "
        "yourself, then call aci_lib.set_data_dir('/path/to/data/processed') "
        "or set the ACI_DATA_DIR environment variable."
    )
