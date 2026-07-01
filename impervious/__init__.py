"""impervious — pacchetto di operazioni riusabili della pipeline.

Logica estratta dai notebook (niente più codice/credenziali inline). I notebook
Marimo importano da qui:

    from impervious.params import load_params
    from impervious import acquire, nuts, osm, db, raster, annotate, dataset, model
    from impervious.config import settings, pg_engine

Sottomoduli:
  config    credenziali/segreti da .env
  params    parametri pipeline da config/pipeline.yaml
  acquire   Sentinel-2 via STAC + COG (CDSE / Earth Search / PC)
  nuts      NUTS4 (comuni) da PostGIS entro l'AoI
  osm       download OSM (osmnx) + load PostGIS
  db        query PostGIS + utilità geometrie (dedup, bbox)
  raster    tiling raster (find_olSize, raster_tile[_overlap])
  annotate  geometrie -> label YOLO-seg (batch tiles_to_labels)
  dataset   split train/val/test + data.yaml
  model     training/inferenza YOLO-seg (con gestione slice MIG)
"""

from .config import pg_engine, pg_url, settings
from .params import load_params

__all__ = ["settings", "pg_engine", "pg_url", "load_params"]
