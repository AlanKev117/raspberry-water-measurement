import os
import json
from datetime import datetime, timedelta

from ..sensor.WaterLevelSensor import WaterLevelSensor
from ..sensor.DummyWaterLevelSensor import DummyWaterLevelSensor
from ..sensor.DiscreteWaterLevelSensor import DiscreteWaterLevelSensor
from ..sensor.SerialGravityWaterLevelSensor import SerialGravityWaterLevelSensor, MIN_REF, MAX_REF

def to_list(json_list_string: str):
    try:
        json_list = json.loads(json_list_string)
        assert isinstance(json_list, list)
        return json_list
    except:
        return None

class Bouncer:
    def __init__(self, bouncing_time=0.2):
        self.last_call_times = {}
        self.last_call_results = {}
        self.bouncing_time = timedelta(seconds=bouncing_time)

    def call_again(self, method, now):
        return self.last_call_times[method] + self.bouncing_time < now

    def apply(self, method):
        def inner(*args, **kwargs):
        
            now = datetime.now()

            uncalled_method = method not in self.last_call_times

            if uncalled_method or self.call_again(method, now):
                self.last_call_times[method] = now
                self.last_call_results[method] = method(*args, **kwargs)
                return self.last_call_results[method]
            else:
                return self.last_call_results[method]
        
        return inner
    
def initialize_sensor() -> WaterLevelSensor:
    
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