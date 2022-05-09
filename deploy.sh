#!/bin/bash

# Install requirements
pip3.8 install -r requirements.txt

# Copy service file to right path
SYSTEMDIR="$HOME/.config/systemd/user"
[ -d $SYSTEMDIR ] || mkdir -p $SYSTEMDIR
cp water_level.service $SYSTEMDIR

# Assert service got copied to right path
SERVICE_FILE="$SYSTEMDIR/water_level.service"
[ -f "$SERVICE_FILE" ] || ( echo "Missing service file in right location" && exit 1)

# Enable service to run on boot
source water.env
systemctl enable --user --now water_level.service
sleep 1
