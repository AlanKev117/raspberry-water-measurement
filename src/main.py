import os

from fastapi import FastAPI

from SerialGravityWaterLevelSensor import SerialGravityWaterLevelSensor
from SerialGravityWaterLevelSensor import MAX_SLOPE
from SerialGravityWaterLevelSensor import MIN_SLOPE

WATER_MIN_SLOPE = float(os.environ.get("WATER_MIN_SLOPE", MIN_SLOPE))
WATER_MAX_SLOPE = float(os.environ.get("WATER_MAX_SLOPE", MAX_SLOPE))

sensor = SerialGravityWaterLevelSensor(
    min_slope=WATER_MIN_SLOPE, 
    max_slope=WATER_MAX_SLOPE
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
        "temperature": temperature
    }
