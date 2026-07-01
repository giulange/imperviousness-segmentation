#!/usr/bin/env bash
# =============================================================================
#  postgis_up.sh — avvia PostGIS (kartoza) sulla VM, con credenziali da .env.
#  NIENTE password hardcoded (a differenza del vecchio docker/postgis/run.sh).
#
#  USO (sulla VM, dopo aver compilato .env):
#    bash scripts/postgis_up.sh
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f .env ] || { echo "Manca .env (copia da .env.example e compila)"; exit 1; }
set -a; . ./.env; set +a

CONTAINER="${PG_CONTAINER:-pgis-osm}"
IMAGE="${PG_IMAGE:-kartoza/postgis:latest}"
PORT="${PG_PORT:-65432}"
DATA_VOL="${PG_DATA_VOL:-pgis_osm_data}"

if [ "$(docker ps -aq -f name="^${CONTAINER}$")" ]; then
  echo "Container ${CONTAINER} esistente: lo rimuovo e ricreo."
  docker rm -f "${CONTAINER}" >/dev/null
fi

echo "Avvio ${CONTAINER} (${IMAGE}) su :${PORT}, db=${PG_DB}"
docker run -d --name "${CONTAINER}" --restart=always \
  -e POSTGRES_USER="${PG_USER}" \
  -e POSTGRES_PASS="${PG_PASSWORD}" \
  -e POSTGRES_DBNAME="${PG_DB}" \
  -e ALLOW_IP_RANGE=0.0.0.0/0 \
  -e POSTGRES_MULTIPLE_EXTENSIONS=postgis \
  -p "${PORT}:5432" \
  -v "${DATA_VOL}:/var/lib/postgresql" \
  "${IMAGE}"

echo "Fatto. Verifica: docker logs -f ${CONTAINER}"
echo "Popola con:  pixi run -e default python scripts/load_osm.py"
