#!/bin/bash

# [USAGE]
# sudo bash setup.sh [test]

set -e

TEST_FLAG=$1

### Install Python 3 from source

# Install compiling dependencies
echo "[INFO] Downloading Python installation dependencies..."
apt -y install libssl-dev libffi-dev

# Latest Python version
PYTHON_VERSION=3.12.4

# Get source from the internet
echo "[INFO] Downloading Python release ${PYTHON_VERSION}..."
wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz

# Extract and cd to Python sources dir.
echo "[INFO] Extracting release source files..."
tar -xf Python-${PYTHON_VERSION}.tar.xz
cd Python-${PYTHON_VERSION}

# Checks for installation requirements
echo "[INFO] Validating installation requirements for Python release..."
./configure

# Compile sources into objects
echo "[INFO] Preparing Python release for install..."
make

# Optional, it may not finish via SSH
if [ "${TEST_FLAG}" = "test" ]
then
    echo "[INFO] Testing Python release..."
    make test
fi

# Puts binaries together
# make altinstall => installs the downloaded release as an alternative one
# make install => installs the downloaded release as the main one for the system
echo "[INFO] Installing Python release..."
make altinstall

# Clean up temporary files.
echo "[INFO] Python ${PYTHON_VERSION} installed successfully!" 
echo "[INFO] Cleaning up files..."
cd ..
rm -r Python-${PYTHON_VERSION}
rm Python-${PYTHON_VERSION}.tar.xz
