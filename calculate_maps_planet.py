from constants import *


class ChoiceMap():
    def __init__(self, graha_in_degrees, graha_in_house):
        self.graha_in_degrees = graha_in_degrees
        self.graha_in_house = graha_in_house


def get_new_map_from_planets(graha_in_degrees, PLANET_NUMBER):
    graha_nm_degrees, graha_nm_house = [0] * 9, [0] * 9
    for pozition in PLANETS_RANGE:

        diff_sun_and_planets = graha_in_degrees[pozition] - graha_in_degrees[PLANET_NUMBER]

        if diff_sun_and_planets >= 0:
            graha_nm_degrees[pozition] = diff_sun_and_planets
        else:
            graha_nm_degrees[pozition] = SECONDS_IN_ZODIAC + diff_sun_and_planets

        graha_nm_house[pozition] = int(graha_nm_degrees[pozition] / SECONDS_IN_ZNAK)

    return ChoiceMap(graha_nm_degrees, graha_nm_house)
