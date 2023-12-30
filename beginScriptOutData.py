import math
import time

import calculate_compound_file
import calculateBindy
from dictsData import dictOfDahasChakra, dictOfKalaChakraDashas
import calculateRashi
import calculate_kendras_trikonas
import calculate_break
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
import calculate_code_of_day
import calculate_sunrise_time
import anlgeDistansPlanets
import beginScript_POW
import bhava_aspects_calculate


from datetime import timedelta
from datetime import datetime

from constants import *

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


class ChooiseValue():
    def __init__(self, outPowPlanet, dynamic_strenght_VRGTick, CalcDistansPlanetsTick, CalcDistansVargasTick):
        self.outPowPlanet = outPowPlanet
        self.dynamic_strenght_VRGTick = dynamic_strenght_VRGTick
        self.CalcDistansPlanetsTick = CalcDistansPlanetsTick
        self.CalcDistansVargasTick = CalcDistansVargasTick


def prognoz_inTime_data(new_command, first_date, first_time, degree_hourUTCq, degree_northLatitudeq, degree_eastLongitudeq,
                   d3_startTimeStr, d3_finishTimeStr, graphic_name, days_calculate):
    time_d3_startTime = datetime.strptime(d3_startTimeStr, FORMAT_DATE)
    time_d3_finishTime = datetime.strptime(d3_finishTimeStr, FORMAT_DATE)
    time_first_date = datetime.strptime(first_date, FORMAT_DATE)

    zero_time = datetime.strptime(ZERO_TIME, FORMAT_TIME)
    burn_time = datetime.strptime(first_time, FORMAT_TIME)

    start_period = time_d3_startTime
    finish_period = time_d3_finishTime

    simple_period_days = int((finish_period - start_period).days)

    houses_nature_default = [0] * 12

    """
        вычисление координат планет на установленное время рождения
    """
    rashi_data = calculateCoordsPlanet.calculate_coords_planet(first_date, first_time)

    graha_in_degrees = rashi_data.graha_in_degrees

    retrogr_planet = rashi_data.retrogr_planet

    """
        вычисление лагны
    """
    degree_north_latitude = time.strptime(degree_northLatitudeq, FORMAT_COORDS)
    ltd_degr = degree_north_latitude.tm_yday + (
            degree_north_latitude.tm_min * MINUTS_IN_HOUR + degree_north_latitude.tm_sec) / SECONDS_IN_HOUR

    degree_east_longitude = time.strptime(degree_eastLongitudeq, FORMAT_COORDS)
    lng_degr = degree_east_longitude.tm_yday + (
            degree_east_longitude.tm_min * MINUTS_IN_HOUR + degree_east_longitude.tm_sec) / SECONDS_IN_HOUR

    degree_hour_utc = time.strptime(degree_hourUTCq, "%H")
    utc = degree_hour_utc.tm_hour

    b_year = int(time_first_date.year)
    b_month = int(time_first_date.month)
    b_day = int(time_first_date.day)

    b_time = int(burn_time.hour * SECONDS_IN_HOUR + burn_time.minute * MINUTS_IN_HOUR + burn_time.second)

    sun_rise = int(calculate_sunrise_time.get_calculate_sunrise(ltd_degr, lng_degr, b_day, b_month, b_year, utc))

    sunrise_hour = sun_rise / SECONDS_IN_HOUR
    sunrise_minute = (sunrise_hour - math.trunc(sunrise_hour)) * MINUTS_IN_HOUR
    sunrise_second = (sunrise_minute - math.trunc(sunrise_minute)) * MINUTS_IN_HOUR

    sun_rise_seconds = int(sunrise_hour * 3600 + sunrise_minute * 60 + sunrise_second)
    sunrise_in_degrees = graha_in_degrees[SUN_PLANET_NUMBER]

    lagna_in_seconds = mathCalculateLagna.asc_calculate(sunrise_in_degrees, sun_rise_seconds, b_time, ltd_degr)
    lagna_in_seconds_znak = math.fmod(lagna_in_seconds, 108000)
    polojenie_lagna_rashi = int(lagna_in_seconds / 108000)

    """
        построение карты раши D1
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
    bhava_aspects_rashi = bhava_aspects_calculate.bhava_aspec(graha_in_degrees, polojenie_lagna_rashi, retrogr_planet)
    """
        градусы относительно лагны
    """

    graha_in_house_degrees = list(
        map(lambda x, y: x * 30 + (y / SECONDS_IN_HOUR), graha_in_house, absolut_dergrees_planets))

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
    bindy_lagna = graha_in_house[0:7]
    bindy_lagna.append(0)
    array_bindy = calculateBindy.calculate_bindy_vargas(bindy_lagna, [0])

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

    # оценка силы каждого дома
    def power_pl(pozition):
        nonlocal max_number
        nonlocal min_number
        # назначим силу домов, в расчете на количество лучей планеты
        houses_nature_default[pozition] = (((sudarshana_chakra_rasha[pozition] + sudarshana_chakra_chandra[pozition] +
                                             sudarshana_chakra_syria[pozition] + bhava_to_aspects[pozition]) +
                                            array_bindy[pozition]) + bala_shodasha[hozaeva_in_house[pozition]]) + \
                                          ratio_of_good_planet[hozaeva_in_house[pozition]] * \
                                          power_planet_rashi[hozaeva_in_house[pozition]] * ratio_of_ch_bhavas[pozition]
        if max_number < houses_nature_default[pozition]:
            max_number = houses_nature_default[pozition]

        if min_number > houses_nature_default[pozition]:
            min_number = houses_nature_default[pozition]

    list(map(lambda x: power_pl(x), ZODIAK_RANGE))

    ratio_of_good_bhavas = list(
        map(lambda x: (x - min_number) / (max_number - min_number) * 100, houses_nature_default))

    step_days = 1

    """
        построение транзитов планет
    """
    num_points = 0

    detals = 1
    HOUR_DUNAMYC = [420]

    # print("next_tranzit_str", "tranzit_retrograd", "power_planet_transit", "compound_grahas", "planet_jogakaraky_tr")
    if graphic_name != NAME_GRAPHICS[NO_GRAPHICS]:

        outPowPlanet = np.zeros((9, simple_period_days))
        aspects_ticks = np.zeros((13122, simple_period_days))
        dynamic_strenght_VRGTick = np.zeros((162, simple_period_days))
        CalcDistansPlanetsTick = np.zeros((81, simple_period_days))
        CalcDistansVargasTick = np.zeros((1458, simple_period_days))

        DataOutput = []
        # print('размеры таблицы составят:')
        col_len = len(DataOutput) + len(outPowPlanet) + len(aspects_ticks) + len(dynamic_strenght_VRGTick) + len(
                  CalcDistansPlanetsTick) + len(CalcDistansVargasTick)
        # print('summ colomns:', col_len)
        # print('количество значений:', col_len*simple_period_days)
        for nextPlanet in PLANETS_RANGE:
            # print()
            # print("analiz_planets--- ", NAME_PLANETS_DREK[nextPlanet], end=' ')
            per_last = 0
            for day_tranzit in np.arange(0, simple_period_days, step_days):
                percent_days = np.round(day_tranzit/simple_period_days*50, 0)

                if per_last < percent_days:
                    sum_pluss = '+'*int(percent_days-per_last)
                    per_last = percent_days
                    # print(sum_pluss, end='')

                next_tranzit = start_period + timedelta(days=int(day_tranzit) + 1)
                tranzit_weekday = next_tranzit.weekday()
                if day_tranzit>=len(DataOutput): DataOutput.append(next_tranzit)

                for i in np.arange(detals):
                    num_points += 1
                    hourses = 600 + HOUR_DUNAMYC[i]
                    next_tranzit_time = zero_time + timedelta(minutes=int(hourses))

                    next_tranzit_str = next_tranzit.strftime(FORMAT_DATE)
                    next_tranzit_time_str = next_tranzit_time.strftime(FORMAT_TIME)

                    trazit_data = calculateCoordsPlanet.calculate_coords_planet(next_tranzit_str, next_tranzit_time_str)

                    transit_graha_in_degrees = trazit_data.graha_in_degrees
                    tranzit_strenght_speed = trazit_data.sp_strenght_planet

                    tranzit_retrograd = trazit_data.retrogr_planet

                    tranzit_rashi = calculateRashi.calculate_rashi_card(transit_graha_in_degrees,
                                                                        graha_in_znak[MOON_PLANET_NUMBER])

                    tranzit_in_degrees = tranzit_rashi.graha_in_degrees
                    tranzit_in_znak = tranzit_rashi.graha_in_znak
                    tranzit_in_bhava = tranzit_rashi.graha_in_house

                    tranzit_absolut_degree = tranzit_rashi.absolut_dergrees_planets

                    transit_in_gradus_360 = list(map(lambda x: x/3600, tranzit_in_degrees))
                    """
                        вычисление угловых расстояний между планетами
                        nextPlanet - планета, относительно которой измеряются расстояния
                        transit_in_gradus_360 - угловое положение планет в градусах
                    """
                    CalcDist_PLN = anlgeDistansPlanets.calculateDistansePlanets(nextPlanet, transit_in_gradus_360)
                    for poz, valu in zip(PLANETS_RANGE, CalcDist_PLN):
                        ind_X = poz + nextPlanet * 9
                        CalcDistansPlanetsTick[ind_X][day_tranzit] = valu

                    lagna_in_seconds_znakTr = math.fmod(tranzit_in_degrees[nextPlanet], 108000)
                    polojenie_lagna_rashiTr = int(tranzit_in_degrees[nextPlanet] / 108000)

                    map_vargasPart = calculateVimshopakaBala.get_calculate_bala_of_planets(tranzit_absolut_degree,
                                                                                       tranzit_in_znak,
                                                                                       ALL_VARGAS_PARTS,
                                                                                       lagna_in_seconds_znakTr,
                                                                                       polojenie_lagna_rashiTr)

                    """
                        анализ по каждой варге-----------------------------------------------------------
                    """
                    for npo in enumerate(map_vargasPart):
                        nextVarga = npo[0]
                        next_map_varga = npo[1]
                        """
                            подсчет расстояний между планетами по каждой варге
                        """
                        nextVarga_in_gradus = list(map(lambda x: x*30, next_map_varga))


                        CalcDist_VRG = anlgeDistansPlanets.calculateDistansePlanets(nextPlanet, nextVarga_in_gradus)
                        for poz, valu in zip(PLANETS_RANGE, CalcDist_VRG):

                            ind_X = poz+nextVarga*9+nextPlanet*162
                            CalcDistansVargasTick[ind_X][day_tranzit] = valu


                        """
                            подсчет силы транзитов по каждой варге
                        """
                        nextVarga_in_degrees = list(map(lambda x: x*108000, next_map_varga))

                        varga_rashi = calculateRashi.calculate_rashi_card(nextVarga_in_degrees,
                                                                            next_map_varga[nextPlanet])

                        varga_in_degrees = varga_rashi.graha_in_degrees
                        varga_in_znak = varga_rashi.graha_in_znak
                        varga_in_bhava = varga_rashi.graha_in_house

                        varga_hozaevaInHouse = tranzit_rashi.hozaeva_in_house
                        varga_absolut_degree = varga_rashi.absolut_dergrees_planets

                        lagna_in_seconds_znak_VRG = math.fmod(varga_in_degrees[nextPlanet], 108000)

                        planet_nature_and_rising_sign_VRG = PlanetNatureCalculator().calculate(varga_in_degrees)
                        bindy_nature_grahas_VRG = calculateVimshopakaBala.get_calculate_bala_of_planets(
                            varga_absolut_degree, varga_in_znak,
                            BINDY_VARGA_CHARITY, lagna_in_seconds_znak_VRG, -1)

                        if len(planet_jogakaraky_D1.list_good_planets_joga) > 0:
                            for x_planet in PLANETS_RANGE:
                                for val_x in np.arange(len(planet_jogakaraky_D1.list_good_planets_joga)):
                                    if planet_jogakaraky_D1.list_good_planets_joga[val_x][0] == x_planet:
                                        planet_nature_and_rising_sign_VRG[x_planet] = \
                                        planet_jogakaraky_D1.list_good_planets_joga[val_x][1]
                        if len(planet_jogakaraky_D9.list_good_planets_joga) > 0:
                            for x_planet in PLANETS_RANGE:
                                for val_x in np.arange(len(planet_jogakaraky_D9.list_good_planets_joga)):
                                    if planet_jogakaraky_D9.list_good_planets_joga[val_x][0] == x_planet:
                                        planet_nature_and_rising_sign_VRG[x_planet] = \
                                        planet_jogakaraky_D9.list_good_planets_joga[val_x][1]

                        absolut_nature_planet_VRG = list(
                            map(lambda x, y, z1, z2: x + y + ((z1 + z2) / 2), planet_nature_and_rising_sign_VRG,
                                bindy_nature_grahas_VRG,
                                planet_jogakaraky_D1.relate_jogakaraka, planet_jogakaraky_D9.relate_jogakaraka))

                        tranzit_elements_planet_VRG = calculate_strenght_first_elements.strenght_first_elements(
                            varga_in_znak)

                        power_break_ganda_VRG = calculate_break.get_power_calculate_degress(varga_in_degrees, array_bindy,
                                                                                        graha_in_chandra_degrees,
                                                                                        tranzit_retrograd)

                        power_planet_transit_VRG = calculate_relations_file.calculate_relationS_grah(varga_in_znak)

                        power_planet_VRG = calculate_kendras_trikonas.kendra_trikonas(absolut_nature_planet_VRG,
                                                                                  varga_in_bhava,
                                                                                  varga_hozaevaInHouse)

                        compound_grahas_VRG = calculate_compound_file.calculate_compound_grahas(varga_in_degrees)

                        """
                            формула подсчета выводящей силы планет
                        """
                        summ_ganda_VRG = list(map(lambda x: ((trazit_data.sp_strenght_planet[x] * power_planet_transit_VRG[x]) + \
                                                         (ratio_of_good_bhavas[varga_in_bhava[x]] * (
                                                             ratio_of_good_planet[x]) / 4 - 25) + \
                                                         tranzit_elements_planet_VRG[x] + power_planet_VRG[x] +
                                                         tranzit_strenght_speed[x] - power_break_ganda_VRG[
                                                             x]) * RATIO_TR[x], PLANETS_RANGE))

                        summ_ganda_VRG = sum(summ_ganda_VRG)

                        day_strenght = calculate_code_of_day.code_moon_day(varga_in_degrees, tranzit_weekday)

                        ind_X = nextVarga+nextPlanet*18
                        dynamic_strenght_VRGTick[ind_X][day_tranzit] = (summ_ganda_VRG + day_strenght - sum(compound_grahas_VRG)) / 63


                        """
                                СИЛЫ ПЛАНЕТ В ВАРГАХ
                                aspects_ticks - сила планет в варгах, относительно лагн-планет
                        """
                        for planet_S in PLANETS_RANGE:
                            power_planet_in_varga = beginScript_POW.calculate_power_planet(nextVarga_in_degrees, tranzit_retrograd, nextVarga_in_degrees[planet_S])

                            for planet_POW in enumerate(power_planet_in_varga):

                                ind_X = planet_POW[0] + planet_S * 9 + nextVarga * 81 + nextPlanet * 729

                                aspects_ticks[ind_X][day_tranzit] = planet_POW[1]



                    """
                        переиначим природу планет
                    """
                    PLANETS_RANGE_TR = [nextPlanet]

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

                    bindy_lagna = tranzit_in_znak[0:7]
                    bindy_lagna.append(graha_in_znak[MOON_PLANET_NUMBER])

                    tranzit_elements_planet = calculate_strenght_first_elements.strenght_first_elements(tranzit_in_znak)

                    """
                        расположение планет в бинду
                    """
                    power_break_ganda = calculate_break.get_power_calculate_degress(tranzit_in_degrees, array_bindy,
                                                                                    graha_in_chandra_degrees,
                                                                                    tranzit_retrograd)
                    """
                        отношения грах между собой
                    """
                    power_planet_transit = calculate_relations_file.calculate_relationS_grah(tranzit_in_znak)

                    power_planet = calculate_kendras_trikonas.kendra_trikonas(absolut_nature_planet,
                                                                              tranzit_in_bhava,
                                                                              hozaeva_in_house)

                    """
                        соединения грах
                    """
                    compound_grahas = calculate_compound_file.calculate_compound_grahas(tranzit_in_degrees)

                    """
                        количество лучей грахи в знаках зодиака
                    """
                    bala_shodasha = calculateVimshopakaBala.get_calculate_bala_of_planets(tranzit_absolut_degree, tranzit_in_znak,
                                                                                          VARGA_SHODASHA, graha_in_znak[MOON_PLANET_NUMBER], -1)

                    """
                        формула подсчета выводящей силы планет
                    """
                    summ_ganda = list(map(lambda x: ((trazit_data.sp_strenght_planet[x] * power_planet_transit[x]) + \
                                                     (ratio_of_good_bhavas[tranzit_in_bhava[x]] * (
                                                         ratio_of_good_planet[x]) / 4 - 25)+ bala_shodasha[x] + \
                                                     tranzit_elements_planet[x] + power_planet[x] + tranzit_strenght_speed[x] - power_break_ganda[
                                                         x]) * RATIO_TR[x], PLANETS_RANGE_TR))

                    summ_ganda = sum(summ_ganda)

                    day_strenght = calculate_code_of_day.code_moon_day(transit_graha_in_degrees, tranzit_weekday)

                    outPowPlanet[nextPlanet][day_tranzit] = (summ_ganda + day_strenght - sum(compound_grahas)) / 63

        # print()

        # print('Сжатие данных...')
        DataOutput = np.array(DataOutput).reshape(1, simple_period_days)
        print(DataOutput.shape, outPowPlanet.shape, aspects_ticks.shape, dynamic_strenght_VRGTick.shape, CalcDistansPlanetsTick.shape,
              CalcDistansVargasTick.shape)


        Data_Gen = np.concatenate((DataOutput, outPowPlanet, aspects_ticks, dynamic_strenght_VRGTick, CalcDistansPlanetsTick, CalcDistansVargasTick), axis=0)

        import pandas as pd
        df = pd.DataFrame(Data_Gen.T)
        # print("len control-", df.shape)
        ppp = input('ПРОВЕРЬТЕ НАЛИЧИЕ ФЛЕШКИ В ДИСКЕ C:, затем нажмите ENTER')
        print("save......", end='')
        df.to_csv(r'C:\new_file.csv', index=False, sep=';')
        print("done!")
    return df
