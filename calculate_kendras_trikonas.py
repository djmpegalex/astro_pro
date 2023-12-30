from constants import *
import math
import numpy as np

def summ_dristi(graha_in_house, drishti_planet):
    drishti = math.fmod((graha_in_house + drishti_planet), ZNAKS_IN_ZODIAK)

    return drishti


def kendra_trikonas(absolut_nature_planet, graha_in_house, hozaeva_in_house, PLANETS_RANGE_TR=PLANETS_RANGE):
    power_kendr_trikon = absolut_nature_planet

    for houses in [0, 3, 4, 6, 8, 9]:

        """
            выведем планету, которая управляет кендрой или триконой
        """

        power_kendr_trikon[hozaeva_in_house[houses]] += 0.25

        if (houses == 4) or (houses == 8) or (houses == 0):
            power_kendr_trikon[hozaeva_in_house[houses]] += 2

            """
                установим планеты, которые соеденены с правителями триконы
            """

            for planet in PLANETS_RANGE:
                if graha_in_house[hozaeva_in_house[houses]] == graha_in_house[planet]:
                    if hozaeva_in_house[houses] != planet:
                        power_kendr_trikon[planet] += 3

        for i in PLANETS_RANGE:
            """
                выведем планету, которая аспектирует трикону или кендру, а также собственный знак
            """

            for aspect in np.arange(3):
                if (houses == int(summ_dristi(graha_in_house[i], DRISHTI_PLANETS[i * 3 + aspect]))) and (
                        DRISHTI_PLANETS[i * 3 + aspect] < 10):
                    power_kendr_trikon[i] += 0.5

                if (hozaeva_in_house[houses] == hozaeva_in_house[int(summ_dristi(graha_in_house[i], DRISHTI_PLANETS[i * 3 + aspect]))]) and (
                        DRISHTI_PLANETS[i * 3 + aspect] < 10):
                    power_kendr_trikon[i] += 1.5

            """
                выведем планету, расположенную в кендре или триконе
            """

            if houses == graha_in_house[i]:
                power_kendr_trikon[i] += 0.5

                """
                    выведем планету, которая находится в доме хозяина расположенного в кендре или триконе
                """

                for xxx in ZODIAK_RANGE:
                    if hozaeva_in_house[xxx] == i:

                        for yyy in PLANETS_RANGE:
                            if graha_in_house[yyy] == xxx:
                                power_kendr_trikon[yyy] += 0.25

    return power_kendr_trikon
