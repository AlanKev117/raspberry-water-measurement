#!/bin/bash

set -e

CWD=$(pwd)

# Install requirements
pip3.8 install -r requirements.txt

# Copy service file to right path
SYSTEMDIR="/etc/systemd/system/"
[ -d $SYSTEMDIR ] || mkdir -p $SYSTEMDIR
cp water_level.service $SYSTEMDIR

# Assert service got copied to right path
SERVICE_FILE="$SYSTEMDIR/water_level.service"
[ -f "$SERVICE_FILE" ] || ( echo "Missing service file in right location" && exit 1)

# Enable service to run on boot
systemctl enable water_level.service

# Set up env vars to be loaded on boot
WATER_ENV_FILE=$CWD/water.env

if grep -Fxq "source ${WATER_ENV_FILE}" "/etc/profile" 
then
    exit 0
else
    echo "" >> /etc/profile
    echo "source ${WATER_ENV_FILE}" >> /etc/profile
    echo "" >> /etc/profile
fi