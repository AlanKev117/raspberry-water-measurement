import logging

from WaterLevelSensor import WaterLevelSensor

from gpiozero import SmoothedInputDevice


MAX_RESOLUTION = 27
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
        to_input = lambda pin: SmoothedInputDevice(pin)
        self.pins = list(map(to_input, pin_numbers))


    def get_percentage(self) -> int:
        to_active = lambda i: int(i.is_active)
        actives = list(map(to_active, self.pins))
        first_inactive = actives.index(0)
        assert sum(actives[first_inactive: -1]) == 0, WRONG_ORDER_WARN
        return int(first_inactive / self.resolution * 100)


    def is_charging(self) -> bool:
        # TODO: refactor once new hardware is implemented.
        return False
