from constants import *
import math

GRAHAS_RELATE = [1.2, 1.0, 1.4, 1.0, 1.2, 1.0, 0.8, 0.8, 1.2,
                 0.8, 1.0, 1.0, 1.2, 1.0, 1.4, 1.2, 1.2, 1.2,
                 1.0, 1.2, 0.8, 1.4, 1.0, 1.2, 1.2, 1.0, 1.0,
                 1.2, 1.4, 1.2, 0.8, 1.2, 0.8, 0.8, 0.8, 0.8,
                 1.4, 1.2, 1.2, 1.2, 1.2, 0.8, 0.8, 0.8, 0.8,
                 0.8, 1.2, 0.8, 1.4, 1.0, 1.2, 1.2, 1.0, 1.0,
                 0.8, 1.0, 1.0, 1.2, 1.0, 1.4, 1.2, 1.2, 1.2,
                 1.2, 1.0, 1.4, 1.0, 1.2, 1.0, 0.8, 0.8, 1.2,
                 1.2, 1.0, 1.2, 1.0, 1.4, 1.0, 1.0, 1.2, 1.0,
                 0.8, 1.0, 1.0, 1.0, 0.8, 1.2, 1.4, 1.2, 1.2,
                 0.8, 1.0, 1.0, 1.0, 0.8, 1.2, 1.4, 1.2, 1.2,
                 1.2, 1.0, 1.2, 1.0, 1.4, 1.0, 1.0, 1.2, 1.0]

RATIO_IN_ZNAK = [-.2, .2, .2, .2, -.2, -.2, -.2, -.2, -.2, .2, .2, .2]

SUBHA_GRAHANKI = [0.03, 0.07, 0.13, 0.25, 0.37, 0.50]

GRAHAS_OVER_FALL = [1, 0, .75, 0, 0, 0, -1, 0, 0,
                    0, 1, 0, 0, 0, .75, 0, 1, -1,
                    0, 0, 0, .75, 0, 0, 0, 0, 0,
                    0, .75, -1, 0, 1, 0, 0, 0, 0,
                    .75, 0, 0, 0, 0, 0, 0, 0, .75,
                    0, 0, 0, 1, 0, -1, 0, 0, 0,
                    -1, 0, 0, 0, 0, .75, 1, 0, 0,
                    0, -1, 0, 0, 0, 0, 0, -1, 1,
                    0, 0, 0, 0, .75, 0, 0, 0, 0,
                    0, 0, 1, 0, -1, 0, .75, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, .75, 0,
                    0, 0, 0, -1, 0, 1, 0, 0, 0]


def defferense_znak(planet_in_znak, znak_kepper):
    if planet_in_znak >= znak_kepper:
        index_diff = planet_in_znak - znak_kepper
    else:
        index_diff = znak_kepper - planet_in_znak

    return index_diff


def calculate_relationS_grah(graha_in_znak, PLANETS_RANGE_TR=PLANETS_RANGE):
    power_planet = []

    for planet in PLANETS_RANGE_TR:
        power_planet.append(SUBHA_GRAHANKI[int(((GRAHAS_RELATE[planet + (graha_in_znak[planet] * 9)] +
                                                 RATIO_IN_ZNAK[defferense_znak(planet, graha_in_znak[
                                                     WHO_UPRAVLAET_ZNAKOM[graha_in_znak[planet]]])]) * 60 + .001) / 12 - 3)] + (
                                GRAHAS_OVER_FALL[graha_in_znak[planet] * 9 + planet]))

        aspect_time = int(math.fmod((graha_in_znak[planet] + 6), 12))

        if WHO_UPRAVLAET_ZNAKOM[aspect_time] == planet:
            power_planet[planet] += .75

        if WHO_UPRAVLAET_ZNAKOM[graha_in_znak[planet]] == planet:
            power_planet[planet] += 1

    return power_planet
