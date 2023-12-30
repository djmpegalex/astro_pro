"""
    LIVE_BINDY                          продолжительность жизни натива на основе количества рекх, в днях
"""
import csv
import math
from constants import *
import numpy as np

LIVE_BINDY = [2, 1.5, 1, .5, 7.5, 720, 1440, 2160, 2880]

PINDY_ZODIAKS = [7, 10, 8, 4, 10, 5, 7, 8, 9, 5, 11, 12]
PINDY_PLANETS = [5, 5, 8, 5, 10, 7, 5]
PLANET_RASPOLOJ = [9, 4, 3, 4, 5, 7, 8]


class Chosen():
    def __init__(self, min_bindy, max_bindy, nk_trik_negativ, zn_trik_negativ):
        self.min_bindy = min_bindy
        self.max_bindy = max_bindy
        self.nk_trik_negativ = nk_trik_negativ
        self.zn_trik_negativ = zn_trik_negativ

class NewChosen():
    def __init__(self, planet_varga_sum, planet_in_goods_location):
        self.planet_varga_sum = planet_varga_sum
        self.planet_in_goods_location = planet_in_goods_location


def calculate_bindy_vargas(graha_in_znak_varga, graha_in_znaks):
    planet_varga_all = []
    min_bindy, max_bindy, nk_trik_negativ, zn_trik_negativ = [], [], [], []
    live = 0
    with open('resources/PlanetsInBINDY.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            planet_varga = []
            for planet in GRAHAS_RANGE:
                str_planet = (row[planet])
                bindy = [0] * 12
                if planet != 1:
                    for dom_pozit in ZODIAK_RANGE:
                        if str_planet[dom_pozit:(dom_pozit + 1)] == "0":
                            summ_bindy_and_graha = int(math.fmod(dom_pozit + graha_in_znak_varga[planet], 12))
                            bindy[summ_bindy_and_graha] = 1

                planet_varga.append(bindy)

            list_bindy = list(map(lambda y: sum(list(map(lambda x: planet_varga[x][y], GRAHAS_RANGE))), ZODIAK_RANGE))
            # live += sum(list(map(lambda x: LIVE_BINDY[x], list_bindy)))
            planet_varga_all.append(list_bindy)
    planet_varga_sum = list(map(lambda y: sum(list(map(lambda x: planet_varga_all[x][y], GRAHAS_RANGE))), ZODIAK_RANGE))

    planet_in_goods_location = []
    for planet in GRAHAS_RANGE:
        if planet_varga_all[planet][graha_in_znak_varga[planet]] > 4: planet_in_goods_location.append(1)
        elif planet_varga_all[planet][graha_in_znak_varga[planet]] < 4: planet_in_goods_location.append(-1)
        else: planet_in_goods_location.append(0)

    if len(graha_in_znaks) > 2:
        """
            методы трикона, экадхипатйа-шодхана и пинду сокращений
        """
        # print(planet_varga_all)
        # print("live:", int(live / 36) / 10, "years")

        for n in range(len(planet_varga_all)):
            next_varga = planet_varga_all[n]
            trikona_zip = [0] * 12
            """
                сокращение трикона
            """
            for m in range(4):
                start = int(math.fmod(m + graha_in_znaks[n], 12))
                next_list = list(map(lambda x: next_varga[int(math.fmod(start + (x * 4), 12))], range(3)))
                next_list = list(map(lambda x: next_list[x] - np.min(next_list), range(3)))
                for b in range(3):
                    trikona_zip[int(math.fmod(start + (b * 4), 12))] = next_list[b]
            """
                сокращение шодхана
            """
            for m in range(2, 7, 1):
                if ((PLANET_UPRAV[m][0] in graha_in_znaks) == False) and ((PLANET_UPRAV[m][1] in graha_in_znaks) == False):
                    next_list = [trikona_zip[PLANET_UPRAV[m][0]], trikona_zip[PLANET_UPRAV[m][1]]]
                    if trikona_zip[PLANET_UPRAV[m][0]] == trikona_zip[PLANET_UPRAV[m][1]]:
                        trikona_zip[PLANET_UPRAV[m][0]] = 0
                        trikona_zip[PLANET_UPRAV[m][1]] = 0
                    else:
                        if np.min(next_list) > 0:
                            trikona_zip[PLANET_UPRAV[m][0]] = np.max(next_list)
                            trikona_zip[PLANET_UPRAV[m][1]] = np.max(next_list)
                if ((PLANET_UPRAV[m][0] in graha_in_znaks) == False) and ((PLANET_UPRAV[m][1] in graha_in_znaks) == True):
                    if trikona_zip[PLANET_UPRAV[m][0]] > trikona_zip[PLANET_UPRAV[m][1]]:
                        trikona_zip[PLANET_UPRAV[m][0]] -= trikona_zip[PLANET_UPRAV[m][1]]
                    if trikona_zip[PLANET_UPRAV[m][0]] <= trikona_zip[PLANET_UPRAV[m][1]]:
                        trikona_zip[PLANET_UPRAV[m][0]] = 0

                if ((PLANET_UPRAV[m][0] in graha_in_znaks) == True) and ((PLANET_UPRAV[m][1] in graha_in_znaks) == False):
                    if trikona_zip[PLANET_UPRAV[m][1]] > trikona_zip[PLANET_UPRAV[m][0]]:
                        trikona_zip[PLANET_UPRAV[m][1]] -= trikona_zip[PLANET_UPRAV[m][0]]
                    if trikona_zip[PLANET_UPRAV[m][1]] <= trikona_zip[PLANET_UPRAV[m][0]]:
                        trikona_zip[PLANET_UPRAV[m][1]] = 0
            """
                пинду сокращение
            """
            rashi_pinda = sum(list(map(lambda x: trikona_zip[x] * PINDY_ZODIAKS[x], range(12))))
            graha_pinda = sum(list(map(lambda x: trikona_zip[graha_in_znaks[x]] * PINDY_PLANETS[x], range(7))))
            shodia_pinda = rashi_pinda + graha_pinda
            """
                вычисление неблагоприятных накшатр и знаков для каждой из грах при транзите сатурна через них
            """

            mtpl_pinda = planet_varga_sum[int(math.fmod(graha_in_znaks[n] + PLANET_RASPOLOJ[n], 12))] * shodia_pinda
            nk_trik_negativ_ones = list(map(lambda x: int(math.fmod(int(math.fmod(mtpl_pinda, 27)) + x * 9, 27)), range(3)))
            zn_trik_negativ_ones = list(map(lambda x: int(math.fmod(int(math.fmod(mtpl_pinda, 12)) + x * 4, 12)), range(3)))

            min_bindy_ones = list(filter(lambda x: int(planet_varga_all[n][x] == np.min(planet_varga_all[n])) * (x + 1), ZODIAK_RANGE))
            max_bindy_ones = list(filter(lambda x: int(planet_varga_all[n][x] == np.max(planet_varga_all[n])) * (x + 1), ZODIAK_RANGE))

            nk_trik_negativ.append(nk_trik_negativ_ones)
            zn_trik_negativ.append(zn_trik_negativ_ones)
            min_bindy.append(min_bindy_ones)
            max_bindy.append(max_bindy_ones)

            """
                min_bindy, max_bindy знаки при которых бинду минимальны и максимальны. нужно для транзитов и вывод в цвет
                nk_trik_negativ, zn_trik_negativ транзиты сатурна дает неблагоприятные результаты по функции той или иной грахи
            """
        return Chosen(min_bindy, max_bindy, nk_trik_negativ, zn_trik_negativ)
    elif len(graha_in_znaks) > 1:
        return NewChosen(planet_varga_sum, planet_in_goods_location)
    else:
        return planet_varga_sum
