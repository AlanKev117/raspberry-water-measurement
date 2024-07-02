from math import ceil
from datetime import datetime, timedelta

import board
import adafruit_mpu6050

from .WaterLevelSensor import WaterLevelSensor
from ..tools.misc import Bouncer

MIN_REF = [-0.66, 13]
MAX_REF = [5.6, 65]

bouncer = Bouncer()

class SerialGravityWaterLevelSensor(WaterLevelSensor):
    """Uses the Pi's I2C pins to read data from the MPU6050 module."""

    def __init__(self, ref1=MIN_REF, ref2=MAX_REF):
        self.ref1 = ref1
        self.ref2 = ref2
        self.slope = (ref2[1] - ref1[1]) / (ref2[0] - ref1[0])
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
        percentage = self.slope * (value - self.ref1[0]) + self.ref1[1]
        percentage = ceil(percentage)
        self.update_last_read(percentage, now)
        return percentage

    def is_charging(self):
        return self.is_charging_value

    @bouncer.apply
    def get_value(self):
        return self.mpu.acceleration[0]
    
    @bouncer.apply
    def get_acceleration(self):
        return self.mpu.acceleration

    @bouncer.apply
    def get_temperature(self):
        return self.mpu.temperature