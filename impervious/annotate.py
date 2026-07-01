"""Conversione geometrie -> label YOLO-seg e batch di annotazione.

Estratto da annotations.py. Coordinate relative al tile (0..1), origine in alto
a sinistra (y invertita), classe configurabile. Formato riga:
    <class_id> x1 y1 x2 y2 ...   (il vertice di chiusura viene omesso)
"""

from __future__ import annotations

import glob
from pathlib import Path

import numpy as np

from . import db, raster

__all__ = ["geom_to_yolo_lines", "write_label", "tiles_to_labels", "count_labels"]


def _ring_to_line(coords_xy, bbox, class_id: int) -> str:
    xn, yn, xx, yx = bbox
    x, y = np.array(coords_xy)
    xr = (np.array(x) - xn) / (xx - xn)
    yr = (yx - np.array(y)) / (yx - yn)          # y invertita: top = 0
    parts = [str(class_id)]
    for k in range(len(xr) - 1):                  # omette il vertice di chiusura
        parts += [str(xr[k]), str(yr[k])]
    return " ".join(parts)


def geom_to_yolo_lines(geom, bbox, class_id: int = 0) -> list[str]:
    """Righe di label YOLO-seg per una geometria (Polygon o MultiPolygon)."""
    lines: list[str] = []
    if geom.geom_type == "Polygon":
        lines.append(_ring_to_line(geom.exterior.coords.xy, bbox, class_id))
    elif geom.geom_type == "MultiPolygon":
        for g in geom.geoms:
            lines.append(_ring_to_line(g.exterior.coords.xy, bbox, class_id))
    return lines


def write_label(txt_path, lines: list[str]) -> None:
    with open(txt_path, "w") as f:
        for line in lines:
            f.write(line + "\n")


def tiles_to_labels(tile_dir, *, table="buildings", class_id=0, dst_srid=32633,
                    engine=None, skip_existing=True) -> int:
    """Per ogni tile .tif genera il .txt di label interrogando PostGIS.

    Replica il batch di annotations.py: bbox del tile -> geometrie intersecate ->
    dedup -> conversione YOLO -> scrittura .txt. Ritorna il numero di annotazioni.
    """
    engine = engine or db.pg_engine()
    total = 0
    for tif in sorted(glob.glob(str(Path(tile_dir) / "*.tif"))):
        txt = tif[:-4] + ".txt"
        if skip_existing and Path(txt).exists():
            continue
        bbox = raster.tile_bounds(tif)
        res = db.read_geometries_in_bbox(bbox, table=table, engine=engine, dst_srid=dst_srid)
        if len(res) == 0:
            continue
        uniq = res.iloc[db.get_unique_geom_indexes(res.geometry)]
        lines: list[str] = []
        for geom in uniq.geometry:
            lines += geom_to_yolo_lines(geom, bbox, class_id)
        write_label(txt, lines)
        total += len(lines)
    return total


def count_labels(label_dir) -> int:
    """Numero totale di righe (annotazioni) nei .txt di una cartella."""
    n = 0
    for txt in glob.glob(str(Path(label_dir) / "*.txt")):
        with open(txt) as f:
            n += sum(1 for _ in f)
    return n
