#!/bin/bash

set -e

# run specific commands as root for env vars on boot
WATER_ENV_FILE=$(pwd)/water.env

if grep -Fxq "source ${WATER_ENV_FILE}" "/etc/profile" 
then
    exit 0
else
    echo "" >> /etc/profile
    echo "source ${WATER_ENV_FILE}" >> /etc/profile
    echo "" >> /etc/profile
fi