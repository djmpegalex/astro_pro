import math
import numpy as np

import calculate_relations_betwen_planets
from constants import NUMBER_OF_ASPECTS, DEGREES_IN_ZNAK, SECONDS_HALF_ZNAK, SECONDS_IN_ZODIAC, SECONDS_IN_HALF_ZODIAC, \
    PLANETS_RANGE, ASPECTS_RANGE, SUN_PLANET_NUMBER, MOON_PLANET_NUMBER, NUMBER_OF_PLANETS, WHO_UPRAVLAET_ZNAKOM_LI, NUMBER_OF_ZNAKS

def calc_data_relative(graha_in_degrees, graha_in_retrograd, graha_in_degrees_transit, is_horoscop = True):

    graha_in_degrees = np.array(graha_in_degrees) + 2500
    for planet in PLANETS_RANGE:
        if graha_in_degrees[planet] > SECONDS_IN_ZODIAC:
            graha_in_degrees[planet] -= SECONDS_IN_ZODIAC

    planets_look_grahas = []
    planets_aspects_znaks = [[],[],[],[],[],[],[],[],[]]

    planet_in_znak = np.asarray(np.asarray(graha_in_degrees) / 108000, dtype='int8')
    # planet_angles = np.array(graha_in_degrees) / 3600

    for nm in ASPECTS_RANGE:

        n = int(nm / 7)
        if not is_horoscop and n == 1: continue

        if n == (nm / 7):
            looks = []
            for n2 in PLANETS_RANGE:

                if not is_horoscop and n2 == 1: continue

                if n == n2: continue
                graha_1_deg = graha_in_degrees[n]
                graha_2_deg = graha_in_degrees[n2]
                diff = graha_2_deg - graha_1_deg
                if diff < -SECONDS_IN_HALF_ZODIAC:
                    diff = SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg
                if diff > SECONDS_IN_HALF_ZODIAC:
                    diff = -SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg

                if abs(diff) < SECONDS_HALF_ZNAK:
                    looks.append(n2)
            planets_look_grahas.append(looks)

        n_aspect = np.fmod(nm, 7)
        if graha_in_retrograd[n] == 1:
            if n_aspect in [1, 2, 3]: continue
        if graha_in_retrograd[n] == 0:
            if n_aspect in [4, 5, 6]: continue

        if n_aspect in [1, 2, 3][0:NUMBER_OF_ASPECTS[n]] or n_aspect in [4, 5, 6][0:NUMBER_OF_ASPECTS[n]]:
            znak_und_aspect = math.trunc(graha_in_degrees_transit[nm] / DEGREES_IN_ZNAK)
            planets_aspects_znaks[n].append(znak_und_aspect)

    # list_planets_in_otnoseniya_data = calculate_relations_betwen_planets.calc_rel_planets(planet_angles, planet_in_znak)
    # list_planets_in_start_otnosheniya = list_planets_in_otnoseniya_data.list_planets_in_start_otnosheniya
    # list_planets_in_znak = list_planets_in_otnoseniya_data.list_planets_in_znak

    # bad_good_data = calculate_relations_betwen_planets.calc_rel_connect_planets(planets_look_grahas,
    #                                                                             list_planets_in_start_otnosheniya, list_planets_in_znak, planet_in_znak,
    #                                                                             planets_aspects_znaks, graha_in_retrograd)
    coef = []
    for planet in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        if planet != 1:
            coef.append(planet_in_znak[planet])
        else:
            """
                Получаем номер лунного дня
            """
            diff_sun_moon_degrees = np.fmod(graha_in_degrees[SUN_PLANET_NUMBER] - \
                                            graha_in_degrees[MOON_PLANET_NUMBER] + SECONDS_IN_ZODIAC, SECONDS_IN_ZODIAC)
            diff_sun_moon_day = diff_sun_moon_degrees / 43200
            if 0<=diff_sun_moon_day<=15:
                coef.append(3)
            else:
                coef.append(1)
        # for num, rel in enumerate(bad_good_data):
        #     if (bad_good_data[num][planet][0] - bad_good_data[num][planet][1]) == 0 or \
        #             bad_good_data[num][planet][1] == 0: coef.append(0)
        #     else:
        #         good = abs(bad_good_data[num][planet][0])
        #         bad = abs(bad_good_data[num][planet][1])
        #
        #         result = math.log(int(round(good / bad, 100) * 100)+2, 10)
        #
        #         coef.append(result)

    return coef


def bacfic(graha_in_znak, lagna_in_znak):
    """
        Функция для вычисления баллов оперативного анализа карты по БАКФИК
    """

    balls_in_znaks = np.zeros(NUMBER_OF_ZNAKS)

    balls_in_znaks[lagna_in_znak] = 3  #3
    balls_in_znaks[graha_in_znak[WHO_UPRAVLAET_ZNAKOM_LI[lagna_in_znak][0]]] += 2  #2

    balls_in_znaks[graha_in_znak[SUN_PLANET_NUMBER]] += 2
    balls_in_znaks[graha_in_znak[MOON_PLANET_NUMBER]] += 3

    # распределение планет по знакам
    for planet, znak in zip(np.arange(2, 7, 1), graha_in_znak[2:7]):

        if planet == WHO_UPRAVLAET_ZNAKOM_LI[lagna_in_znak][0]: continue

        balls_in_znaks[graha_in_znak[planet]] += 1 + int(planet == WHO_UPRAVLAET_ZNAKOM_LI[znak][0])

    #TODO нужно добавить проверку на обмен между знаками

    return balls_in_znaks * 15


