#!/bin/bash

set -e

CWD=$(pwd)
INSTALLATION_DIR=/home/pi/water-level-app

# Install Python dependencies.
pip3.8 install -r requirements.txt

# Copy source files to installation dir.
[ -d "$INSTALLATION_DIR" ] || mkdir $INSTALLATION_DIR
rm -r $INSTALLATION_DIR
cp -r $CWD/src/* $INSTALLATION_DIR

# Copy service file to the right location for systemd.
SYSTEMDIR="/etc/systemd/system/"
[ -d $SYSTEMDIR ] || mkdir -p $SYSTEMDIR
cp water_level.service $SYSTEMDIR

# Assert service got copied to the right location.
SERVICE_FILE="$SYSTEMDIR/water_level.service"
[ -f "$SERVICE_FILE" ] || ( echo "Missing service file in right location" && exit 1)

# Enable service to run on boot.
systemctl enable water_level.service

# Set up env vars to be loaded on boot.
WATER_ENV_FILE=$CWD/water.env

# Check env vars file is loaded on boot.
if grep -Fxq "source ${WATER_ENV_FILE}" "/etc/profile" 
then
    exit 0
else
    echo "" >> /etc/profile
    echo "source ${WATER_ENV_FILE}" >> /etc/profile
    echo "" >> /etc/profile
fi