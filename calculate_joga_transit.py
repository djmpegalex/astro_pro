from constants import *
import numpy as np
import math

from toolkits.math_distance import dist_in_degrees


def get_calculate_joga_transit(tranzit_in_znak, tranzit_in_bhava, tranzit_retrograd,
                               list_joga_D1, list_joga_D9, PLANETS_RANGE_TR=PLANETS_RANGE):
    """
        проверка сработает ли йога в гороскопе в данное время
         1. соединение двух планет йоги в домах (благоприятность даст соединение в кендре или триконе)
         2. взаимный аспект планет йоги из домов триконы и кендры
         3. две планеты занимают друг друга дома

         list_joga_D1 = [list_jewelry_joga, list_laksmi_joga, list_radja_joga, ] код йог соответствующий: 0, 1, 2...
    """

    joga_day = []

    for n_joga in np.arange(len(list_joga_D1)):
        joga_day.append([])
        for planet1 in PLANETS_RANGE_TR:
            for planet2 in PLANETS_RANGE_TR:
                if planet1 != planet2:
                    # проверка на соединение планет
                    if tranzit_in_znak[planet1] == tranzit_in_znak[planet2]:
                        # проверка на транзит в кендре или триконе соединяемых планет
                        if tranzit_in_bhava[planet1] in [0, 3, 4, 6, 8, 9]:
                            """
                                йога
                            """
                            if len(list_joga_D1[n_joga]) > 0:
                                for len_jew in np.arange(len(list_joga_D1[n_joga])):
                                    if ((list_joga_D1[n_joga][len_jew][0] == planet1) and (list_joga_D1[n_joga][len_jew][1] == planet2)) or (
                                            (list_joga_D1[n_joga][len_jew][1] == planet1) and (list_joga_D1[n_joga][len_jew][0] == planet2)):
                                        joga_day[n_joga].append([planet1, planet2])

                            if len(list_joga_D9[n_joga]) > 0:
                                for len_jew in np.arange(len(list_joga_D9[n_joga])):
                                    if ((list_joga_D9[n_joga][len_jew][0] == planet1) and (list_joga_D9[n_joga][len_jew][1] == planet2)) or (
                                            (list_joga_D9[n_joga][len_jew][1] == planet1) and (list_joga_D9[n_joga][len_jew][0] == planet2)):
                                        joga_day[n_joga].append([planet1, planet2])


                    if (tranzit_in_bhava[planet1] in [0, 3, 4, 6, 8, 9]) and (tranzit_in_bhava[planet2] in [0, 3, 4, 6, 8, 9]):
                        # проверка взаимный аспект планет друг на друга из домов триконы
                        for casp_n in range(len(ASP[planet1])):
                            if ASP[planet1][casp_n] > 0:
                                for ret_n in range(tranzit_retrograd[planet1] + 1):
                                    """
                                        проверка на наличие второй планеты, куда идет аспект с учетом признака ретроградности
                                    """
                                    if int(math.fmod(tranzit_in_znak[planet1] + ASP[planet1][casp_n] - ret_n + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK)) == tranzit_in_znak[planet2]:
                                        """
                                            проверка взаимного аспекта
                                        """
                                        for casp_m in range(len(ASP[planet2])):
                                            if ASP[planet2][casp_m] > 0:
                                                for ret_m in range(tranzit_retrograd[planet2] + 1):
                                                    """
                                                        проверка на наличие второй планеты, куда идет аспект с учетом признака ретроградности
                                                    """
                                                    if int(math.fmod(tranzit_in_znak[planet2] + ASP[planet2][casp_m] - ret_m + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK)) == tranzit_in_znak[planet1]:
                                                        """
                                                            йога
                                                        """
                                                        if len(list_joga_D1[n_joga]) > 0:
                                                            for len_jew in np.arange(len(list_joga_D1[n_joga])):
                                                                if ((list_joga_D1[n_joga][len_jew][0] == planet1) and (list_joga_D1[n_joga][len_jew][1] == planet2)) or (
                                                                        (list_joga_D1[n_joga][len_jew][1] == planet1) and (list_joga_D1[n_joga][len_jew][0] == planet2)):
                                                                    joga_day[n_joga].append([planet1, planet2])

                                                        if len(list_joga_D9[n_joga]) > 0:
                                                            for len_jew in np.arange(len(list_joga_D9[n_joga])):
                                                                if ((list_joga_D9[n_joga][len_jew][0] == planet1) and (list_joga_D9[n_joga][len_jew][1] == planet2)) or (
                                                                        (list_joga_D9[n_joga][len_jew][1] == planet1) and (list_joga_D9[n_joga][len_jew][0] == planet2)):
                                                                    joga_day[n_joga].append([planet1, planet2])

                    # две планеты занимают дома друг друга
                    for planet1_uprav in np.arange(len(PLANET_UPRAV[planet1])):
                        for planet2_uprav in np.arange(len(PLANET_UPRAV[planet2])):
                            if (PLANET_UPRAV[planet1_uprav] == tranzit_in_znak[planet2]) and (PLANET_UPRAV[planet2_uprav] == tranzit_in_znak[planet1]):
                                """
                                    йога
                                """
                                if len(list_joga_D1[n_joga]) > 0:
                                    for len_jew in np.arange(len(list_joga_D1[n_joga])):
                                        if ((list_joga_D1[n_joga][len_jew][0] == planet1) and (list_joga_D1[n_joga][len_jew][1] == planet2)) or (
                                                (list_joga_D1[n_joga][len_jew][1] == planet1) and (list_joga_D1[n_joga][len_jew][0] == planet2)):
                                            joga_day[n_joga].append([planet1, planet2])

                                if len(list_joga_D9[n_joga]) > 0:
                                    for len_jew in np.arange(len(list_joga_D9[n_joga])):
                                        if ((list_joga_D9[n_joga][len_jew][0] == planet1) and (list_joga_D9[n_joga][len_jew][1] == planet2)) or (
                                                (list_joga_D9[n_joga][len_jew][1] == planet1) and (list_joga_D9[n_joga][len_jew][0] == planet2)):
                                            joga_day[n_joga].append([planet1, planet2])



    return joga_day

def get_calculate_yoga_horoscop(graha_in_house, retrogr_planet, lagna_in_znak):
    parametrs_planets = {}

    for planet in PLANETS_RANGE:
        parametrs_planets.update({planet:[]})

        """
            Присвоение планетам ранга в триконе, в квадранте
        """
        if graha_in_house[planet] in [0, 4, 8]: parametrs_planets[planet].append('расположен в триконе')
        if graha_in_house[planet] in [0, 3, 6, 9]: parametrs_planets[planet].append('расположен в квадранте')

        """
            Указываем какие дома аспектируют планеты
        """
        for aspect in ASPECTS_FOR_YOGA[planet]:
            retrograd = int(retrogr_planet[planet] == 1)
            if aspect == 0: retrograd = 0
            aspect_on_bhava = int(np.fmod(aspect + graha_in_house[planet] - retrograd + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK))
            parametrs_planets[planet].append('влияет на дом ' + str(aspect_on_bhava + 1))

    who_upravlaet_house = WHO_UPRAVLAET_ZNAKOM_LI[lagna_in_znak:] + WHO_UPRAVLAET_ZNAKOM_LI[:lagna_in_znak]

    for house, upr_planets in enumerate(who_upravlaet_house):
        if house in [0, 4, 8]:
            for upr_planet in upr_planets:
                parametrs_planets[upr_planet].append('управитель трикона')
        if house in [0, 3, 6, 9]:
            for upr_planet in upr_planets:
                parametrs_planets[upr_planet].append('управитель кендры')

    """
        Раджа-Йога первого типа
        Хозяин триады и хозяин квадранта располагаются в одном доме
    """
    for planet_trikon in PLANETS_RANGE:
        if 'управитель трикона' in parametrs_planets[planet_trikon]:
            for planet_kvadrant in PLANETS_RANGE:
                if planet_trikon == planet_kvadrant: continue
                if 'управитель кендры' in parametrs_planets[planet_kvadrant]:
                    if graha_in_house[planet_trikon] == graha_in_house[planet_kvadrant]:
                        parametrs_planets[planet_trikon].append(
                            'раджа-йога тип 1 ' + NAME_PLANETS_DREK[planet_trikon] + ' ' + NAME_PLANETS_DREK[planet_kvadrant] + ' дом ' + str(graha_in_house[planet_trikon]))
                        parametrs_planets[planet_kvadrant].append(
                            'раджа-йога тип 1 ' + NAME_PLANETS_DREK[planet_trikon] + ' ' + NAME_PLANETS_DREK[planet_kvadrant] + ' дом ' + str(graha_in_house[planet_kvadrant]))

    """
        Раджа-йога второго типа
        Хозяева триады и квадранта одновременно влияют на один дом
    """
    for planet_trikon in PLANETS_RANGE:
        if 'управитель трикона' in parametrs_planets[planet_trikon]:
            for planet_kvadrant in PLANETS_RANGE:
                if planet_trikon == planet_kvadrant: continue
                if 'управитель кендры' in parametrs_planets[planet_kvadrant]:
                    for parametrs_planet_1 in parametrs_planets[planet_trikon]:
                        if str(parametrs_planet_1).find('влияет на') != -1:
                            for parametrs_planet_2 in parametrs_planets[planet_kvadrant]:
                                if str(parametrs_planet_2).find('влияет на') != -1:
                                    if parametrs_planet_1 == parametrs_planet_2:
                                        parametrs_planets[planet_trikon].append(
                                            'раджа-йога тип 2 ' + NAME_PLANETS_DREK[planet_trikon] + ' ' + NAME_PLANETS_DREK[
                                                planet_kvadrant] + ' дом ' + str(parametrs_planet_1)[-2:].replace(' ', ''))
                                        parametrs_planets[planet_kvadrant].append(
                                            'раджа-йога тип 2 ' + NAME_PLANETS_DREK[planet_trikon] + ' ' + NAME_PLANETS_DREK[
                                                planet_kvadrant] + ' дом ' + str(parametrs_planet_2)[-2:].replace(' ', ''))

    """
        Раджа-йога третьего типа
        Обмен домами между хояевами триады и квадранта
    """
    for planet_trikon in PLANETS_RANGE:
        if 'управитель трикона' in parametrs_planets[planet_trikon]:
            for planet_kvadrant in PLANETS_RANGE:
                if planet_trikon == planet_kvadrant: continue
                if 'управитель кендры' in parametrs_planets[planet_kvadrant]:
                    if graha_in_house[planet_trikon] in who_upravlaet_house[graha_in_house[planet_kvadrant]] and \
                       graha_in_house[planet_kvadrant] in who_upravlaet_house[graha_in_house[planet_trikon]]:
                        parametrs_planets[planet_trikon].append(
                            'раджа-йога тип 3 ' + NAME_PLANETS_DREK[planet_trikon] + ' ' + NAME_PLANETS_DREK[
                                planet_kvadrant] + ' дом ' + str(graha_in_house[planet_trikon]))
                        parametrs_planets[planet_kvadrant].append(
                            'раджа-йога тип 3 ' + NAME_PLANETS_DREK[planet_trikon] + ' ' + NAME_PLANETS_DREK[
                                planet_kvadrant] + ' дом ' + str(graha_in_house[planet_kvadrant]))

    """
        Раджа-йога четвертого типа
        Управитель триконы в кендре, управитель кендры в триконе
    """
    for planet in PLANETS_RANGE:
        if ('управитель трикона' in parametrs_planets[planet] and
            'расположен в квадранте' in parametrs_planets[planet]) or \
           ('управитель кендры' in parametrs_planets[planet] and
            'расположен в триконе' in parametrs_planets[planet]):
            parametrs_planets[planet].append(
                'раджа-йога тип 4 ' + NAME_PLANETS_DREK[planet] + ' дом ' + str(graha_in_house[planet]))

    """
        Раджа-йога пятого типа
        Двое из правителей 1й бхавы 5й бхавы и 9й бхавы соеденены или бросают взаимный аспект
    """
    for planet_trikon_1 in PLANETS_RANGE:
        if 'управитель трикона' in parametrs_planets[planet_trikon_1]:
            for planet_trikon_2 in PLANETS_RANGE:
                if planet_trikon_1 == planet_trikon_2: continue
                if 'управитель трикона' in parametrs_planets[planet_trikon_2]:
                    for parametrs_planet_1 in parametrs_planets[planet_trikon_1]:
                        if str(parametrs_planet_1).find('влияет на') != -1:
                            if str(graha_in_house[planet_trikon_2]) == str(parametrs_planet_1)[-2:].replace(' ', ''):
                                for parametrs_planet_2 in parametrs_planets[planet_trikon_2]:
                                    if str(parametrs_planet_2).find('влияет на') != -1:
                                        if str(graha_in_house[planet_trikon_1]) == str(parametrs_planet_2)[-2:].replace(' ', ''):
                                            parametrs_planets[planet_trikon_2].append(
                                                'раджа-йога тип 5 ' + NAME_PLANETS_DREK[planet_trikon_1] + ' ' + NAME_PLANETS_DREK[
                                                    planet_trikon_2] + ' дом ' + str(graha_in_house[planet_trikon_1]))
                                            parametrs_planets[planet_trikon_2].append(
                                                'раджа-йога тип 5 ' + NAME_PLANETS_DREK[planet_trikon_1] + ' ' + NAME_PLANETS_DREK[
                                                    planet_trikon_2] + ' дом ' + str(graha_in_house[planet_trikon_2]))

    """
        Раджа-йога шестого типа
        Один из правителей триконы или кендры аспектирует другого правителя из его же знака управления
    """
    for planet_trikon in PLANETS_RANGE:
        if 'управитель трикона' in parametrs_planets[planet_trikon]:
            for planet_kvadrant in PLANETS_RANGE:
                if planet_trikon == planet_kvadrant: continue
                if 'управитель кендры' in parametrs_planets[planet_kvadrant]:
                    """
                        Находится ли управитель кендры в знаке управления управителя триконы
                    """
                    if planet_kvadrant in who_upravlaet_house[graha_in_house[planet_trikon]]:
                        for parametrs_planet in parametrs_planets[planet_trikon]:
                            if str(parametrs_planet).find('влияет на') != -1:
                                if str(graha_in_house[planet_kvadrant]) == str(parametrs_planet)[-2:].replace(' ', ''):
                                    parametrs_planets[planet_kvadrant].append(
                                        'раджа-йога тип 5 ' + NAME_PLANETS_DREK[planet_trikon] + ' ' +
                                        NAME_PLANETS_DREK[
                                            planet_kvadrant] + ' дом ' + str(graha_in_house[planet_kvadrant]))

                    """
                        Находится ли управитель триконы в знаке управления управителя кендры
                    """
                    if planet_trikon in who_upravlaet_house[graha_in_house[planet_kvadrant]]:
                        for parametrs_planet in parametrs_planets[planet_kvadrant]:
                            if str(parametrs_planet).find('влияет на') != -1:
                                if str(graha_in_house[planet_trikon]) == str(parametrs_planet)[-2:].replace(' ', ''):
                                    parametrs_planets[planet_trikon].append(
                                        'раджа-йога тип 5 ' + NAME_PLANETS_DREK[planet_trikon] + ' ' +
                                        NAME_PLANETS_DREK[
                                            planet_trikon] + ' дом ' + str(graha_in_house[planet_trikon]))
    """
        Подсчет количества йог
    """
    all_yogas = []
    for planet in parametrs_planets.keys():
        for parametrs in parametrs_planets[planet]:
            if str(parametrs).find("йога") != -1 and parametrs not in all_yogas: all_yogas.append(parametrs)

    return len(all_yogas)

def get_calculate_baby_generate(graha_in_house, lagna_in_znak, tranzit_retrograd, tranzit_in_znak):
    who_upravlaet_house = WHO_UPRAVLAET_ZNAKOM_LI[lagna_in_znak:] + WHO_UPRAVLAET_ZNAKOM_LI[:lagna_in_znak]
    tranzit_in_house = [int(np.fmod(tranzit_in_znak[planet] - lagna_in_znak + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK)) for planet in PLANETS_RANGE]

    parametrs_planets = {}

    flag_baby = [0, 0, 0, 0]

    for n_planet, planet in enumerate([SATURN_PLANET_NUMBER, JUPITER_PLANET_NUMBER,
                                       MARS_PLANET_NUMBER, MOON_PLANET_NUMBER]):
        parametrs_planets.update({planet:[]})

        """
            Указываем какие дома аспектируют планеты
        """
        for aspect in ASPECTS_FOR_YOGA[planet]:
            retrograd = int(tranzit_retrograd[planet] == 1)
            if aspect == 0: retrograd = 0
            aspect_on_bhava = int(np.fmod(aspect + graha_in_house[planet] - retrograd + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK))
            parametrs_planets[planet].append(aspect_on_bhava)

            if aspect_on_bhava in [4, 8]: flag_baby[n_planet] += 1

        """
            Указываем правителей каких домов влияет аспект планет
        """
        for house, upr_planets in enumerate(who_upravlaet_house):
            """
                Находим управителя 5го и 9го дома
            """
            if house in [4, 8]:
                for upr_planet in upr_planets:
                    # if upr_planet in [7, 8]: continue #Исключаем из расчета управителей Раху и Кету
                    """
                        Если управители 5го и 9го домов под аспектом Сатурна и Юпитера - флаг = 1
                    """
                    if tranzit_in_house[upr_planet] in parametrs_planets[planet]: flag_baby[n_planet] += 1

        if planet == MOON_PLANET_NUMBER and \
            tranzit_in_house[MOON_PLANET_NUMBER] in [0, 6, 4, 10, 8, 2]: flag_baby[n_planet] += 1

    result = [int(flag_baby[0] + flag_baby[1]), flag_baby[2], flag_baby[3]]

    for n in range(len(result)):
        if result[n] > 5: result[n] = 5

    return result

def calculate_oil_down(graha_in_znak=None, tranzit_retrograd=None, main_planet=MERCURY_PLANET_NUMBER):

    """
        Функция для вычисления вероятности обвала рынка нефти
        ключевые влияния на меркурий и его дома - Sa Ra Ju Ma и соединение с планетой ретранслятором
        пагубные планеты могут сгорать от солнца, венера нейтрализует сатурн

        1. вычисляем аспеты на меркурий от каждой из планет
        2. венера и солнце и другие планеты могут выступать планетами ретрансляторами, если есть соединение c ними -
            здесь нужно создать словарь, какая планета берет на себя энергию какой планеты
    """

    spl = []
    for planet in [MERCURY_PLANET_NUMBER, MARS_PLANET_NUMBER, JUPITER_PLANET_NUMBER, SATURN_PLANET_NUMBER, RAHY_PLANET_NUMBER, KETY_PLANET_NUMBER]:
        if planet != main_planet: spl.append(planet)

    parametrs_planets = {}
    regress_toplanets = {}

    for planet in PLANETS_RANGE:
        parametrs_planets.update({planet:[]})

        """
            Указываем какие знаки аспектируют планеты
        """
        for aspect in ASPECTS_FOR_YOGA[planet]:
            retrograd = int(tranzit_retrograd[planet] == 1)
            if aspect == 0: retrograd = 0
            aspect_on_bhava = int(np.fmod(aspect + graha_in_znak[planet] - retrograd + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK))
            parametrs_planets[planet].append(aspect_on_bhava)

    for planet1 in PLANETS_RANGE:
        regress_toplanets.update({planet1: []})

        """
            Собираем данные какая планета находится под чьими аспектами
        """
        for planet2 in PLANETS_RANGE:

            if planet1 == planet2: continue
            #проверка на условие - сгорает ли планета под лучами солнца, чтобы аннулировать действие аспектов
            if graha_in_znak[SUN_PLANET_NUMBER] == graha_in_znak[planet2] and planet2 in [1,2,4,5,6] and \
                graha_in_znak[SUN_PLANET_NUMBER] not in [graha_in_znak[RAHY_PLANET_NUMBER], graha_in_znak[KETY_PLANET_NUMBER]]: continue

            if graha_in_znak[planet1] in parametrs_planets[planet2]: regress_toplanets[planet1].append(planet2)

        """
            Собираем данные дома какой планеты находятся под чьими аспектами
        """
        for uprav in PLANET_UPRAV[planet1]:
            for planet2 in PLANETS_RANGE:

                if planet1 == planet2: continue
                # проверка на условие - сгорает ли планета под лучами солнца, чтобы аннулировать действие аспектов
                if graha_in_znak[SUN_PLANET_NUMBER] == graha_in_znak[planet2] and planet2 in [1, 2, 4, 5, 6] and \
                        graha_in_znak[SUN_PLANET_NUMBER] not in [graha_in_znak[RAHY_PLANET_NUMBER],
                                                                 graha_in_znak[KETY_PLANET_NUMBER]]: continue

                if uprav in parametrs_planets[planet2]: regress_toplanets[planet1].append(planet2)

    """
        проверка влияния планет с учетом ретрансляции
    """
    trance_planets = {}
    for planet1 in PLANETS_RANGE:
        trance_planets.update({planet1: []})
        for planet2 in PLANETS_RANGE:
            if planet2 == planet1: continue

            if graha_in_znak[planet1] == graha_in_znak[planet2]:
                for parametr in regress_toplanets[planet2]:
                    trance_planets[planet1].append(parametr)

    """
        трансляция влияния планет на меркурий
    """
    for planet2 in PLANETS_RANGE:
        if planet2 == main_planet: continue

        if graha_in_znak[main_planet] == graha_in_znak[planet2]:
            for parametr in trance_planets[planet2]:
                regress_toplanets[main_planet].append(parametr)

    # # Если планета находится в собственном знаке, и она одна в знаке, что влияние на нее аннулируется
    # if graha_in_znak[MERCURY_PLANET_NUMBER] in SELF_ZNAKS[MERCURY_PLANET_NUMBER] and \
    #     graha_in_znak[MERCURY_PLANET_NUMBER] not in graha_in_znak[:MERCURY_PLANET_NUMBER] + graha_in_znak[MERCURY_PLANET_NUMBER + 1:]:
    #     regress_toplanets[MERCURY_PLANET_NUMBER] = []
    counts_yoga = 0
    for planet in spl:
        counts_yoga += int(planet in regress_toplanets[main_planet])
                   
    counts = 0
    if counts_yoga >= 3:
        counts = -3

        # Оценка положения самого меркурия
        if graha_in_znak[main_planet] == SELF_DEBILITATION[main_planet]: counts += 3
        if tranzit_retrograd[main_planet] == 1: counts += 3

        for param in regress_toplanets[main_planet]:
            if param in spl:
                counts += 1

    if counts > 15: counts = 15
    elif counts < 12: counts = 0

    return counts


def calculate_SNP500_down(graha_in_degrees=None, tranzit_retrograd=None,
                          main_planets=None, break_planets=None, sphuta=None):
    """
        преобразование с учетом спхуты
    """
    main_planets = main_planets + np.arange(9, 9+len(sphuta)).tolist()
    planets_range = np.arange(9 + len(sphuta))
    graha_in_degrees_ = graha_in_degrees[0:9] + sphuta
    graha_in_znak = np.asarray(np.array(graha_in_degrees) / 108000, dtype='int32').tolist()
    aspects_for_yoga = ASPECTS_FOR_YOGA + [[0]]
    tranzit_retrograd += [0]

    parametrs_planets = {}
    regress_toplanets = {}
    parametrs_planets_znak = {}

    for planet in planets_range:
        parametrs_planets.update({planet: []})
        parametrs_planets_znak.update({planet: []})

        """
            Указываем какие градусы аспектируют планеты
        """
        for aspect in aspects_for_yoga[planet]:
            retrograd = int(tranzit_retrograd[planet] == 1)
            if aspect == 0: retrograd = 0
            aspect_on_bhava = int(
                np.fmod(aspect*108000 + graha_in_degrees_[planet] - retrograd*108000 + SECONDS_IN_ZODIAC, SECONDS_IN_ZODIAC))
            parametrs_planets[planet].append(aspect_on_bhava)

            aspect_on_bhava_znak = int(np.fmod(aspect + int(graha_in_degrees_[planet]/108000) - retrograd + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK))
            parametrs_planets_znak[planet].append(aspect_on_bhava_znak)

    for planet1 in main_planets:
        regress_toplanets.update({planet1: []})

        """
            Собираем данные какая планета находится под чьими аспектами
        """
        for planet2 in break_planets:
            if planet1 == planet2: continue

            for aspect in parametrs_planets[planet2]:
                if dist_in_degrees(M=graha_in_degrees_[planet1], S=aspect) < 36000: regress_toplanets[planet1].append(planet2)

            if graha_in_znak[planet1] in parametrs_planets_znak[planet2]: regress_toplanets[planet1].append(planet2)

    counts_yoga = 0
    for planet1 in main_planets:
        for planet2 in break_planets:
            counts_yoga += int(planet2 in regress_toplanets[planet1])

    if counts_yoga < 3: counts_yoga=0
    elif counts_yoga > 9: counts_yoga = 8
    else: counts_yoga = int(counts_yoga)

    return counts_yoga