#!/bin/bash
# DESCRIPTION
#  This script pulls the default kartoza/postgis:latest image.
# 
# REFERENCES
#   - ...
#
# ISSUES
#  ...
#
# CALL
#  ./pull.sh [<IMAGE-NAME>]
#  ./pull.sh kartoza/postgis:latest

# ========= PARAMETERS =============
DEF_IMAGE_NAME=kartoza/postgis:latest
#postgis/postgis #kartoza/postgis:9.6-2.4

# ========= ARGS =============
IMAGE_NAME=${1:-$DEF_IMAGE_NAME}

# ========= START =============
echo ""
echo "START-----------------------"
echo ""
echo "docker pull $IMAGE_NAME"
echo "..."
docker pull $IMAGE_NAME
echo ""
echo "----------------------------"
echo ""
echo ""