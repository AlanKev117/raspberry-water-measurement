import os

from fastapi import FastAPI

from DiscreteWaterLevelSensor import DiscreteWaterLevelSensor
from misc import to_list

WATER_PINS = os.environ.get("WATER_PINS", "[]")

pins = to_list(WATER_PINS)


if pins is None:
    sensor = DiscreteWaterLevelSensor()
else:
    sensor = DiscreteWaterLevelSensor(pins)
    
app = FastAPI()


@app.get("/")
async def root():
    return {
        "level": f"{sensor.get_percentage()}%",
        "is_charging": sensor.is_charging()
    }
