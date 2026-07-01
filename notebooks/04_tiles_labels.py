import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # 04 · Tile + Label YOLO

        Taglia il raster di riferimento in tile (con overlap) e per ogni tile
        genera le label YOLO-seg interrogando PostGIS. Parametri: `tiles`.
        """
    )
    return


@app.cell
def _():
    import rasterio as rio
    from impervious.params import load_params
    from impervious import raster, annotate

    P = load_params()
    return P, annotate, raster, rio


@app.cell
def _(mo):
    # imposta il raster di riferimento (granulo Sentinel-2 sulla VM)
    ref_raster = mo.ui.text(
        value="data/S2A_MSIL1C_..._T33TVF_....SAFE/GRANULE/.../IMG_DATA/..._TCI.jp2",
        label="Raster di riferimento (.jp2/.tif)", full_width=True,
    )
    tile_out = mo.ui.text(value="annotations/tiles", label="Cartella tile", full_width=True)
    mo.hstack([ref_raster, tile_out])
    return ref_raster, tile_out


@app.cell
def _(P, raster, ref_raster, rio):
    # overlap intero per un tiling esatto
    with rio.open(ref_raster.value) as _src:
        H, W = _src.shape
    olX, NteX = raster.find_olSize(P.tiles["n_tiles_x"], P.tiles["size"], H)
    olY, NteY = raster.find_olSize(P.tiles["n_tiles_y"], P.tiles["size"], W)
    print(f"olX={olX} NteX={NteX} | olY={olY} NteY={NteY}")
    return NteX, NteY, olX, olY


@app.cell
def _(NteX, NteY, P, olX, olY, raster, ref_raster, tile_out):
    # esegui il tiling (togli il commento per lanciarlo)
    # status = raster.raster_tile_overlap(
    #     ref_raster.value, tile_out.value, "tile",
    #     P.tiles["size"], P.tiles["size"], NteX, NteY, olX, olY,
    # )
    # print(status)
    return


@app.cell
def _(P, annotate, tile_out):
    # genera le label per tutti i tile (interroga PostGIS)
    # n = annotate.tiles_to_labels(
    #     tile_out.value, table=P.osm["postgis_table"],
    #     class_id=P.tiles["class_id"], dst_srid=P.aoi["crs_projected"],
    # )
    # print(f"{n} annotazioni scritte")
    return


if __name__ == "__main__":
    app.run()
