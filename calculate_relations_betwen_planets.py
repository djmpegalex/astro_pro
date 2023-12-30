from typing import List
import copy

from constants import RESULT_EKSALTATION, \
    WHO_UPRAVLAET_ZNAKOM, NAME_BALA, PLANETS_RANGE, SCALA_BALA, NAME_LIGHT_TR, RELATION_PLANETS_START, DICT_BALA, \
    NATURE_PLANETS, FRND, ENEM, NTRL, WHO_UPRAVLAET_ZNAKOM_LI, RATION_SPEED, EKSATS_PLANETS_IN_ZNAKS, \
    JUPITER_PLANET_NUMBER, SELF
from numpy import fmod as np_fmod

class Chousen():

    def __init__(self,list_planets_in_otnoseniya, list_in_simple_otnosheniya, list_planets_in_start_otnosheniya,
                 list_planets_in_znak):

        self.list_planets_in_otnoseniya = list_planets_in_otnoseniya
        self.list_in_simple_otnosheniya = list_in_simple_otnosheniya
        self.list_planets_in_start_otnosheniya = list_planets_in_start_otnosheniya
        self.list_planets_in_znak = list_planets_in_znak

def calc_rel_planets(planet_angles, planet_in_znak):
    """
       временные отношения грах, взависимости где они расположены
    """
    list_planets_in_otnoseniya = []
    list_in_simple_otnosheniya = []
    list_planets_in_start_otnosheniya = []

    list_planets_in_znak = [] # Массив, показывающий, с какими планетами планета находится в одном знаке

    for n in PLANETS_RANGE[0:9]:
        n_index = 4
        for m, m_index in enumerate(SCALA_BALA):
            if (planet_angles[n] >= RESULT_EKSALTATION[n][m][0]) and (planet_angles[n] < RESULT_EKSALTATION[n][m][1]):
                n_index = m_index
                break

        otnoseniya = NAME_BALA[n_index]
        list_planets_in_start_otnosheniya.append(otnoseniya)
        planets_in_common_znak = []
        for n2 in PLANETS_RANGE[0:9]:
            if n == n2: continue
            if planet_in_znak[n] == planet_in_znak[n2]:
                planets_in_common_znak.append(n2)

        list_planets_in_znak.append(planets_in_common_znak)

        if np_fmod(
                planet_in_znak[WHO_UPRAVLAET_ZNAKOM[planet_in_znak[n]]] - planet_in_znak[n] + 12, 12) in [
            9, 3, 10, 2, 1, 11]: otnoseniya_times = 'в дружественном'
        else: otnoseniya_times = 'во вражеском'

        if (otnoseniya == otnoseniya_times) and (otnoseniya_times == 'в дружественном'):
            otnoseniya = 'большой друг'
        elif (otnoseniya == otnoseniya_times) and (otnoseniya_times == 'во вражеском'):
            otnoseniya = 'большой враг'
        elif (otnoseniya == 'в дружественном') and (otnoseniya_times == 'во вражеском'):
            otnoseniya = 'в нейтральном'
        elif (otnoseniya == 'в нейтральном') and (otnoseniya_times == 'во вражеском'):
            otnoseniya = 'во вражеском'
        elif (otnoseniya == 'в нейтральном') and (otnoseniya_times == 'в дружественном'):
            otnoseniya = 'в дружественном'

        if otnoseniya in NAME_LIGHT_TR[0:5]: list_in_simple_otnosheniya.append(1)
        elif otnoseniya in NAME_LIGHT_TR[6:9]: list_in_simple_otnosheniya.append(-1)
        else: list_in_simple_otnosheniya.append(0)

        list_planets_in_otnoseniya.append(otnoseniya)

    return Chousen(list_planets_in_otnoseniya, list_in_simple_otnosheniya, list_planets_in_start_otnosheniya,
                   list_planets_in_znak)

def calc_rel_connect_planets(planets_look_grahas, list_planets_in_start_otnosheniya,
                             list_planets_in_znak, planet_in_znak, planets_aspects_znaks, graha_in_retrograd):

    planets_base_bals: List[List[int]] = []
    total_bals = [[0, -100], [50, -50], [0, -100], [0, 0], [100, 0], [100, 0], [0, -100], [0, -100], [0, -100]]
    # total_bals = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

    planets_total_bals = copy.deepcopy(total_bals)

    for param in list_planets_in_start_otnosheniya:
        planets_base_bals.append(list(DICT_BALA[param]))

    """
        Планета входит в знак, которым управляет другая планета
    """
    for planet_1 in PLANETS_RANGE:
        for n, rltn in zip([0, 1], [FRND, ENEM]):
            for planet_2 in WHO_UPRAVLAET_ZNAKOM_LI[planet_in_znak[planet_1]]:
                planets_base_bals[planet_2][n] += (DICT_BALA[RELATION_PLANETS_START[planet_2][planet_1]][n] * RATION_SPEED[n])

    """
        Планета аспектирует знак которым управляет другая планета
    """
    for planet_1 in PLANETS_RANGE:
        for n, rltn in zip([0, 1], [FRND, ENEM]):
            for aspects_znak in planets_aspects_znaks[planet_1]:
                for planet_2 in WHO_UPRAVLAET_ZNAKOM_LI[aspects_znak]:
                    planets_base_bals[planet_2][n] += (DICT_BALA[RELATION_PLANETS_START[planet_2][planet_1]][n] * RATION_SPEED[n])

    """
        Планета входит в знак которым управляет сама
    """
    for planet_1 in PLANETS_RANGE:
        for n, rltn in zip([0], [SELF]):
            for planet_1 in WHO_UPRAVLAET_ZNAKOM_LI[planet_in_znak[planet_1]]:
                planets_base_bals[planet_1][n] += (DICT_BALA[RELATION_PLANETS_START[planet_1][planet_1]][n] * RATION_SPEED[n])


    for planet_1, look_planets in enumerate(planets_look_grahas):
        for n, rltn in zip([0, 1], [FRND, ENEM]):

            planets_total_bals[planet_1][n] += planets_base_bals[planet_1][n]

            for planet_2 in list_planets_in_znak[planet_1]:
                planets_total_bals[planet_1][n] += (planets_base_bals[planet_2][n] * RATION_SPEED[n])

            for planet_2 in look_planets:
                if planet_in_znak[planet_2] == planet_in_znak[planet_1]:
                    planets_total_bals[planet_1][n] += (planets_base_bals[planet_2][n] * RATION_SPEED[n])

            """
                Планета в знаке экзальтации другой планеты
            """
            for planet_2 in PLANETS_RANGE:
                if planet_in_znak[planet_2] == EKSATS_PLANETS_IN_ZNAKS[planet_1]:
                    planets_total_bals[planet_1][n] += (planets_base_bals[planet_2][n] * RATION_SPEED[n])

    """
        Нужно еще учитывать, что Юпитер находится в знаке управляющей планеты и все что происходит
        с этой планетой отражается тоже на юпитере
    """
    for n, rltn in zip([0, 1], [FRND, ENEM]):
        for planet_2 in WHO_UPRAVLAET_ZNAKOM_LI[planet_in_znak[JUPITER_PLANET_NUMBER]]:
            if planet_2 != JUPITER_PLANET_NUMBER:
                planets_total_bals[JUPITER_PLANET_NUMBER][n] -= (planets_base_bals[planet_2][n] * RATION_SPEED[n])

    """
        Дифференциация планет по знакам
    """
    znak_coef = [1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10]
    for n in [0, 1]:
        for planet in PLANETS_RANGE:
            planets_total_bals[planet][n] += znak_coef[planet_in_znak[planet]]

    return [planets_total_bals]
