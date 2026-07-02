"""Accesso PostGIS + utilità sulle geometrie (estratte da annotations/nuts/osm).

Nessuna credenziale hardcoded: l'engine viene da impervious.config (che legge
.env). Le query replicano quelle originali dei notebook.
"""

from __future__ import annotations

import geopandas as gpd

from .config import pg_engine

__all__ = [
    "pg_engine",
    "bbox_to_wkt",
    "read_geometries_in_bbox",
    "read_query",
    "load_geojson_to_postgis",
    "get_unique_geom_indexes",
    "drop_duplicated_geometries",
]


def bbox_to_wkt(xn: float, yn: float, xx: float, yx: float) -> str:
    """WKT del rettangolo (ordine orario dall'angolo alto-sinistra), come nei notebook."""
    return (
        f"POLYGON(({xn} {yx}, {xx} {yx}, {xx} {yn}, {xn} {yn}, {xn} {yx}))"
    )


def read_geometries_in_bbox(bbox, table="buildings", *, engine=None,
                            dst_srid=32633, src_srid=4326, geom_col="geometry") -> gpd.GeoDataFrame:
    """Geometrie della `table` che intersecano il bbox, ritagliate e riproiettate.

    `bbox = (xn, yn, xx, yx)` in `dst_srid` (CRS metrico del tile). L'intersezione
    avviene nel CRS nativo `src_srid` (usa l'indice spaziale e NON trasforma tutte
    le geometrie — evita l'errore PROJ "point outside projection domain" su feature
    fuori-zona); solo il bbox e il risultato vengono riproiettati in `dst_srid`.
    `ST_MakeValid` protegge da geometrie non valide.
    """
    engine = engine or pg_engine()
    wkt = bbox_to_wkt(*bbox)
    qry = f"""
        WITH bb AS (
            SELECT ST_Transform(ST_GeomFromText('{wkt}', {dst_srid}), {src_srid}) AS g
        )
        SELECT ST_Transform(
                   ST_Intersection(ST_MakeValid(a.geometry), bb.g), {dst_srid}
               ) AS {geom_col}
        FROM public.{table} a, bb
        WHERE ST_Intersects(a.geometry, bb.g)
    """
    return gpd.read_postgis(qry, engine, geom_col=geom_col)


def read_query(sql: str, *, engine=None, geom_col="geometry") -> gpd.GeoDataFrame:
    """Esegue una query e restituisce un GeoDataFrame."""
    engine = engine or pg_engine()
    return gpd.read_postgis(sql, engine, geom_col=geom_col)


def load_geojson_to_postgis(path, table="buildings", *, engine=None,
                            if_exists="append", index=True) -> int:
    """Carica un GeoJSON in PostGIS. Ritorna il numero di righe caricate."""
    engine = engine or pg_engine()
    gdf = gpd.read_file(path)
    gdf.to_postgis(table, engine, schema="public", if_exists=if_exists, index=index)
    return len(gdf)


def get_unique_geom_indexes(geoseries: gpd.GeoSeries) -> list:
    """Indici delle geometrie uniche (confronto geometrico, non testuale).

    Estratta da annotations.py — necessaria perché `drop_duplicates` non tiene
    conto della geometria.
    """
    indexes_to_skip: list = []
    processed_indexes: list = []
    for index, geom in geoseries.items():
        if index not in indexes_to_skip:
            processed_indexes.append(index)
            indexes_to_skip.append(index)
            for other_index, other_geom in geoseries.items():
                if other_index not in indexes_to_skip and geom.equals(other_geom):
                    indexes_to_skip.append(other_index)
    return processed_indexes


def drop_duplicated_geometries(geoseries: gpd.GeoSeries) -> gpd.GeoSeries:
    """Rimuove le geometrie duplicate da una GeoSeries (vedi get_unique_geom_indexes)."""
    return geoseries.iloc[get_unique_geom_indexes(geoseries)]
