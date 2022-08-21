# Dependencies used by the compiler
sudo apt install libssl-dev
sudo apt install libffi-dev

# Python 3.8 version, change if you wish
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
sudo make altinstall

# Remove sources (optional)

# run this command in the path where both your tar.xz 
# file and your Python source live
cd ..
rm -r Python-${PYTHON_38_VERSION}
rm Python-${PYTHON_38_VERSION}.tar.xz