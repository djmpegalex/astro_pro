import math
from constants import *
import numpy as np


BALLS_BHAVA = [60, 30, 0, 60, 60, 0, 60, 30, 60, 60, 0, 30]


def get_analis_sudarshana(massiv_sudarshana, nature_planet):
    analis_sudarshana = [0] * 12
    max_nature = -SECONDS_IN_HOUR

    """
        get maximum god effect planet
    """
    def natur_pl(i):
        nonlocal max_nature
        if nature_planet[i] > max_nature:
            max_nature = nature_planet[i]

    list(map(lambda x: natur_pl(x), PLANETS_RANGE))
    """
        analise position planets
    """

    def sudars(i):
        planet = int(math.fmod(i, NUMBER_OF_PLANETS))
        p_hause = int(massiv_sudarshana[i] / DAYS_IN_MOON_MONTH)
        if BALLS_BHAVA[p_hause] == 60:
            analis_sudarshana[p_hause] += BALLS_BHAVA[p_hause] * nature_planet[planet]
        else:
            analis_sudarshana[p_hause] += BALLS_BHAVA[p_hause] * (
                    max_nature - nature_planet[planet])

    list(map(lambda y: sudars(y), np.arange(len(massiv_sudarshana) - 1)))

    max_number = -SECONDS_IN_ZNAK
    min_number = SECONDS_IN_ZNAK

    def max_min(i):
        nonlocal max_number
        nonlocal min_number
        if max_number < analis_sudarshana[i]:
            max_number = analis_sudarshana[i]
        if min_number > analis_sudarshana[i]:
            min_number = analis_sudarshana[i]

    list(map(lambda u: max_min(u), ZODIAK_RANGE))

    return list(map(lambda x: (math.trunc((x - min_number) / (max_number - min_number) * 100)), analis_sudarshana))
