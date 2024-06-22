import logging

from gpiozero import DigitalInputDevice

from WaterLevelSensor import WaterLevelSensor

MAX_RESOLUTION = 26
MIN_RESOLUTION = 1

RESOLUTION_WARN = "Resolution must be between {} and {}."
RESOLUTION_WARN = RESOLUTION_WARN.format(MIN_RESOLUTION, MAX_RESOLUTION)

WRONG_ORDER_WARN = "Cables in the discrete sensor are misplaced."

class DiscreteWaterLevelSensor(WaterLevelSensor):

    def __init__(self, pin_numbers=[1,2,3,4,5,6,7,8,9,10]):
        
        # Assert resolution limits so there's no conflict with gpiozero.
        resolution = len(pin_numbers)
        assert MIN_RESOLUTION <= resolution <= MAX_RESOLUTION, RESOLUTION_WARN
        self.resolution = resolution

        # Map pin numbers to input objects
        self.pins = [DigitalInputDevice(pin, pull_up=True) for pin in pin_numbers]


    def get_percentage(self):

        marks = self.get_digital_marks()

        # Validate active sensors vs last active
        active_marks = sum(marks)
        last_active = self.get_last_active(marks)

        if active_marks != last_active:
            print(f"Warning: some sensors might be damaged - 0 {marks} {len(marks) - 1}")

        percentage = int(last_active / self.resolution * 100)
        return percentage


    def is_charging(self):
        # TODO: refactor once new hardware is implemented.
        return False

    def get_temperature(self):
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
