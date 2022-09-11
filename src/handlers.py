from datetime import datetime

from SerialGravityWaterLevelSensor import SerialGravityWaterLevelSensor

class SensorHandlers:
    def __init__(self, sensor: SerialGravityWaterLevelSensor):
        self.sensor = sensor

    def get_sensor_data(self, label=None):
        percentage = self.sensor.get_percentage()
        is_charging = self.sensor.is_charging()
        value = self.sensor.get_value()
        temperature = self.sensor.get_temperature()
        acceleration = self.sensor.get_acceleration()

        payload = {
            "level": percentage,
            "label": label,
            "value": value,
            "is_charging": is_charging,
            "acceleration": acceleration,
            "temperature": temperature,
            "time": datetime.now()
        }

        return payload

    def get_percentage(self):
        return self.sensor.get_percentage()