import os

from fastapi import FastAPI
from gpiozero import DistanceSensor

MAX_DISTANCE = os.getenv("MAX_DISTANCE", 1.17)
ECHO_PIN = os.getenv("ECHO_PIN", 17)
TRIGGER_PIN = os.getenv("TRIGGER_PIN", 18)

app = FastAPI()

distanceSensor = DistanceSensor(
    echo=ECHO_PIN, 
    trigger=TRIGGER_PIN, 
    max_distance=MAX_DISTANCE
)

@app.get("/")
async def root():
    return {
        "percentage": distanceSensor.value
    }
