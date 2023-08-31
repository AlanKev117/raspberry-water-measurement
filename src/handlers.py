from datetime import datetime

from SerialGravityWaterLevelSensor import SerialGravityWaterLevelSensor

class SensorHandlers:
    def __init__(self, sensor: SerialGravityWaterLevelSensor):
        self.sensor = sensor

    def get_sensor_data(self, label=None):
        percentage = self.sensor.get_percentage()
        is_charging = self.sensor.is_charging()
        temperature = self.sensor.get_temperature()
        acceleration = self.sensor.get_acceleration()

        payload = {
            "level": percentage,
            "label": label,
            "is_charging": is_charging,
            "acceleration": acceleration,
            "temperature": temperature,
            "time": datetime.now()
        }

        return payload

    def get_minimal_data(self):
        return {
            "level": self.sensor.get_percentage(),
            "charging": self.sensor.is_charging()
        }