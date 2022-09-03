import os

from fastapi import FastAPI

from SerialWaterLevelSensor import SerialWaterLevelSensor
from SerialWaterLevelSensor import MAX_VOLTAGE
from SerialWaterLevelSensor import MIN_VOLTAGE

WATER_MIN_VOLTAGE = os.environ.get("WATER_MIN_VOLTAGE", MIN_VOLTAGE)
WATER_MAX_VOLTAGE = os.environ.get("WATER_MAX_VOLTAGE", MAX_VOLTAGE)

sensor = SerialWaterLevelSensor(
    min_voltage=WATER_MAX_VOLTAGE, 
    max_voltage=WATER_MAX_VOLTAGE
)
    
app = FastAPI()


@app.get("/")
async def root():
    percentage = sensor.get_percentage()
    level = f"{percentage}%" if percentage is not None else "calculating..."
    is_charging = sensor.is_charging()
    voltage, _ = sensor.get_voltage_and_value()
    return {
        "level": level,
        "is_charging": is_charging,
        "voltage": voltage
    }
