import csv, numpy as np
import math

from constants import nak_nam_pl, SECONDS_IN_NAKSHATRA, WHO_UPRAVLAET_ZNAKOM_LI, PLANET_UPRAV, NAME_PLANETS_DREK, \
    ASPECTS_FOR_YOGA, ASPECTS_FOR_YOGA_DICT, SECONDS_IN_ZNAK, DICT_NAME_PLANETS, SECONDS_IN_ZODIAC
from toolkits.math_distance import dist_in_degrees

FILE_PATH = 'resources/baseOfAstrologyUtf.csv'

data_of_dict = {}

with open(FILE_PATH, encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
    for count, row in enumerate(reader):
        if count == 0:
            for name_col in row:
                if 'Name' in name_col: name_col = 'Name'
                data_of_dict.update({name_col: []})
        else:
            for value, col in zip(row, data_of_dict.keys()):

                if col == 'Name': data_of_dict[col].append(value)
                else: data_of_dict[col].append(int(value))

def verify_str(strings=None):
    if len(strings) == 1: strings = '0' + strings
    return strings

def create_planets_code(planets_in_seconds=None, planets_retrograd=None, planets_in_houses=None,
                        planets_in_d9_sec=None):

    def refused_dict(ratio=None, add_ratio=1, part=None, in_str1='None', name_1=None, in_str2='None',
                     name_int2=None, name_col='None', vratio=1.0):
        if len(in_str2) == 1: in_str2 = '0' + in_str2

        planet_of_dicts = {'planet_in_znak': name_1 + 'Z' + in_str2, 'lagna_in_znak': 'LgZ' + in_str2,
                           'planet_in_house': name_1 + 'H' + in_str2,
                           'planet_in_nakshatra_pada': name_1 + 'N' + in_str2 + 'P' + in_str1,
                           'uprav_house_in_house': in_str1 + 'H' + in_str2,
                           'planet_in_nakshatra_aspect': name_planet + 'N' + in_str1 + 'A' + in_str2,
                           'planet_in_nakshatra': name_1 + 'N' + in_str2}

        if ratio is None:
            ratio = (part / .75 + .56) * add_ratio * vratio
            if ratio > 1: ratio = 1

        if name_int2 is not None:
            name_2 = NAME_PLANETS_DREK[name_int2]
        else:
            name_2 = name_1

        dict_of_ratios_planets[name_1].append(ratio)
        dict_of_ratios_planets[name_2].append((1 - ratio) * add_ratio)
        dict_of_code_planets[name_2].append(planet_of_dicts[name_col])

    def verify_part(part=None):
        if part <= .33: return -1
        elif part >= .67: return 1
        else: return 0

    """
        Кодировка
    """

    dict_of_code_planets = {}
    dict_of_ratios_planets = {}
    for name_planet in nak_nam_pl:
        dict_of_code_planets.update({name_planet: []})
        dict_of_ratios_planets.update({name_planet: []})

    if planets_in_houses is not None and True: # флаг для того что мы смотрим чисто по транзитам или мы еще знаем лагну (точное время рождения)
        lagna_in_znak_drop = math.modf(math.fmod(planets_in_seconds[0] / 108000 - planets_in_houses[0] + 12, 12))
        lagna_in_part, lagna_in_znak = lagna_in_znak_drop[0], int(lagna_in_znak_drop[1])

        """
            Добавление кодировки для Лагны гороскопа
        """
        ratio1 = 1.0
        lagna_in_znak_str1 = verify_str(str(int(lagna_in_znak)))
        lagna_in_znak_str2 = None

        for name_planet_int in WHO_UPRAVLAET_ZNAKOM_LI[lagna_in_znak]:
            name_planet = NAME_PLANETS_DREK[name_planet_int]
            dict_of_code_planets[name_planet].append('LgZ' + lagna_in_znak_str1)
            if .33 <= lagna_in_part <= .67:
                dict_of_ratios_planets[name_planet].append(ratio1)
            else:
                lagna_in_znak2 = int(math.fmod(int(lagna_in_znak) + verify_part(part=lagna_in_part) + 12, 12))
                lagna_in_znak_str2 = str(lagna_in_znak2)
                for name_planet2_int in WHO_UPRAVLAET_ZNAKOM_LI[lagna_in_znak2]:
                    refused_dict(part=lagna_in_part, name_1=name_planet, in_str2=lagna_in_znak_str2,
                                 name_int2=name_planet2_int, name_col='lagna_in_znak')

        """
            получение управителей
        """
        who_upravlaet_house = {}
        for ind, planets_u in enumerate(PLANET_UPRAV):
            uprav = []
            for planet_u in planets_u:
                uprav.append(int(math.fmod(planet_u - lagna_in_znak + 12, 12)))
            who_upravlaet_house.update({nak_nam_pl[ind]: uprav})

        """
            Добавление кодировки расположения планеты в доме гороскопа
        """
        for name_planet, planet_in_house, planet_in_parts in zip(nak_nam_pl, planets_in_houses, np.modf(np.array(planets_in_seconds) / 108000)[0]):
            ratio1 = 1.0

            planet_in_house_str1 = verify_str(str(int(planet_in_house)))
            planet_in_house_str2 = None

            dict_of_code_planets[name_planet].append(name_planet + 'H' + planet_in_house_str1)
            if .33 <= planet_in_parts <= .67:
                dict_of_ratios_planets[name_planet].append(ratio1)
            else:
                planet_in_house_str2 = str(int(math.fmod(int(planet_in_house) + verify_part(part=planet_in_parts) + 12, 12)))
                refused_dict(part=planet_in_parts, name_1=name_planet, in_str2=planet_in_house_str2,
                             name_col='planet_in_house')

            """
                Добавление кодировки - хозяин Х дома в У доме
            """
            for upravlaet_house in who_upravlaet_house[name_planet]:
                upravlaet_house_str1 = verify_str(str(int(upravlaet_house)))

                dict_of_code_planets[name_planet].append(upravlaet_house_str1 + 'H' + planet_in_house_str1)

                if .33 <= planet_in_parts <= .67:
                    dict_of_ratios_planets[name_planet].append(ratio1)
                else:
                    refused_dict(ratio=ratio1, name_1=name_planet, in_str1=upravlaet_house_str1,
                                 in_str2=planet_in_house_str2, name_col='uprav_house_in_house')

    for planets_in_second, vratio in zip([planets_in_seconds, planets_in_d9_sec], [1.0, 0.7]):

        """
            Добавление кодировки положения планет в знаках с учетом пограничного положения
        """
        for name_planet, planet_in_znak, planet_in_parts in zip(nak_nam_pl, np.modf(np.array(planets_in_second)/108000)[1], np.modf(np.array(planets_in_second)/108000)[0]):
            planet_in_znak_str1 = verify_str(str(int(planet_in_znak)))

            dict_of_code_planets[name_planet].append(name_planet + 'Z' + planet_in_znak_str1)
            if .33 <= planet_in_parts <= .67:
                dict_of_ratios_planets[name_planet].append(vratio)
            else:
                planet_in_znak_str2 = str(int(math.fmod(int(planet_in_znak) + verify_part(part=planet_in_parts) + 12, 12)))
                refused_dict(part=planet_in_parts, name_1=name_planet, in_str2=planet_in_znak_str2,
                             name_col='planet_in_znak', vratio=vratio)

        """
            выясняем какая планета аспектирует какую
        """
        dict_who_aspect_who = {}
        for name_planet in nak_nam_pl:
            for aspect in ASPECTS_FOR_YOGA_DICT[name_planet]:
                planet_to_asp = DICT_NAME_PLANETS[name_planet]
                retrograd = planets_retrograd[planet_to_asp]
                aspect_on_seconds = int(np.fmod(aspect * SECONDS_IN_ZNAK + planets_in_second[
                    planet_to_asp] - retrograd * SECONDS_IN_ZNAK + SECONDS_IN_ZODIAC, SECONDS_IN_ZODIAC))

                for planet2, position2 in zip(NAME_PLANETS_DREK, planets_in_second):
                    dist = dist_in_degrees(M=aspect_on_seconds, S=position2)
                    if dist < 36000 and planet2 != name_planet:
                        ratio = 1 - dist / 36000
                        if planet2 not in dict_who_aspect_who.keys():
                            dict_who_aspect_who.update({planet2: {name_planet: ratio}})
                        else:
                            dict_who_aspect_who[planet2].update({name_planet: ratio})

        """
            Добавление положения планет в накшатре и паде с учетом пограничного положения
        """
        planets_in_nakshatra = np.array(planets_in_second) / SECONDS_IN_NAKSHATRA
        planets_in_pada = np.modf(planets_in_nakshatra)[0] * 4

        for planet_in_nakshatra, name_planet, planet_in_pada, planet_in_parts in zip(planets_in_nakshatra, nak_nam_pl, np.modf(planets_in_pada)[1], np.modf(planets_in_pada)[0]):

            planets_in_nakshatra_str = verify_str(str(int(planet_in_nakshatra)))
            planet_in_pada_str1 = str(int(planet_in_pada))

            dict_of_code_planets[name_planet].append(name_planet + 'N' + planets_in_nakshatra_str + 'P' + planet_in_pada_str1)
            if .33 <= planet_in_parts <= .67:
                dict_of_ratios_planets[name_planet].append(vratio)
            else:
                planet_in_pada_2 = int(planet_in_pada) + verify_part(part=planet_in_parts)

                if planet_in_pada_2 == -1:
                    planets_in_nakshatra_str = verify_str(str(int(math.fmod(int(planet_in_nakshatra) - 1 + 27, 27))))
                    planet_in_pada_2 = 3
                elif planet_in_pada_2 == 4:
                    planets_in_nakshatra_str = verify_str(str(int(math.fmod(int(planet_in_nakshatra) + 1 + 27, 27))))
                    planet_in_pada_2 = 0

                planet_in_pada_str2 = str(planet_in_pada_2)

                refused_dict(part=planet_in_parts, in_str1=planet_in_pada_str2, name_1=name_planet,
                             in_str2=planets_in_nakshatra_str, name_col='planet_in_nakshatra_pada', vratio=vratio)

            """
                Добавление кодировки расположения планеты под аспектом другой планеты
            """
            if name_planet in dict_who_aspect_who.keys():
                for who_aspect in dict_who_aspect_who[name_planet].keys():
                    nakshatra_in_parts = math.modf(planet_in_nakshatra)[0]

                    dict_of_code_planets[name_planet].append(name_planet + 'N' + planets_in_nakshatra_str + 'A' + who_aspect)
                    ratio_s = dict_who_aspect_who[name_planet][who_aspect] * vratio

                    if .33 <= nakshatra_in_parts <= .67:
                        dict_of_ratios_planets[name_planet].append(ratio_s)
                    else:
                        planet_in_nak_str2 = verify_str(str(int(math.fmod(int(planet_in_nakshatra) + verify_part(part=nakshatra_in_parts) + 27, 27))))
                        refused_dict(add_ratio=dict_who_aspect_who[name_planet][who_aspect], part=nakshatra_in_parts,
                                     in_str1=planet_in_nak_str2, name_1=name_planet,
                                     in_str2=who_aspect, name_col='planet_in_nakshatra_aspect', vratio=vratio)

                    """
                        Добавление для проверки частных случаев
                    """
                    dict_of_code_planets[name_planet].append(name_planet + 'N' + planets_in_nakshatra_str + 'P' + planet_in_pada_str1 + 'A' + who_aspect)
                    dict_of_ratios_planets[name_planet].append(ratio_s)

            """
                Добавление кодировки только Луны в накшатре
            """
            if name_planet == 'Mo':
                nakshatra_in_parts = math.modf(planet_in_nakshatra)[0]
                dict_of_code_planets[name_planet].append(name_planet + 'N' + planets_in_nakshatra_str)
                if .33 <= nakshatra_in_parts <= .67:
                    dict_of_ratios_planets[name_planet].append(1.0)
                else:
                    planet_in_nak_str2 = verify_str(str(int(math.fmod(int(planet_in_nakshatra) + verify_part(part=nakshatra_in_parts) + 27, 27))))
                    refused_dict(part=nakshatra_in_parts, name_1=name_planet, in_str2=planet_in_nak_str2,
                                 name_col='planet_in_nakshatra', vratio=vratio)

    return dict_of_code_planets, dict_of_ratios_planets


def decode_planets_code(dict_of_codes=None, dict_of_ratios=None):

    result_dict_words = {}
    result_dict_ratios = {}
    for name_planet in nak_nam_pl:
        result_dict_words.update({name_planet: []})
        result_dict_ratios.update({name_planet: []})

        for codes_planet, ratios_planet in zip(dict_of_codes[name_planet], dict_of_ratios[name_planet]):
            if codes_planet in data_of_dict.keys():
                for indexes_code in np.array(np.nonzero(data_of_dict[codes_planet])).tolist()[0]:
                    result_dict_words[name_planet].append(data_of_dict['Name'][indexes_code])
                    result_dict_ratios[name_planet].append(ratios_planet)

    """
        Собираем все качества в один массив суммируя при этом все коэффициенты
    """
    dict_unique_words = {}
    for name_planet in nak_nam_pl:
        for dict_words, dict_ratios in zip(result_dict_words[name_planet], result_dict_ratios[name_planet]):
            if dict_words in dict_unique_words.keys():
                dict_unique_words[dict_words]['Sum'] += dict_ratios

                if name_planet in dict_unique_words[dict_words].keys():
                    dict_unique_words[dict_words][name_planet] += dict_ratios
                else:
                    dict_unique_words[dict_words].update({name_planet: dict_ratios})
            else:
                dict_unique_words.update({dict_words: {'Sum': dict_ratios, name_planet: dict_ratios}})

    """
        Сортировка данных словарей внутри главного словаря и приведение к процентному виду
    """
    dict_unique_words_per = {}
    for unique_words in dict_unique_words.keys():
        dict_unique_words_per.update({unique_words: {'Sum': np.round(dict_unique_words[unique_words]['Sum'], 4)}})
        list_ratio = []
        for word in dict_unique_words[unique_words].keys():
            if word != 'Sum': list_ratio.append(dict_unique_words[unique_words][word])

        new_sum = 0

        for value in sorted(list_ratio)[::-1]:

            for words_value in dict_unique_words[unique_words].keys():
                if (value == dict_unique_words[unique_words][words_value] and
                    words_value not in dict_unique_words_per[unique_words].keys() and
                    dict_unique_words[unique_words]['Sum'] > 0 and
                    value > 0):

                    if dict_unique_words[unique_words]['Sum'] > 1: koef1 = 1
                    else: koef1 = dict_unique_words[unique_words]['Sum']

                    if len(dict_unique_words[unique_words]) > 4: koef2 = 1
                    else: koef2 = .25 * (len(dict_unique_words[unique_words]) - 1)

                    adding = round(value / dict_unique_words[unique_words]['Sum'] * 100 * koef1 * koef2, 2)
                    new_sum += adding

                    dict_unique_words_per[unique_words].update({words_value: adding})

        # Пересчет суммы
        dict_unique_words_per[unique_words]['Sum'] = round(new_sum, 2)

    """
        Сортировка словаря
    """
    dict_unique_words_sorted = {}
    sorted_values = []
    for dict_values in dict_unique_words_per.values():
        sorted_values.append(dict_values['Sum'])

    for value in sorted(sorted_values)[::-1]:
        for unique_words in dict_unique_words_per.keys():

            if value == dict_unique_words_per[unique_words]['Sum'] and unique_words not in dict_unique_words_sorted.keys() and dict_unique_words_per[unique_words]['Sum'] >= 1:
                dict_unique_words_sorted.update({unique_words: dict_unique_words_per[unique_words]})

    # """
    #     Вывод результатов в консоль
    # """
    # for dict_unique_word_sorted in dict_unique_words_sorted.keys():
    #     print(dict_unique_word_sorted, dict_unique_words_sorted[dict_unique_word_sorted])

    return dict_unique_words_sorted
