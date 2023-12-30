import math
import numpy as np

import calculate_compound_file
import calculateRashi
import calculate_kendras_trikonas
import calculate_kepper
import calculate_relations_file
import calculateFirePlanet
import calculatePowerPlanetInZnaks
import calculate_strenght_first_elements
import calculateVimshopakaBala
import calculator_aspects_planet
import calculate_jogakaraky

from constants import *

POSITION_GRAHA = [-60, 0, -60, 60, 60, 0, -60, 0, 0]
NAYASARGIKA_BALA = [60 * 1.000, 60 * 0.857, 60 * 0.286, 60 * 0.429, 60 * 0.571, 60 * 0.714, 60 * 0.143, 60 * 1.000,
                    60 * 0.750]

POWER_GRAH_IN_HOUSE = [60, 30, 15, 60, 30, 15, 60, 30, 15, 60, 30, 15]


def calculate_power_planet(graha_in_degrees, retrogr_planet, lagna_in_seconds):
    """
        param:  graha_in_degrees - градусы планет в варге
                retrogr_planet - ретроградные планеты
                lagna_in_seconds - расположение планеты-лагны в основной карте транзита

        return: ratio_of_good_planet - силу 9 планет в варге, относительно назначения лагны

    """

    """
        вычисление лагны
    """
    lagna_in_seconds_znak = math.fmod(lagna_in_seconds, 108000)
    polojenie_lagna_rashi = int(lagna_in_seconds / 108000)

    """
        построение карты раши D1 относительно варги
    """
    map_rashi = calculateRashi.calculate_rashi_card(graha_in_degrees, polojenie_lagna_rashi)

    graha_in_degrees = map_rashi.graha_in_degrees
    absolut_dergrees_planets = map_rashi.absolut_dergrees_planets
    filter_dashas = list(map(lambda x: int(x / 36000), absolut_dergrees_planets))
    for n in PLANETS_RANGE:
        if retrogr_planet[n] == 1:
            if filter_dashas[n] == 2:
                filter_dashas[n] = 0
                continue
            if filter_dashas[n] == 0: filter_dashas[n] = 2

    graha_in_znak = map_rashi.graha_in_znak
    graha_in_house = map_rashi.graha_in_house
    hozaeva_in_house = map_rashi.hozaeva_in_house

    """
        вычисление аспектов планет
    """
    graha_in_degrees_rashi_as = list(
        map(lambda x: int(math.fmod(x / 3600 - (polojenie_lagna_rashi * 30) + 360, 360)), graha_in_degrees))

    bhava_aspects_rashi = list(map(lambda x: 0, np.arange(63)))

    def bhava_aspec(n):
        poz = int(n * 7)

        bhava_aspects_rashi[poz] = graha_in_degrees_rashi_as[n]
        bhava_aspects_rashi[poz + 1] = math.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3] * 30), 360)
        bhava_aspects_rashi[poz + 2] = math.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3 + 1] * 30), 360)
        bhava_aspects_rashi[poz + 3] = math.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3 + 2] * 30), 360)

        if retrogr_planet[n] == 1:
            bhava_aspects_rashi[poz + 4] = math.fmod((graha_in_degrees_rashi_as[n] + (DPLA[n * 3] - 1) * 30), 360)
            bhava_aspects_rashi[poz + 5] = math.fmod((graha_in_degrees_rashi_as[n] + (DPLA[n * 3 + 1] - 1) * 30), 360)
            bhava_aspects_rashi[poz + 6] = math.fmod((graha_in_degrees_rashi_as[n] + (DPLA[n * 3 + 2] - 1) * 30), 360)
        else:
            bhava_aspects_rashi[poz + 4] = math.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3] * 30), 360)
            bhava_aspects_rashi[poz + 5] = math.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3 + 1] * 30), 360)
            bhava_aspects_rashi[poz + 6] = math.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3 + 2] * 30), 360)

    list(map(lambda x: bhava_aspec(x), PLANETS_RANGE))

    """
        подсчет силовых характеристик планет
    """

    map_vargas = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, graha_in_znak,
                                                                       ALL_VARGAS_PARTS, lagna_in_seconds_znak, polojenie_lagna_rashi)

    bala_shodasha = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, graha_in_znak,
                                                                          VARGA_SHODASHA, lagna_in_seconds_znak, -1)
    bala_sapta = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, graha_in_znak,
                                                                       VARGA_SAPTA, lagna_in_seconds_znak, -1)
    bala_even_odd = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, graha_in_znak,
                                                                          EVEN_ODD, lagna_in_seconds_znak, -1)
    """
        вычисление естественной силы грах
    """
    bala_shad = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, graha_in_znak,
                                                                      VARGA_SHAD, lagna_in_seconds_znak, -1)

    nature_planet_strenght = list(map(lambda x, y: x + y, bala_shad, NAYASARGIKA_BALA))
    """
        подсчет природы планет (благотворность и пагубность)
    """
    planet_nature_and_rising_sign = PlanetNatureCalculator().calculate(graha_in_degrees)
    bindy_nature_grahas = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, graha_in_znak,
                                                                                BINDY_VARGA_CHARITY, lagna_in_seconds_znak, -1)

    """
        определение планет йога-караки (благоприятной планеты)
    """
    planet_jogakaraky_D1 = calculate_jogakaraky.get_calculate_jogakaraky(graha_in_znak, polojenie_lagna_rashi, retrogr_planet, planet_nature_and_rising_sign)
    planet_jogakaraky_D9 = calculate_jogakaraky.get_calculate_jogakaraky(map_vargas[8], map_vargas[8][9], retrogr_planet, planet_nature_and_rising_sign)

    """
        переиначим природу планет
    """
    if len(planet_jogakaraky_D1.list_good_planets_joga) > 0:
        for x_planet in PLANETS_RANGE:
            for val_x in np.arange(len(planet_jogakaraky_D1.list_good_planets_joga)):
                if planet_jogakaraky_D1.list_good_planets_joga[val_x][0] == x_planet: planet_nature_and_rising_sign[x_planet] = planet_jogakaraky_D1.list_good_planets_joga[val_x][1]
    if len(planet_jogakaraky_D9.list_good_planets_joga) > 0:
        for x_planet in PLANETS_RANGE:
            for val_x in np.arange(len(planet_jogakaraky_D9.list_good_planets_joga)):
                if planet_jogakaraky_D9.list_good_planets_joga[val_x][0] == x_planet: planet_nature_and_rising_sign[x_planet] = planet_jogakaraky_D9.list_good_planets_joga[val_x][1]

    absolut_nature_planet = list(map(lambda x, y, z1, z2: x + y + ((z1 + z2) / 2), planet_nature_and_rising_sign, bindy_nature_grahas,
                                     planet_jogakaraky_D1.relate_jogakaraka, planet_jogakaraky_D9.relate_jogakaraka))

    power_nature_all = calculate_kendras_trikonas.kendra_trikonas(absolut_nature_planet, graha_in_house,
                                                                  hozaeva_in_house)
    """
        подсчет аспектов планет на другие планеты
    """
    power_to_aspects = calculator_aspects_planet.get_strenght_aspect_on_planets(graha_in_degrees, power_nature_all)

    """
        подсчет силы планет по положению в знаках по первоэлементам земли, огня, воды, воздуха, эфира
    """
    power_elements_planet = calculate_strenght_first_elements.strenght_first_elements(graha_in_znak)

    """
        получение силы от аспектов для хозяинов бхав
    """
    balls_for_keeper_grahas = calculate_kepper.calculate_balls_kepper_house(hozaeva_in_house, power_to_aspects)

    """
        сгорание планет
    """
    array_FireSunPlanets = calculateFirePlanet.calculate_fire_planet_func(graha_in_degrees)

    """
        количество лучей грахи в знаках зодиака
    """
    array_power_planets_in_znaks = calculatePowerPlanetInZnaks.calculate_power_planet_in_znaks_func(graha_in_znak,
                                                                                                    array_FireSunPlanets,
                                                                                                    bala_shodasha,
                                                                                                    graha_in_degrees)
    """
         отношения грах между собой
    """
    power_planet_rashi = calculate_relations_file.calculate_relationS_grah(graha_in_znak)

    """
        получение силы для бхав от занимаемой ими планеты
    """
    add_power_house = [0] * ZNAKS_IN_ZODIAK

    def add_power_h(position):
        add_power_house[int(graha_in_house[position])] += POSITION_GRAHA[position]

    list(map(lambda x: add_power_h(x), PLANETS_RANGE))

    """
        подведение всех расчетов в одну формулу, подчет силы грах для даш
    """

    static_nature_planets = []

    max_number = -SECONDS_IN_ZNAK
    min_number = SECONDS_IN_ZNAK

    folmula_of_power_planet = np.sum(list(map(lambda a, b, c, d, f, g, h, i, j, k, l: (a + b) / 40 + (
            c + POWER_GRAH_IN_HOUSE[d] + add_power_house[d] + (f + g * 60) + h + i + j * 60) * k * l / 60,
                                              bala_shodasha, bala_sapta, nature_planet_strenght,
                                              graha_in_house, bala_even_odd, balls_for_keeper_grahas,
                                              power_elements_planet, array_power_planets_in_znaks, power_to_aspects,
                                              power_nature_all, array_FireSunPlanets)))

    def formula_pl(i):
        nonlocal max_number
        nonlocal min_number

        static_nature_planets.append(folmula_of_power_planet + abs(folmula_of_power_planet * power_planet_rashi[i]))

        if max_number < static_nature_planets[i]:
            max_number = static_nature_planets[i]

        if min_number > static_nature_planets[i]:
            min_number = static_nature_planets[i]

    list(map(lambda x: formula_pl(x), PLANETS_RANGE))

    ratio_of_good_planet = list(
        map(lambda x: (x - min_number) / (max_number - min_number) * 100, static_nature_planets))


    return ratio_of_good_planet