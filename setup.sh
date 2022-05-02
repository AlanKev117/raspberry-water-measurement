#!/bin/bash

# Install requirements
pip3.8 install -r requirements.txt

# Copy service file to right path
SYSTEMDIR="$HOME/.config/systemd/user"
[ -d $SYSTEMDIR ] || mkdir -p $SYSTEMDIR
cp water_level.service $SYSTEMDIR
