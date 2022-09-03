import os

from fastapi import FastAPI

from SerialWaterLevelSensor import SerialWaterLevelSensor

sensor = SerialWaterLevelSensor()
    
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
