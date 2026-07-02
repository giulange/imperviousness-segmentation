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
        # 07 · Studio firme spettrali — Sentinel-2 vs OSM `building`

        Su una AoI piccola: acquisisce le bande multispettrali (COG), rasterizza
        gli edifici OSM (da PostGIS) sulla griglia dell'immagine, campiona i pixel
        e confronta **edificio vs sfondo** (firma spettrale, indici, anteprima).
        Parametri in `config/pipeline.yaml` → `analysis`.
        """
    )
    return


@app.cell
def _():
    import geopandas as gpd
    import numpy as np
    import matplotlib.pyplot as plt
    from shapely.geometry import box

    from impervious.params import load_params
    from impervious import acquire, db, analysis

    P = load_params()
    BANDS = P.analysis["bands"]
    return BANDS, P, acquire, analysis, box, db, gpd, np, plt


@app.cell
def _(P, box, gpd):
    # AoI di studio: box in EPSG:32633 (metrico) -> versione 4326 per la ricerca STAC
    xn, yn, xx, yx = P.analysis["study_box_32633"]
    bbox32633 = (xn, yn, xx, yx)
    aoi4326 = gpd.GeoSeries([box(xn, yn, xx, yx)], crs=32633).to_crs(4326).iloc[0]
    return aoi4326, bbox32633


@app.cell
def _(BANDS, P, acquire, aoi4326):
    # acquisizione multispettrale finestrata sull'AoI (prima scena disponibile)
    acquire.configure_s3(P.acquire["stac"])
    items = acquire.search_s2(
        aoi4326, date_from=P.acquire["date_from"], date_to=P.acquire["date_to"],
        max_cloud=P.analysis["max_cloud_cover"], collection=P.acquire["collection"],
        stac=P.acquire["stac"], stac_url=P.acquire["stac_url"],
    )
    ds = acquire.load_bands_aoi(items[:1], BANDS, aoi4326,
                               resolution=P.acquire["resolution"], crs="EPSG:32633")
    print(f"scena: {items[0].id} | bande: {BANDS} | griglia: {dict(ds.sizes)}")
    return (ds,)


@app.cell
def _(bbox32633, db):
    # edifici OSM che intersecano l'AoI (da PostGIS, in EPSG:32633)
    buildings = db.read_geometries_in_bbox(bbox32633, table="buildings", dst_srid=32633)
    print(f"{len(buildings)} geometrie edificio nell'AoI")
    return (buildings,)


@app.cell
def _(BANDS, analysis, buildings, ds):
    mask = analysis.building_mask(buildings, ds)
    df = analysis.add_indices(analysis.samples_dataframe(ds, mask, BANDS))
    n_b = int(df["is_building"].sum())
    print(f"pixel campionati: {len(df)} | edificio: {n_b} ({100*n_b/len(df):.1f}%)")
    return df, mask


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Firma spettrale media (edificio vs sfondo)""")
    return


@app.cell
def _(BANDS, df, plt):
    _means = df.groupby("is_building")[BANDS].mean()
    _fig, _ax = plt.subplots(figsize=(7, 4))
    for _cls, _lbl, _c in [(True, "edificio", "#d62728"), (False, "sfondo", "#2ca02c")]:
        if _cls in _means.index:
            _ax.plot(BANDS, _means.loc[_cls].values, marker="o", label=_lbl, color=_c)
    _ax.set_ylabel("riflettanza (DN, ×1e-4)"); _ax.set_xlabel("banda")
    _ax.set_title("Firma spettrale media"); _ax.legend(); _ax.grid(alpha=0.3)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Separabilità: NDVI vs NDBI""")
    return


@app.cell
def _(df, plt):
    _fig, _ax = plt.subplots(figsize=(6, 5))
    if {"NDVI", "NDBI"} <= set(df.columns):
        _s = df.sample(min(5000, len(df)), random_state=0)
        for _cls, _lbl, _c in [(False, "sfondo", "#2ca02c"), (True, "edificio", "#d62728")]:
            _m = _s["is_building"] == _cls
            _ax.scatter(_s[_m]["NDVI"], _s[_m]["NDBI"], s=4, alpha=0.4, label=_lbl, color=_c)
        _ax.set_xlabel("NDVI"); _ax.set_ylabel("NDBI"); _ax.legend(); _ax.grid(alpha=0.3)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Anteprima RGB + maschera edifici""")
    return


@app.cell
def _(ds, mask, np, plt):
    def _norm(a):
        a = np.asarray(a, dtype="float32")
        lo, hi = np.nanpercentile(a, [2, 98])
        return np.clip((a - lo) / (hi - lo + 1e-6), 0, 1)

    _sel = lambda b: (ds[b].isel(time=0) if "time" in ds[b].dims else ds[b]).values
    _rgb = np.dstack([_norm(_sel("red")), _norm(_sel("green")), _norm(_sel("blue"))])
    _fig, _axs = plt.subplots(1, 2, figsize=(11, 5))
    _axs[0].imshow(_rgb); _axs[0].set_title("RGB"); _axs[0].axis("off")
    _axs[1].imshow(_rgb); _axs[1].imshow(np.ma.masked_where(~mask.values, mask.values),
                                         cmap="autumn", alpha=0.6)
    _axs[1].set_title("edifici OSM"); _axs[1].axis("off")
    _fig
    return


if __name__ == "__main__":
    app.run()
