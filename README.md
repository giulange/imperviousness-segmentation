# imperviousness-segmentation
Develop DL imperviousness segmentation using Remote Sensing data

## Notes - after egu23

### CVAT 
Use it for annotations.

### OSM
Get labeled maps to be filtered and then labeled as expected by the YOLO model

#### List of tags

 - https://wiki.openstreetmap.org/wiki/Map_features

#### extract urban from OSM data
 
 - *** https://kodu.ut.ee/~kmoch/geopython2021/L4/osm-urban.html
 - **** https://pygis.io/docs/d_access_osm.html
 - https://geoffboeing.com/2017/04/urban-form-analysis-openstreetmap/
 



#### Downloading data
Get the best of data retrievement from these tutorials:
 - [towardsDataScience](https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0)
   - I can use [native OSM API](https://wiki.openstreetmap.org/wiki/API), or
   - overpass API: [Documentation](https://python-overpy.readthedocs.io/en/latest/) , [Germany](http://overpass-api.de/)
   - there are 3 basic components in the OSM data model:
     - node: point
     - way: lines and polygons
     - relation: order list of nodes, ways and/or relations
 - [using the OSMnx](https://pygis.io/docs/d_access_osm.html)


 - https://wiki.openstreetmap.org/wiki/Downloading_data
   - you can consider the [Planet.osm](https://wiki.openstreetmap.org/wiki/Planet.osm)




### YOLO
...see repo and the preparation made on Agritech-GCI VM.

