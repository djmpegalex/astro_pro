import math
from constants import *

E_GROUND = 5
E_FIRE = 7
E_WATER = 11
E_OXUGEN = 13
E_EFIR = 17

ZNAKS_OF_ELEMENT = [E_FIRE, E_GROUND, E_OXUGEN, E_WATER,
                    E_FIRE, E_GROUND, E_OXUGEN, E_WATER,
                    E_FIRE, E_GROUND, E_OXUGEN, E_WATER]
PLANET_OF_ELEMENT = [E_FIRE, E_WATER, E_FIRE, E_GROUND, E_EFIR, E_WATER, E_OXUGEN, E_OXUGEN, E_FIRE]

def strenght_first_elements(graha_in_znake, PLANETS_RANGE_TR=PLANETS_RANGE):
    power_elements_planet = []

    for i in PLANETS_RANGE_TR:
        if ZNAKS_OF_ELEMENT[graha_in_znake[i]] == PLANET_OF_ELEMENT[i]:
            power_elements_planet.append(60)
        elif (ZNAKS_OF_ELEMENT[graha_in_znake[i]] + PLANET_OF_ELEMENT[i]) == 18:
            power_elements_planet.append(0)
        else:
            power_elements_planet.append(30)

    return power_elements_planet