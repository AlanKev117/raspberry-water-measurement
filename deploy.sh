#!/bin/bash

# Script to deploy or redeploy the application as systemd services to run on boot.
# [USAGE]
# sudo bash deploy.sh reqs # first deployment (installs Python dependencies)
# sudo bash deploy.sh # newer deployments (does not install Python dependencies)

set -e

REQS_FLAG=$1
CWD=$(pwd)
INSTALLATION_DIR=/home/pi/water-level-app

# Install Python dependencies.
if [ "$REQS_FLAG" == "reqs" ]
then
    pip3.12 install -r requirements.txt
fi

# Copy source files to installation dir.
echo "[INFO] Copying source files to execution paths..."
[ -d "$INSTALLATION_DIR" ] && rm -rf $INSTALLATION_DIR
mkdir $INSTALLATION_DIR
cp -r $CWD/src/* $INSTALLATION_DIR
cp -r $CWD/iot/* $INSTALLATION_DIR
cp -r $CWD/water.env $INSTALLATION_DIR
cp -r $CWD/publisher.env $INSTALLATION_DIR

# Copy service files to the right location for systemd.
echo "[INFO] Installing service files..."
SYSTEMDIR="/etc/systemd/system/"
LEVEL_SENSOR_SERVICE="level_sensor.service"
LEVEL_PUBLISHER_SERVICE="level_publisher.service"

[ -d $SYSTEMDIR ] || mkdir -p $SYSTEMDIR
cp water_level.service level_publisher.service $SYSTEMDIR

# Assert services got copied to their right location.
echo "[INFO] Verifying service files..."
SERVICE_FILE="$SYSTEMDIR/${LEVEL_SENSOR_SERVICE}"
[ -f "$SERVICE_FILE" ] || ( echo "Missing level sensor service file in right location" && exit 1)
SERVICE_FILE="$SYSTEMDIR/${LEVEL_PUBLISHER_SERVICE}"
[ -f "$SERVICE_FILE" ] || ( echo "Missing level publisher service file in right location" && exit 1)

# Enable services to run on boot.
echo "[INFO] Enabling services to run on boot..."
systemctl enable water_level.service
systemctl restart water_level.service
systemctl enable level_publisher.service
systemctl restart level_publisher.service