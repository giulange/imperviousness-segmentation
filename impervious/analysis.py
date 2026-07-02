"""Studio preliminare: firme spettrali Sentinel-2 vs classe OSM (building).

Ponte tra i COG acquisiti (xarray/odc-stac) e i poligoni OSM in PostGIS:
- building_mask: rasterizza gli edifici sulla griglia dell'immagine
- samples_dataframe: tabella pixel (valori bande + is_building) per l'analisi
- add_indices: indici spettrali comuni (NDVI, NDBI, NDWI)
"""

from __future__ import annotations

import numpy as np

__all__ = ["building_mask", "samples_dataframe", "add_indices"]


def building_mask(gdf, ds):
    """Maschera booleana (True = edificio) allineata alla griglia di `ds`.

    `gdf`: GeoDataFrame di poligoni nello STESSO CRS di `ds` (es. EPSG:32633).
    `ds` : Dataset odc-stac (ha l'accessor `.odc.geobox`).
    """
    import xarray as xr
    from rasterio.features import rasterize

    gb = ds.odc.geobox
    shapes = [
        (g, 1) for g in gdf.geometry
        if g is not None and not g.is_empty and g.geom_type in ("Polygon", "MultiPolygon")
    ]
    arr = (
        rasterize(shapes, out_shape=gb.shape, transform=gb.transform, fill=0, dtype="uint8")
        if shapes else np.zeros(gb.shape, dtype="uint8")
    )
    return xr.DataArray(arr.astype(bool), dims=("y", "x"),
                        coords={"y": ds["y"], "x": ds["x"]}, name="building")


def samples_dataframe(ds, mask, bands, *, max_pixels=200_000, seed=0):
    """DataFrame: una riga per pixel con i valori delle bande + `is_building`.

    Scarta i pixel nodata (tutte bande 0) e sottocampiona a `max_pixels`.
    """
    import pandas as pd

    data = {}
    for b in bands:
        a = ds[b]
        a = a.isel(time=0) if "time" in a.dims else a
        data[b] = np.asarray(a.values).ravel()
    data["is_building"] = np.asarray(mask.values).ravel()
    df = pd.DataFrame(data).dropna()
    df = df[(df[bands] > 0).any(axis=1)]           # via i pixel tutti-nodata
    if len(df) > max_pixels:
        df = df.sample(max_pixels, random_state=seed)
    return df.reset_index(drop=True)


def add_indices(df):
    """Aggiunge NDVI/NDBI/NDWI se le bande necessarie sono presenti."""
    def nd(a, b):
        s = (df[a] + df[b]).replace(0, np.nan)
        # indice normalizzato: limitato a [-1, 1] (evita artefatti da denominatore ~0)
        return ((df[a] - df[b]) / s).clip(-1, 1)

    cols = set(df.columns)
    if {"nir", "red"} <= cols:
        df["NDVI"] = nd("nir", "red")
    if {"swir16", "nir"} <= cols:
        df["NDBI"] = nd("swir16", "nir")
    if {"green", "nir"} <= cols:
        df["NDWI"] = nd("green", "nir")
    return df
