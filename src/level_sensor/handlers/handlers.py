from ..sensor.WaterLevelSensor import WaterLevelSensor

class SensorHandlers:
    def __init__(self, sensor: WaterLevelSensor):
        self.sensor = sensor

    def get_minimal_data(self):
        return {
            "level": self.sensor.get_percentage(),
            "charging": self.sensor.is_charging()
        }