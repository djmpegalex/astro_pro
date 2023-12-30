import calculateCoordsPlanet
import math
import numpy as np
from constants import *


class choose_option():
    def __init__(self, graha_in_degrees_transit, natal_moon_degrees, graha_in_degrees,graha_in_retrograd, graha_speed):
        self.graha_in_degrees_transit = graha_in_degrees_transit
        self.natal_moon_degrees = natal_moon_degrees
        self.graha_in_degrees = graha_in_degrees
        self.graha_in_retrograd = graha_in_retrograd
        self.graha_speed = graha_speed


def calculate_tranzit_map(new_date_tranzit, first_date, first_time, lagna=None, delta=0):
    rashi_data = calculateCoordsPlanet.calculate_coords_planet(first_date, first_time, delta=delta)
    graha_in_degrees = rashi_data.graha_in_degrees

    if lagna is None: natal_moon_degrees = int(graha_in_degrees[1] / 108000) * 108000
    else: natal_moon_degrees = int(lagna) * 108000

    rashi_data = calculateCoordsPlanet.calculate_coords_planet(new_date_tranzit, first_time, delta=delta)
    graha_in_degrees = rashi_data.graha_in_degrees
    graha_in_retrograd = rashi_data.retrogr_planet
    graha_in_retrograd[7], graha_in_retrograd[8] = 1, 1
    graha_speed = rashi_data.speed_planet

    graha_in_degrees_transit = list(
        map(lambda x: (math.fmod(x - natal_moon_degrees + 1296000, 1296000) / 3600), graha_in_degrees))

    graha_aspects = list(map(lambda x: 0, np.arange(63)))

    def calc_trans(n):
        poz = n * 7

        graha_aspects[poz] = graha_in_degrees_transit[n]
        if graha_in_retrograd[n] == 0:
            graha_aspects[poz + 1] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3] * 30), 360)
            graha_aspects[poz + 2] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3 + 1] * 30), 360)
            graha_aspects[poz + 3] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3 + 2] * 30), 360)
        else:
            graha_aspects[poz + 1] = math.fmod((graha_in_degrees_transit[n] + (DPLA[n * 3] - 1) * 30), 360)
            graha_aspects[poz + 2] = math.fmod((graha_in_degrees_transit[n] + (DPLA[n * 3 + 1] - 1) * 30), 360)
            graha_aspects[poz + 3] = math.fmod((graha_in_degrees_transit[n] + (DPLA[n * 3 + 2] - 1) * 30), 360)

        if graha_in_retrograd[n] == 1:
            graha_aspects[poz + 4] = math.fmod((graha_in_degrees_transit[n] + (DPLA[n * 3] - 1) * 30), 360)
            graha_aspects[poz + 5] = math.fmod((graha_in_degrees_transit[n] + (DPLA[n * 3 + 1] - 1) * 30), 360)
            graha_aspects[poz + 6] = math.fmod((graha_in_degrees_transit[n] + (DPLA[n * 3 + 2] - 1) * 30), 360)
        else:
            graha_aspects[poz + 4] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3] * 30), 360)
            graha_aspects[poz + 5] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3 + 1] * 30), 360)
            graha_aspects[poz + 6] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3 + 2] * 30), 360)

    list(map(lambda x: calc_trans(x), PLANETS_RANGE))

    return choose_option(graha_aspects, natal_moon_degrees,graha_in_degrees, graha_in_retrograd, graha_speed)


def calc_aspects(graha_in_znaks):
    graha_aspects = []
    for m in PLANETS_RANGE:
        graha_aspects.extend((graha_in_znaks[m],
                              int(math.fmod((graha_in_znaks[m] + DPLA[m * 3]), 12)),
                              int(math.fmod((graha_in_znaks[m] + DPLA[m * 3 + 1]), 12)),
                              int(math.fmod((graha_in_znaks[m] + DPLA[m * 3 + 2]), 12)),
                              int(math.fmod((graha_in_znaks[m] + DPLA[m * 3]), 12)),
                              int(math.fmod((graha_in_znaks[m] + DPLA[m * 3 + 1]), 12)),
                              int(math.fmod((graha_in_znaks[m] + DPLA[m * 3 + 2]), 12))))

    return graha_aspects


def calculate_VRGAspect_map(graha_in_degrees, graha_in_retrograd):
    natal_moon_degrees = graha_in_degrees[1]

    graha_in_degrees_transit = list(
        map(lambda x: (math.fmod(x - natal_moon_degrees + 1296000, 1296000) / 3600), graha_in_degrees))

    graha_aspects = list(map(lambda x: 0, np.arange(63)))

    def calc_trans(n):
        poz = n * 7

        graha_aspects[poz] = graha_in_degrees_transit[n]
        graha_aspects[poz + 1] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3] * 30), 360)
        graha_aspects[poz + 2] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3 + 1] * 30), 360)
        graha_aspects[poz + 3] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3 + 2] * 30), 360)

        if graha_in_retrograd[n] == 1:
            graha_aspects[poz + 4] = math.fmod((graha_in_degrees_transit[n] + (DPLA[n * 3] - 1) * 30), 360)
            graha_aspects[poz + 5] = math.fmod((graha_in_degrees_transit[n] + (DPLA[n * 3 + 1] - 1) * 30), 360)
            graha_aspects[poz + 6] = math.fmod((graha_in_degrees_transit[n] + (DPLA[n * 3 + 2] - 1) * 30), 360)
        else:
            graha_aspects[poz + 4] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3] * 30), 360)
            graha_aspects[poz + 5] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3 + 1] * 30), 360)
            graha_aspects[poz + 6] = math.fmod((graha_in_degrees_transit[n] + DPLA[n * 3 + 2] * 30), 360)

    list(map(lambda x: calc_trans(x), PLANETS_RANGE))

    return choose_option(graha_aspects, natal_moon_degrees)


def get_obmen_znakami(tranzit_in_znak=None):

    in_obmens = []

    # планета 1 находится в знаке Меркурий в Овне
    for planet1 in PLANETS_RANGE:

        # смотрим управителей знака, в котором находится планета 1 - управитель Овна = Марс
        upravitels = WHO_UPRAVLAET_ZNAKOM_LI[tranzit_in_znak[planet1]]

        # Перебираем управителей знака
        for upravitel in upravitels:

            # смотрим расположение управителя знака - Марс в Близнецах
            upravitel_in_znak = tranzit_in_znak[upravitel]

            # смотрим кто управляет знаком, где находится управитель того знака, где находится планета1
            upravitels2 = WHO_UPRAVLAET_ZNAKOM_LI[upravitel_in_znak]

            # ищем управителя кто управляет знаком - Меркурий
            for upravitel2 in upravitels2:

                # если возвращаемся к изначальной планете, то происходит обмен
                if upravitel2 == planet1 and tranzit_in_znak[planet1] != tranzit_in_znak[upravitel]:
                    in_obmens.append(planet1)
                    in_obmens.append(upravitel)

    return np.unique(in_obmens)
