import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Pipeline (onnicomprensivo)

    Notebook di **sviluppo della pipeline end-to-end**: acquisizione →
    AoI/NUTS → OSM → tile+label → dataset → training. I notebook `00`–`06`
    restano per esplorazione/test dei singoli step; questo li mette in fila.

    Le operazioni pesanti (download, tiling, training) sono **commentate**:
    togli il commento allo step che vuoi eseguire. Logica e parametri stanno
    in `impervious/` e `config/pipeline.yaml` — qui si orchestra soltanto.
    """)
    return


@app.cell
def _():
    import geopandas as gpd
    import rasterio as rio

    from impervious.params import load_params
    from impervious.config import settings, pg_engine
    from impervious import acquire, nuts, osm, db, raster, annotate, dataset, model

    P = load_params()
    return P, acquire, gpd, nuts


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · AoI
    """)
    return


@app.cell
def _(P, gpd):
    sa = gpd.read_file(P.aoi["file"]).to_crs(P.aoi["crs_geographic"])
    aoi = sa.union_all()
    sa.plot()
    return (aoi,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · Acquisizione Sentinel-2 (STAC + COG)
    """)
    return


@app.cell
def _(P, acquire, aoi):
    s2_items = acquire.search_s2(
        aoi, date_from=P.acquire["date_from"], date_to=P.acquire["date_to"],
        max_cloud=P.acquire["max_cloud_cover"], collection=P.acquire["collection"],
        stac=P.acquire["stac"], stac_url=P.acquire["stac_url"],
    )
    print(f"{len(s2_items)} prodotti")
    # acquire.configure_s3(P.acquire["stac"])
    # s2_ds = acquire.load_bands_aoi(s2_items[:1], P.acquire["bands"], aoi,
    #     resolution=P.acquire["resolution"], crs=f"EPSG:{P.aoi['crs_projected']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 · NUTS4 + OSM → PostGIS
    """)
    return


@app.cell
def _(P, aoi, nuts):
    cities = nuts.clean_multipolygons(
        nuts.read_nuts_in_aoi(
            aoi, table=P.nuts["table"], name_col=P.nuts["name_column"],
            geom_col=P.nuts["geom_column"], srid=P.aoi["crs_geographic"],
        )
    )
    print(f"{len(cities)} comuni")
    return


@app.cell
def _():
    # osm.batch_download_nuts(cities, tags=P.osm["tags"], out_dir=P.osm["out_dir"],
    #                         name_col=P.nuts["name_column"])
    # osm.load_dir_to_postgis(P.osm["out_dir"], table=P.osm["postgis_table"],
    #                         keep_columns=P.osm["keep_columns"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 · Tile + Label YOLO
    """)
    return


@app.cell
def _():
    ref_raster = "data/REFERENCE_GRANULE_TCI.jp2"   # granulo S2 sulla VM
    tiles_dir = "annotations/tiles"
    # with rio.open(ref_raster) as _s: H, W = _s.shape
    # olX, NteX = raster.find_olSize(P.tiles["n_tiles_x"], P.tiles["size"], H)
    # olY, NteY = raster.find_olSize(P.tiles["n_tiles_y"], P.tiles["size"], W)
    # raster.raster_tile_overlap(ref_raster, tiles_dir, "tile", P.tiles["size"],
    #     P.tiles["size"], NteX, NteY, olX, olY)
    # annotate.tiles_to_labels(tiles_dir, table=P.osm["postgis_table"],
    #     class_id=P.tiles["class_id"], dst_srid=P.aoi["crs_projected"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · Dataset + 6 · Training
    """)
    return


@app.cell
def _(P):
    ds_root = f"datasets/{P.dataset['name']}"
    ds_yaml = f"datasets/{P.dataset['name']}.yaml"
    # dataset.split_train_val_test(tiles_dir, ds_root, ratios=P.dataset["split"],
    #     seed=P.dataset["seed"])
    # dataset.write_data_yaml(ds_yaml, ds_root, P.dataset["classes"])
    # model.train(ds_yaml, model=P.train["model"], epochs=P.train["epochs"],
    #     imgsz=P.train["imgsz"], batch=P.train["batch"], workers=P.train["workers"],
    #     cache=P.train["cache"], mig_uuid=model.first_mig_uuid())
    return


if __name__ == "__main__":
    app.run()
