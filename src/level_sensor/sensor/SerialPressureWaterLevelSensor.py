import board
import busio
from datetime import datetime, timedelta

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

from .WaterLevelSensor import WaterLevelSensor

MIN_VOLTAGE = 2.0
MAX_VOLTAGE = 3.2

class SerialPressureWaterLevelSensor(WaterLevelSensor):
    """Uses the Pi's I2C pins to read data from the ADS1115 ADC module."""

    def __init__(self, min_voltage=MIN_VOLTAGE, max_voltage=MAX_VOLTAGE):
        self.min_voltage = min_voltage
        self.max_voltage = max_voltage
        self.slope = 100 / (max_voltage - min_voltage)
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)
        self.ads.mode = Mode.CONTINUOUS
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
        voltage, value = self.get_voltage_and_value()
        now = datetime.now()
        self.update_last_read(value, now)
        percentage = self.slope * (voltage - self.min_voltage)
        return round(percentage, 2)

    def is_charging(self):
        return self.is_charging_value

    def get_voltage_and_value(self):
        channel = AnalogIn(self.ads, ADS.P0)
        voltage = channel.voltage
        value = channel.value
        return voltage, value