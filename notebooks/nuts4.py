import marimo

__generated_with = "0.23.11"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # NUTS4
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Notes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### EuroStat
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Consider to retrive data from API <br>
    https://ec.europa.eu/eurostat/web/main/data/web-services
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %load_ext autoreload
    # '%autoreload 2' command supported automatically in marimo
    return


@app.cell
def _():
    # %load import.py
    #
    from IPython.display import IFrame

    # 
    import numpy as np
    import pandas as pd

    #
    from datetime import date

    #
    import rioxarray
    import geopandas as gpd
    import rasterio as rio

    #
    from matplotlib import pyplot
    from rasterio.plot import show

    #
    from sqlalchemy import create_engine # query PostGIS
    from sqlalchemy import inspect

    #
    import osmnx as ox

    #
    from shapely.geometry import Polygon, box, MultiPolygon
    import shapely.ops as so

    #
    import json

    #
    import os
    from pathlib import Path
    import fnmatch
    import glob

    #
    from osgeo import gdal

    #
    import random

    #
    import shutil

    #
    from tqdm import tqdm
    import time

    #
    import folium
    from folium import plugins

    return MultiPolygon, create_engine, folium, gpd, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## PostGIS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Study Area
    """)
    return


@app.cell
def _():
    # sa_fil = "italy_center_south.geojson"
    sa_fil = "naples_metropolytan.geojson"
    return (sa_fil,)


@app.cell
def _(gpd, sa_fil):
    sa = gpd.read_file(sa_fil)
    return (sa,)


@app.cell
def _(sa):
    sa.plot()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Get list of NUTS4 within Study Area (sa)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Source: LandSupport DEV
     - reference code is in [LTM_ADVANCED_EU.ipynb](http://192.168.30.11:8888/notebooks/release/work/repo/middleware/api/PPProcessor/jupyter/management/LTM_ADVANCED_EU.ipynb) <br>
     - reference lib in in [psql_lib.ipynb](http://192.168.30.11:8888/notebooks/release/work/repo/middleware/api/PPProcessor/jupyter/lib/psql_lib.ipynb) (which I should download locally as `psql_lib.py`)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Using LandSupport lib | DEPRECATED
    """)
    return


@app.cell
def _():
    from psql_lib import run_qry_read

    return (run_qry_read,)


@app.cell
def _(run_qry_read):
    # test connection
    run_qry_read("SELECT * FROM public.nuts_4_2013 LIMIT 2", "192.168.30.11")
    return


@app.cell
def _(modelQuery, pd, retrieveFromLSDB):
    # == roiNameList ==

    roiList = retrieveFromLSDB(modelQuery)
    roi_df = pd.DataFrame(roiList, columns=["cntr_code","nuts_name","xmin","ymin","xmax","ymax","polygon","area_km2"])
    print("N roi-s:  " + str(len(roi_df)))
    return


@app.cell
def _(LIMIT, NUTS_LEVEL, SELECT, WHERE):
    qry = SELECT + " FROM public.nuts_" + str(NUTS_LEVEL) + "_2013" + " " + \
          WHERE + " " + " ORDER BY cntr_code " + LIMIT
    print(qry)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Using GeoPandas | easiest way
    """)
    return


@app.cell
def _(create_engine, gpd):
    # test connection
    db_connection_url = "postgresql://postgres:4set2000@192.168.30.11:5432/landsupport"
    con = create_engine(db_connection_url)
    sql = "SELECT * FROM public.nuts_4_2013 LIMIT 2"
    df = gpd.read_postgis(sql, con)
    df
    return


app._unparsable_cell(
    r"""
    # https://gis.stackexchange.com/questions/300684/how-get-intersection-of-polygons-in-the-same-table-by-postgis
    SELECT ST_INTERSECTION(a.geom, b.geom), 'fair'
    FROM mytable a, mytable b
    WHERE a.ID < b.ID
    AND ST_INTERSECTS(a.geom, b.geom);
    """,
    name="_"
)


@app.cell
def _(create_engine):
    db_connection_url_1 = 'postgresql://postgres:4set2000@192.168.30.11:5432/landsupport'
    con_1 = create_engine(db_connection_url_1)
    return (con_1,)


@app.cell
def _(sa):
    sa.geometry
    return


app._unparsable_cell(
    r"""
    SELECT *
    	FROM public.nuts_4_2013 a
    	WHERE ST_Intersects( a.geom, ST_GeomFromText('POLYGON((14.361045626349181 41.103914339356834, 
    										13.774994031715778 40.73105495025638, 
    										14.349257232204224 40.467649910920244, 
    										14.92352043269267 40.709356940236546, 
    										14.64733519844043 40.95146172820617, 
    										14.361045626349181 41.103914339356834))',4326)
    					 )
    """,
    name="_"
)


@app.cell
def _(sa):
    sql_1 = "\nSELECT nuts_name,geom\n\tFROM public.nuts_4_2013 a\n\tWHERE ST_Intersects( a.geom, ST_GeomFromText('" + str(sa.geometry[0]) + "',4326)\n\t\t\t\t\t )\n"
    print(sql_1)
    return (sql_1,)


@app.cell
def _(con_1, gpd, sql_1):
    cities_gdf = gpd.read_postgis(sql_1, con_1)
    return (cities_gdf,)


@app.cell
def _(cities_gdf):
    cities_gdf
    return


@app.cell
def _(cities_gdf):
    cities_gdf["nuts_name"][0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Check geometries - lots of MultiPolygons!
    """)
    return


@app.cell
def _(gpd):
    naisc = gpd.read_file("nuts4_sa_nap-ischia.geojson")
    naisc
    return (naisc,)


@app.cell
def _(naisc):
    naisc_e = naisc.explode(index_parts=False)
    naisc_e
    return (naisc_e,)


@app.cell
def _(MultiPolygon, naisc_e):
    geom_mp_na = MultiPolygon(naisc_e.geometry.values)
    geom_mp_na
    return (geom_mp_na,)


@app.cell
def _(geom_mp_na, gpd):
    naisc_mp = gpd.GeoDataFrame({'id':[0],'geometry':[geom_mp_na]}, crs=4326)
    naisc_mp
    return (naisc_mp,)


@app.cell
def _(naisc_mp):
    naisc_mp.to_file("na-isc-multipolygon.geojson")
    return


@app.cell
def _(gpd):
    naisc_mp_1 = gpd.read_file('na-isc-multipolygon.geojson')
    return (naisc_mp_1,)


@app.cell
def _(naisc_mp_1):
    naisc_mp_1.explode(index_parts=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Process geodataframe to get clean Polygons
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The list of geometries got from LandSupport DB has a lot of MultiPolygons where it is actually a Polygon.<br>
    Here I have to convert MultiPolygons into Polygons, if possibile.
    """)
    return


@app.cell
def _():
    #...ToDo
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Search for duplicated nuts4
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It may happen that the same city has two overlapping geometries (see Procida).<br>
    In that case, I need a preliminary check to avoid duplicate nuts4.
    """)
    return


@app.cell
def _():
    #...ToDo
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Save vector data
    """)
    return


@app.cell
def _(cities_gdf):
    cities_gdf.to_file("nuts4_sa_napoli.geojson")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Plot geodataframe - Folium
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    https://www.linkedin.com/pulse/visualize-dem-interactive-map-chonghua-yin/?trk=related_artice_Visualize%20DEM%20in%20An%20Interactive%20Map_article-card_title
    """)
    return


@app.cell
def _(gpd):
    cities_gdf_1 = gpd.read_file('nuts4_sa_napoli.geojson')
    return (cities_gdf_1,)


@app.cell
def _():
    nuts4_idx = 0
    return (nuts4_idx,)


@app.cell
def _(cities_gdf_1, nuts4_idx):
    print(cities_gdf_1.geometry[nuts4_idx])
    return


@app.cell
def _(folium):
    m = folium.Map([40, 14], zoom_start=7, tiles='cartodbpositron')
    folium.GeoJson('naples_metropolytan.geojson').add_to(m)
    folium.LatLngPopup().add_to(m)
    #m.fit_bounds([[xn,yn],[xx,yx]])
    m
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Get list of NUTS4 within Products
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### To be done...
    """)
    return


if __name__ == "__main__":
    app.run()
