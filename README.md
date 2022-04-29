# Water Level Measurement with Raspberry Pi

This project is meant to use a Raspberry Pi Zero W+ to help measure water level in a water tank placed on the roof of a house.


## Prerequirements

* Python 3.8
* Setup your Raspberry Pi's user, network and ssh access if you wish
* `apt update && apt upgrade`

## Software installation

```bash
pip3 install -r requirements.txt
```

## Wiring and physical setup

This project uses the ultrasonic sensor `aj-sr04m`, which is waterproof and shall be installed in the water tank as shown in the picture bellow, aiming at the bottom of the same.

When the tank is full, there should be a gap between the sensor and the water level as close to ### cm as possible. Otherwise feel free to mutate the variables ### as needed.

The sensor wiring to the Pi is the next one:
* Vcc to the 3.3V pin
* GND to any GND pin
* Echo to any GPIO pin, defaults to 17
* Trigger to any GPIO pin, defaults to 18


## Execution and usage

> Make sure to fetch your Pi's IP address.

In your Pi device run the server:

```bash
python3 main.py
```

In a web browser enter your Pi's IP address as follows: `{ip-address}:8000`

You should GET a response like this:

```plain
{"percentage": <percentage value>}
```