"""Carica i GeoJSON OSM (osm_data/) in PostGIS. Usa impervious + config/pipeline.yaml.

USO:  pixi run -e default python scripts/load_osm.py
"""

from impervious.params import load_params
from impervious import osm


def main() -> None:
    P = load_params()
    n = osm.load_dir_to_postgis(
        P.osm["out_dir"],
        table=P.osm["postgis_table"],
        keep_columns=P.osm["keep_columns"],
    )
    print(f"Caricate {n} geometrie nella tabella '{P.osm['postgis_table']}'.")


if __name__ == "__main__":
    main()
