import numpy

import calculateBindy
import calculateCoordsPlanet
import calculateRashi
import calculateVimshopakaBala
import calculate_break
import calculate_break_parts_of_body
import calculate_compound_file
import calculate_jogakaraky
import calculate_kendras_trikonas
import calculate_relations_file
import calculate_strenght_first_elements
import calculator_aspects_planet
from constants import MOON_PLANET_NUMBER, PLANETS_RANGE, RATIO_TR, VARGA_SHODASHA, WHO_UPRAVLAET_ZNAKOM, \
    BINDY_VARGA_CHARITY, ALL_VARGAS_PARTS


def calc_bala_transit(next_tranzit_str, next_tranzit_time_str, PLANETS=PLANETS_RANGE):

    trazit_data = calculateCoordsPlanet.calculate_coords_planet(next_tranzit_str, next_tranzit_time_str)

    transit_graha_in_degrees = trazit_data.graha_in_degrees
    tranzit_strenght_speed = trazit_data.sp_strenght_planet

    tranzit_retrograd = trazit_data.retrogr_planet


    tranzit_rashi = calculateRashi.calculate_rashi_card(transit_graha_in_degrees, 0)
    absolut_dergrees_planets = tranzit_rashi.absolut_dergrees_planets
    tranzit_in_degrees = tranzit_rashi.graha_in_degrees
    tranzit_in_znak = tranzit_rashi.graha_in_znak

    tranzit_absolut_degree = tranzit_rashi.absolut_dergrees_planets

    bindy_lagna = tranzit_in_znak[0:7]
    bindy_lagna.append(tranzit_in_znak[MOON_PLANET_NUMBER])
    array_bindy = calculateBindy.calculate_bindy_vargas(bindy_lagna, [0])

    tranzit_elements_planet = calculate_strenght_first_elements.strenght_first_elements(tranzit_in_znak)

    """
        расположение планет в бинду
    """
    power_break_ganda = calculate_break.get_power_calculate_degress(tranzit_in_degrees, array_bindy,
                                                                    tranzit_in_znak,
                                                                    tranzit_retrograd)
    """
        отношения грах между собой
    """
    power_planet_transit = calculate_relations_file.calculate_relationS_grah(tranzit_in_znak)

    """
        соединения грах
    """
    compound_grahas = calculate_compound_file.calculate_compound_grahas(tranzit_in_degrees)

    """
        количество лучей грахи в знаках зодиака
    """
    bala_shodasha = calculateVimshopakaBala.get_calculate_bala_of_planets(tranzit_absolut_degree, tranzit_in_znak,
                                                                          VARGA_SHODASHA, tranzit_in_znak[MOON_PLANET_NUMBER], -1)
    """
        подсчет природы планет (благотворность и пагубность)
    """
    planet_nature_and_rising_sign = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    bindy_nature_grahas = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, tranzit_in_znak,
                                                                                BINDY_VARGA_CHARITY, 0, -1)
    """
        определение планет йога-караки (благоприятной планеты)
    """

    map_vargas = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, tranzit_in_znak,
                                                                       ALL_VARGAS_PARTS, 0, tranzit_in_znak[MOON_PLANET_NUMBER])

    planet_jogakaraky_D1 = calculate_jogakaraky.get_calculate_jogakaraky(tranzit_in_znak, 0, tranzit_retrograd, planet_nature_and_rising_sign)
    planet_jogakaraky_D9 = calculate_jogakaraky.get_calculate_jogakaraky(map_vargas[8], map_vargas[8][9], tranzit_retrograd, planet_nature_and_rising_sign)

    """
        переиначим природу планет
    """
    if len(planet_jogakaraky_D1.list_good_planets_joga) > 0:
        for x_planet in PLANETS_RANGE:
            for val_x in numpy.arange(len(planet_jogakaraky_D1.list_good_planets_joga)):
                if planet_jogakaraky_D1.list_good_planets_joga[val_x][0] == x_planet: planet_nature_and_rising_sign[x_planet] = planet_jogakaraky_D1.list_good_planets_joga[val_x][1]
    if len(planet_jogakaraky_D9.list_good_planets_joga) > 0:
        for x_planet in PLANETS_RANGE:
            for val_x in numpy.arange(len(planet_jogakaraky_D9.list_good_planets_joga)):
                if planet_jogakaraky_D9.list_good_planets_joga[val_x][0] == x_planet: planet_nature_and_rising_sign[x_planet] = planet_jogakaraky_D9.list_good_planets_joga[val_x][1]

    absolut_nature_planet = list(map(lambda x, y, z1, z2: x + y + ((z1 + z2) / 2), planet_nature_and_rising_sign, bindy_nature_grahas,
                                     planet_jogakaraky_D1.relate_jogakaraka, planet_jogakaraky_D9.relate_jogakaraka))



    power_nature_all = calculate_kendras_trikonas.kendra_trikonas(absolut_nature_planet, tranzit_in_znak,
                                                                  WHO_UPRAVLAET_ZNAKOM)
    """
        подсчет аспектов планет на другие планеты
    """
    power_to_aspects = calculator_aspects_planet.get_strenght_aspect_on_planets(tranzit_in_degrees, power_nature_all)

    """
        вычисление точной дрекканы
    """
    whole_drekkana = calculateVimshopakaBala.get_whole_drekkana(absolut_dergrees_planets, tranzit_in_znak)

    get_break_parts = calculate_break_parts_of_body.get_break_parts_of_body(whole_drekkana, tranzit_in_znak,
                                                                            power_nature_all, power_to_aspects)
    break_parts_of_body_balls = get_break_parts.ratio_parts_of_body_drakkana

    """
        формула подсчета выводящей силы планет
    """
    # tranzit_elements_planet[x] + \
    # break_parts_of_body_balls[x]) *RATIO_TR[x] + \
    # power_break_ganda[x] \
    # + tranzit_strenght_speed[x]
    # trazit_data.sp_strenght_planet[x] * power_planet_transit[x] + \
    summ_ganda = sum(list(map(lambda x:
                                    bala_shodasha[x],
                                    PLANETS)))/63

    return summ_ganda