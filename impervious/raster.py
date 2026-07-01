"""Tiling di raster (estratto fedelmente da annotations.py).

- find_olSize: calcola l'overlap intero che rende il tiling esatto
- raster_tile / raster_tile_overlap: taglia il raster in tile via gdal_translate
- tile_bounds: bounds (xn,yn,xx,yx) di un tile
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["find_olSize", "raster_tile", "raster_tile_overlap", "tile_bounds"]

_CREATION_OPTS = ["COMPRESS=LZW", "NUM_THREADS=ALL_CPUS", "INTERLEAVE=BAND"]


def find_olSize(nTiles: int, tileSize: int, gridSize: int):
    """Overlap intero `olSize` e n. tile esteso `Nte` per un tiling esatto.

    Condizione: (Nte*tileSize) - (Nte-1)*olSize == gridSize, con olSize intero.
    Ritorna (olSize, Nte) oppure (None, None) se non trovato entro 30 tentativi.
    """
    for t in range(1, 30):
        Nte = nTiles + t
        if ((Nte * tileSize) - gridSize) % (Nte - 1) == 0:
            olSize = ((Nte * tileSize) - gridSize) // (Nte - 1)
            return olSize, Nte
    return None, None


def raster_tile(ras_file, oPath, tile_base_name, tile_size_x, tile_size_y) -> str:
    """Taglia il raster in tile NON sovrapposti (griglia semplice)."""
    from osgeo import gdal

    oPath = str(oPath).rstrip("/") + "/"
    Path(oPath).mkdir(parents=True, exist_ok=True)
    dso = gdal.Open(str(ras_file))
    xsize = dso.GetRasterBand(1).XSize
    ysize = dso.GetRasterBand(1).YSize
    ii = 0
    for i in range(0, xsize, tile_size_x):
        ii += 1
        jj = 0
        tsx = min(tile_size_x, xsize - (ii - 1) * tile_size_x)
        for j in range(0, ysize, tile_size_y):
            jj += 1
            tsy = min(tile_size_y, ysize - (jj - 1) * tile_size_y)
            name = f"{tile_base_name}__{ii:03d}_{jj:03d}.tif"
            ds = gdal.Translate(oPath + name, dso, creationOptions=_CREATION_OPTS,
                                srcWin=[i, j, tsx, tsy])
            if ds is None:
                return f"fail - {i} - {j}"
            ds = None
    dso = None
    return "success"


def raster_tile_overlap(ras_file, oPath, tile_base_name, tSx, tSy, NteX, NteY, olSx, olSy) -> str:
    """Taglia il raster in tile sovrapposti (overlap olSx/olSy, vedi find_olSize)."""
    from osgeo import gdal

    oPath = str(oPath).rstrip("/") + "/"
    Path(oPath).mkdir(parents=True, exist_ok=True)
    dso = gdal.Open(str(ras_file))
    ii = 0
    for tX in range(NteX):
        ii += 1
        i = tX * (tSx - olSx)
        jj = 0
        for tY in range(NteY):
            jj += 1
            j = tY * (tSy - olSy)
            name = f"{tile_base_name}__{ii:03d}_{jj:03d}.tif"
            ds = gdal.Translate(oPath + name, dso, creationOptions=_CREATION_OPTS,
                                srcWin=[i, j, tSx, tSy])
            if ds is None:
                return f"fail - {i} - {j}"
            ds = None
    dso = None
    return "success"


def tile_bounds(tif_path):
    """Bounds (xn, yn, xx, yx) del tile."""
    import rasterio as rio

    with rio.open(str(tif_path)) as src:
        b = src.bounds
    return b.left, b.bottom, b.right, b.top
