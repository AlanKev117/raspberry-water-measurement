# Water Level Measurement with Raspberry Pi

This project is meant to use a Raspberry Pi Zero W+ to help measure water level in a water tank placed on the roof of a house.


## Prerequirements

Make sure to run `sudo apt update` and `sudo apt upgrade` to have all of the
built-in dependencies up to date in your Pi device.
### Set up your Raspberry Pi (OS, user, network and ssh access, if you wish)
Follow the [official docs](https://www.raspberrypi.com/documentation/computers/configuration.html) to configure your Pi device as you wish. This project made use of the 32-bit version of Raspberry Pi OS Lite with a [headless configuration](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi).

### Enable I2C communication in your Pi

Run `sudo raspi-config` and enable I2C using the menu.

### Install Python 3.8

This project was developed in Python 3.8. In order for you to install such version, I recommend not to install it via `apt`, since it takes a lot to have `pip` working.

Instead, download the latest Python 3.8 version from the official site, which is 3.8.13 by the time this README file was written. You can do so by running `setup.sh` (I recommend running one command at a time if you are accessing your Pi via SSH).

### Install `pigpio` pin factory

In order to get more accurate readings from the GPIO pins, the `pigpio`
daemon will be very helpful.

```bash
sudo apt install pigpio python3-pigpio
sudo systemctl enable --now pigpiod.service
```

## Deployment

NGINX, NGINX file, deploy.sh

```bash
```

## Wiring and physical setup


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