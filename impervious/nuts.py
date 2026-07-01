"""NUTS4 (comuni) da PostGIS entro l'AoI. Estratto da nuts4.py.

Nota: nei notebook originali i NUTS4 venivano da un DB esterno (LandSupport).
Qui la query è la stessa ma l'engine è configurabile (di default il DB su .env).
Se la tabella NUTS non è nel DB principale, passare un `engine`/`db` dedicato
o caricarvi i dati (vedi scripts/postgis).
"""

from __future__ import annotations

import geopandas as gpd

from . import db

__all__ = ["read_nuts_in_aoi", "clean_multipolygons"]


def read_nuts_in_aoi(aoi, *, table="nuts_4_2013", name_col="nuts_name",
                     geom_col="geom", srid=4326, engine=None) -> gpd.GeoDataFrame:
    """Comuni NUTS che intersecano l'AoI.

    `aoi` può essere una geometria shapely o un WKT (in `srid`).
    """
    engine = engine or db.pg_engine()
    aoi_wkt = aoi.wkt if hasattr(aoi, "wkt") else str(aoi)
    qry = f"""
        SELECT {name_col}, {geom_col}
        FROM public.{table} a
        WHERE ST_Intersects(a.{geom_col}, ST_GeomFromText('{aoi_wkt}', {srid}))
    """
    return gpd.read_postgis(qry, engine, geom_col=geom_col)


def clean_multipolygons(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Esplode i MultiPolygon in Polygon singoli (molti NUTS sono MP inutili)."""
    return gdf.explode(index_parts=False).reset_index(drop=True)
