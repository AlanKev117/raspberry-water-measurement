#!/bin/bash

set -e

### Install and configure nginx
apt -y install nginx
systemctl enable nginx

# Install nginx server block
APP_DOMAIN=rotoplas.casa
APP_SERVER_PATH=/etc/nginx/sites-available/$APP_DOMAIN
APP_SERVER_PATH_LINK=/etc/nginx/sites-enabled/$APP_DOMAIN
[ -f "$APP_SERVER_PATH_LINK" ] && rm $APP_SERVER_PATH_LINK
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

# Create symbolic link to site (server block)
ln -s APP_SERVER_PATH APP_SERVER_PATH_LINK
nginx -t
systemctl reload nginx


### Install and configure local DNS server

apt -y install dnsmasq

echo "server=8.8.8.8" >> /etc/dnsmasq.conf 
echo "server=8.8.4.4" >> /etc/dnsmasq.conf 
echo "cache-size=1000" >> /etc/dnsmasq.conf
echo -e "127.0.0.1\t${APP_DOMAIN}" >> /etc/hosts

systemctl restart dnsmasq

### Install Python 3.8 from source

# Install compiling dependencies
apt -y install libssl-dev libffi-dev

# Latest Python 3.8 version
PYTHON_38_VERSION=3.8.13

# Get source from the internet
wget https://www.python.org/ftp/python/${PYTHON_38_VERSION}/Python-${PYTHON_38_VERSION}.tar.xz

# Extract and cd to Python sources dir.
tar -xf Python-${PYTHON_38_VERSION}.tar.xz
cd Python-${PYTHON_38_VERSION}

# Checks for installation requirements
./configure

# Compile sources into objects
make

# optional, it may not finish via SSH
make test

# Puts binaries together
# altinstall=3.8 is a side Python version in your Pi
# install=3.8 is the default Python version in your Pi
make altinstall

# Remove sources (optional)

cd ..
rm -r Python-${PYTHON_38_VERSION}
rm Python-${PYTHON_38_VERSION}.tar.xz
