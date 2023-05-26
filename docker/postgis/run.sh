#!/bin/bash
# DESCRIPTION
#  This script runs the postgis container on top of 
#  the kartoza/postgis:latest image.
# 
# REFERENCES
#   - https://alexurquhart.com/post/set-up-postgis-with-docker/
#   - https://hub.docker.com/r/kartoza/postgis
#
# ISSUES
#  Image from postgis/postgis does not work fine during run.
#  Therefore, I used kartoza one.
#
# CALL
#  ./run.sh [<IMAGE-NAME> , <CONTAINER-NAME>]
#  ./run.sh kartoza/postgis:latest pgis-car

# ========= PARAMETERS =============
DEF_CONTAINER_NAME=pgis-osm
DEF_IMAGE_NAME=kartoza/postgis:latest #postgis/postgis #kartoza/postgis:9.6-2.4

NET_NAME=bridge_impclass
DATA_PATH=~/work/jupyter/docker/postgis/docker-persistencies
PORT=65432
# It doesn't matter which values you use for the DB,user,pswd below
# in order to let the container run properly.
PG_USER="giuliano"
PG_PSWD="antonietta"
PG_DB="osm" #CAR

# ========= ARGS =============
IMAGE_NAME=${1:-$DEF_IMAGE_NAME}
CONTAINER_NAME=${2:-$DEF_CONTAINER_NAME}

# ========= START =============
echo "Docker cycle is:   IMAGE(${IMAGE_NAME}) --> CONTAINER(${CONTAINER_NAME})"

# check container existence and kill it before to run again:
container_id=$(docker ps -a -q --filter "name=$CONTAINER_NAME$")

if [ ! -z "$container_id" ]; then
  echo "  container $CONTAINER_NAME already running..."
  echo "    stopping it.."
  docker stop $container_id
  echo "    removing it..."
  docker rm $container_id
else
  echo "  container $CONTAINER_NAME not existent..."
fi

echo "  Start container $CONTAINER_NAME running on top of $IMAGE_NAME image"
echo "      > PG_USER      : $PG_USER"
echo "      > PG_PSWD      : $PG_PSWD"
echo "      > PG_DB        : $PG_DB"
echo "      > data         : $DATA_PATH"
echo "      > port         : $PORT"
echo "      > docker net   : $NET_NAME"
echo ""
#docker run \
#  --name $CONTAINER_NAME \
#  --restart=always \
#  -d \
#  -v $DATA_PATH/data:/var/lib/postgresql \
#  -v $DATA_PATH/share:/share \
#  -p $PORT:5432 \
#  --network=$NET_NAME \
#  -e POSTGRES_PASSWORD=$PS_PSWD \
#  $IMAGE_NAME

echo "
docker run \
  --name=$CONTAINER_NAME \
  --network=$NET_NAME \
  -d \
  -e POSTGRES_USER=$PG_USER \
  -e POSTGRES_PASS=$PG_PSWD \
  -e POSTGRES_DBNAME=$PG_DB \
  -e ALLOW_IP_RANGE=0.0.0.0/0 \
  -p $PORT:5432 \
  -v $DATA_PATH:/var/lib/postgresql \
  --restart=always \
  $IMAGE_NAME
"
docker run \
  --name=$CONTAINER_NAME \
  --network=$NET_NAME \
  -d \
  -e "POSTGRES_USER=$PG_USER" \
  -e "POSTGRES_PASS=$PG_PSWD" \
  -e "POSTGRES_DBNAME=$PG_DB" \
  -e ALLOW_IP_RANGE=0.0.0.0/0 \
  -p $PORT:5432 \
  -v $DATA_PATH:/var/lib/postgresql \
  --restart=always \
  $IMAGE_NAME
#  -v $INITD_PATH:/docker-entrypoint-initdb.d \
#--mac-address 02:42:ac:12:00:05 \
#--ip=172.18.0.5 \

echo ""
echo "  ...done!"
echo ""
echo ""