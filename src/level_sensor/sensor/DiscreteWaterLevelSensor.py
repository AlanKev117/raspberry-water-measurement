import logging

from gpiozero import DigitalInputDevice

from .WaterLevelSensor import WaterLevelSensor

MAX_RESOLUTION = 26
MIN_RESOLUTION = 1

RESOLUTION_WARN = "Resolution must be between {} and {}."
RESOLUTION_WARN = RESOLUTION_WARN.format(MIN_RESOLUTION, MAX_RESOLUTION)

OFFSET_WARN = "Offset cannot be a negative value."

WRONG_ORDER_WARN = "Cables in the discrete sensor are misplaced."

class DiscreteWaterLevelSensor(WaterLevelSensor):

    def __init__(self, pins, offset=0, pull_up=False):
        
        # Assert resolution limits so there's no conflict with gpiozero.
        resolution = len(pins)
        assert MIN_RESOLUTION <= resolution <= MAX_RESOLUTION, RESOLUTION_WARN
        self.resolution = resolution

        # Assign offset
        assert offset >= 0, OFFSET_WARN
        self.offset = offset

        # Pre-calculate levels for each pin based on the offset and resolution.
        if self.offset > 0:
            self.levels = [0]
            for i in range(self.resolution):
                self.levels.append(int(i / (self.resolution - 1) * (100 - self.offset) + self.offset))
        else:
            self.levels = [0]
            for i in range(self.resolution):
                self.levels.append(int((i + 1) / self.resolution * 100))

        # Map pin numbers to input objects
        self.pins = [DigitalInputDevice(pin, pull_up=pull_up) for pin in pins]


    def get_percentage(self):

        marks = self.get_digital_marks()

        # Validate active sensors vs last active
        active_marks = sum(marks)
        last_active = self.get_last_active(marks)

        # We validate last active sensor matches the total number of active sensors
        if active_marks != last_active:
            print(f"Warning: some sensors might be damaged - 0 {marks} {len(marks) - 1}")

        percentage = self.levels[last_active]

        return percentage


    def is_charging(self):
        # TODO: implement once we have hardware.
        return False

    def get_temperature(self):
        # TODO: implement once we have hardware
        return 0.0

    def get_digital_marks(self):
        # Map bool to int for better handling
        marks = [int(pin.is_active) for pin in self.pins]
        return marks

    def get_last_active(self, items):
        # Reverse array to search from right
        ritems = items[::-1]
        # Search number 1 in list
        try:
            i = ritems.index(1)
            last_active = len(ritems) - i
        except:
            last_active = 0
        # Return the index adjusted
        return last_active
