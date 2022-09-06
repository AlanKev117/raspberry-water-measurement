import board
import busio
from datetime import datetime, timedelta

import adafruit_mpu6050

from WaterLevelSensor import WaterLevelSensor

MIN_SLOPE = 2.0
MAX_SLOPE = 3.2

class SerialGravityWaterLevelSensor(WaterLevelSensor):
    """Uses the Pi's I2C pins to read data from the MPU6050 module."""

    def __init__(self, min_slope=MIN_SLOPE, max_slope=MAX_SLOPE):
        self.min_slope = min_slope
        self.max_slope = max_slope
        self.slope = 100 / (max_slope - min_slope)
        i2c = board.I2C()
        self.mpu = adafruit_mpu6050.MPU6050(i2c)
        self.last_read = None
        self.last_read_datetime = None
        self.is_charging_value = False

    def update_last_read(self, read, now):
        
        if self.last_read == None:
            self.last_read = read
            self.last_read_datetime = now
            return
        
        if self.last_read_datetime + timedelta(minutes=1) < now:
            self.is_charging_value = read > self.last_read
            self.last_read_datetime = now
            self.last_read = read


    def get_percentage(self):
        value = self.get_value()
        now = datetime.now()
        self.update_last_read(value, now)
        percentage = self.slope * (value - self.min_slope)
        return round(percentage, 2)

    def is_charging(self):
        return self.is_charging_value

    def get_value(self):
        return self.mpu.gyro[1]