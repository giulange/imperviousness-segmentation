import marimo

__generated_with = "0.23.11"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        > ⚠️ **DA RISCRIVERE per CDSE.** Questo notebook usa SentinelSat/SciHub,
        > **dismesso**. L'acquisizione va portata sul Copernicus Data Space
        > Ecosystem (`cdsetool` / `pystac-client`, credenziali `CDSE_*` in `.env`).
        > Vedi `MIGRATION.md` §4. Le celle sottostanti NON funzionano finché non
        > sono migrate.
        """
    )
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import subprocess

    return (subprocess,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SentinelSat
     - [GitHub](https://github.com/sentinelsat/sentinelsat)
     - [ReadTheDocs](https://sentinelsat.readthedocs.io/en/stable/api_overview.html#lta-products)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Load
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
    import numpy as np
    import pandas as pd

    #
    from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
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
    from shapely.geometry import Polygon, box
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

    return SentinelAPI, date, geojson_to_wkt, json, read_geojson, rioxarray


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Study Area
    """)
    return


@app.cell
def _():
    # sa_fil = "italy_center_south.geojson"
    sa_fil = "naples_metropolytan.geojson"
    return (sa_fil,)


@app.cell
def _(read_geojson, sa_fil):
    sa_j = read_geojson(sa_fil)
    return (sa_j,)


@app.cell
def _(sa_j):
    type(sa_j)
    return


@app.cell
def _(geopandas, sa_fil):
    sa = geopandas.read_file(sa_fil)
    return (sa,)


@app.cell
def _(sa):
    type(sa)
    return


@app.cell
def _(sa):
    sa.plot()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geospatial raster and Vector data with Python
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [EGU short course 2023](https://github.com/esciencecenter-digital-skills/2023-04-25-ds-geospatial-python-EGU)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Check out `RapidEye time series for Sentinel-2`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [ESA link](https://earth.esa.int/eogateway/catalog/rapideye-time-series-for-sentinel-2)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## PROCEDURE
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Credentials / API
    """)
    return


@app.cell
def _():
    sentinelsat_credentials_file = "sentinelsat_credentials.json"
    return (sentinelsat_credentials_file,)


@app.cell
def _(json, sentinelsat_credentials_file):
    # Opening JSON file
    with open( sentinelsat_credentials_file ) as json_file:
        sensat = json.load(json_file)
 
        # Print the type of data variable
    #    print("Type:", type(data))
 
        # Print the data of dictionary
    #    print("\nUser      :", data['user'])
    #    print("\nPassword  :", data['password'])
    return (sensat,)


@app.cell
def _(sensat):
    user = sensat['user']
    pswd = sensat['password']
    sentinelSat_endpoint = "https://apihub.copernicus.eu/apihub"
    return pswd, sentinelSat_endpoint, user


@app.cell
def _(SentinelAPI, pswd, sentinelSat_endpoint, user):
    api = SentinelAPI(user, pswd, sentinelSat_endpoint)
    return (api,)


@app.cell
def _(api):
    api.session
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Request Sat Products
    """)
    return


@app.cell
def _(date):
    date_FROM = date(2023,4,1)
    date_TO   = date(2023,5,1)
    return date_FROM, date_TO


@app.cell
def _():
    platform_name = "Sentinel-2"
    return (platform_name,)


@app.cell
def _():
    cloud_coverage = (0,10)
    return (cloud_coverage,)


@app.cell
def _(
    api,
    cloud_coverage,
    date_FROM,
    date_TO,
    geojson_to_wkt,
    platform_name,
    sa_j,
):
    # search by polygon, time, and SciHub query keywords
    products = api.query( geojson_to_wkt(sa_j),
                          date = ( date_FROM, date_TO ),
                          platformname = platform_name,
                          cloudcoverpercentage = cloud_coverage
                        )
    return (products,)


@app.cell
def _(products):
    len(products)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### GeoDataFrame from Products
    """)
    return


@app.cell
def _(api, products):
    gdf = api.to_geodataframe(products)
    return (gdf,)


@app.cell
def _(gdf):
    type(gdf)
    return


@app.cell
def _(gdf):
    gdf.head(1)
    return


@app.cell
def _(gdf):
    gdf.plot()
    return


@app.cell
def _(gdf):
    gdf.bounds
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Select Products
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Get the list of first 5 keys:
    """)
    return


@app.cell
def _(products):
    list(products.keys())[0:5]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Select only the first product:
    """)
    return


@app.cell
def _(products):
    sel_products = dict(list(products.items())[:1])
    return (sel_products,)


@app.cell
def _(api, sel_products):
    api.get_product_odata( list(sel_products.keys())[0] )
    return


@app.cell
def _(api, sel_products):
    api.to_geodataframe(sel_products)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Save GeoDF
    """)
    return


@app.cell
def _(api, sel_products):
    sel_prod_gdf = api.to_geodataframe(sel_products)
    return (sel_prod_gdf,)


@app.cell
def _(sel_prod_gdf):
    sel_prod_gdf.to_file("sel_products.geojson",driver="GeoJSON")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Download Selected Products
    """)
    return


@app.cell
def _():
    # Activate only if required:
    # api.download_all(sel_products,directory_path="data/")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Map Selected Products
    """)
    return


@app.cell
def _():
    ras_path_20m = "data/S2A_MSIL1C_20230427T095031_N0509_R079_T33TVF_20230427T115004.SAFE/GRANULE/L1C_T33TVF_A040974_20230427T095813/IMG_DATA/"
    return (ras_path_20m,)


@app.cell
def _(ras_path_20m, rioxarray):
    raster = rioxarray.open_rasterio(ras_path_20m + "T33TVF_20230427T095031_TCI.jp2")
    return (raster,)


@app.cell
def _(raster):
    raster
    return


@app.cell
def _(raster):
    raster.rio.crs
    return


@app.cell
def _(raster):
    raster.plot()
    return


@app.cell
def _(raster):
    raster.plot.imshow()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Get Sentinel-2 tiling grid
    """)
    return


@app.cell
def _(subprocess):
    #! wget https://sentinel.esa.int/documents/247904/1955685/S2A_OPER_GIP_TILPAR_MPC__20151209T095117_V20150622T000000_21000101T000000_B00.kml
    subprocess.call(['wget', 'https://sentinel.esa.int/documents/247904/1955685/S2A_OPER_GIP_TILPAR_MPC__20151209T095117_V20150622T000000_21000101T000000_B00.kml'])
    return


@app.cell
def _(geopandas):
    s2_tile_grid = geopandas.read_file("S2A_OPER_GIP_TILPAR_MPC__20151209T095117_V20150622T000000_21000101T000000_B00.kml")
    return (s2_tile_grid,)


@app.cell
def _(s2_tile_grid):
    s2_tile_grid.head(20).plot()
    return


if __name__ == "__main__":
    app.run()
