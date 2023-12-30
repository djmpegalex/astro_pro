import math
from constants import *


class ChoiseData():
    def __init__(self, graha_in_degrees, absolut_dergrees_planets, graha_in_nakshatra,
                 graha_in_znak, graha_in_house, hozaeva_in_house, graha_in_gradus, graha_in_znak_parts):
        self.graha_in_degrees = graha_in_degrees
        self.absolut_dergrees_planets = absolut_dergrees_planets
        self.graha_in_nakshatra = graha_in_nakshatra
        self.graha_in_znak = graha_in_znak
        self.graha_in_house = graha_in_house
        self.hozaeva_in_house = hozaeva_in_house
        self.graha_in_gradus = graha_in_gradus
        self.graha_in_znak_parts = graha_in_znak_parts


def calculate_rashi_card(graha_in_degrees, locate_lagna):
    hozaeva_in_house = [-1] * 12
    graha_in_znak, graha_in_nakshatra, graha_in_house, \
    graha_in_gradus, absolut_dergrees_planets, graha_in_znak_parts = [0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9

    for pozition in PLANETS_RANGE:

        if graha_in_degrees[pozition] < 0:
            graha_in_degrees[pozition] += SECONDS_IN_ZODIAC

        pos_znak = graha_in_degrees[pozition]
        absolut_dergrees_planets[pozition] = ((pos_znak / SECONDS_IN_ZNAK) - (math.trunc(pos_znak / SECONDS_IN_ZNAK))) * SECONDS_IN_ZNAK

        graha_in_nakshatra[pozition] = math.trunc(graha_in_degrees[pozition] / SECONDS_IN_NAKSHATRA * 10) / 10
        graha_in_znak_parts[pozition] = graha_in_degrees[pozition] / SECONDS_IN_ZNAK
        graha_in_znak[pozition] = int(graha_in_znak_parts[pozition])

        graha_in_house[pozition] = int(graha_in_znak[pozition] - locate_lagna)
        graha_in_house[pozition] = int(math.fmod(graha_in_house[pozition], SECONDS_IN_ZNAK))

        if graha_in_house[pozition] < 0:
            graha_in_house[pozition] += ZNAKS_IN_ZODIAK

        graha_in_gradus[pozition] = int(absolut_dergrees_planets[pozition] / 3600)

    for pozition in ZODIAK_RANGE:
        if pozition - locate_lagna >= 0:
            hozaeva_in_house[int(pozition - locate_lagna)] = WHO_UPRAVLAET_ZNAKOM[pozition]
        else:
            hozaeva_in_house[int(pozition - locate_lagna + ZNAKS_IN_ZODIAK)] = WHO_UPRAVLAET_ZNAKOM[pozition]
    graha_in_znak_parts.append(locate_lagna)
    return ChoiseData(graha_in_degrees,
                      absolut_dergrees_planets,
                      graha_in_nakshatra,
                      graha_in_znak,
                      graha_in_house,
                      hozaeva_in_house,
                      graha_in_gradus, graha_in_znak_parts)
