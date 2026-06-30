"""impervious — utility condivise per la pipeline di segmentazione imperviousness.

Sostituisce il vecchio pattern `%load import.py` dei notebook (che non funziona
in Marimo). Nei notebook Marimo importa esplicitamente ciò che serve, es.::

    from impervious.config import settings, pg_engine

Il modulo è volutamente leggero: gli import pesanti (gdal, geopandas, ...)
si fanno nelle singole celle, così Marimo traccia correttamente le dipendenze.
"""

from .config import settings, pg_engine, pg_url

__all__ = ["settings", "pg_engine", "pg_url"]
