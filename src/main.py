import os
from json import loads, dumps
from datetime import datetime

from fastapi import FastAPI

from SerialGravityWaterLevelSensor import SerialGravityWaterLevelSensor
from SerialGravityWaterLevelSensor import MAX_REF
from SerialGravityWaterLevelSensor import MIN_REF

WATER_MIN_REF = loads(os.environ.get("WATER_MIN_REF", dumps(MIN_REF)))
WATER_MAX_REF = loads(os.environ.get("WATER_MAX_REF", dumps(MAX_REF)))

sensor = SerialGravityWaterLevelSensor(
    ref1=WATER_MIN_REF,
    ref2=WATER_MAX_REF
)

app = FastAPI()


@app.get("/")
async def root():

    percentage = sensor.get_percentage()
    is_charging = sensor.is_charging()
    value = sensor.get_value()
    temperature = sensor.get_temperature()
    acceleration = sensor.get_acceleration()

    return {
        "level": f"{percentage}%",
        "value": value,
        "is_charging": "yes" if is_charging else "no",
        "acceleration": acceleration,
        "temperature": temperature,
        "time": datetime.now()
    }
