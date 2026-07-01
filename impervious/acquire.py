"""Acquisizione Sentinel-2 via STAC + lettura COG finestrata sull'AoI.

Sostituisce sentinelsat/SciHub (dismesso). Provider supportati (config `acquire.stac`):
  - cdse               : Copernicus Data Space Ecosystem (ufficiale ESA). Asset
                         JP2 in SAFE su S3 EODATA -> serve GDAL configurato con le
                         chiavi S3 (CDSE_S3_* in .env, vedi configure_cdse_s3()).
  - earth-search       : Element84 su AWS Open Data (S2 L2A COG pubblici, no auth).
  - planetary-computer : Microsoft PC (S2 L2A COG, firma via token).

Il vantaggio STAC+COG: si legge SOLO la finestra AoI delle bande richieste, senza
scaricare l'intero SAFE (~800 MB).
"""

from __future__ import annotations

import os

from .config import settings

__all__ = ["configure_cdse_s3", "stac_client", "search_s2", "load_bands_aoi",
           "download_product"]


def configure_cdse_s3() -> None:
    """Configura GDAL/rasterio per leggere gli asset S3 EODATA del CDSE."""
    os.environ.setdefault("AWS_S3_ENDPOINT", "eodata.dataspace.copernicus.eu")
    os.environ.setdefault("AWS_VIRTUAL_HOSTING", "FALSE")
    os.environ.setdefault("AWS_HTTPS", "YES")
    if settings.cdse_s3_access_key:
        os.environ["AWS_ACCESS_KEY_ID"] = settings.cdse_s3_access_key
    if settings.cdse_s3_secret_key:
        os.environ["AWS_SECRET_ACCESS_KEY"] = settings.cdse_s3_secret_key


def stac_client(stac: str, url: str):
    """Apre un client STAC. Per 'planetary-computer' applica il modifier di firma."""
    import pystac_client

    if stac == "planetary-computer":
        import planetary_computer as pc

        return pystac_client.Client.open(url, modifier=pc.sign_inplace)
    return pystac_client.Client.open(url)


def search_s2(aoi, *, date_from, date_to, max_cloud=10, collection="SENTINEL-2",
              stac="cdse", stac_url="https://catalogue.dataspace.copernicus.eu/stac",
              processing_level="L2A", limit=50):
    """Cerca prodotti Sentinel-2 che coprono l'AoI nel periodo dato.

    `aoi`: geometria shapely (in EPSG:4326). Ritorna la lista di STAC Item.
    """
    client = stac_client(stac, stac_url)
    # filtro nuvole: la chiave differisce per provider
    query = {"eo:cloud_cover": {"lt": max_cloud}}
    if stac == "cdse":
        query = {"cloudCover": {"lt": max_cloud}}
    search = client.search(
        collections=[collection],
        bbox=list(aoi.bounds),
        datetime=f"{date_from}/{date_to}",
        query=query,
        max_items=limit,
    )
    return list(search.items())


def load_bands_aoi(items, bands, aoi, *, resolution=10, crs="EPSG:32633"):
    """Carica SOLO la finestra AoI delle bande richieste come xarray (odc-stac).

    Legge i COG in modo finestrato: niente download dell'intero prodotto.
    """
    import odc.stac

    return odc.stac.load(
        items,
        bands=bands,
        geopolygon=aoi,
        resolution=resolution,
        crs=crs,
        chunks={},
    )


def download_product(item, out_dir="data", *, concurrency=4):
    """Scarica il prodotto SAFE completo dal CDSE (cdsetool). Serve per L1C/uso pieno."""
    from cdsetool.credentials import Credentials
    from cdsetool.download import download_feature

    creds = Credentials(settings.cdse_user, settings.cdse_password)
    return download_feature(item, out_dir, {"concurrency": concurrency}, credentials=creds)
