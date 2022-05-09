import os


from gpiozero import DistanceSensor, Device
from gpiozero.pins.pigpio import PiGPIOFactory


ECHO_PIN = os.getenv("ECHO_PIN", 22)
TRIGGER_PIN = os.getenv("TRIGGER_PIN", 23)
DEPTH = os.getenv("DEPTH", 0.75)
EMPTY_SPACE = os.getenv("EMPTY_SPACE", 0.21)
VOLUME_PER_CM = os.getenv("VOLUME_PER_CM", 10)

Device.pin_factory = PiGPIOFactory()


class TankSensor:

    def __init__(self, depth=DEPTH,
                 empty_space=EMPTY_SPACE,
                 volume_per_cm=VOLUME_PER_CM):

        assert 0.2 <= empty_space < 1.0, ("empty space between tank cap "
                                          "and water at top level should be "
                                          "more than 0.2 and less than 1.0 "
                                          "meters")
        assert 0 < depth < 8.0 - empty_space, ("depth must be between greater "
                                               "than 0 and less than "
                                               f"{8.0 - empty_space} meters, "
                                               "given empty_space = "
                                               f"{empty_space}")

        assert volume_per_cm > 0

        self.empty_space = empty_space
        self.depth = depth
        self.volume_per_cm = volume_per_cm

        self.sensor = DistanceSensor(
            echo=ECHO_PIN,
            trigger=TRIGGER_PIN,
            max_distance=empty_space + depth
        )

    def get_level_over_100(self):
        return 100.0 - (self.sensor.distance - self.empty_space) / self.depth

    def get_distance_from_ground(self):
        return round(self.empty_space + self.depth - self.sensor.distance)

    def get_level_in_volume(self):
        return self.get_distance_from_ground() * 100 * self.volume_per_cm
