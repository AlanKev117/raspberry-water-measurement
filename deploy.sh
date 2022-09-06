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
cp -r $CWD/water.env $INSTALLATION_DIR

# Copy service file to the right location for systemd.
SYSTEMDIR="/etc/systemd/system/"
[ -d $SYSTEMDIR ] || mkdir -p $SYSTEMDIR
cp water_level.service $SYSTEMDIR

# Assert service got copied to the right location.
SERVICE_FILE="$SYSTEMDIR/water_level.service"
[ -f "$SERVICE_FILE" ] || ( echo "Missing service file in right location" && exit 1)

# Enable service to run on boot.
systemctl enable water_level.service
systemctl restart water_level.service

# Install nginx server block
APP_DOMAIN=watertankpi.xyz
APP_SERVER_PATH=/etc/nginx/sites-available/$APP_DOMAIN
APP_SERVER_PATH_LINK=/etc/nginx/sites-enabled/$APP_DOMAIN
[ -f "$APP_SERVER_PATH" ] && rm $APP_SERVER_PATH

echo <<EOT > $APP_SERVER_PATH
server {
    listen 80;
    server_name $APP_DOMAIN;

    location / {
        proxy_pass http://localhost:8000;
    }
}
EOT

ln -s APP_SERVER_PATH APP_SERVER_PATH_LINK
nginx -t
systemctl reload nginx
