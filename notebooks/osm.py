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
    # OSM
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [Wiki Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API#Building_blocks)
     - [Python Overpass API](https://python-overpy.readthedocs.io/en/latest/example.html)
     - [Loading data from OSM with Python and the Overpass API](https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0)
     - [PyGIS - Accessing OSM data in python](https://pygis.io/docs/d_access_osm.html)
     - [OSM tags Wiki](https://wiki.openstreetmap.org/wiki/Tags)
     - [OSM and urban data, in book "Geospatial Analysis with Python and R"](https://kodu.ut.ee/~kmoch/geopython2021/L4/osm-urban.html)
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

    return Polygon, create_engine, fnmatch, inspect, os, ox


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Retrieve tags
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Get BBox from Selected Products
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Load GeoDF
    """)
    return


@app.cell
def _(geopandas):
    sel_prod_gdf = geopandas.read_file("sel_products.geojson")
    return (sel_prod_gdf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Check GeoDF
    """)
    return


@app.cell
def _(sel_prod_gdf):
    sel_prod_gdf
    return


@app.cell
def _(sel_prod_gdf):
    type(sel_prod_gdf)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TAGS definition
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Buildings
    """)
    return


@app.cell
def _():
    # List key-value pairs for tags
    tags = {'building': True}
    return (tags,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Convert GeoDataFrame geometry (polygon / multipolygon) into Shapely polygon
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Use the Products bounding box | too large | <i style="color:magenta">not working</b>
    """)
    return


@app.cell
def _(sel_prod_gdf):
    x,y = sel_prod_gdf.explode(index_parts=False).geometry[0].exterior.coords.xy
    return x, y


@app.cell
def _(Polygon, x, y):
    sel_prod_pol = Polygon(list(zip(x, y)))
    return (sel_prod_pol,)


@app.cell
def _(sel_prod_pol):
    sel_prod_pol
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Retrieve OSM data
    """)
    return


@app.cell
def _(ox, sel_prod_pol, tags):
    osm_data = ox.features_from_polygon( sel_prod_pol, tags )
    return (osm_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Save OSM data
    """)
    return


@app.cell
def _(osm_data):
    osm_data.to_file("osm_data/buildings.geojson", driver='GeoJSON')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Use the Study Area bounding box | smaller | <i style="color:magenta">not working</b>
    """)
    return


@app.cell
def _(sa):
    x_1, y_1 = sa.explode(index_parts=False).geometry[0].exterior.coords.xy
    return x_1, y_1


@app.cell
def _(Polygon, x_1, y_1):
    sel_prod_pol_1 = Polygon(list(zip(x_1, y_1)))
    return (sel_prod_pol_1,)


@app.cell
def _(sel_prod_pol_1):
    sel_prod_pol_1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Retrieve OSM data
    """)
    return


@app.cell
def _(ox, sel_prod_pol_1, tags):
    osm_data_1 = ox.features_from_polygon(sel_prod_pol_1, tags)
    return (osm_data_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Save OSM data
    """)
    return


@app.cell
def _(osm_data_1):
    osm_data_1.to_file('osm_data/buildings.geojson', driver='GeoJSON')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Use PostGIS cities within Products bounding box
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Retrieve OSM data
    """)
    return


@app.cell
def _(cities_gdf, ox, tags):
    osm_data_2 = ox.features_from_place(cities_gdf['nuts_name'][0], tags)
    return (osm_data_2,)


@app.cell
def _(osm_data_2):
    osm_data_2.head(3).plot()
    return


@app.cell
def _(osm_data_2):
    osm_data_2.head(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Save OSM data
    """)
    return


@app.cell
def _(cities_gdf, osm_data_2):
    _fname = 'osm_data/buildings__' + cities_gdf['nuts_name'][0] + '.geojson'
    osm_data_2.to_file(_fname, driver='GeoJSON')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### OSM data :: BATCH retrieve + save
    """)
    return


@app.cell
def _():
    dir_osmdata = "osm_data/"
    return (dir_osmdata,)


@app.cell
def _(tags):
    tags
    return


@app.cell
def _(ox, tags):
    osm_data_3 = ox.features_from_place('Moschiano', tags)
    return (osm_data_3,)


@app.cell
def _(osm_data_3):
    len(osm_data_3)
    return


@app.cell
def _(cities_gdf, dir_osmdata, fnmatch, os, ox, tags):
    for _row, fields in cities_gdf.iterrows():
        Found = False
        for filename in os.listdir(dir_osmdata):
            if filename.startswith('buildings__'):
                if fnmatch.fnmatch(filename, 'buildings__' + fields[0] + '.geojson'):
                    print('%04d' % _row, '%40s' % fields[0], '  [existent]')
                    Found = True
        if not Found:
            try:
                print('%04d' % _row, '%40s' % fields[0], '  [downloading]')
                osm_data_4 = ox.features_from_place(fields[0], tags)
                if not len(osm_data_4) == 0:
                    _fname = dir_osmdata + 'buildings__' + fields[0] + '.geojson'
                    osm_data_4.to_file(_fname, driver='GeoJSON')
                else:
                    print('%45s' % "Skipped because it's empty.")
            except OSError as err:
                print('  OS error:', err)
            except ValueError:
                print('%45s' % 'Could not find.')
            except Exception as err:
                print(f'  Unexpected err={err!r}, type(err)={type(err)!r}')
                raise
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### OSM data :: MANUAL psql insert
    """)
    return


@app.cell
def _():
    dir_osmdata_1 = 'osm_data/'
    tag = 'buildings'
    _CRS = 4326
    geom_used = ['Polygon', 'MultiPolygon']
    return dir_osmdata_1, geom_used, tag


@app.cell
def _():
    filename_1 = 'buildings__Afragola.geojson'
    return (filename_1,)


@app.cell
def _(filename_1):
    city = filename_1.split('__')[1].split('.geo')[0]
    city
    return (city,)


@app.cell
def _(dir_osmdata_1, filename_1, geopandas):
    #tmp = geopandas.read_file("osm_data/buildings__Lettere.geojson")
    tmp = geopandas.read_file(dir_osmdata_1 + filename_1)
    return (tmp,)


@app.cell
def _(tmp):
    tmp.head(1)
    return


@app.cell
def _(city, tmp):
    tmp[tmp["addr:city"]==city].shape
    return


@app.cell
def _(city, tmp):
    tmp["addr:city"]=city
    return


@app.cell
def _(city, tmp):
    tmp[tmp["addr:city"]==city].shape
    return


@app.cell
def _(geom_used, tmp):
    _geom_types = tmp.geometry.type.unique()
    for _g in _geom_types:
        _nrows = tmp[tmp.geometry.type == _g].shape[0]
        if _g in geom_used:
            print('  > ' + _g + ' [included %d]' % _nrows)
        else:
            print('  > ' + _g + ' [discarded] %d]' % _nrows)
            tmp_1 = tmp.drop(tmp[tmp.geometry.type == _g].index)
    return (tmp_1,)


@app.cell
def _():
    import warnings
    warnings.simplefilter(action='ignore', category=UserWarning) # setting ignore as a parameter and further adding category
    return (warnings,)


@app.cell
def _(warnings):
    warnings.simplefilter(action='default')
    return


@app.cell
def _(WKTElement, tmp_1):
    # this is useless using to_postgis instead of to_sql:
    tmp_1['geometry'] = tmp_1['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))
    return


@app.cell
def _(create_engine):
    _db_connection_url = 'postgresql://giuliano:antonietta@192.168.20.80:65432/osm'
    con = create_engine(_db_connection_url)
    return (con,)


@app.cell
def _(con, inspect):
    # test connection
    inspector = inspect(con)
    print( inspector.get_schema_names() )
    print( inspector.get_table_names( 'public' ) )
    return (inspector,)


@app.cell
def _(inspector):
    tbl_names = inspector.get_table_names( 'public' )
    tbl_names
    return (tbl_names,)


@app.cell
def _(tag, tbl_names):
    if tag in tbl_names:
        print('Found table *%s* in db:OSM schema:public' % tag)
    return


@app.cell
def _(con, tmp_1):
    tmp_1.to_postgis('buildings', con, schema='public', if_exists='append', index=True)  #, dtype={'geometry': Geometry('POLYGON', srid=4326)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### OSM data :: BATCH psql insert
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### fix issues before I could run the bathc procedure below
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ISSUE #01 :: geojson files have different sets of columns
    """)
    return


@app.cell
def _():
    #contact:housenumber
    return


@app.cell
def _(geopandas):
    a = geopandas.read_file("osm_data/buildings__Angri.geojson")
    b = geopandas.read_file("osm_data/buildings__Afragola.geojson")
    return a, b


@app.cell
def _(a):
    a.head(1)
    return


@app.cell
def _(b):
    b.head(1)
    return


@app.cell
def _(a):
    a.shape
    return


@app.cell
def _(b):
    b.shape
    return


@app.cell
def _(a, b):
    ac = list(a.columns)
    bc = list(b.columns)
    return ac, bc


@app.cell
def _(ac):
    ac
    return


@app.cell
def _(bc):
    bc
    return


@app.cell
def _(ac, bc):
    # intersection:
    list(set(ac) & set(bc))
    return


@app.cell
def _(ac, bc):
    # setxor:
    set(ac).symmetric_difference(bc)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Final remark:**
    I decide to keep only few columns to avoid wasting time.
    """)
    return


@app.cell
def _():
    column_used = ['element_type','osmid','nodes','building','addr:city','geometry']
    return (column_used,)


@app.cell
def _(a, column_used):
    a[column_used].shape
    return


@app.cell
def _(b, column_used):
    b[column_used].shape
    return


@app.cell
def _(b):
    c = b.drop(columns='osmid')
    return (c,)


@app.cell
def _(c, column_used):
    c[column_used].shape
    return


@app.cell
def _(c):
    c.shape
    return


@app.cell
def _(c, column_used):
    list( set(list(c.columns)) & set(column_used) )
    return


@app.cell
def _(c, column_used):
    # change a | b | c below in *.columns:
    if len(list( set(list(c.columns)) & set(column_used) )) < len(column_used):
        print('error')
    else:
        print('good')
    return


@app.cell
def _(c, column_used):
    # columns that are missing in c.columns compared to column_used:
    _not_found = list(set(column_used) - set(c.columns))
    _not_found
    return


@app.cell
def _(c):
    c.insert(loc=len(c.columns),column='osmid',value=None)
    return


@app.cell
def _(c, column_used):
    # columns that are missing in c.columns compared to column_used:
    _not_found = list(set(column_used) - set(c.columns))
    _not_found
    return


@app.cell
def _(b, column_used):
    c_1 = b.drop(columns=['osmid', 'nodes'])
    _not_found = list(set(column_used) - set(c_1.columns))
    print(_not_found)
    for _nf in _not_found:
        c_1.insert(loc=len(c_1.columns) - 1, column=_nf, value=None)
    _not_found = list(set(column_used) - set(c_1.columns))
    print(_not_found)
    return (c_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Run BATCH
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Database pgis-osm installed in docker on Pedometrics-VM
    """)
    return


@app.cell
def _():
    dir_osmdata_2 = 'osm_data/'
    tag_1 = 'buildings'
    _CRS = 4326
    geom_used_1 = ['Polygon', 'MultiPolygon']
    column_used_1 = ['element_type', 'osmid', 'nodes', 'building', 'addr:city', 'geometry']
    return column_used_1, dir_osmdata_2, geom_used_1, tag_1


@app.cell
def _(
    c_1,
    column_used_1,
    create_engine,
    dir_osmdata_2,
    geom_used_1,
    geopandas,
    inspect,
    os,
    tag_1,
):
    _row = 0
    tmp_2 = filename_2 = None
    try:
        _db_connection_url = 'postgresql://giuliano:antonietta@192.168.20.80:65432/osm'
        con_1 = create_engine(_db_connection_url)
        inspector_1 = inspect(con_1)
        tbl_names_1 = inspector_1.get_table_names('public')
        if tag_1 in tbl_names_1:
            print('Found table *%s* in db:OSM schema:public' % tag_1)
        else:
            print('Table *%s* not found in db:OSM schema:public' % tag_1)
    except OSError as err:
        print('  OS error:', err)
    except ValueError:
        print('%45s' % 'Could not connect to postGIS')
    except Exception as err:
        print(f'  Unexpected err={err!r}, type(err)={type(err)!r}')
        raise
    for filename_2 in os.listdir(dir_osmdata_2):
        if filename_2.startswith(tag_1 + '__'):
            _row = _row + 1
            try:
                print('%04d' % _row, '%40s' % filename_2, ' ...')
                tmp_2 = geopandas.read_file(dir_osmdata_2 + filename_2)
                _not_found = list(set(column_used_1) - set(tmp_2.columns))
                for _nf in _not_found:
                    print('  > add missing column %s' % _nf)
                    tmp_2.insert(loc=len(tmp_2.columns) - 1, column=_nf, value=None)
                _not_found = list(set(column_used_1) - set(c_1.columns))
                if not len(_not_found) == 0:
                    print('Tag: %s, City: %s :: skipped for issues on missing columns')
                    continue
                tmp_2 = tmp_2[column_used_1]
                city_1 = filename_2.split('__')[1].split('.geo')[0]
                tmp_2['addr:city'] = city_1
                _geom_types = tmp_2.geometry.type.unique()
                for _g in _geom_types:
                    _nrows = tmp_2[tmp_2.geometry.type == _g].shape[0]
                    if _g in geom_used_1:
                        print('  > ' + _g + ' [included %d]' % _nrows)
                    else:
                        print('  > ' + _g + ' [discarded] %d]' % _nrows)
                        tmp_2 = tmp_2.drop(tmp_2[tmp_2.geometry.type == _g].index)
                tmp_2.to_postgis(tag_1, con_1, schema='public', if_exists='append', index=True)
                tmp_2 = None
                print('')
            except OSError as err:
                print('  OS error:', err)
            except ValueError:
                print('%45s' % 'Could not PSQL insert')
            except Exception as err:
                print(f'  Unexpected err={err!r}, type(err)={type(err)!r}')
                raise
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Reproject OSM data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read geojson
    """)
    return


@app.cell
def _(geopandas):
    tmp_3 = geopandas.read_file('osm_data/buildings__Lettere.geojson')
    return (tmp_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Reproject
    """)
    return


@app.cell
def _(tmp_3):
    tmp_4 = tmp_3.to_crs(32633)
    return (tmp_4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remove possible Point geometries
    """)
    return


@app.cell
def _(tmp_4):
    tmp_4.geom_type.unique()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Save geojson (overwrite)
    """)
    return


if __name__ == "__main__":
    app.run()
