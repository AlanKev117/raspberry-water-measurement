#!/bin/bash

set -e

# Install requirements
pip3.8 install -r requirements.txt

# Copy service file to right path
SYSTEMDIR="$HOME/.config/systemd/user"
[ -d $SYSTEMDIR ] || mkdir -p $SYSTEMDIR
cp water_level.service $SYSTEMDIR

# Assert service got copied to right path
SERVICE_FILE="$SYSTEMDIR/water_level.service"
[ -f "$SERVICE_FILE" ] || ( echo "Missing service file in right location, make sure to run setup.sh first" && exit 1)

# Enable service to run on boot
systemctl enable --user --now water_level.service

