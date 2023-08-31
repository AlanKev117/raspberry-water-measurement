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
        to_input = lambda pin: DigitalInputDevice(pin, pull_up=True)
        self.pins = list(map(to_input, pin_numbers))


    def get_percentage(self):

        # Map bool to int for better handling
        to_active = lambda i: int(i.is_active)
        actives = list(map(to_active, self.pins))

        # Get position of first inactive bit.
        try:
            first_inactive = actives.index(0)
        except:
            first_inactive = self.resolution

        # Assert every bit before first 0 is 1 and the rest is 0.
        prior_are_on = sum(actives[0: first_inactive]) == first_inactive
        rest_are_off = sum(actives[first_inactive: -1]) == 0

        # If correct, return the level, otherwise, return None.
        if prior_are_on and rest_are_off:
            return int(first_inactive / self.resolution * 100)
        else:
            return None


    def is_charging(self):
        # TODO: refactor once new hardware is implemented.
        return False
