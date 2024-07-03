import os
import json

from .sensor.WaterLevelSensor import WaterLevelSensor
from .sensor.DummyWaterLevelSensor import DummyWaterLevelSensor
from .sensor.DiscreteWaterLevelSensor import DiscreteWaterLevelSensor
from .sensor.SerialGravityWaterLevelSensor import SerialGravityWaterLevelSensor, MIN_REF, MAX_REF

def initialize_sensor():
    
    sensor_type = os.environ.get("WATER_SENSOR_TYPE", "dummy")

    assert sensor_type in ("discrete", "gravity", "dummy"), f"Sensor type not supported: '{sensor_type}'"

    if sensor_type == "discrete":
        # Create a DiscreteWaterLevelSensor
        pins = json.loads(os.environ.get("WATER_PINS"))
        assert type(pins) == list and type(pins[0]) == int
        sensor = DiscreteWaterLevelSensor(pins)
    
    elif sensor_type == "gravity":
        # Create a SerialGravityWaterLevelSensor
        WATER_MIN_REF = json.loads(os.environ.get("WATER_MIN_REF", json.dumps(MIN_REF)))
        WATER_MAX_REF = json.loads(os.environ.get("WATER_MAX_REF", json.dumps(MAX_REF)))

        sensor = SerialGravityWaterLevelSensor(
            ref1=WATER_MIN_REF,
            ref2=WATER_MAX_REF
        )
    
    else:
        # Create a dummy sensor
        sensor = DummyWaterLevelSensor()

    return sensor