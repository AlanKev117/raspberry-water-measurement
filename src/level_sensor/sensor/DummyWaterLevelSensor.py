import random

from .WaterLevelSensor import WaterLevelSensor

class DummyWaterLevelSensor(WaterLevelSensor):
    def __init__(self):
        self.values = [60, 70, 80, 90, 100]

    def get_percentage(self):
        return random.choice(self.values)

    def is_charging(self):
        return random.choice([True, False])
