import os
import json

from .sensor.WaterLevelSensor import WaterLevelSensor
from .sensor.DummyWaterLevelSensor import DummyWaterLevelSensor
from .sensor.DiscreteWaterLevelSensor import DiscreteWaterLevelSensor
from .sensor.SerialGravityWaterLevelSensor import SerialGravityWaterLevelSensor, MIN_REF, MAX_REF

def initialize_sensor():
    
    sensor_type = os.environ.get("WATER_SENSOR", "dummy")

    assert sensor_type in ("discrete", "gravity", "dummy"), f"Sensor type not supported: '{sensor_type}'"

    print(f"[INFO] - Sensor type: {sensor_type}")

    if sensor_type == "discrete":
        # Create a DiscreteWaterLevelSensor
        pins = json.loads(os.environ.get("WATER_PINS"))
        offset = int(os.environ.get("WATER_OFFSET", "0"))
        pull_up = os.environ.get("WATER_PULL_UP", "false") == "true"
        assert type(pins) == list and type(pins[0]) == int
        print(f"[INFO] - Pins: {pins}")
        print(f"[INFO] - Offset: {offset}")
        print(f"[INFO] - Pull-up: {pull_up}")
        sensor = DiscreteWaterLevelSensor(pins, offset=offset, pull_up=pull_up)
    
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
