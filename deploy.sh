#!/bin/bash

# Script to deploy or redeploy the application as systemd services to run on boot.
# [USAGE]
# sudo bash deploy.sh reqs # first deployment (installs Python dependencies)
# sudo bash deploy.sh # newer deployments (does not install Python dependencies)

set -e

REQS_FLAG=$1
WORK_DIR=$(pwd)
APP_DIR=/home/pi/water-level-app

# Install Python dependencies.
if [ "$REQS_FLAG" == "reqs" ]
then
    pip3.12 install -r requirements.txt
fi

# Copy source files to installation dir.
echo "[INFO] Copying source files to execution paths..."
[ -d "$APP_DIR" ] && rm -rf $APP_DIR
mkdir $APP_DIR
cp -r $WORK_DIR/src/ $APP_DIR
cp -r $WORK_DIR/iot/ $APP_DIR
cp -r $WORK_DIR/static/ $APP_DIR
cp -r $WORK_DIR/templates/ $APP_DIR
cp -r $WORK_DIR/level_sensor.env $APP_DIR
cp -r $WORK_DIR/level_publisher.env $APP_DIR

# Copy service files to the right location for systemd.
echo "[INFO] Installing service files..."
SYSTEMDIR="/etc/systemd/system/"
LEVEL_SENSOR_SERVICE="level_sensor.service"
LEVEL_PUBLISHER_SERVICE="level_publisher.service"

[ -d "${SYSTEMDIR}" ] || mkdir -p ${SYSTEMDIR}
cp ${LEVEL_SENSOR_SERVICE} ${LEVEL_PUBLISHER_SERVICE} ${SYSTEMDIR}

# Assert services got copied to their right location.
echo "[INFO] Verifying service files..."
SERVICE_FILE="${SYSTEMDIR}/${LEVEL_SENSOR_SERVICE}"
[ -f "$SERVICE_FILE" ] || ( echo "Missing level sensor service file in right location" && exit 1)
SERVICE_FILE="${SYSTEMDIR}/${LEVEL_PUBLISHER_SERVICE}"
[ -f "$SERVICE_FILE" ] || ( echo "Missing level publisher service file in right location" && exit 1)

# Enable services to run on boot.
echo "[INFO] Enabling services to run on boot..."
systemctl enable ${LEVEL_SENSOR_SERVICE}
systemctl restart ${LEVEL_SENSOR_SERVICE}
systemctl enable ${LEVEL_PUBLISHER_SERVICE}
systemctl restart ${LEVEL_PUBLISHER_SERVICE}