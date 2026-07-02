"""Download OSM (osmnx 2.x) e caricamento in PostGIS. Estratto da osm.py.

osmnx 2.x: `features_from_place` / `features_from_polygon` (ex geometries_from_*).
"""

from __future__ import annotations

import os
from pathlib import Path

import geopandas as gpd

from . import db

__all__ = [
    "BUILDING_TAGS",
    "download_features",
    "batch_download_nuts",
    "harmonize_columns",
    "reproject",
    "load_dir_to_postgis",
]

BUILDING_TAGS = {"building": True}


def download_features(area, tags=BUILDING_TAGS) -> gpd.GeoDataFrame:
    """Scarica le feature OSM per un nome di luogo (str) o un poligono shapely."""
    import osmnx as ox
    from shapely.geometry.base import BaseGeometry

    if isinstance(area, BaseGeometry):
        return ox.features_from_polygon(area, tags)
    return ox.features_from_place(area, tags)


def batch_download_nuts(cities, tags=BUILDING_TAGS, out_dir="osm_data",
                        name_col="nuts_name", skip_existing=True) -> list[str]:
    """Scarica edifici per ogni comune (colonna `name_col`) e salva un GeoJSON.

    Ritorna la lista dei file scritti. Salta i comuni già scaricati o vuoti.
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for _, row in cities.iterrows():
        name = row[name_col]
        fname = Path(out_dir) / f"buildings__{name}.geojson"
        if skip_existing and fname.exists():
            continue
        try:
            gdf = download_features(name, tags)
            if len(gdf):
                gdf.to_file(fname, driver="GeoJSON")
                written.append(str(fname))
        except (OSError, ValueError):
            continue
    return written


def harmonize_columns(gdf: gpd.GeoDataFrame, keep_columns) -> gpd.GeoDataFrame:
    """Uniforma le colonne: tiene solo `keep_columns`, aggiungendo le mancanti a None.

    Serve perché i GeoJSON OSM hanno set di colonne diversi (issue #01 di osm.py).
    """
    out = gdf.copy()
    for col in keep_columns:
        if col not in out.columns:
            out[col] = None
    return out[list(keep_columns)]


def reproject(gdf: gpd.GeoDataFrame, epsg: int) -> gpd.GeoDataFrame:
    return gdf.to_crs(epsg)


def sanitize_for_postgis(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Rende le colonne caricabili in PostGIS.

    - gli ID OSM (osmid) sono a 64 bit -> a testo (evita overflow INTEGER)
    - colonne con liste/dict (es. `nodes`) -> a testo
    """
    out = gdf.copy()
    geom_col = out.geometry.name
    for col in out.columns:
        if col == geom_col:
            continue
        s = out[col]
        if col == "osmid" or s.map(lambda v: isinstance(v, (list, dict))).any():
            out[col] = s.map(lambda v: None if v is None else str(v))
    return out


def load_dir_to_postgis(osm_dir="osm_data", table="buildings", *, engine=None,
                        keep_columns=None) -> int:
    """Carica tutti i buildings__*.geojson di una cartella in PostGIS.

    Ritorna il totale di righe caricate.
    """
    engine = engine or db.pg_engine()
    total = 0
    for fname in sorted(os.listdir(osm_dir)):
        if not (fname.startswith("buildings__") and fname.endswith(".geojson")):
            continue
        gdf = gpd.read_file(Path(osm_dir) / fname)
        if keep_columns:
            gdf = harmonize_columns(gdf, keep_columns)
        gdf = sanitize_for_postgis(gdf)
        gdf.to_postgis(table, engine, schema="public", if_exists="append", index=True)
        total += len(gdf)
    return total
