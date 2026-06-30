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
    # Annotations
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
    #### Create annotations:
     - [Yolov5 documentation](https://docs.ultralytics.com/yolov5/tutorials/train_custom_data/#12-create-labels_1)
     - Satellite image annotation [GitHub](https://github.com/satellite-image-deep-learning/annotation)
       - [IRIS](https://github.com/ESA-PhiLab/iris)
       - [Kili](https://kili-technology.com/data-labeling/best-geospatial-annotation-tool-what-to-look-for-in-software#finding-the-right-geospatial-annotation-tool)
     - Python [split_raster](https://github.com/cuicaihao/split_raster) lib
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Split Raster(s)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [xarray doc](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.to_numpy.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Split Raster(s)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [gdal_translate](https://gdal.org/programs/gdal_translate.html) documentation
     - [test GDAL Translate](https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_gdal_translate_lib.py) code
     - [gdaltest.py](https://github.com/OSGeo/gdal/blob/master/autotest/pymod/gdaltest.py) on GitHub
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

    return (
        Path,
        Polygon,
        create_engine,
        folium,
        gdal,
        glob,
        gpd,
        np,
        os,
        pd,
        pyplot,
        rio,
        rioxarray,
        show,
        so,
        tqdm,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Split Raster(s)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Load GeoDF
    """)
    return


@app.cell
def _(gpd):
    sel_prod_gdf = gpd.read_file("sel_products.geojson")
    return (sel_prod_gdf,)


@app.cell
def _(sel_prod_gdf):
    prod_id = sel_prod_gdf["title"][0]
    prod_id
    return (prod_id,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Reference raster
    """)
    return


@app.cell
def _():
    ref_ras_file = "./data/S2A_MSIL1C_20230427T095031_N0509_R079_T33TVF_20230427T115004.SAFE/GRANULE/L1C_T33TVF_A040974_20230427T095813/IMG_DATA/T33TVF_20230427T095031_TCI.jp2"
    return (ref_ras_file,)


@app.cell
def _(ref_ras_file, rio):
    ref_ras = rio.open( ref_ras_file )
    return (ref_ras,)


@app.cell
def _(ref_ras):
    bbox = ref_ras.bounds
    bbox
    return


@app.cell
def _(ref_ras):
    ref_ras.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Procedure to Split Raster
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### DEF
    """)
    return


@app.cell
def _(ref_ras):
    tileSize = 32*15
    nTilesX = int(ref_ras.shape[0] / tileSize)
    nTilesY = int(ref_ras.shape[1] / tileSize)
    print("Tile size %d x %d." % (tileSize,tileSize))
    print("Grid size %d x %d." % (nTilesX,nTilesY))
    return nTilesX, nTilesY, tileSize


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The condition $Tot \;\%\; tileSize = 0$ must be verified, where <br><br>
    $Tot = (Nte \times tileSize) - (Nte-1)\times olSize$, where Nte = nTiles[X|Y] +1

    The condition above can be written as <br><br>
    $(Nte \times tileSize) - (Nte-1) \times olSize = gridSize$, which for the problem at hand becomes: <br><br>
    $olSize = \frac{(Nte \,\times\, tileSize) \,-\, gridSize}{(Nte\,-\,1)}$
    """)
    return


@app.function
def find_olSize(nTiles,tileSize,gridSize):
    Found = False
    for t in range(30):
        if t > 0:
            # Nte: `Ntiles Extended` to accommodate the overlapping zone
            Nte = nTiles + t
            #print('nTiles: ',Nte)
            Mod = ( (Nte*tileSize) - gridSize ) % (Nte-1)
            if Mod==0:
                Found = True
                olSize = ( (Nte*tileSize) - gridSize ) / (Nte-1)
                #print( '  olSize = %d (found at Nte=%d)' % (olSize,Nte) )
                break

    if not Found:
        return(None,None)
    else:
        return(olSize,Nte)


@app.cell
def _(nTilesX, nTilesY, ref_ras, tileSize):
    olSizeX,NteX = find_olSize(nTilesX,tileSize,ref_ras.shape[0])
    olSizeY,NteY = find_olSize(nTilesY,tileSize,ref_ras.shape[0])
    print("olSizeX=%d , NteX=%d , isCorrect=%d" % (olSizeX,NteX,bool((NteX * tileSize - (NteX-1)*olSizeX) - ref_ras.shape[0] == 0) ))
    print("olSizeY=%d , NteY=%d , isCorrect=%d" % (olSizeY,NteY,bool((NteY * tileSize - (NteY-1)*olSizeY) - ref_ras.shape[1] == 0) ))
    return NteX, NteY, olSizeX, olSizeY


@app.cell
def _(gdal):
    def raster_tile_overlap(ras_file, oPath, tile_base_name, tSx, tSy, NteX, NteY, olSx, olSy):
        dso = gdal.Open(ras_file)
        band = dso.GetRasterBand(1)
        xsize = band.XSize  # ==== GDAL INFO
        ysize = band.YSize
        print('Xsize             :  ' + str(xsize))
        print('Ysize             :  ' + str(ysize))
        print('Output path       :  ' + oPath)
        print('Tile base name    :  ' + tile_base_name + '__i_j.tif')
        print('rmn, rmx          :  ' + 'row min, row max')
        print('cmn, cmx          :  ' + 'col min, col max')
        ii = 0
        for tX in range(NteX):
            ii = ii + 1
            i = tX * (tSx - olSx)  # srcWin = [i,j,tile_size_x,tile_size_y]
            jj = 0
            for tY in range(NteY):
                jj = jj + 1
                _j = tY * (tSy - olSy)
                tile_name_ij = tile_base_name + '__' + str(ii).rjust(3, '0') + '_' + str(jj).rjust(3, '0') + '.tif'
                print('i: %03d j: %03d  -  rmn: %5d rmx: %5d cmn: %5d cmx: %5d' % (ii, jj, i, i + tSx, _j, _j + tSy))
                ds = gdal.Translate(oPath + tile_name_ij, dso, creationOptions=['COMPRESS=LZW', 'NUM_THREADS=ALL_CPUS', 'INTERLEAVE=BAND'], srcWin=[i, _j, tSx, tSy])
                if ds is None:
                    return 'fail::isNotNone - ' + str(i) + ' - ' + str(_j)
                else:
                    ds = None
        dso = None
        return 'success'

    return (raster_tile_overlap,)


@app.cell
def _(gdal):
    def raster_tile(ras_file, oPath, tile_base_name, tile_size_x, tile_size_y):
        dso = gdal.Open(ras_file)
        band = dso.GetRasterBand(1)
        xsize = band.XSize  # ==== GDAL INFO
        ysize = band.YSize
        print('Xsize             :  ' + str(xsize))
        print('Ysize             :  ' + str(ysize))
        print('Output path       :  ' + oPath)
        print('Tile base name    :  ' + tile_base_name + '__i_j.tif')
        print('rmn, rmx          :  ' + 'row min, row max')
        print('cmn, cmx          :  ' + 'col min, col max')
        ii = 0
        for i in range(0, xsize, tile_size_x):
            ii = ii + 1
            jj = 0
            tile_size_x_end = min(tile_size_x, xsize - (ii - 1) * tile_size_x)
            for _j in range(0, ysize, tile_size_y):
                jj = jj + 1
                tile_size_y_end = min(tile_size_y, ysize - (jj - 1) * tile_size_y)
                tile_name_ij = tile_base_name + '__' + str(ii).rjust(3, '0') + '_' + str(jj).rjust(3, '0') + '.tif'
                print('i: %03d j: %03d  -  rmn: %5d rmx: %5d cmn: %5d cmx: %5d' % (ii, jj, i, i + tile_size_x_end, _j, _j + tile_size_y_end))
                ds = gdal.Translate(oPath + tile_name_ij, dso, creationOptions=['COMPRESS=LZW', 'NUM_THREADS=ALL_CPUS', 'INTERLEAVE=BAND'], srcWin=[i, _j, tile_size_x_end, tile_size_y_end])
                if ds is None:
                    return 'fail::isNotNone - ' + str(i) + ' - ' + str(_j)
                else:
                    ds = None
        dso = None
        return 'success'

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Run
    """)
    return


@app.cell
def _(prod_id, tileSize):
    dir_annotation_ras = "annotations/" + str(tileSize) + "x" + str(tileSize) + "/" + prod_id + "/"
    dir_annotation_ras
    return (dir_annotation_ras,)


@app.cell
def _(dir_annotation_ras, os):
    if not os.path.exists( dir_annotation_ras ):
        print("Creating directory %s" % dir_annotation_ras)
        os.makedirs(dir_annotation_ras)
    return


@app.cell
def _():
    #raster_tile(ref_ras_file,dir_annotation_ras,prod_id,610,610)
    return


@app.cell
def _(
    NteX,
    NteY,
    dir_annotation_ras,
    olSizeX,
    olSizeY,
    prod_id,
    raster_tile_overlap,
    ref_ras_file,
    tileSize,
):
    raster_tile_overlap( ref_ras_file , dir_annotation_ras , prod_id , tileSize,tileSize, NteX,NteY, olSizeX,olSizeY)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plot notes
    """)
    return


@app.cell
def _(dir_annotation_ras, prod_id, rioxarray):
    i = 13
    _j = 12
    nr = rioxarray.open_rasterio(dir_annotation_ras + prod_id + '__' + str(i).rjust(3, '0') + '_' + str(_j).rjust(3, '0') + '.tif')
    nr.plot.imshow()
    return (nr,)


@app.cell
def _(nr):
    nr
    return


@app.cell
def _(dir_annotation_ras, rio):
    src = rio.open( dir_annotation_ras + "S2A_MSIL1C_20230427T095031_N0509_R079_T33TVF_20230427T115004__001_001.tif" )
    return (src,)


@app.cell
def _(pyplot, src):
    pyplot.imshow(src.read(1), cmap='pink')
    return


@app.cell
def _(pyplot, show, src):
    _fig, (axr, axg, axb) = pyplot.subplots(1, 3, figsize=(21, 7))
    show((src, 1), ax=axr, cmap='Reds', title='red channel')
    show((src, 2), ax=axg, cmap='Greens', title='green channel')
    show((src, 3), ax=axb, cmap='Blues', title='blue channel')
    pyplot.show()
    return


@app.cell
def _(dir_annotation_ras, pyplot, rio):
    masked = rio.open( dir_annotation_ras + "S2A_MSIL1C_20230427T095031_N0509_R079_T33TVF_20230427T115004__001_001.tif" )
    pyplot.imshow(masked.read(1), cmap='pink')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Split Polygon(s)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [Yolo8 documentation about polygon annotations](https://docs.ultralytics.com/datasets/segment/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Dev code
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *PREMISE*<br>
    I split the raster (110km x 110km) in square tiles of size 610 pixels.<br>
    I inserted all the downloaded geojson OSM tags (only building for now) in postGIS.<br>

    *OBJECTIVE*<br>
    I have to
     - load the bbox of any raster tile
     - intersect in postGIS the ['Polygon','MultiPolygon'] geometries
     - for each geometry, write the correspondent row as `label_id x_1 y_1 x_2 y_2 x_3 y_3 ...`, where
       - label_id: numeric from 0
       - a point Pi(x_i , y_i) has relative coordinates where
         - xmin : left   bbox border =0
         - ymin : top    bbox border =0
         - xmax : right  bbox border =1
         - ymax : bottom bbox border =1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Select GRANULE
    """)
    return


@app.cell
def _(gpd):
    sel_prod_gdf_1 = gpd.read_file('sel_products.geojson')
    return (sel_prod_gdf_1,)


@app.cell
def _(sel_prod_gdf_1):
    prod_id_1 = sel_prod_gdf_1['title'][0]
    prod_id_1
    return (prod_id_1,)


@app.cell
def _(prod_id_1, tileSize):
    dir_annotation_ras_1 = 'annotations/' + str(tileSize) + 'x' + str(tileSize) + '/' + prod_id_1 + '/'
    dir_annotation_ras_1
    return (dir_annotation_ras_1,)


@app.cell
def _(dir_annotation_ras_1, glob):
    f = glob.glob(dir_annotation_ras_1 + '*.tif')
    len(f)
    return (f,)


@app.cell
def _():
    i_1 = 321
    return (i_1,)


@app.cell
def _(f, i_1):
    f[i_1]
    return


@app.cell
def _(f, i_1):
    f[i_1].split('/')[3]
    return


@app.cell
def _(f, i_1, rio):
    src_1 = rio.open(f[i_1])
    return (src_1,)


@app.cell
def _(src_1):
    type(src_1)
    return


@app.cell
def _(src_1):
    src_1
    return


@app.cell
def _(show, src_1):
    show(src_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### GRANULE BBox
    """)
    return


@app.cell
def _(src_1):
    xn, yn, xx, yx = src_1.bounds
    print('Xmin: %8.3f, Xmax: %8.3f, Ymin: %8.3f, Ymax: %8.3f' % (xn, xx, yn, yx))
    return xn, xx, yn, yx


@app.cell
def _(xn, xx):
    dx = xx-xn
    dx
    return


@app.cell
def _(yn, yx):
    dy = yx-yn
    dy
    return


@app.cell
def _(Polygon, xn, xx, yn, yx):
    bb_pol = Polygon([ [xn,yx],[xx,yx],[xx,yn],[xn,yn],[xn,yx] ])
    print(type(bb_pol))
    print(bb_pol)
    bb_pol
    return (bb_pol,)


@app.cell
def _(bb_pol, gpd):
    bb_gdf = gpd.GeoDataFrame(index=[0], crs='epsg:32633', geometry=[bb_pol])
    print(bb_gdf.geometry[0])
    return (bb_gdf,)


@app.cell
def _(xn, xx, yn, yx):
    pol_str = "POLYGON((" + str(xn) + " " + str(yx) + ", " + \
                            str(xx) + " " + str(yx) + ", " + \
                            str(xx) + " " + str(yn) + ", " + \
                            str(xn) + " " + str(yn) + ", " + \
                            str(xn) + " " + str(yx) + "))"
    print(pol_str)
    return (pol_str,)


@app.cell
def _(bb_gdf):
    print(bb_gdf.to_crs(4326).geometry[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Folium map
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    https://www.linkedin.com/pulse/visualize-dem-interactive-map-chonghua-yin/?trk=related_artice_Visualize%20DEM%20in%20An%20Interactive%20Map_article-card_title
    """)
    return


@app.cell
def _(folium):
    m = folium.Map([40, 14], zoom_start=7, tiles='cartodbpositron')
    folium.GeoJson('naples_metropolytan.geojson').add_to(m)
    folium.LatLngPopup().add_to(m)
    #m.fit_bounds([[xn,yn],[xx,yx]])
    m
    return


@app.cell
def _(f):
    from scipy.ndimage import imread
    import imageio
    im = imageio.imread(f[1])
    return


@app.cell
def _(dir_annotation_ras_1, prod_id_1):
    i_2 = 13
    _j = 12
    fil = dir_annotation_ras_1 + prod_id_1 + '__' + str(i_2).rjust(3, '0') + '_' + str(_j).rjust(3, '0') + '.tif'
    return (fil,)


@app.cell
def _(fil, rioxarray):
    # read xarray data
    xad = rioxarray.open_rasterio( fil )
    print(type(xad))
    # convert to numpy array:
    npa = xad.to_numpy()
    print(type(npa))
    return (xad,)


@app.cell
def _(xad):
    xad
    return


@app.cell
def _(fil, rio):
    src_2 = rio.open(fil)
    xn_1, yn_1, xx_1, yx_1 = src_2.bounds
    xc = (xn_1 + xx_1) / 2
    yc = (yn_1 + yx_1) / 2
    return xn_1, xx_1, yn_1, yx_1


@app.cell
def _(IFrame, fil, folium, xn_1, xx_1, yn_1, yx_1):
    m_1 = folium.Map(location=[40.7, 14], zoom_start=9, tiles='cartodbpositron')
    folium.GeoJson('naples_metropolytan.geojson').add_to(m_1)
    folium.LatLngPopup().add_to(m_1)  #tiles="Stamen Terrain"
    folium.raster_layers.ImageOverlay(fil, [[yn_1, xn_1], [yx_1, xx_1]], opacity=0.7).add_to(m_1)
    html_file = 'raster.html'
    m_1.save(html_file)
    # Overlay the image
    IFrame(src=html_file, width=900, height=400)
    return (m_1,)


@app.cell
def _(m_1):
    # if using Spyder.5
    import webbrowser
    m_1.save('test.html')
    webbrowser.open_new_tab('test.html')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### PSQL query to get geometries within the GRANULE BBox
    """)
    return


@app.cell
def _(pol_str):
    qry = """
    SELECT ST_GeometryType(a.geometry),*
        FROM public.buildings a
        WHERE ST_Intersects( ST_Transform(a.geometry,32633), 
                            ST_GeomFromText('""" + pol_str + """',32633))
    """
    print(qry)
    return


@app.cell
def _(sa):
    sql = """
    SELECT nuts_name,geom
    	FROM public.nuts_4_2013 a
    	WHERE ST_Intersects( a.geom, ST_GeomFromText('""" + str(sa.geometry[0]) + """',4326)
    					 )
    """
    sql
    return


@app.cell
def _(pol_str):
    qry_1 = "\nSELECT ST_Intersection(ST_Transform(a.geometry,32633), b.geometry) as geometry\n    FROM public.buildings a JOIN ST_GeomFromText('" + pol_str + "',32633) as b\n    ON ST_Intersects(ST_Transform(a.geometry,32633), b.geometry)\n"
    print(qry_1)
    return (qry_1,)


@app.cell
def _(create_engine):
    _db_connection_url = 'postgresql://giuliano:antonietta@192.168.20.80:65432/osm'
    con = create_engine(_db_connection_url)
    return (con,)


@app.cell
def _(con, gpd, qry_1):
    res = gpd.read_postgis(qry_1, con, geom_col='geometry')
    return (res,)


@app.cell
def _(res):
    type(res)
    return


@app.cell
def _(res):
    geoSeries = res.geometry
    type(geoSeries)
    return


@app.cell
def _(res):
    res.shape
    return


@app.cell
def _(res):
    res.head(2)
    return


@app.cell
def _(res):
    res.geometry[1]
    return


@app.cell
def _(res):
    res.crs
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### remove duplicate geometries
     - Check out [this interesting blog](https://ml-gis-service.com/index.php/2021/09/24/toolbox-drop-duplicated-geometries-from-geodataframe/)
     - Read also [differences between GeoSeries and GeoDataframes](https://geopandas.org/en/stable/docs/user_guide/data_structures.html)

     Do not use **gdf.drop_duplicates** since it works without taking care of the geometries.<br>
     Use the DEF function reported below.
    """)
    return


@app.cell
def _(res):
    cleaned = res.drop_duplicates('geometry')
    return (cleaned,)


@app.cell
def _(cleaned):
    cleaned.shape
    return


@app.cell
def _(cleaned, res):
    res.shape[0] - cleaned.shape[0]
    return


@app.cell
def _(gpd):
    def get_unique_geom_indexes(geoseries: gpd.GeoSeries):
        """
        Function modified from the original one above.
            
        INPUT:
    
        :param geoseries: (gpd.GeoSeries)
    
        OUTPUT:
    
        :returns: (list)
        """
    
        indexes_to_skip = []
        processed_indexes = []
    
        for index, geom in geoseries.items():
            if index not in indexes_to_skip:
                processed_indexes.append(index)
                indexes_to_skip.append(index)
                for other_index, other_geom in geoseries.items():
                    if other_index in indexes_to_skip:
                        pass
                    else:
                        if geom.equals(other_geom):
                            indexes_to_skip.append(other_index)
                        else:
                            pass
        return processed_indexes

    return (get_unique_geom_indexes,)


@app.cell
def _(gpd):
    def drop_duplicated_geometries(geoseries: gpd.GeoSeries):
        """
        Function drops duplicated geometries from a geoseries. It works as follow:
    
            1. Take record from the dataset. Check it's index against list of indexes-to-skip.
            If it's not there then move to the next step.
            2. Store record's index in the list of processed indexes (to re-create geoseries without duplicates)
            and in the list of indexes-to-skip.
            3. Compare this record to all other records. If any of them is a duplicate then store its index in
            the indexes-to-skip.
            4. If all records are checked then re-create dataframe without duplicates based on the list
            of processed indexes.
        
        INPUT:
    
        :param geoseries: (gpd.GeoSeries)
    
        OUTPUT:
    
        :returns: (gpd.Geoseries)
        """
    
        indexes_to_skip = []
        processed_indexes = []
    
        for index, geom in geoseries.items():
            if index not in indexes_to_skip:
                processed_indexes.append(index)
                indexes_to_skip.append(index)
                for other_index, other_geom in geoseries.items():
                    if other_index in indexes_to_skip:
                        pass
                    else:
                        if geom.equals(other_geom):
                            indexes_to_skip.append(other_index)
                        else:
                            pass
        output_gs = geoseries[processed_indexes].copy()
        return output_gs

    return (drop_duplicated_geometries,)


@app.cell
def _(drop_duplicated_geometries, res):
    gs_cleaned = drop_duplicated_geometries(res.geometry)
    return (gs_cleaned,)


@app.cell
def _(gs_cleaned):
    gs_cleaned.shape
    return


@app.cell
def _(get_unique_geom_indexes, res):
    gs_unique = get_unique_geom_indexes(res.geometry)
    return (gs_unique,)


@app.cell
def _(gs_unique):
    len(gs_unique)
    return


@app.cell
def _(res):
    #res2 = res.concat([res.iloc[1],df.loc[:]]).reset_index(drop=True)
    res2 = res
    res2.loc[len(res2)] = res2.iloc[1]
    return (res2,)


@app.cell
def _(res2):
    res2.shape
    return


@app.cell
def _(get_unique_geom_indexes, res2):
    gs_unique_1 = get_unique_geom_indexes(res2.geometry)
    len(gs_unique_1)
    return (gs_unique_1,)


@app.cell
def _(gs_unique_1, res2):
    res2_1 = res2.iloc[gs_unique_1]
    res2_1.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Convert CRS of geometries
    """)
    return


@app.cell
def _(res):
    r = res.to_crs(32633)
    return (r,)


@app.cell
def _(r):
    r
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Convert geospatial coordinates into yolo relative ones
    """)
    return


@app.cell
def _(r):
    r.geometry.type.unique()
    return


@app.cell
def _(r):
    r[r.geometry.type=='MultiPolygon']
    return


@app.cell
def _():
    row=34
    return (row,)


@app.cell
def _(r, row):
    r.geometry[row]
    return


@app.cell
def _(r, row):
    str(r.geometry[row])
    return


@app.cell
def _(r, row):
    r.iloc[[row]]
    return


@app.cell
def _(np, r, xn_1, xx_1, yn_1, yx_1):
    for i_3, row_1 in r.iterrows():
        if row_1.geometry.type == 'Polygon':
            x, y = np.array(row_1.geometry.exterior.coords.xy)
            xr = (np.array(x) - xn_1) / (xx_1 - xn_1)
            yr = (yx_1 - np.array(y)) / (yx_1 - yn_1)
            txt_line = '0 '
            for _j in range(len(xr) - 1):
                txt_line = txt_line + ' ' + str(xr[_j]) + ' ' + str(yr[_j])
            print(txt_line)
        if row_1.geometry.type == 'MultiPolygon':
            _re = row_1.explode()
            for _g in _re.geometry:
                x, y = np.array(_g.exterior.coords.xy)
                xr = (np.array(x) - xn_1) / (xx_1 - xn_1)
                yr = (yx_1 - np.array(y)) / (yx_1 - yn_1)
                txt_line = '0 '
                for _j in range(len(xr) - 1):
                    txt_line = txt_line + ' ' + str(xr[_j]) + ' ' + str(yr[_j])
                print(txt_line)
    return x, y


@app.cell
def _(np, x, xn_1, xx_1, y, yn_1, yx_1):
    xr_1 = (np.array(x) - xn_1) / (xx_1 - xn_1)
    yr_1 = (yx_1 - np.array(y)) / (yx_1 - yn_1)
    return xr_1, yr_1


@app.cell
def _(xr_1, yr_1):
    print(xr_1)
    print(yr_1)
    return


@app.cell
def _(xr_1, yr_1):
    txt_line_1 = '0 '
    for i_4 in range(len(xr_1) - 1):
        txt_line_1 = txt_line_1 + ' ' + str(xr_1[i_4]) + ' ' + str(yr_1[i_4])
    print(txt_line_1)
    return (txt_line_1,)


@app.cell
def _(f):
    ftxt = f[2].split('.tif')[0] + '.txt'
    print(ftxt)
    return (ftxt,)


@app.cell
def _(ftxt, txt_line_1):
    with open(ftxt, 'w') as _txt:
        _txt.write(txt_line_1 + '\n')
    return


@app.cell
def _(r):
    # test annotations
    r.to_file('annotations/test/r.geojson')
    return


@app.cell
def _(np):
    x1 = np.array([0, 0, 1, 1, 0])
    y1 = np.array([0, 1, 1, 0, 0])
    return x1, y1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### explore some plots
    """)
    return


@app.cell
def _(pyplot, x1, xr_1, y1, yr_1):
    _fig, _ax = pyplot.subplots()
    _ax.plot(xr_1, yr_1, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
    _ax.plot(x1, y1)
    _ax.set_title('Polygon')
    pyplot.show()
    return


@app.cell
def _(pyplot, x1, xr_1, y1, yr_1):
    _fig, _ax = pyplot.subplots()
    _ax.plot(xr_1, yr_1, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
    _ax.plot(x1, y1)
    _ax.set_title('Polygon')
    pyplot.show()
    return


@app.cell
def _(f, np, r, xn_1, xx_1, yn_1, yx_1):
    ftxt_1 = f[2].split('.tif')[0] + '.txt'
    with open(ftxt_1, 'w') as _txt:
        for _g in r.geometry:
            x_1, y_1 = np.array(_g.exterior.coords.xy)
            xr_2 = (np.array(x_1) - xn_1) / (xx_1 - xn_1)
            yr_2 = (yx_1 - np.array(y_1)) / (yx_1 - yn_1)
            txt_line_2 = '0 '
            for i_5 in range(len(xr_2) - 1):
                txt_line_2 = txt_line_2 + ' ' + str(xr_2[i_5]) + ' ' + str(yr_2[i_5])
            print(txt_line_2)
            _txt.write(txt_line_2 + '\n')
    return (txt_line_2,)


@app.cell
def _(txt_line_2):
    txt_line_2
    return


@app.function
def pol_square(xn,xx,yn,yx):
    pol_str = "POLYGON((" + str(xn) + " " + str(yx) + ", " + \
                            str(xx) + " " + str(yx) + ", " + \
                            str(xx) + " " + str(yn) + ", " + \
                            str(xn) + " " + str(yn) + ", " + \
                            str(xn) + " " + str(yx) + "))"
    return pol_str


@app.cell
def _(Polygon):
    def Polygon_square(xn,xx,yn,yx):
        pol_str = Polygon([(xn,yx),
                           (xx,yx),
                           (xx,yn),
                           (xn,yn),
                        ])
        return pol_str

    return (Polygon_square,)


@app.cell
def _():
    pol_str_1 = pol_square(0.1, 0.5, 1 - 0.1, 1 - 0.5)
    return


@app.cell
def _(Polygon_square):
    box_1 = Polygon_square(0, 1, 0, 1)
    pol_str_2 = Polygon_square(0.1, 0.5, 1 - 0.1, 1 - 0.5)
    return box_1, pol_str_2


@app.cell
def _(box_1, gpd, pol_str_2, pyplot):
    _p = gpd.GeoSeries(pol_str_2)
    b = gpd.GeoSeries(box_1)
    _p.plot()
    b.plot()
    pyplot.show()
    return


@app.cell
def _(Polygon, gpd, pyplot):
    polygon1 = Polygon([(0, 5), (1, 1), (3, 0)])
    print(polygon1)
    _p = gpd.GeoSeries(polygon1)
    _p.plot()
    pyplot.show()
    return


@app.cell
def _(Path, np):
    from matplotlib.patches import PathPatch
    from matplotlib.collections import PatchCollection

    def plot_polygon(ax, poly, **kwargs):
        path = Path.make_compound_path(Path(np.asarray(poly.exterior.coords)[:, :2]), *[Path(np.asarray(ring.coords)[:, :2]) for ring in poly.interiors])
        patch = PathPatch(path, **kwargs)
        collection = PatchCollection([patch], **kwargs)
        _ax.add_collection(collection, autolim=True)
        _ax.autoscale_view()
        return collection

    return (plot_polygon,)


@app.cell
def _(Polygon, plot_polygon, pyplot):
    import matplotlib.pyplot as plt
    polygon = Polygon(shell=((0, 0), (1, 0), (1, 1), (0, 1)), holes=(((0.1, 0.1), (0.1, 0.5), (0.5, 0.5), (0.5, 0.1)), ((0.9, 0.9), (0.9, 0.5), (0.5, 0.5), (0.5, 0.9))))
    _fig, _ax = pyplot.subplots()
    plot_polygon(_ax, polygon, facecolor='lightblue', edgecolor='red')
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### BATCH processing
    """)
    return


@app.cell
def _(gpd):
    def drop_duplicated_geometries_1(geoseries: gpd.GeoSeries):
        """
        Function drops duplicated geometries from a geoseries. It works as follow:
    
            1. Take record from the dataset. Check it's index against list of indexes-to-skip.
            If it's not there then move to the next step.
            2. Store record's index in the list of processed indexes (to re-create geoseries without duplicates)
            and in the list of indexes-to-skip.
            3. Compare this record to all other records. If any of them is a duplicate then store its index in
            the indexes-to-skip.
            4. If all records are checked then re-create dataframe without duplicates based on the list
            of processed indexes.
        
        INPUT:
    
        :param geoseries: (gpd.GeoSeries)
    
        OUTPUT:
    
        :returns: (gpd.Geoseries)
        """
        indexes_to_skip = []
        processed_indexes = []
        for index, geom in geoseries.items():
            if index not in indexes_to_skip:
                processed_indexes.append(index)
                indexes_to_skip.append(index)
                for other_index, other_geom in geoseries.items():
                    if other_index in indexes_to_skip:
                        pass
                    elif geom.equals(other_geom):
                        indexes_to_skip.append(other_index)
                    else:
                        pass
        output_gs = geoseries[processed_indexes].copy()
        return output_gs

    return


@app.cell
def _(gpd):
    def get_unique_geom_indexes_1(geoseries: gpd.GeoSeries):
        """
        Function modified from the original one above.
            
        INPUT:
    
        :param geoseries: (gpd.GeoSeries)
    
        OUTPUT:
    
        :returns: (list)
        """
        indexes_to_skip = []
        processed_indexes = []
        for index, geom in geoseries.items():
            if index not in indexes_to_skip:
                processed_indexes.append(index)
                indexes_to_skip.append(index)
                for other_index, other_geom in geoseries.items():
                    if other_index in indexes_to_skip:
                        pass
                    elif geom.equals(other_geom):
                        indexes_to_skip.append(other_index)
                    else:
                        pass
        return processed_indexes

    return (get_unique_geom_indexes_1,)


@app.cell
def _(gpd):
    sel_prod_gdf_2 = gpd.read_file('sel_products.geojson')
    sel_prod_gdf_2.iloc[[0]]
    return (sel_prod_gdf_2,)


@app.cell
def _(sel_prod_gdf_2):
    prod_id_2 = sel_prod_gdf_2['title'][0]
    prod_id_2
    return (prod_id_2,)


@app.cell
def _(prod_id_2, tileSize):
    dir_annotation_ras_2 = 'annotations/' + str(tileSize) + 'x' + str(tileSize) + '/' + prod_id_2 + '/'
    dir_annotation_ras_2
    return (dir_annotation_ras_2,)


@app.cell
def _():
    skipExistent = True
    return


@app.cell
def _(glob):
    ftxt_2 = glob.glob('annotations/480x480/S2A_MSIL1C_20230427T095031_N0509_R079_T33TVF_20230427T115004/S2A_MSIL1C_20230427T095031_N0509_R079_T33TVF_20230427T115004__001_007.txt')
    ftxt_2 = ftxt_2[0]
    ftxt_2
    return


@app.cell
def _(
    create_engine,
    dir_annotation_ras_2,
    get_unique_geom_indexes_1,
    glob,
    gpd,
    np,
    rio,
):
    import warnings
    from shapely.errors import ShapelyDeprecationWarning
    warnings.filterwarnings('ignore', category=ShapelyDeprecationWarning)
    _db_connection_url = 'postgresql://giuliano:antonietta@192.168.20.80:65432/osm'
    con_1 = create_engine(_db_connection_url)
    i_6 = -1
    Count = 0
    for f_1 in glob.glob(dir_annotation_ras_2 + '*.tif'):
        ftxt_3 = f_1.split('.tif')[0] + '.txt'
        i_6 = i_6 + 1
        if i_6 >= 0:
            print('%04d\t%s' % (i_6, f_1.split('/')[3]))
            if glob.glob(ftxt_3):
                print('  > SKIP --> %s exists!' % f_1.split('/')[3].replace('.tif', '.txt'))
                continue
            src_3 = rio.open(f_1)
            xn_2, yn_2, xx_2, yx_2 = src_3.bounds
            pol_str_3 = 'POLYGON((' + str(xn_2) + ' ' + str(yx_2) + ', ' + str(xx_2) + ' ' + str(yx_2) + ', ' + str(xx_2) + ' ' + str(yn_2) + ', ' + str(xn_2) + ' ' + str(yn_2) + ', ' + str(xn_2) + ' ' + str(yx_2) + '))'
            qry_2 = "\n        SELECT ST_Intersection(ST_Transform(a.geometry,32633), b.geometry) as geometry\n            FROM public.buildings a JOIN ST_GeomFromText('" + pol_str_3 + "',32633) as b\n            ON ST_Intersects(ST_Transform(a.geometry,32633), b.geometry)\n            ORDER BY a.index\n        "
            res_1 = gpd.read_postgis(qry_2, con_1, geom_col='geometry')
            if len(res_1) == 0:
                print('  > None')
                continue
            else:
                uGidx = get_unique_geom_indexes_1(res_1.geometry)
                print('  > %d of %d duplicate geometries' % (res_1.shape[0] - len(uGidx), res_1.shape[0]))
                r_1 = res_1.iloc[uGidx]
                with open(ftxt_3, 'w') as _txt:
                    for ir, row_2 in r_1.iterrows():
                        if row_2.geometry.type == 'Polygon':
                            x_2, y_2 = np.array(row_2.geometry.exterior.coords.xy)
                            xr_3 = (np.array(x_2) - xn_2) / (xx_2 - xn_2)
                            yr_3 = (yx_2 - np.array(y_2)) / (yx_2 - yn_2)
                            txt_line_3 = '0 '
                            for _j in range(len(xr_3) - 1):
                                txt_line_3 = txt_line_3 + ' ' + str(xr_3[_j]) + ' ' + str(yr_3[_j])
                            _txt.write(txt_line_3 + '\n')
                            Count = Count + 1
                        if row_2.geometry.type == 'MultiPolygon':
                            _re = row_2.explode()
                            for _g in _re.geometry:
                                x_2, y_2 = np.array(_g.exterior.coords.xy)
                                xr_3 = (np.array(x_2) - xn_2) / (xx_2 - xn_2)
                                yr_3 = (yx_2 - np.array(y_2)) / (yx_2 - yn_2)
                                txt_line_3 = '0 '
                                for _j in range(len(xr_3) - 1):
                                    txt_line_3 = txt_line_3 + ' ' + str(xr_3[_j]) + ' ' + str(yr_3[_j])
                                _txt.write(txt_line_3 + '\n')
                                Count = Count + 1
                print('  > %d annotations' % r_1.shape[0])
    print('\nTOT annotations:\n%d.\n' % Count)
    warnings.resetwarnings()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Count all labels
    """)
    return


@app.cell
def _(dir_annotation_ras_2, glob):
    _Nlines = 0
    Ntxt = len(glob.glob(dir_annotation_ras_2 + '*.txt'))
    Ntif = len(glob.glob(dir_annotation_ras_2 + '*.tif'))
    for f_2 in glob.glob(dir_annotation_ras_2 + '*.txt'):
        with open(f_2, 'r') as _txt:
            _Nlines = _Nlines + len(_txt.readlines())
    print('Folder    : ', dir_annotation_ras_2)
    print(' N lines  : ', _Nlines)
    print(' N files  : %d / %d [txt / tif]' % (Ntxt, Ntif))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Double-check annotation geometries
    """)
    return


@app.cell
def _(dir_annotation_ras_2, glob):
    N = len(glob.glob(dir_annotation_ras_2 + '*.txt'))
    print('%d annotation text files found in %s.' % (N, dir_annotation_ras_2))
    return


@app.cell
def _(Polygon, create_engine, dir_annotation_ras_2, glob, gpd, np, rio):
    isel = [0, 77, 170]
    pol2backtransform = 2
    _db_connection_url = 'postgresql://giuliano:antonietta@192.168.20.80:65432/osm'
    con_2 = create_engine(_db_connection_url)
    i_7 = -1
    for f_3 in glob.glob(dir_annotation_ras_2 + '*.txt'):
        i_7 = i_7 + 1
        nLine = 0
        if i_7 in isel:
            print('\n%04d\t%s' % (i_7, f_3.split('/')[2]))
            ftif = f_3.split('.txt')[0] + '.tif'
            src_4 = rio.open(ftif)
            xn_3, yn_3, xx_3, yx_3 = src_4.bounds
            pol_str_4 = 'POLYGON((' + str(xn_3) + ' ' + str(yx_3) + ', ' + str(xx_3) + ' ' + str(yx_3) + ', ' + str(xx_3) + ' ' + str(yn_3) + ', ' + str(xn_3) + ' ' + str(yn_3) + ', ' + str(xn_3) + ' ' + str(yx_3) + '))'
            qry_3 = "\n        SELECT ST_Intersection(ST_Transform(a.geometry,32633), b.geometry) as geometry\n            FROM public.buildings a JOIN ST_GeomFromText('" + pol_str_4 + "',32633) as b\n            ON ST_Intersects(ST_Transform(a.geometry,32633), b.geometry)\n            ORDER BY a.index\n        "
            res_2 = gpd.read_postgis(qry_3, con_2, geom_col='geometry')
            with open(f_3, 'r') as _txt:
                for line in _txt:
                    nLine = nLine + 1
                    if nLine <= pol2backtransform:
                        line = line.replace('\n', '')
                        print('  > %s' % line)
                        xy = line[3:].split(' ')
                        x_3, y_3 = (xy[::2], xy[1::2])
                        xa = np.array(x_3, dtype=float) * (xx_3 - xn_3) + xn_3
                        ya = yx_3 - np.array(y_3, dtype=float) * (yx_3 - yn_3)
                        pol_geom = Polygon(zip(xa, ya))
                        difference = res_2.geometry[nLine - 1] - pol_geom
                        print('    Difference is an empty Polygon: %s' % bool(difference.is_empty))
                        print('    Area:  %.3f - %.3f = %.3f' % (pol_geom.area, res_2.geometry[nLine - 1].area, difference.area))
                        pol = gpd.GeoDataFrame(index=[0], crs='epsg:32633', geometry=[pol_geom])
                        pol.to_file(filename='annotations/pol_backtransformed/' + 'pol' + str(nLine) + '_back__' + f_3.split('.txt')[0].split('/')[2] + '.geojson', driver='GeoJSON')
                        res_2.iloc[[nLine - 1]].to_file(filename='annotations/pol_backtransformed/' + 'pol' + str(nLine) + '_orig__' + f_3.split('.txt')[0].split('/')[2] + '.geojson', driver='GeoJSON')
                        print('')
    return (res_2,)


@app.cell
def _(plt, so):
    def plot_two_polygons(geom0, geom1):
        new_shape = so.unary_union([geom0, geom1])
        _fig, axs = plt.subplots()
        axs.set_aspect('equal', 'datalim')
        i = 0
        for geom in new_shape.geoms:
            xs, ys = geom.exterior.xy
            print('%d - %s' % (i, geom))
            axs.fill(xs, ys, alpha=0.5, fc='black', ec='gray')
            i = i + 1
        plt.show()

    return (plot_two_polygons,)


@app.cell
def _(plot_two_polygons, res_2):
    plot_two_polygons(res_2.geometry[0], res_2.geometry[1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Double-check duplicated annotations
    """)
    return


@app.cell
def _():
    fil_annotated="annotations/imp_class/labels/val/S2A_MSIL1C_20230427T095031_N0509_R079_T33TVF_20230427T115004__013_016.txt"
    fil_annotated
    return (fil_annotated,)


@app.cell
def _(fil_annotated, np, pd, tqdm):
    with open(fil_annotated, 'r') as _txt:
        _Nlines = len(_txt.readlines())
        print('Nlines: ', _Nlines)
    duplicates = pd.DataFrame(columns=['First', 'Second'])
    ii = 0
    with open(fil_annotated, 'r') as _txt:
        for count1, line1 in tqdm(enumerate(_txt)):
            if count1 >= 0:
                xy1 = line1[3:].split(' ')
                with open(fil_annotated, 'r') as txt2:
                    for count2, line2 in enumerate(txt2):
                        if count2 >= 0:
                            xy2 = line2[3:].split(' ')
                            if len(xy1) == len(xy2):
                                if count1 != count2:
                                    d = np.absolute(np.array(xy1, dtype=float) - np.array(xy2, dtype=float))
                                    s = sum(d)
                                    if s == 0:
                                        ii = ii + 1
                                        duplicates = pd.concat([duplicates, pd.DataFrame([[count1, count2]], columns=['First', 'Second'])], ignore_index=True)
    duplicates.drop_duplicates(inplace=True)
    # unable to remove duplicates since they are on two different columns:
    print('Number of duplicate labels %d.' % len(duplicates))  #print(ii, count1, count2, " - sum=",s, " - list ", d)
    return


if __name__ == "__main__":
    app.run()
