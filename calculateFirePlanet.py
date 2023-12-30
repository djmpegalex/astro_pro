from constants import *

FIRE_PLANET_AT_SUN = [-1, 43200, 61200, 50400, 39600, 36000, 57600, -1.0, -1.0]


def calculate_fire_planet_func(grahas_degrees):
    fire_planets = [1.0] * NUMBER_OF_PLANETS
    for ind in PLANETS_RANGE:
        if FIRE_PLANET_AT_SUN != -1:
            between_surya_degrees = abs(grahas_degrees[SUN_PLANET_NUMBER] - grahas_degrees[ind])
            if abs(between_surya_degrees) <= FIRE_PLANET_AT_SUN[ind]:
                fire_planets[ind] = 0
            else:
                fire_planets[ind] = round(between_surya_degrees / SECONDS_IN_ZODIAC * 20, 2)

    return fire_planets
