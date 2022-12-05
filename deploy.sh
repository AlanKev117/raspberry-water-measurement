#!/bin/bash

set -e

CWD=$(pwd)
INSTALLATION_DIR=/home/pi/water-level-app

# Install Python dependencies.
pip3.8 install -r requirements.txt

# Copy source files to installation dir.
[ -d "$INSTALLATION_DIR" ] && rm -rf $INSTALLATION_DIR
mkdir $INSTALLATION_DIR
cp -r $CWD/src/* $INSTALLATION_DIR
cp -r $CWD/iot/* $INSTALLATION_DIR
cp -r $CWD/water.env $INSTALLATION_DIR
cp -r $CWD/publisher.env $INSTALLATION_DIR

# Copy service files to the right location for systemd.
SYSTEMDIR="/etc/systemd/system/"
[ -d $SYSTEMDIR ] || mkdir -p $SYSTEMDIR
cp water_level.service level_publisher.service $SYSTEMDIR

# Assert services got copied to their right location.
SERVICE_FILE="$SYSTEMDIR/water_level.service"
[ -f "$SERVICE_FILE" ] || ( echo "Missing water level service file in right location" && exit 1)
SERVICE_FILE="$SYSTEMDIR/level_publisher.service"
[ -f "$SERVICE_FILE" ] || ( echo "Missing level publisher service file in right location" && exit 1)

# Enable services to run on boot.
systemctl enable water_level.service
systemctl restart water_level.service
systemctl enable level_publisher.service
systemctl restart level_publisher.service