from constants import *


def calc_level_up_Sa_Ju(mahadasha: int = None, antardasha: int = None, pratiadasha: int = None,
                        menegers_bhavas: list = None,
                        planets_in_degrees_horoscop: list = None, planets_in_retrogard_horoscop: list = None,
                        planets_in_degrees_transit: list = None, planets_in_retrogard_transit: list = None,
                        lagna_bhava: int = None, bhavas: list= None):
    """
        Функция для посчета времени карьерного взлета (в бедущем можно так анализировать все бхавы гороскопа)
    :param mahadasha: планета-хозяин данной махадаши
    :param antardasha: планета-хозяин данной антардаши
    :param menegers_bhavas: лист управителей бхав для данного гороскопа
    :param planets_in_degrees_horoscop: расположение планет в гороскопе в угловых секундах
    :param planets_in_degrees_transit: расположение планет в транзитах в угловых секундах
    :param planets_in_retrogard_transit: состояние прямого/обратного движения планет в транзитах: 0-прямое, 1-обратное
    :param lagna_bhava: расположение лагны в гороскопе (знак)
    :return:
    """
    planets_in_znak_horoscop = [int(n / SECONDS_IN_ZNAK) for n in planets_in_degrees_horoscop]
    planets_in_house_horoscop = [int(np.fmod(planets_in_znak_horoscop[planet] - lagna_bhava + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK)) for
                        planet in PLANETS_RANGE]

    planets_in_znak_transit = [int(n / SECONDS_IN_ZNAK) for n in planets_in_degrees_transit]
    planets_in_house_transit_moon = [int(np.fmod(planets_in_znak_transit[planet] - planets_in_znak_horoscop[MOON_PLANET_NUMBER] + \
                                            ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK)) for planet in PLANETS_RANGE]
    planets_in_house_transit_lagna = [int(np.fmod(planets_in_znak_transit[planet] - lagna_bhava + \
                                            ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK)) for planet in PLANETS_RANGE]

    parametrs_aspects_planets_to_bhava_in_horoscop = {}
    parametrs_aspects_planets_to_bhava_in_transit_moon = {}
    parametrs_aspects_planets_to_bhava_in_transit_lagna = {}

    """
        Анализ самого гороскопа
    """
    for planet in PLANETS_RANGE:
        parametrs_aspects_planets_to_bhava_in_horoscop.update({planet: []})
        """
            Указываем какие дома аспектируют планеты в гороскопе
        """
        for aspect in ASPECTS_FOR_YOGA[planet]:
            retrograd = int(planets_in_retrogard_horoscop[planet] == 1)
            if aspect == 0: retrograd = 0
            aspect_on_bhava = int(np.fmod(aspect + planets_in_house_horoscop[planet] - retrograd + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK))
            parametrs_aspects_planets_to_bhava_in_horoscop[planet].append(aspect_on_bhava)

    """
        Анализ транзитов от Луны
    """
    for planet in PLANETS_RANGE:
        parametrs_aspects_planets_to_bhava_in_transit_moon.update({planet: []})
        """
            Указываем какие дома аспектируют планеты в транзитах
        """
        for aspect in ASPECTS_FOR_YOGA[planet]:
            retrograd = int(planets_in_retrogard_transit[planet] == 1)
            if aspect == 0: retrograd = 0
            aspect_on_bhava = int(
                np.fmod(aspect + planets_in_house_transit_moon[planet] - retrograd + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK))
            parametrs_aspects_planets_to_bhava_in_transit_moon[planet].append(aspect_on_bhava)

    """
        Анализ транзитов от Лагны
    """
    for planet in PLANETS_RANGE:
        parametrs_aspects_planets_to_bhava_in_transit_lagna.update({planet: []})
        """
            Указываем какие дома аспектируют планеты в транзитах
        """
        for aspect in ASPECTS_FOR_YOGA[planet]:
            retrograd = int(planets_in_retrogard_transit[planet] == 1)
            if aspect == 0: retrograd = 0
            aspect_on_bhava = int(
                np.fmod(aspect + planets_in_house_transit_lagna[planet] - retrograd + ZNAKS_IN_ZODIAK, ZNAKS_IN_ZODIAK))
            parametrs_aspects_planets_to_bhava_in_transit_lagna[planet].append(aspect_on_bhava)

    results = []
    for house in bhavas:  # перечислим все дома связанные с богатством
        result = 0
        result_sa = 0
        result_ju = 0
        """
            хозяин махадаши, хозяин антардаши аспектирует 10й дом или под аспектом 10го правителя или он и есть 10й правитель
        """
        result += menegers_bhavas[house] == mahadasha
        result += menegers_bhavas[house] == antardasha
        result += menegers_bhavas[house] == pratiadasha

        result += planets_in_house_horoscop[menegers_bhavas[house]] in parametrs_aspects_planets_to_bhava_in_horoscop[mahadasha]
        result += planets_in_house_horoscop[menegers_bhavas[house]] in parametrs_aspects_planets_to_bhava_in_horoscop[antardasha]
        result += planets_in_house_horoscop[menegers_bhavas[house]] in parametrs_aspects_planets_to_bhava_in_horoscop[pratiadasha]

        result += planets_in_house_horoscop[mahadasha] in parametrs_aspects_planets_to_bhava_in_horoscop[menegers_bhavas[house]]
        result += planets_in_house_horoscop[antardasha] in parametrs_aspects_planets_to_bhava_in_horoscop[menegers_bhavas[house]]
        result += planets_in_house_horoscop[pratiadasha] in parametrs_aspects_planets_to_bhava_in_horoscop[menegers_bhavas[house]]

        """
            Транзитные Sa и Ju аспектируют 10й дом от Лагны, 10й дом от Луны, управителя 10го дома, также 5й и 7й и 9й дома
        """
        result_sa += house in parametrs_aspects_planets_to_bhava_in_transit_moon[SATURN_PLANET_NUMBER]
        result_ju += house in parametrs_aspects_planets_to_bhava_in_transit_moon[JUPITER_PLANET_NUMBER]

        result_sa += house in parametrs_aspects_planets_to_bhava_in_transit_lagna[SATURN_PLANET_NUMBER]
        result_ju += house in parametrs_aspects_planets_to_bhava_in_transit_lagna[JUPITER_PLANET_NUMBER]

        result_sa += planets_in_house_transit_moon[menegers_bhavas[house]] in parametrs_aspects_planets_to_bhava_in_transit_moon[SATURN_PLANET_NUMBER]
        result_ju += planets_in_house_transit_moon[menegers_bhavas[house]] in parametrs_aspects_planets_to_bhava_in_transit_moon[JUPITER_PLANET_NUMBER]

        results.append((result + result_sa + result_ju) * ((result_sa > 0) or (result_ju > 0)))
        if max(results) > 11: return 11
    return max(results)