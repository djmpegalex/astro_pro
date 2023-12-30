from dictsData import dictOfAspects
import math
from constants import *

# данные об аспектах планет, взависимости от удаления от аспектирующей планеты
aspect_dict = dictOfAspects.get_aspects_strenght_data()
# градусы
degrees_aspect_dict = dictOfAspects.get_aspects_degrees(aspect_dict)

PLANET_RATIO_ASPECT = [0.25, 0.25, 0.25, 1.00, 1.00, 0.25, 0.25, 0.25, 0.25]

BHAVA_DEGREES = [54000, 162000, 270000, 378000, 486000, 594000, 702000, 810000, 918000, 1026000, 1134000, 1242000]
HALF_MIN = 1800


def get_middle_degrees(difference):
    difference = ((math.trunc(difference / HALF_MIN)) * HALF_MIN)

    return difference


def get_strenght_aspect_on_planets(grahas_degrees, nature_planets):
    to_planet_aspect = [0] * NUMBER_OF_PLANETS

    for from_graha in PLANETS_RANGE:
        for to_graha in PLANETS_RANGE:
            range_degr = float(get_middle_degrees(get_pozitiv_number(grahas_degrees[from_graha], grahas_degrees[to_graha])))
            strenght_of_aspect = [aspect_dict.get(range_degr).sun_strenght,
                                  aspect_dict.get(range_degr).moon_strenght,
                                  aspect_dict.get(range_degr).mars_strenght,
                                  aspect_dict.get(range_degr).mercury_strenght,
                                  aspect_dict.get(range_degr).jupiter_strenght,
                                  aspect_dict.get(range_degr).venus_strenght,
                                  aspect_dict.get(range_degr).saturn_strenght,
                                  aspect_dict.get(range_degr).rahy_strenght,
                                  aspect_dict.get(range_degr).kety_strenght]

            to_planet_aspect[to_graha] += (strenght_of_aspect[from_graha] * nature_planets[from_graha]) * PLANET_RATIO_ASPECT[
                from_graha] / 60

    return to_planet_aspect


def get_strenght_aspect_on_bhavas(grahas_degrees, nature_planets):
    to_bhava_aspect = [0] * ZNAKS_IN_ZODIAK

    for to_bhava in ZODIAK_RANGE:
        for from_graha in PLANETS_RANGE:
            range_degr = float((math.trunc(get_pozitiv_number(grahas_degrees[from_graha], BHAVA_DEGREES[to_bhava]) / HALF_MIN)) * HALF_MIN)
            strenght_of_aspect = [aspect_dict.get(range_degr).sun_strenght,
                                  aspect_dict.get(range_degr).moon_strenght,
                                  aspect_dict.get(range_degr).mars_strenght,
                                  aspect_dict.get(range_degr).mercury_strenght,
                                  aspect_dict.get(range_degr).jupiter_strenght,
                                  aspect_dict.get(range_degr).venus_strenght,
                                  aspect_dict.get(range_degr).saturn_strenght,
                                  aspect_dict.get(range_degr).rahy_strenght,
                                  aspect_dict.get(range_degr).kety_strenght]

            to_bhava_aspect[to_bhava] += (strenght_of_aspect[from_graha] * nature_planets[from_graha]) * PLANET_RATIO_ASPECT[
                from_graha] / 60

    return to_bhava_aspect


def get_pozitiv_number(from_planet, to_planet):
    difference = from_planet

    if (from_planet + to_planet) < SECONDS_IN_ZODIAC:
        if from_planet >= to_planet:
            difference -= to_planet
        else:
            difference = (to_planet - difference)
    else:
        difference += abs(SECONDS_IN_ZODIAC - difference + to_planet)

    if difference >= SECONDS_IN_ZODIAC:
        difference -= SECONDS_IN_ZODIAC

    return difference


def znak_number(new_number):
    if new_number != 0:
        new_number /= new_number

    return new_number
