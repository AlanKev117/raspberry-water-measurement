from src.SerialWaterLevelSensor import SerialWaterLevelSensor

sensor = SerialWaterLevelSensor()

while True:
    print(f"Value: {sensor.get_percentage()}")
    print(f"Charging: {sensor.is_charging()}")