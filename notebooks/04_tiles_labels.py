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

        Catena validata: **acquisizione COG → mosaico GeoTIFF (AoI, CRS metrico) →
        tile → label YOLO-seg da PostGIS**. Le operazioni pesanti (scrittura raster,
        tiling, label) sono **commentate**: togli il commento per eseguirle.
        Parametri in `config/pipeline.yaml` (`acquire`, `tiles`, `osm`).
        """
    )
    return


@app.cell
def _():
    import geopandas as gpd
    import rasterio as rio
    from shapely.geometry import box

    from impervious.params import load_params
    from impervious import acquire, raster, annotate

    P = load_params()
    return P, acquire, annotate, box, gpd, raster, rio


@app.cell
def _(P, gpd):
    # AoI (EPSG:4326). Per prove usa un sotto-box, es:
    #   from shapely.geometry import box
    #   aoi = gpd.GeoSeries([box(438000,4517000,443000,4522000)], crs=32633).to_crs(4326).iloc[0]
    sa = gpd.read_file(P.aoi["file"]).to_crs(P.aoi["crs_geographic"])
    aoi = sa.union_all()
    return (aoi,)


@app.cell
def _(P, acquire, aoi):
    # ricerca prodotti (leggera) + config accesso S3 per il provider
    acquire.configure_s3(P.acquire["stac"])
    items = acquire.search_s2(
        aoi, date_from=P.acquire["date_from"], date_to=P.acquire["date_to"],
        max_cloud=P.acquire["max_cloud_cover"], collection=P.acquire["collection"],
        stac=P.acquire["stac"], stac_url=P.acquire["stac_url"],
    )
    print(f"{len(items)} prodotti")
    return (items,)


@app.cell
def _(P, acquire, aoi, items):
    ref_raster = "annotations/aoi_rgb.tif"
    tiles_dir = "annotations/tiles"
    # 1) mosaico AoI -> GeoTIFF metrico (items[:N] = quanti prodotti compositare)
    # acquire.write_raster(items[:1], P.acquire["bands"], ref_raster, aoi=aoi,
    #     resolution=P.acquire["resolution"], crs=f"EPSG:{P.aoi['crs_projected']}", dtype="uint16")
    return ref_raster, tiles_dir


@app.cell
def _(P, raster, ref_raster, tiles_dir):
    # 2) tiling in tile quadrati (griglia semplice; per overlap: raster_tile_overlap + find_olSize)
    # raster.raster_tile(ref_raster, tiles_dir, "tile", P.tiles["size"], P.tiles["size"])
    return


@app.cell
def _(P, annotate, tiles_dir):
    # 3) label YOLO per ogni tile (interroga PostGIS)
    # n = annotate.tiles_to_labels(tiles_dir, table=P.osm["postgis_table"],
    #     class_id=P.tiles["class_id"], dst_srid=P.aoi["crs_projected"])
    # print(f"{n} annotazioni scritte")
    return


if __name__ == "__main__":
    app.run()
