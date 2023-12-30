import math
import time
import calendar

import calculateTranzitMap
import calculate_exult_planets, calculate_main_avasths
import calculateBindy
from dictsData import dictOfDahasChakra, dictOfKalaChakraDashas, dictOfGraphicsCompany
import calculateRashi
import calculate_kendras_trikonas
import calculate_kepper
import calculate_relations_file
import calculateFirePlanet
import calculate_maps_planet
import calculateCoordsPlanet
import calculatePowerPlanetInZnaks
import calculate_strenght_first_elements
import calculateVimshopakaBala
import calculator_aspects_planet
import calculate_analis_sudarshana
import calculate_jogakaraky
import mathCalculateLagna
import calculate_joga_transit

import calculate_break_parts_of_body
import calculate_sunrise_time
import calculate_D_combination
import bhava_aspects_calculate
import calculate_main_avasths

from datetime import timedelta
from datetime import datetime

import calc_relations_data
from calculate_Sa_Ju_levelup import calc_level_up_Sa_Ju
from calculate_bala_transit import calc_bala_transit
from calculate_bindy_scores import get_bindy_scores
from calculate_krizis import calc_krizis
from constants import *
from dictsData.dictOfBaseAstrology import *
from toolkits.calculate_break_moments import get_break_recomendation, get_break_data_analis
from toolkits.calculate_parameters import calc_param_date, get_score_date
from toolkits.math_distance import dist_in_degrees, sum_in_degrees

RATIO_DASHA = [1.60, 1.0, .40, .08]
RATIO_KALA_DASHA = [0.160, 0.100, 0.040, 0.008]
RATIO_CHACRA = [.09, .05, 0.009]

POSITION_GRAHA = [-60, 0, -60, 60, 60, 0, -60, 0, 0]
NAYASARGIKA_BALA = [60 * 1.000, 60 * 0.857, 60 * 0.286, 60 * 0.429, 60 * 0.571, 60 * 0.714, 60 * 0.143, 60 * 1.000,
                    60 * 0.750]
ALG_COEF = 10000
DEGREESES_IN_ZNAK = 30
POWER_GRAH_IN_HOUSE = [60, 30, 15, 60, 30, 15, 60, 30, 15, 60, 30, 15]
ZERO_TIME = "00:00:00"
PERIODS_DASHA = [2520, 7200, 2160, 3600, 2520, 6480, 5760, 6840, 6120]
PERIODS_LONG = [0, 2520, 9720, 11880, 15480, 18000, 24480, 30240, 37080]

# данные о планетных периодов даши и сударшины чакры
dasha_dict = dictOfDahasChakra.get_dasha_data()
# кто управляет
time_dasha = dictOfDahasChakra.get_dasha_uprav(dasha_dict)

# данные о раши периодов даш
kala_dasha_dict = dictOfKalaChakraDashas.get_kala_dasha_data()
# кто управляет
kala_time_dasha = dictOfKalaChakraDashas.get_kala_dasha_rashi(kala_dasha_dict)

# данные о динамике SNP500
cost_companies_data = dictOfGraphicsCompany.get_companies_data()

class ChooiseValue_analis():
    def __init__(self, time_in_zachatie):
        self.time_in_zachatie = time_in_zachatie


class ChooiseValue():
    def __init__(self, OX_coords, OY_coords, OY_krizis, data_snp500,
                        general_OXresult, general_OZresult,
                        general_maha_dasha, general_antar_dasha, general_pratia_dasha,
                        ratio_of_good_planet, ratio_of_good_bhavas, bhava_aspects_rashi,
                        whole_drekkana, break_parts_of_body_balls, planets_parts_of_body, polojenie_lagna_rashi,
                        general_maha_kala_dasha, ratio_matrix_vargas, map_vargas,
                        value_joga, D_combination, speed_planet_tranzit_days,
                        num_exalt_planets_days, planets_in_avasths, light_transit_tr,
                 time_in_zachatie, days_in_utroba, moon_in_nakshatra, retrogr_planet, trazit_retrograd, planets_in_border,
                 planets_in_look_grahas, planets_in_look_aspects, planets_in_znak, coef_relations,
                 ashtaka_varga, sarva_ashtaka, planets_obmen, vina_yoga, musala_yoga, samudra_yoga, chakra_yoga,baby_sa_ju,
                 number_of_yogas, data_level_Sa_Ju, counts_oil_down, phase_moon, counts_snp500_down,
                 event_for_maha, event_for_antar, event_for_pratia, graha_in_degrees, planets_in_breakangle,
                 words_base_astrology, hard_community, scores, obmen_znakami, scores_rajya, planets_in_degrees_transit):

        self.OX_coords = OX_coords
        self.OY_coords = OY_coords
        self.OY_krizis = OY_krizis
        self.data_snp500 = data_snp500
        self.general_OXresult = general_OXresult
        self.general_OZresult = general_OZresult
        self.general_maha_dasha = general_maha_dasha
        self.general_antar_dasha = general_antar_dasha
        self.general_pratia_dasha = general_pratia_dasha
        self.ratio_of_good_planet = ratio_of_good_planet
        self.ratio_of_good_bhavas = ratio_of_good_bhavas
        self.bhava_aspects_rashi = bhava_aspects_rashi
        self.whole_drekkana = whole_drekkana
        self.break_parts_of_body_balls = break_parts_of_body_balls
        self.planets_parts_of_body = planets_parts_of_body
        self.polojenie_lagna_rashi = polojenie_lagna_rashi
        self.general_maha_kala_dasha = general_maha_kala_dasha
        self.ratio_matrix_vargas = ratio_matrix_vargas
        self.map_vargas = map_vargas
        self.value_joga = value_joga
        self.D_combination = D_combination
        self.speed_planet_tranzit_days = speed_planet_tranzit_days
        self.num_exalt_planets_days = num_exalt_planets_days
        self.planets_in_avasths = planets_in_avasths
        self.light_transit_tr = light_transit_tr
        self.time_in_zachatie = time_in_zachatie
        self.days_in_utroba = days_in_utroba
        self.moon_in_nakshatra = moon_in_nakshatra
        self.retrogr_planet = retrogr_planet
        self.trazit_retrograd = trazit_retrograd
        self.planets_in_border = planets_in_border
        self.planets_in_look_grahas = planets_in_look_grahas
        self.planets_in_look_aspects = planets_in_look_aspects
        self.planets_in_znak = planets_in_znak
        self.coef_relations = coef_relations
        self.ashtaka_varga = ashtaka_varga
        self.sarva_ashtaka = sarva_ashtaka
        self.planets_obmen = planets_obmen
        self.vina_yoga = vina_yoga
        self.musala_yoga = musala_yoga
        self.samudra_yoga = samudra_yoga
        self.chakra_yoga = chakra_yoga
        self.baby_sa_ju = baby_sa_ju
        self.number_of_yogas = number_of_yogas
        self.data_level_Sa_Ju = data_level_Sa_Ju
        self.counts_oil_down = counts_oil_down
        self.phase_moon = phase_moon
        self.counts_snp500_down = counts_snp500_down
        self.event_for_maha = event_for_maha
        self.event_for_antar = event_for_antar
        self.event_for_pratia = event_for_pratia
        self.graha_in_degrees = graha_in_degrees
        self.planets_in_breakangle = planets_in_breakangle
        self.words_base_astrology = words_base_astrology
        self.hard_community = hard_community
        self.scores = scores
        self.obmen_znakami = obmen_znakami
        self.scores_rajya = scores_rajya
        self.planets_in_degrees_transit = planets_in_degrees_transit


def prognoz_inTime(new_command, first_date, first_time, degree_hourUTCq, degree_northLatitudeq, degree_eastLongitudeq,
                   d3_startTimeStr, d3_finishTimeStr, graphic_name, days_calculate):

    if days_calculate == 'lahiri': delta = 0
    elif days_calculate == 'surya siddhanta': delta = SURIA_SIDDHANTA_AINAMSHA
    else: delta = 0

    t1 = time.time()

    degree_hour_utc = time.strptime(degree_hourUTCq, "%H")
    utc = degree_hour_utc.tm_hour


    time_d3_startTime = datetime.strptime(d3_startTimeStr, FORMAT_DATE)
    time_d3_finishTime = datetime.strptime(d3_finishTimeStr, FORMAT_DATE)
    time_first_date = datetime.strptime(first_date, FORMAT_DATE)
    name_graphics = graphic_name
    OX_coords = []
    OY_coords = [0, 100]
    OY_krizis = []
    try_weekdays = []
    try_dates = []

    zero_time = datetime.strptime(ZERO_TIME, FORMAT_TIME)
    burn_time = datetime.strptime(first_time, FORMAT_TIME)

    time_burn_date = datetime.strptime(first_date + '-' + first_time, FORMAT_DATE + '-' + FORMAT_TIME)

    jamna_day = time_first_date
    start_period = time_d3_startTime
    finish_period = time_d3_finishTime

    simple_period_days = int((finish_period - start_period).days)
    power_planets_massiveOxOy, general_OXresult, general_OXresult_tr, general_OYresult = [], [], [], [0, 100]

    houses_nature_default = [0] * 12
    general_maha_dasha, general_antar_dasha, general_pratia_dasha, general_sukshma_dasha, general_table_year, general_table_month, general_table_day = [], [], [], [], [], [], []
    general_maha_kala_dasha, general_antar_kala_dasha, general_pratia_kala_dasha, general_sukshma_kala_dasha = [], [], [], []
    value_joga = []
    value_joga_kala = []
    value_joga_chacra = []
    """
        вычисление координат планет на установленное время рождения
    """

    rashi_data = calculateCoordsPlanet.calculate_coords_planet(first_date, first_time, utc=utc, delta=delta)

    graha_in_degrees = rashi_data.graha_in_degrees

    retrogr_planet = rashi_data.retrogr_planet

    """
        вычисление лагны
    """
    degree_north_latitude = degree_northLatitudeq.split('.')
    ltd_degr = int(degree_north_latitude[0]) + (
            int(degree_north_latitude[1]) * MINUTS_IN_HOUR + int(degree_north_latitude[2])) / SECONDS_IN_HOUR

    degree_east_longitude = degree_eastLongitudeq.split('.')
    lng_degr = int(degree_east_longitude[0]) + (
            int(degree_east_longitude[1]) * MINUTS_IN_HOUR + int(degree_east_longitude[2])) / SECONDS_IN_HOUR

    degree_hour_utc = time.strptime(degree_hourUTCq, "%H")
    utc = degree_hour_utc.tm_hour

    b_year = int(time_first_date.year)
    b_month = int(time_first_date.month)
    b_day = int(time_first_date.day)

    # b_time измеряется в сидерических секундах
    b_time = int(burn_time.hour * SECONDS_IN_HOUR + burn_time.minute * MINUTS_IN_HOUR + burn_time.second)

    sun_rise, sun_set = calculate_sunrise_time.get_calculate_sunrise(ltd_degr, lng_degr, b_day, b_month, b_year, utc)
    # sun_rise, sun_set = int(sun_rise), int(sun_set)

    sunrise_hour = sun_rise / SECONDS_IN_HOUR
    sunrise_minute = (sunrise_hour - math.trunc(sunrise_hour)) * MINUTS_IN_HOUR
    sunrise_second = (sunrise_minute - math.trunc(sunrise_minute)) * MINUTS_IN_HOUR
    sun_rise_seconds = int(sunrise_hour * 3600 + sunrise_minute * 60 + sunrise_second)

    sunrise_in_degrees = graha_in_degrees[SUN_PLANET_NUMBER]
    lagna_in_seconds = mathCalculateLagna.asc_calculate(sunrise_in_degrees, sun_rise_seconds, b_time, ltd_degr)
    lagna_in_seconds_znak = math.fmod(lagna_in_seconds, 108000)
    lagna_in_znak = int(lagna_in_seconds / 108000)

    print('lagna_in:', int(lagna_in_seconds_znak/3600), '-', int(np.fmod(lagna_in_seconds_znak, 3600) / 60),
          '-', int(np.fmod(np.fmod(lagna_in_seconds_znak, 3600), 60)))

    """
        построение карты раши D1
    """
    map_rashi = calculateRashi.calculate_rashi_card(graha_in_degrees, lagna_in_znak)

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
    graha_in_znak_parts = map_rashi.graha_in_znak_parts
    """
        вычисление аспектов планет
    """
    bhava_aspects_rashi = bhava_aspects_calculate.bhava_aspec(graha_in_degrees, lagna_in_znak, retrogr_planet)

    """
        градусы относительно лагны
    """
    moon_in_degrees = graha_in_degrees[MOON_PLANET_NUMBER]
    moon_in_nakshatra = moon_in_degrees / 48000  # по накшатре находим группу чакра-даши
    moon_in_pada = (moon_in_nakshatra - int(moon_in_nakshatra)) * 4  # по накшатре находим четверть
    # maha_kala_dasha = moon_in_pada / 4  # по пройденному расстоянию находим положение чакра-даши при рождении

    naksh_gr = NAKSHATRA_GR[int(moon_in_nakshatra)]
    days_in_fullperiod = DAYS_IN_GROUP[naksh_gr * 4 + int(moon_in_pada)]

    # code_dict_kala_dasha = str(naksh_gr) + str(int(moon_in_pada))  # находим кодировку для обращения в словарь
    # start_kala_dasha = maha_kala_dasha * days_in_fullperiod  # точка отсчета в днях

    graha_in_house_degrees = list(
        map(lambda x, y: x * 30 + (y / SECONDS_IN_HOUR), graha_in_house, absolut_dergrees_planets))

    """
        подсчет силовых характеристик планет
    """

    map_vargas = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, graha_in_znak,
                                                                       ALL_VARGAS_PARTS, lagna_in_seconds_znak, lagna_in_znak)
    """
        Просчет комбинаций планет по варгам для сравнения их с дашами
    """
    D_combination = calculate_D_combination.calculate_new_D_combination(graha_in_znak_parts, map_vargas, retrogr_planet)

    # print('D_combination', D_combination)

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
    planet_nature_and_rising_sign = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    bindy_nature_grahas = calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_planets, graha_in_znak,
                                                                                BINDY_VARGA_CHARITY, lagna_in_seconds_znak, -1)

    """
        определение планет йога-караки (благоприятной планеты)
    """
    planet_jogakaraky_D1 = calculate_jogakaraky.get_calculate_jogakaraky(graha_in_znak, lagna_in_znak, retrogr_planet, planet_nature_and_rising_sign)
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
        вычисление точной дрекканы
    """
    whole_drekkana = calculateVimshopakaBala.get_whole_drekkana(absolut_dergrees_planets, graha_in_znak)

    """
        вычисление пагубности положения планет в дрекканах и знаках
    """
    get_break_parts = calculate_break_parts_of_body.get_break_parts_of_body(whole_drekkana, graha_in_znak,
                                                                            power_nature_all, power_to_aspects)
    break_parts_of_body_balls = get_break_parts.ratio_parts_of_body_drakkana
    planets_parts_of_body = get_break_parts.planets_of_znakbody

    """
        подсчет силы планет по положению в знаках по первоэлементам земли, огня, воды, воздуха, эфира
    """
    power_elements_planet = calculate_strenght_first_elements.strenght_first_elements(graha_in_znak)

    """
        получение силы от аспектов для хозяинов бхав
    """
    balls_for_keeper_grahas = calculate_kepper.calculate_balls_kepper_house(hozaeva_in_house, power_to_aspects)

    """
        подсчет аспектов планет на бхавы
    """
    bhava_to_aspects = calculator_aspects_planet.get_strenght_aspect_on_bhavas(graha_in_degrees, power_nature_all)

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
        построение сударшана чакры (оценка силы домов)
    """
    bindy_lagna = graha_in_house
    bindy_lagna.append(0)
    array_bindy_data = calculateBindy.calculate_bindy_vargas(bindy_lagna, [0, 0])
    array_bindy = array_bindy_data.planet_varga_sum

    vargas_bindy = calculateBindy.calculate_bindy_vargas(bindy_lagna, graha_in_znak)
    max_bindy = vargas_bindy.max_bindy
    min_bindy = vargas_bindy.min_bindy

    """
        Построение точного бинду
    """
    get_bindy = get_bindy_scores(graha_in_znak, lagna_in_seconds_znak)
    ashtaka_varga = get_bindy.filtr_scores_varga
    sarva_ashtaka = get_bindy.bindy_scores_sarva


    """
        Подсчет процентного расположения планет в пределах знака
    """
    part_in_znaks = np.abs((np.modf(np.array(graha_in_znak_parts))[0]*100)[0:9]).tolist()

    """
        Получение кодировки расположения планет
    """
    planets_code, planets_ratios = create_planets_code(planets_in_seconds=graha_in_degrees,
                                                       planets_retrograd=retrogr_planet,
                                                       planets_in_houses=graha_in_house,
                                                       planets_in_d9_sec=map_vargas[8][0:9])
    words_base_astrology = decode_planets_code(dict_of_codes=planets_code, dict_of_ratios=planets_ratios)

    """
        построение чандра-раши
    """
    map_chandra = calculate_maps_planet.get_new_map_from_planets(graha_in_degrees, MOON_PLANET_NUMBER)

    graha_in_chandra_degrees = map_chandra.graha_in_degrees
    graha_in_chandra_house = map_chandra.graha_in_house

    # построение сурья-раши
    map_syria = calculate_maps_planet.get_new_map_from_planets(graha_in_degrees, SUN_PLANET_NUMBER)

    graha_in_syria_degrees = map_syria.graha_in_degrees
    graha_in_syria_house = map_syria.graha_in_house

    """
        вложение планет в массив для построения сударшаны чаркы на панели
    """
    massiv_sudarshana = []

    x_rashi = graha_in_house_degrees
    x_chand = list(map(lambda x: x / SECONDS_IN_HOUR, graha_in_chandra_degrees))
    x_syria = list(map(lambda x: x / SECONDS_IN_HOUR, graha_in_syria_degrees))

    massiv_sudarshana.extend((x_rashi + x_chand + x_syria))

    # Определим положение планет в домах трех гороскопов относительно лагны, оценим силу планет
    sudarshana_chakra_rasha, sudarshana_chakra_chandra, sudarshana_chakra_syria = [0] * 12, [0] * 12, [0] * 12

    def calc_sudars(pozition):
        multiply_power_and_nature_planet = array_power_planets_in_znaks[pozition]
        sudarshana_chakra_rasha[graha_in_house[pozition]] += multiply_power_and_nature_planet
        sudarshana_chakra_chandra[graha_in_chandra_house[pozition]] += multiply_power_and_nature_planet
        sudarshana_chakra_syria[graha_in_syria_house[pozition]] += multiply_power_and_nature_planet

    list(map(lambda x: calc_sudars(x), PLANETS_RANGE))
    """
        анализ благотворных факторов положения планет в сударшана чакре
    """
    ratio_of_ch_bhavas = calculate_analis_sudarshana.get_analis_sudarshana(massiv_sudarshana, power_nature_all)

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

    """
        выделение благотворности бхав
    """
    max_number = -SECONDS_IN_ZNAK
    min_number = SECONDS_IN_ZNAK

    # оценка силы каждого знака по системе БАКФИК
    ratio_of_good_bhavas = calc_relations_data.bacfic(graha_in_znak, lagna_in_znak)

    planets_in_nakshatras = np.asarray(np.asarray(graha_in_degrees) / SECONDS_IN_NAKSHATRA, dtype='int8')
    planets_in_navamsha = np.asarray(
        np.fmod(np.asarray(graha_in_degrees), SECONDS_IN_ZNAK) / SECONDS_IN_NAVAMSHA, dtype='int8')

    """
        вычисление авастхи для каждой планеты (в момент рождения)
        planets_in_nakshatras                       - номер накшатры, в которой планета расположена
        PLANETS_RANGE                               - номер планеты, авастху которой мы вычисляем
        planets_in_navamsha                         - номер навамши планеты, в которой она расположена
        planets_in_nakshatras[MOON_PLANET_NUMBER]   - номер джамна накшатры
        b_time - sun_rise                           - разница в часах между восходом солнца и временем рождения
        polojenie_lagna_rashi                       - расположение лагны в знаке
    """
    planets_in_avasths = calculate_main_avasths.calculate_avasths(planets_in_nakshatras[0:9], PLANETS_RANGE,
                                                                  planets_in_navamsha[0:9],
                                                                  planets_in_nakshatras[MOON_PLANET_NUMBER],
                                                                  (b_time - sun_rise)/3600, lagna_in_znak)
    """
        вычисление положения манди gulika_lagna_in_seconds
        b_time                                      - Время рождения натива
        n_weekday                                   - день недели (0 пн, 1 вт, 2 ср,)
        sun_rise                                    - восход Солнца в секундах времени
        sun_set                                     - закат Солнца в секундах времени
        продолжительность дня                       - (sun_set - sun_rise) в секундах времени
        продолжительность ночи                      - (86400 секунд - продолжительность дня)
    """

    # Используем данные на основе времени рождения до восхода или после восхода Солнца
    n_weekday = calendar.weekday(time_first_date.year, time_first_date.month, time_first_date.day)
    if (b_time >= sun_rise) and (b_time < sun_set):
        gulica_druvanka = GULIKA_DRUVANKA_CONST_DAY[n_weekday]
    else:
        gulica_druvanka = GULIKA_DRUVANKA_CONST_NIGHT[n_weekday]

    """
        Вычисление сколько времени натив пробыл в утробе time_in_utroba и времени зачатия time_in_zachatie
        spashta_rashi                               - Спашты раши (в угловых секундах)
        graha_in_degrees                            - Расположение планет (в угловых секундах)
        lagna_in_seconds                            - Расположение Лагны (в угловых секундах)
        gulika_lagna_in_seconds                     - Расположение Гулики лагны (в угловых секундах)
        
        time_in_utroba                              - Время проведенное в утробе матери (в секундах дня)
        chandra_in_spashta                          - Сколько Луна прошла градусов в спаште, в которой находится
    """

    # spashta_rashi = calculate_spashta_rashi.calc_spashta(ltd_degr)

    BHAVA9 = 108000 * np.fmod(lagna_in_znak+9,12)

    if (BHAVA9 - lagna_in_seconds) >= 0:
        time_in_utroba = BHAVA9 - lagna_in_seconds
    else:
        time_in_utroba = SECONDS_IN_ZODIAC - lagna_in_seconds + BHAVA9

    # Если правитель лагны в более чем 180 градусов от лагны, то дополнительно добавляем поправку
    upravit_lagny = graha_in_degrees[WHO_UPRAVLAET_ZNAKOM[lagna_in_znak]]
    if (upravit_lagny - lagna_in_seconds) >= 0:
        delta_Ul_Lg = upravit_lagny - lagna_in_seconds
    else:
        delta_Ul_Lg = SECONDS_IN_ZODIAC - lagna_in_seconds + upravit_lagny

    if delta_Ul_Lg > SECONDS_IN_HALF_ZODIAC:
        moon_path = 108000 - np.fmod(graha_in_degrees[MOON_PLANET_NUMBER], 108000)
    else:
        moon_path = 108000

    time_in_utroba += moon_path + gulica_druvanka * 3600
    # Перевод угловых секунд в сидерические минуты
    time_in_utroba /= 2.5
    # Перевод сидерических минут в сидерические дни
    days_in_utroba = int(time_in_utroba / 1440)
    if time_burn_date.year > 1000:
        time_in_zachatie = time_burn_date - timedelta(minutes=int(time_in_utroba))
    else:
        time_in_zachatie = 0

    """
        построение даш и прочих дробных планетных периодов
    """
    # past_period_days = (start_period - jamna_day).days

    if name_graphics == NAME_GRAPHICS[HOROSCOP]:
        step_days = int(simple_period_days / 600) + 1
    else:
        step_days = int(simple_period_days / 600) + 1

    general_OZresult = []

    jam_nakshatra = math.fmod(graha_in_degrees[MOON_PLANET_NUMBER] / SECONDS_IN_NAKSHATRA, 9)
    jam_dasha = math.trunc(jam_nakshatra)
    start_day_pozit_dasha = math.trunc(math.fmod(jam_nakshatra, 1) * PERIODS_DASHA[jam_dasha] + PERIODS_LONG[jam_dasha])

    """
        построение опорных точек для анализа
    """
    # timer_dasha = 0

    if new_command == "ANALIS":

        return ChooiseValue_analis(time_in_zachatie)

    # """
    #     Анализ нотальной карты и навамши на предмет наличия раджа-йоги и других йог
    # """
    # yoga_analis = calculate_joga_transit.get_calculate_yoga_horoscop(graha_in_house, retrogr_planet, lagna_in_znak)

    """
        построение транзитов планет
    """
    num_points = 0

    detals = 1
    HOUR_DUNAMYC = [420]

    ratio_matrix_vargas = []
    joga_tranzit = []
    speed_planet_tranzit = []
    num_exalt_planets = []
    light_transit = []
    trazit_retrograd = []
    planets_in_border = []

    speed_planet_tranzit_days = []
    light_transit_tr = []
    planets_in_look_grahas = []
    planets_in_look_aspects = []
    planets_in_znak = []
    coef_relations = []
    planets_obmen = []
    vina_yoga = []
    samudra_yoga = []
    chakra_yoga = []
    musala_yoga = []

    phase_moon = []
    kshetra_sphuta = []
    karakas = []

    counts_oil_down = []
    counts_snp500_down = []

    baby_sa_ju = []
    number_of_yogas = []
    planets_in_degrees_transit = []
    planets_in_retrograd_transit = []
    data_snp500 = []
    hard_community = []

    scores = []
    scores_rajya = []

    print(time.time() - t1)
    t1 = time.time()

    planets_in_breakangle = {'Su':[], 'Mo':[], 'Ma':[], 'Me':[], 'Ju':[], 'Ve':[], 'Sa':[], 'Ra':[], 'Ke':[]}
    obmen_znakami = {'Su': [], 'Mo': [], 'Ma': [], 'Me': [], 'Ju': [], 'Ve': [], 'Sa': [], 'Ra': [], 'Ke': []}

    if graphic_name != NAME_GRAPHICS[NO_GRAPHICS]:
        for day_tranzit in np.arange(0, simple_period_days + 1, step_days):
            next_tranzit = start_period + timedelta(days=int(day_tranzit) + 1)
            for i in np.arange(detals):


                num_points += 1
                hourses = 600 + HOUR_DUNAMYC[i]
                next_tranzit_time = zero_time + timedelta(minutes=int(hourses))

                next_tranzit_str = next_tranzit.strftime(FORMAT_DATE)
                next_tranzit_time_str = next_tranzit_time.strftime(FORMAT_TIME)

                trazit_data = calculateCoordsPlanet.calculate_coords_planet(next_tranzit_str, next_tranzit_time_str, delta=delta)

                transit_graha_in_degrees = trazit_data.graha_in_degrees

                speed_planet_tranzit.append(trazit_data.speed_planet)

                tranzit_retrograd = trazit_data.retrogr_planet

                tranzit_rashi = calculateRashi.calculate_rashi_card(transit_graha_in_degrees,
                                                                    graha_in_znak[MOON_PLANET_NUMBER])

                tranzit_in_znak = tranzit_rashi.graha_in_znak
                tranzit_in_bhava = tranzit_rashi.graha_in_house

                # Расчет фазы луны для отображения с другими планетами
                phase_ = []
                # for plane in PHASE_PLANETS:
                #     planet_an = MOON_PLANET_NUMBER
                #     dist_M = dist_in_degrees(M=transit_graha_in_degrees[plane],
                #                                 S=transit_graha_in_degrees[planet_an], absp=False)
                #
                #     if planet_an == MOON_PLANET_NUMBER:
                #         if dist_M < 324000: phase_.append(1)
                #         elif dist_M < 648000: phase_.append(2)
                #         elif dist_M < 972000: phase_.append(3)
                #         elif dist_M < 1296000: phase_.append(4)
                #
                #     elif planet_an in [MERCURY_PLANET_NUMBER, VENUS_PLANET_NUMBER]:
                #         if dist_M < 30000 and tranzit_retrograd[planet_an] != 1: phase_.append(1)
                #         elif dist_M < 30000 and tranzit_retrograd[planet_an] != 0: phase_.append(3)
                        # elif dist_M < 972000: phase_.append(3)
                        # elif dist_M < 1296000: phase_.append(4)


                phase_moon.append(phase_)

                # Расчет кшетра-спхут тяжелых планет
                kshetra_sphuta_coords = []
                # for sp1, sp2 in zip(SPHUTA_DATA['P1'], SPHUTA_DATA['P2']):
                #     kshetra_sphuta_coords.append(sum_in_degrees(M=transit_graha_in_degrees[sp1], S=transit_graha_in_degrees[sp2]))
                kshetra_sphuta.append(kshetra_sphuta_coords)

                """
                    Подсчет индикатора для поражения юпитера, сатурна или их кшетра-спхуты
                """
                # kshetra_sphuta_0 = kshetra_sphuta_coords[-1]

                #
                # """
                #     Подсчет показаний караки
                # """
                # karakas.append(calculate_karakas.get_karakas(planets_in_degrees=transit_graha_in_degrees))

                planets_in_degrees_transit.append(transit_graha_in_degrees)
                planets_in_retrograd_transit.append(tranzit_retrograd)
                # Данные о кризисах и планеты участвующие в нем

                speed_planet = trazit_data.speed_planet
                # trends = trazit_data.trends
                data_krizis_pack = calc_krizis(transit_graha_in_degrees, speed_planet, graha_in_degrees)
                data_krizis = data_krizis_pack.my_return

                trazit_retrograd.append(data_krizis_pack.retrograd)
                planets_in_border.append(data_krizis_pack.planets_in_border)
                planets_in_look_aspects.append(data_krizis_pack.planets_in_look_aspects)
                planets_in_look_grahas.append(data_krizis_pack.planets_in_look_grahas)
                planets_in_znak.append(data_krizis_pack.planets_in_znak)


                if next_tranzit_str in cost_companies_data.keys():
                    data_snp500.append(float(cost_companies_data[next_tranzit_str].snp500))
                else:
                    if data_snp500[-5:-4] == data_snp500[-4:-3] and data_snp500[-5:-4] == data_snp500[-3:-2] and \
                            data_snp500[-5:-4] == data_snp500[-2:-1] and data_snp500[-5:-4] == data_snp500[-1:]:
                        data_snp500.append(-1)
                    elif len(data_snp500) > 0:
                        data_snp500.append(data_snp500[-1])
                    else:
                        data_snp500 = [-1]


                # planet_in_tranzit = calculateTranzitMap.calculate_tranzit_map(next_tranzit_str, first_date,
                #                                                               '01:00:00')
                # graha_in_degrees_transit = planet_in_tranzit.graha_in_degrees_transit
                # coef_relation = calc_relations_data.calc_data_relative(transit_graha_in_degrees, tranzit_retrograd, graha_in_degrees_transit,
                #                                    is_horoscop=name_graphics == NAME_GRAPHICS[HOROSCOP])


                # graha_in_degrees_aspects = planet_in_tranzit.graha_in_degrees_transit

                # coef_relations.append(coef_relation)

                # counts_oil_down.append(calculate_joga_transit.calculate_oil_down(graha_in_znak=tranzit_in_znak, tranzit_retrograd=tranzit_retrograd))
                #
                # counts_snp500_down.append(calculate_joga_transit.calculate_SNP500_down(graha_in_degrees=transit_graha_in_degrees, tranzit_retrograd=tranzit_retrograd,
                #                                                                        main_planets=[JUPITER_PLANET_NUMBER],
                #                                                                        break_planets=[RAHY_PLANET_NUMBER, MARS_PLANET_NUMBER, KETY_PLANET_NUMBER],
                #                                                                        sphuta=[kshetra_sphuta_0]))

                """
                    Выявление расположения в разрушительных градусах планет
                """
                # for plant, plant_angle in enumerate(np.asarray(np.array(transit_graha_in_degrees[0:9])/3600, dtype='int32')):
                #     planets_in_breakangle[NAME_PLANETS_DREK[plant]].append(plant_angle in dict_break_angles[NAME_PLANETS_DREK[plant]])


                if name_graphics == NAME_GRAPHICS[HOROSCOP]:
                    dynamic_strenght = calc_bala_transit(next_tranzit_str, next_tranzit_time_str, PLANETS=[4, 6])
                    # Набор планет для подсчета суммарной силы

                    """
                        Перебор всех лагн (12 гороскопов 1 дня с выявлением минимального числа раджа-йог)
                    """

                    # tranzit_in_znak планеты в знаках
                    # tranzit_in_bhavas планеты с учетом новой лагны
                    n_of_yogas_D1 = []
                    n_of_yogas_D9 = []


                    """
                        подсчет благоприятность положений планет
                    """
                    num_exalt_planets.append(calculate_exult_planets.calculate_goods_pozition(transit_graha_in_degrees, tranzit_retrograd))

                    """
                        Поиск обмена знаками obmen_znakami
                    """
                    # who_obmen = calculateTranzitMap.get_obmen_znakami(tranzit_in_znak=tranzit_in_znak)
                    #
                    # for pl in PLANETS_RANGE:
                    #     if pl in who_obmen: obmen_znakami[NAME_PLANETS_DREK[pl]].append(1)
                    #     else: obmen_znakami[NAME_PLANETS_DREK[pl]].append(0)

                    """
                        подчет потенциала раджа йоги
                    """
                    # scores_rajya.append(calculate_main_avasths.calculate_rajya_yoga(graha_in_degrees=transit_graha_in_degrees))

                    """
                        ПРАВИЛА ДЛЯ РОЖДЕНИЯ РАЗВИТИЯ ЗАЧАТИЯ РЕБЕНКА
                        Если Сатурн или Юпитер аспектируют 5 9 дом или из правителей
                    """
                    # baby_sa_ju.append(calculate_joga_transit.get_calculate_baby_generate(graha_in_house, lagna_in_znak,
                    #                                                  tranzit_retrograd, tranzit_in_znak))

                    # Пеесчет транзитных градусов на дробные градусы Д9 и расположение в знаках
                    # planet_angles_nava = np.fmod(np.array(transit_graha_in_degrees) / 12000, 12) * 30
                    # planet_in_znak_nava = np.asarray(planet_angles_nava / 30, dtype='int16')


                    # if len(planet_jogakaraky_D1.list_good_planets_joga) > 0:
                    #     for x_planet in PLANETS_RANGE:
                    #         for val_x in np.arange(len(planet_jogakaraky_D1.list_good_planets_joga)):
                    #             if planet_jogakaraky_D1.list_good_planets_joga[val_x][0] == x_planet: planet_nature_and_rising_sign[x_planet] = planet_jogakaraky_D1.list_good_planets_joga[val_x][1]
                    # if len(planet_jogakaraky_D9.list_good_planets_joga) > 0:
                    #     for x_planet in PLANETS_RANGE:
                    #         for val_x in np.arange(len(planet_jogakaraky_D9.list_good_planets_joga)):
                    #             if planet_jogakaraky_D9.list_good_planets_joga[val_x][0] == x_planet: planet_nature_and_rising_sign[x_planet] = planet_jogakaraky_D9.list_good_planets_joga[val_x][1]
                    #
                    # bindy_lagna = tranzit_in_znak[0:7]
                    # bindy_lagna.append(graha_in_znak[MOON_PLANET_NUMBER])

                    # """
                    #     проверка сработает ли йога в гороскопе в данное время
                    #      - соединение двух планет йоги в домах (благоприятность даст соединение в кендре или триконе)
                    #      - взаимный аспект планет йоги из домов триконы и кендры
                    #      - две планеты занимают друг друга дома
                    # """
                    # joga_tranzit.append(calculate_joga_transit.get_calculate_joga_transit(tranzit_in_znak, tranzit_in_bhava, tranzit_retrograd,
                    #                                                                       planet_jogakaraky_D1.list_joga, planet_jogakaraky_D9.list_joga))

                    """
                        вычисление базовых сил и количества лучей грахи в знаках зодиака для зачатия полезно
                    """
                    # planet_in_znak_fl = np.array(transit_graha_in_degrees) / 108000
                    # planet_in_znak = np.asarray(planet_in_znak_fl, dtype='int16')
                    # absolut_dergrees_transit = np.fmod(transit_graha_in_degrees, 108000)
                    #
                    # bala_shodasha_tr = np.mean(calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_transit,
                    #                                 planet_in_znak,VARGA_SHODASHA,lagna_in_seconds_znak, -1)[0:7])
                    # bala_sapta_tr = np.mean(calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_transit,
                    #                                 planet_in_znak,VARGA_SAPTA, lagna_in_seconds_znak, -1)[0:7])
                    # bala_shad_tr = np.mean(calculateVimshopakaBala.get_calculate_bala_of_planets(absolut_dergrees_transit,
                    #                                 planet_in_znak,VARGA_SHAD, lagna_in_seconds_znak, -1)[0:7])
                    #
                    # bala_fire_tr = np.mean(calculateFirePlanet.calculate_fire_planet_func(transit_graha_in_degrees)[0:7])
                    #
                    # sum_bala = bala_shodasha_tr+bala_sapta_tr+bala_shad_tr+bala_fire_tr
                    # light_transit.append(sum_bala)

                    light_transit.append(0)

                    # general_OYresult.append(dynamic_strenght)
                    general_OYresult.append(0)
                else:
                    """
                        Проверка на соединение тяжелых планет
                    """
                    # dict_connect_planets = {}
                    # for planet in planets_hard:
                    #     dict_connect_planets.update({NAME_PLANETS_DREK[planet]: 0})
                    #
                    # for planet1 in planets_hard:
                    #     for planet2 in planets_hard:
                    #         if planet1 >= planet2: continue
                    #
                    #         is_connect = dist_in_degrees(M=transit_graha_in_degrees[planet1],
                    #                                      S=transit_graha_in_degrees[planet2]) < 36000
                    #
                    #         if is_connect:
                    #             dict_connect_planets[NAME_PLANETS_DREK[planet1]] = 1
                    #             dict_connect_planets[NAME_PLANETS_DREK[planet2]] = 1
                    #
                    # hard_community.append(dict_connect_planets)

                    """
                        Вычисление баллов роста падения нефти
                    """

                    # scores.append(get_break_recomendation(
                    #     data_dict=get_break_data_analis(data_break_moments=[next_tranzit_str])))

                OY_krizis.append(data_krizis)

        """
            сборка всех данных в единую систему координат
        """
        past_period_days = (start_period - jamna_day).days
        mass_OX = 0
        value_tranzit = 0
        data_level_up_Sa_Ju, data_level_down_Sa_Ju, data_level_Sa_Ju = [], [], []
        speed_planet_tranzit_days = []
        # if name_graphics == NAME_GRAPHICS[HOROSCOP]:
        #     len_joga = len(joga_tranzit[0])
        light_transit_tr = []

        event_for_maha, event_for_antar, event_for_pratia = [], [], []

        print(time.time() - t1)
        t1 = time.time()

        for index in np.arange(0, simple_period_days, step_days):

            next_date = start_period + timedelta(days=int(index))
            today_date = next_date

            next_date = next_date.strftime(FORMAT_DATE)
            hora_data = str(next_date)[0:5]
            # вычисляем день недели на каждую дату
            time_weekday = calendar.weekday(today_date.year, today_date.month, today_date.day)
            # календарные даты, которые нужно исключить из расчетов

            # исключение дней недени и дат
            if time_weekday not in try_weekdays and hora_data not in try_dates:
                speed_planet_tranzit_days.append(speed_planet_tranzit[int(index / step_days)])
                if name_graphics == NAME_GRAPHICS[HOROSCOP]:
                    light_transit_tr.append(light_transit[int(index/step_days)])

                    # добавим результаты даш
                    dasha_day = int(math.fmod((start_day_pozit_dasha + past_period_days + index), 43200))
                    # kala_day = int(
                    #     str(code_dict_kala_dasha) + str(int(math.fmod((start_kala_dasha + past_period_days + index), days_in_fullperiod))))

                    maha_d = int(dasha_dict.get(dasha_day).maha_d)
                    antar_d = int(dasha_dict.get(dasha_day).antar_d)
                    pratia_d = int(dasha_dict.get(dasha_day).pratia_d)

                    maha_koef = part_in_znaks[maha_d] - float(dasha_dict.get(dasha_day).maha_per)
                    antar_koef = part_in_znaks[antar_d] - float(dasha_dict.get(dasha_day).antar_per)
                    pratia_koef = part_in_znaks[pratia_d] - float(dasha_dict.get(dasha_day).pratia_per)

                    if -7 < maha_koef < 7: event_for_maha.append((7 - abs(maha_koef))*.07)
                    else: event_for_maha.append(0)

                    if -7 < antar_koef < 7: event_for_antar.append((7 - abs(antar_koef))*.07)
                    else: event_for_antar.append(0)

                    if -7 < pratia_koef < 7: event_for_pratia.append((7 - abs(pratia_koef))*.07)
                    else: event_for_pratia.append(0)

                    data_level_up_Sa_Ju = []
                    level_up_Sa_Ju = [calc_level_up_Sa_Ju(mahadasha=maha_d, antardasha=antar_d, pratiadasha=pratia_d,
                                                         menegers_bhavas=hozaeva_in_house,
                                                         planets_in_degrees_horoscop=graha_in_degrees,
                                                         planets_in_retrogard_horoscop=retrogr_planet,
                                                         planets_in_degrees_transit=planets_in_degrees_transit[
                                                             int(index/step_days)],
                                                         planets_in_retrogard_transit=planets_in_retrograd_transit[
                                                             int(index/step_days)],
                                                         lagna_bhava=lagna_in_znak, bhavas=[1, 4, 6, 8, 9, 10]),
                                      calc_level_up_Sa_Ju(mahadasha=maha_d, antardasha=antar_d, pratiadasha=pratia_d,
                                                          menegers_bhavas=hozaeva_in_house,
                                                          planets_in_degrees_horoscop=graha_in_degrees,
                                                          planets_in_retrogard_horoscop=retrogr_planet,
                                                          planets_in_degrees_transit=planets_in_degrees_transit[
                                                              int(index / step_days)],
                                                          planets_in_retrogard_transit=planets_in_retrograd_transit[
                                                              int(index / step_days)],
                                                          lagna_bhava=lagna_in_znak, bhavas=[5, 7, 11])
                                      ]
                    data_level_Sa_Ju.append(level_up_Sa_Ju)

                    # maha_kala_d = int(kala_dasha_dict.get(kala_day).maha_d_kala)

                    # """
                    #     условие, когда йога в транзите будет работать в период подходящей даши
                    # """
                    #
                    # for name_joga in np.arange(len_joga):
                    #     if len(joga_tranzit[value_tranzit]) > 0:
                    #         if len(joga_tranzit[value_tranzit][name_joga]) > 0:
                    #             for len_name_joga in np.arange(len(joga_tranzit[value_tranzit][name_joga])):
                    #
                    #                 value_joga.append([])
                    #                 value_joga_kala.append([])
                    #                 value_joga_chacra.append([])
                    #
                    #                 for ind_joga in [0, 1]:
                    #                     if joga_tranzit[value_tranzit][name_joga][len_name_joga][ind_joga] != joga_tranzit[value_tranzit][name_joga][len_name_joga][ind_joga * (-1) + 1]:
                    #                         if (joga_tranzit[value_tranzit][name_joga][len_name_joga][ind_joga] in [maha_d, antar_d, pratia_d]) and (
                    #                                 joga_tranzit[value_tranzit][name_joga][len_name_joga][ind_joga * (-1) + 1] in [maha_d, antar_d, pratia_d]):
                    #                             value_joga[len(value_joga) - 1].append(name_joga)

                general_OXresult.append(mass_OX)
                #
                OZ_text = str(today_date.day) + "." + str(today_date.month) + "." + str(today_date.year)
                general_OZresult.append(time.strptime(OZ_text, FORMAT_DATE))

                if name_graphics == NAME_GRAPHICS[HOROSCOP]:

                    # запишем результат в OX, OY массив
                    general_maha_dasha.append(int(dasha_dict.get(dasha_day).maha_d))
                    general_antar_dasha.append(int(dasha_dict.get(dasha_day).antar_d))
                    general_pratia_dasha.append(int(dasha_dict.get(dasha_day).pratia_d))

                    # general_maha_kala_dasha.append(maha_kala_d)

                    # добавление подсчета лунного дня (титхи)

                    next_tranzit = start_period + timedelta(days=int(index) + 1)
                    next_tranzit_str = next_tranzit.strftime(FORMAT_DATE)
                    trazit_data = calculateCoordsPlanet.calculate_coords_planet(next_tranzit_str, "00:00:01", delta=delta)

                    transit_graha_in_degrees = trazit_data.graha_in_degrees

                    tranzit_rashi = calculateRashi.calculate_rashi_card(transit_graha_in_degrees,
                                                                        graha_in_znak[MOON_PLANET_NUMBER])

                    tranzit_in_znak = tranzit_rashi.graha_in_znak

                    list_matrix_vargas = [0] * 7
                    for pl in np.arange(NUMBER_OF_GRAHAS):
                        if (maha_d == pl) or (antar_d == pl) or (pratia_d == pl):

                            """
                                присвоение каждому дню класс опасности/безопасности для кадждой функции грахи

                                min_bindy - знаки в которых планеты слабы
                                max_bindy - знаки в которых планеты благоприятны максимально
                                nk_trik_negativ - накшатры в которых сатурн портит функцию грахи
                                zn_trik_negativ - знаки в которых сатурн портит функцию грахи

                                nakshatras_tr - транзит планеты через накшатры
                                tranzit_in_znak - транзит через знак
                            """

                            if tranzit_in_znak[pl] in min_bindy[pl]:
                                list_matrix_vargas[pl] = 20
                            elif tranzit_in_znak[pl] in max_bindy[pl]:
                                list_matrix_vargas[pl] = 80
                            else:
                                list_matrix_vargas[pl] = 50

                    ratio_matrix_vargas.append(list_matrix_vargas)

                """
                    суммарный вывод по бхавам и планетам
                """

                mass_OX += (1 / detals)
            value_tranzit += 1

        """
            уменьшение количества координат, сокращение одинаковых точек для графика
        """
        OX_coords = general_OXresult
        OY_coords = general_OYresult

        # if name_graphics == NAME_GRAPHICS[HOROSCOP]:
        #     len_oy_massiv = len(OY_coords)
        #     if len_oy_massiv > 90:
        #         nix = 1
        #         nix_end = 1 + nix * 2
        #         for q in range(2):
        #             for i in range(nix, len_oy_massiv - 1 - nix):
        #                 balls = 0
        #                 for innix in range(nix_end):
        #                     balls += OY_coords[i + innix - nix]
        #                 OY_coords[i] = balls / nix_end

    lagna_in_znak = [lagna_in_znak, graha_in_znak[1]]

    print(time.time() - t1)
    t1 = time.time()

    return ChooiseValue(OX_coords, OY_coords, OY_krizis, data_snp500,
                        general_OXresult, general_OZresult,
                        general_maha_dasha, general_antar_dasha, general_pratia_dasha,
                        ratio_of_good_planet, ratio_of_good_bhavas, bhava_aspects_rashi,
                        whole_drekkana, break_parts_of_body_balls, planets_parts_of_body, lagna_in_znak,
                        general_maha_kala_dasha, ratio_matrix_vargas, map_vargas,
                        value_joga, D_combination, speed_planet_tranzit_days,
                        num_exalt_planets, planets_in_avasths, light_transit_tr,
                        time_in_zachatie, days_in_utroba, moon_in_nakshatra, retrogr_planet, trazit_retrograd,
                        planets_in_border, planets_in_look_grahas, planets_in_look_aspects, planets_in_znak, coef_relations,
                        ashtaka_varga, sarva_ashtaka, planets_obmen, vina_yoga, musala_yoga, samudra_yoga, chakra_yoga, baby_sa_ju,
                        number_of_yogas, data_level_Sa_Ju, counts_oil_down, phase_moon, counts_snp500_down,
                        event_for_maha, event_for_antar, event_for_pratia, graha_in_degrees, planets_in_breakangle,
                        words_base_astrology, hard_community, scores, obmen_znakami, scores_rajya, planets_in_degrees_transit)
