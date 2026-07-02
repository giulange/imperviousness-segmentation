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
        # 01 · Acquisizione Sentinel-2 (STAC + COG)

        Cerca prodotti sull'AoI e legge **solo la finestra AoI** delle bande
        richieste (nessun download dell'intero SAFE). Provider e parametri in
        `config/pipeline.yaml` → `acquire`.
        """
    )
    return


@app.cell
def _():
    import geopandas as gpd
    from impervious.params import load_params
    from impervious import acquire

    P = load_params()
    return P, acquire, gpd


@app.cell
def _(P, gpd):
    sa = gpd.read_file(P.aoi["file"]).to_crs(P.aoi["crs_geographic"])
    aoi = sa.union_all()
    aoi
    return (aoi,)


@app.cell
def _(P, acquire, aoi):
    items = acquire.search_s2(
        aoi,
        date_from=P.acquire["date_from"],
        date_to=P.acquire["date_to"],
        max_cloud=P.acquire["max_cloud_cover"],
        collection=P.acquire["collection"],
        stac=P.acquire["stac"],
        stac_url=P.acquire["stac_url"],
    )
    print(f"{len(items)} prodotti trovati")
    return (items,)


@app.cell
def _(P, acquire, aoi, items):
    # configura l'accesso S3 per il provider (earth-search: pubblico; cdse: chiavi)
    acquire.configure_s3(P.acquire["stac"])
    # lettura finestrata COG delle bande sull'AoI (primo prodotto)
    ds = acquire.load_bands_aoi(
        items[:1],
        P.acquire["bands"],
        aoi,
        resolution=P.acquire["resolution"],
        crs=f"EPSG:{P.aoi['crs_projected']}",
    )
    ds
    return (ds,)


if __name__ == "__main__":
    app.run()
