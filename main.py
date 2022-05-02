import os

from fastapi import FastAPI
from gpiozero import DistanceSensor, Device
from gpiozero.pins.pigpio import PiGPIOFactory

Device.pin_factory = PiGPIOFactory()

MAX_DISTANCE = os.getenv("MAX_DISTANCE", 1.17)
ECHO_PIN = os.getenv("ECHO_PIN", 22)
TRIGGER_PIN = os.getenv("TRIGGER_PIN", 23)

app = FastAPI()

distance_sensor = DistanceSensor(
    echo=ECHO_PIN, 
    trigger=TRIGGER_PIN, 
    max_distance=MAX_DISTANCE
)

@app.get("/")
async def root():
    return {
        "percentage": distance_sensor.value,
        "distance": distance_sensor.distance
    }
