from typing import List, Any

import numpy as np
import math
from constants import *

verifi_planet = [0, 1, 2, 3, 4, 5, 6, 7, 8]

class choosen():
    def __init__(self, balls_house, map_vargas_in_house):
        self.balls_house = balls_house
        self.map_vargas_in_house = map_vargas_in_house


def f_lambda(m_lambda):
    if m_lambda != []:
        m_lambda = list(np.concatenate(m_lambda))
    return m_lambda


def get_matrix_vargas(planet_in_znaks, planet_in_house, filter_house, lagna):
    """
    подсчет матриц каждой варги и фильтрация ее в соответсвии с транзитным днем
    :param planet_in_znaks: планеты варги в знаках
    :param filter_planet: выборка планетам
    :param filter_house: выборка по домам
    :return: фильтрованные матрицы
    :planet_in_znaks[0][9]: записанное положение лагны
    """

    WHO_UPRAVLAET_HOUSE = list(map(lambda x: WHO_UPRAVLAET_ZNAKOM[int(math.fmod(x + planet_in_znaks[9], 12))], ZODIAK_RANGE))
    znaks_in_house = list(map(lambda x: int(math.fmod(x + lagna, 12)), ZODIAK_RANGE))

    m_lambda = list(map(lambda c: (list(filter(None, list(map(
        lambda x: int(x in list(filter(lambda x: int((int((int(planet_in_house[x] in list(map(
            lambda z: int(math.fmod(planet_in_house[c] + ASP[c][z], 12)), range(len(ASP[c])))))) and (
                                                                  filter_house[x] > 20))) * (x + 1)), PLANETS_RANGE))) * PLANET_UPRAV[x],
        PLANETS_RANGE))))), verifi_planet))

    m_lambda = list(map(lambda x: f_lambda(m_lambda[x]), range(len(m_lambda))))

    concatenate_aspects_planets = list(map(lambda c: list(map(
        lambda x: znaks_in_house[m_lambda[c][x]], range(len(m_lambda[c])))), range(len(m_lambda))))
    concatenate_upravl_planets = list(map(lambda c: list(filter(
        lambda x: int((WHO_UPRAVLAET_HOUSE[x] == c) and (filter_house[x] > 20)) * (x + 1), ZODIAK_RANGE)), verifi_planet))
    concatenate_aspects_bhavas = list(map(lambda c: list(filter(
        lambda x: int(x and (filter_house[x] > 20)) * (x + 1), list(map(
            lambda z: int(math.fmod(planet_in_house[c] + ASP[c][z], 12)), range(len(ASP[c])))))), verifi_planet))

    list_condition: List[Any] = list(
        map(lambda x, y, z: x + y + z, concatenate_aspects_planets, concatenate_upravl_planets, concatenate_aspects_bhavas))

    return list_condition


def get_calculate_analis_vargs(map_vargas_in_znaks, filter_house):
    """
        преобразование варг по отношению к лагне

        map_vargas_in_znaks - массив, в котором указано положение планеты в знаке, размерность (N х 10)
        map_vargas_in_house - массив, в котором указано положение планеты доме, относительно лагны, размерность (N х 10)

        filter_planet - массив, в котором содержатся проценты влияния планет, размерность 9
        filter_house - массив, в котором содержатся проценты влияния домов, размерность 12
    """
    map_vargas_in_house, vargas_matrix_filter, vargas_sort = [], [], []


    def filter_varg(varg):
        nonlocal vargas_matrix_filter
        lagna = map_vargas_in_znaks[varg][9]
        map_vargas_in_house.append(
            list(map(lambda x: int(math.fmod(x - lagna + 12, 12)), list(map_vargas_in_znaks[varg]))))

        vargas_matrix_filter = get_matrix_vargas(list(map_vargas_in_znaks[varg]), list(map_vargas_in_house[varg]), filter_house, lagna)

        balls_house = [0] * 12
        for n in range(len(vargas_matrix_filter)):
            for m in range(len(vargas_matrix_filter[n])):
                balls_house[vargas_matrix_filter[n][m]] += filter_house[vargas_matrix_filter[n][m]]

        if np.sum(balls_house) > 0:
            bal_max = np.max(balls_house)
            balls_house = list(map(lambda x: int(x / bal_max * 100), balls_house))

        for p in ZODIAK_RANGE:
            balls_house[p] = int(balls_house[p]/1.4)

        return balls_house

    balls_house = list(map(lambda x: filter_varg(x), np.arange(len(map_vargas_in_znaks))))

    """
        составим матрицы для каждой варги
    """

    return choosen(balls_house, map_vargas_in_house)
