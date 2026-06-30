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
    # PROCEDURE
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Description
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Define the list of OSM `tags` to be included in the analysis
     - Define a EU study area `sa` by drawing a polygon at [geojson.io](http://geojson.io/#map=2/0/20)
     - Retrive satellite `products` from SentinelSat within `sa`, defining a time slice (fixed?)
     - Get the list of NUTS4 names `nuts_name` (PostGIS or EuroStat) within `sa`
     - Retrive OSM data for all `tags` for each `nuts_name`
     - Create annotations for `DL-model` using (Yolo/any) defined standard
     - Split `train` / `validation` / `testing`
     - Train the `DL-model`
     - Evaluate results on `testing` images
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Links
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - pyGIS :: https://pygis.io/docs/e_new_vectors.html# <br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Libraries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <b style="color:green">NOTES</b> <br>
     - when trying to uninstall you might get permission errors on files, restart the kernel since they could be in use in current notebook
     - ...
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Install
    """)
    return


app._unparsable_cell(
    r"""
    pip install --no-deps pyogrio
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip uninstall -y numpy
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install --no-deps 'numpy==1.21.0'
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip show numpy
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install --no-deps 'pandas<2.0'
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip uninstall -y rioxarray
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install --no-deps rioxarray
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip uninstall -y shapely
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install --no-deps 'shapely==1.8.5'
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip show shapely
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip uninstall -y osmnx
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install --no-deps 'osmnx==1.2.0'
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip show osmnx
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install tqdm
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In order to install gdal I need to firstly install dependencies:

    ```BASH
    sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
    sudo apt-get update
    sudo apt-get install -y gdal-bin
    sudo apt-get install -y libgdal-dev
    export CPLUS_INCLUDE_PATH=/usr/include/gdal
    export C_INCLUDE_PATH=/usr/include/gdal
    ```

    Thenk install from within jupyter notebook:

    ```
    pip install gdal
    ```
    """)
    return


app._unparsable_cell(
    r"""
    pip install gdal
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Installations that must be tested again:
    """)
    return


app._unparsable_cell(
    r"""
    pip install overpy
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install pystac-client
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install pyproj
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install rioxarray
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install splitraster
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install --upgrade ipykernel
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install geoalchemy2
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install --no-deps 'sqlalchemy==1.4.16'
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    pip install gemgis
    """,
    name="_"
)


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
    from IPython.display import IFrame

    # 
    import numpy as np
    import pandas as pd

    #
    from datetime import date

    def read_geojson(path):  # shim per sentinelsat.read_geojson (SciHub dismesso)
        import json
        with open(path) as _f:
            return json.load(_f)

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

    #
    import folium
    from folium import plugins

    return gpd, read_geojson


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Issues
    """)
    return


@app.cell
def _():
    # not working
    import gemgis as gg

    return


@app.cell
def _():
    # not used because the split returns images without CRS
    from splitraster import io

    return


@app.cell
def _():
    # required by to_sql which is not used anymore but the to_postgis function
    #from geoalchemy2 import Geometry, WKTElement
    #from sqlalchemy import *
    return


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
def _(gpd, sa_fil):
    sa = gpd.read_file(sa_fil)
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
    ## Prisma
    https://www.asi.it/scienze-della-terra/prisma/
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SpaceNet
     - https://spacenet.ai/challenges/
     - https://spacenet.ai/sn7-challenge/
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Download data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```BASH
    # run from within Mac terminal after configuring credentials:
    aws s3 cp s3://spacenet-dataset/spacenet/SN7_buildings/tarballs/SN7_buildings_test_public.tar.gz spacenet/SN7/
    aws s3 cp s3://spacenet-dataset/spacenet/SN7_buildings/tarballs/SN7_buildings_train.tar.gz spacenet/SN7/
    aws s3 cp s3://spacenet-dataset/spacenet/SN7_buildings/tarballs/SN7_buildings_train_csvs.tar.gz spacenet/SN7/
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SentinelHub
     - [GitHub](https://github.com/sentinel-hub)
     - [User dashboard](https://apps.sentinel-hub.com/dashboard/#/configurations/92da91b8-dd15-4d37-a6e6-95bea2ef0796)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SentinelSat
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [SentinelSat.ipynb](./sentinelsat.ipynb)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## NUTS4
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [nuts4.ipynb](./nuts4.ipynb)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Open Street Map
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [osm.ipynb](./osm.ipynb)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Annotations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [annotations.ipynb](./annotations.ipynb)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Deep Learning Modeling
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [DL_modeling.ipynb](./DL_modeling.ipynb)
    """)
    return


if __name__ == "__main__":
    app.run()
