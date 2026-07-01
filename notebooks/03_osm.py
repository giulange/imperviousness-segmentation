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
        # 03 · OSM → PostGIS

        Scarica gli edifici OSM per ogni comune e li carica in PostGIS.
        Tag, colonne e tabella in `config/pipeline.yaml` → `osm`.
        """
    )
    return


@app.cell
def _():
    import geopandas as gpd
    from impervious.params import load_params
    from impervious import nuts, osm

    P = load_params()
    return P, gpd, nuts, osm


@app.cell
def _(P, gpd, nuts):
    sa = gpd.read_file(P.aoi["file"]).to_crs(P.aoi["crs_geographic"])
    cities = nuts.clean_multipolygons(
        nuts.read_nuts_in_aoi(
            sa.union_all(), table=P.nuts["table"],
            name_col=P.nuts["name_column"], geom_col=P.nuts["geom_column"],
            srid=P.aoi["crs_geographic"],
        )
    )
    return (cities,)


@app.cell
def _(P, cities, osm):
    # scarica i geojson mancanti (salta gli esistenti)
    written = osm.batch_download_nuts(
        cities, tags=P.osm["tags"], out_dir=P.osm["out_dir"],
        name_col=P.nuts["name_column"],
    )
    print(f"{len(written)} nuovi file scaricati")
    return


@app.cell
def _(P, osm):
    # carica tutti i geojson in PostGIS (esegui quando vuoi popolare il DB)
    # n = osm.load_dir_to_postgis(P.osm["out_dir"], table=P.osm["postgis_table"],
    #                             keep_columns=P.osm["keep_columns"])
    # print(f"{n} righe caricate")
    return


if __name__ == "__main__":
    app.run()
