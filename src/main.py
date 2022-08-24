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
    percentage = sensor.get_percentage()
    level = f"{percentage}%" if percentage is not None else "calculating..."
    is_charging = sensor.is_charging()
    return {
        "level": level,
        "is_charging": is_charging
    }
