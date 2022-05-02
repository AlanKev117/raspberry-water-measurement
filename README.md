# Water Level Measurement with Raspberry Pi

This project is meant to use a Raspberry Pi Zero W+ to help measure water level in a water tank placed on the roof of a house.


## Prerequirements

Make sure to run `sudo apt update` and `sudo apt upgrade` to have all of the
built-in dependencies up to date in your Pi device.
### Set up your Raspberry Pi (OS, user, network and ssh access, if you wish)
Follow the [official docs](https://www.raspberrypi.com/documentation/computers/configuration.html) to configure your Pi device as you wish. This project made use of the 32-bit version of Raspberry Pi OS Lite with a [headless configuration](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi).

### Install Python 3.8

This project was developed in Python 3.8. In order for you to install such version, I recommend not to install it via `apt`, since it takes a lot to have `pip` working.

Instead, download the latest Python 3.8 version from the official site, which is 3.8.13 by the time this README file was written:

```bash
# I recommend running one command at a time if you
# are accessing your Pi via SSH.

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
```

### Install `pigpio` pin factory

In order to get more accurate readings from the GPIO pins, the `pigpio`
daemon will be very helpful.

```bash
sudo apt install pigpio python3-pigpio
sudo systemctl enable --now pigpiod.service
```

## Software deployment

NGINX, NGINX file, setup.sh, deploy.sh

```bash
```

## Wiring and physical setup

This project uses the ultrasonic sensor `aj-sr04m`, which is waterproof and shall be installed in the water tank as shown in the picture bellow, aiming at the bottom of the same.

When the tank is full, there should be a gap between the sensor and the water level as close to ### cm as possible. Otherwise feel free to mutate the variables ### as needed.

The sensor wiring to the Pi is the next one:
* Vcc to the 3.3V pin
* GND to any GND pin
* Echo to any GPIO pin, defaults to 22
* Trigger to any GPIO pin, defaults to 23


## Local execution and usage

> Make sure to fetch your Pi's IP address.

Under a virtual environment, install the dependencies:

```bash
pip3.8 install -r requirements.txt
```

In your Pi device run the development server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

In a web browser enter your Pi's IP address as follows: `{ip-address}:8000`

You should GET a response like this:

```plain
{"percentage": <percentage value>}
```