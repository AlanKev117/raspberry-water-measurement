import os
from json import loads, dumps

from fastapi import FastAPI

from SerialGravityWaterLevelSensor import SerialGravityWaterLevelSensor
from SerialGravityWaterLevelSensor import MAX_REF
from SerialGravityWaterLevelSensor import MIN_REF

from DiscreteWaterLevelSensor import DiscreteWaterLevelSensor

from handlers import SensorHandlers

WATER_SENSOR_TYPE = os.environ.get("WATER_SENSOR_TYPE", "discrete")
assert WATER_SENSOR_TYPE in ("discrete", "gravity")

if WATER_SENSOR_TYPE == "gravity":
    # Create a SerialGravityWaterLevelSensor
    WATER_MIN_REF = loads(os.environ.get("WATER_MIN_REF", dumps(MIN_REF)))
    WATER_MAX_REF = loads(os.environ.get("WATER_MAX_REF", dumps(MAX_REF)))

    sensor = SerialGravityWaterLevelSensor(
        ref1=WATER_MIN_REF,
        ref2=WATER_MAX_REF
    )
elif WATER_SENSOR_TYPE == "discrete":
    # Create a DiscreteWaterLevelSensor
    WATER_PINS = loads(os.environ.get("WATER_PINS"))
    assert type(WATER_PINS) == list and type(WATER_PINS[0]) == int
    sensor = DiscreteWaterLevelSensor(WATER_PINS)

handlers = SensorHandlers(sensor)
app = FastAPI()

@app.get("/label/{label}")
async def label(label: int):
    return handlers.get_sensor_data(label)

@app.get("/details")
async def details():
    return handlers.get_sensor_data()

@app.get("/")
async def root():
    return handlers.get_minimal_data()
