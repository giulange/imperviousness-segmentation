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
        # 02 · AoI + NUTS4

        Legge l'area di studio e i comuni (NUTS4) che la intersecano da PostGIS.
        """
    )
    return


@app.cell
def _():
    import geopandas as gpd
    from impervious.params import load_params
    from impervious import nuts

    P = load_params()
    return P, gpd, nuts


@app.cell
def _(P, gpd):
    sa = gpd.read_file(P.aoi["file"]).to_crs(P.aoi["crs_geographic"])
    aoi = sa.union_all()
    sa.plot()
    return (aoi,)


@app.cell
def _(P, aoi, nuts):
    cities = nuts.read_nuts_in_aoi(
        aoi,
        table=P.nuts["table"],
        name_col=P.nuts["name_column"],
        geom_col=P.nuts["geom_column"],
        srid=P.aoi["crs_geographic"],
    )
    cities_clean = nuts.clean_multipolygons(cities)
    print(f"{len(cities_clean)} comuni")
    return (cities_clean,)


@app.cell
def _(cities_clean):
    cities_clean.plot()
    return


if __name__ == "__main__":
    app.run()
