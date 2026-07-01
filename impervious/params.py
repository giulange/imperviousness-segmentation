"""Caricamento dei parametri della pipeline da YAML (config/pipeline.yaml).

I parametri (non segreti) vivono in un unico YAML; i segreti restano in .env
(vedi impervious.config). Uso::

    from impervious.params import load_params
    P = load_params()
    P.tiles["size"]          # accesso tipo attributo o dizionario
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import yaml

_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PARAMS = _ROOT / "config" / "pipeline.yaml"


class Params(SimpleNamespace):
    """Contenitore dei parametri: accesso sia `P.tiles` sia `P["tiles"]`."""

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)


def load_params(path: str | Path = DEFAULT_PARAMS) -> Params:
    """Legge il YAML dei parametri e lo restituisce come `Params`."""
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return Params(**data)
