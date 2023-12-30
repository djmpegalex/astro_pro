from constants import SECONDS_IN_ZNAK, PLANET_UPRAV, PLANETS_RANGE
from numpy import fmod as np_fmod, sum as np_sum, asarray as np_asarray

def calculate_avasths(planets_in_nakshatras, PLANETS_RANGE, planets_in_navamsha,
                      moon_in_nakshatra, delta_bern_rise, polojenie_lagna_rashi):
    """
    :param planets_in_nakshatras: Планеты в накшатрах int array
    :param PLANETS_RANGE: порядковый номер планеты int array
    :param planets_in_navamsha: планеты в знаке навамши int array
    :param moon_in_nakshatra: номер накшатры, в которой расположена Луна int
    :param delta_bern_rise: разница в часах между временем рождения и временем восхода Солнца float
    :param polojenie_lagna_rashi: номер знака, в котором расположена лагна int
    :return: номер авастхи каждой планете, согласно списку LIST_AVASTH_NAME
    """
    delta_bern_rise = int(delta_bern_rise*2.5+.5)

    return np_fmod(
        np_asarray(
            planets_in_nakshatras) * np_asarray(
            PLANETS_RANGE) * np_asarray(
            planets_in_navamsha) + np_asarray(
            moon_in_nakshatra) + np_asarray(
            delta_bern_rise) + np_asarray(
            polojenie_lagna_rashi)+12, 12)


def calculate_rajya_yoga(graha_in_degrees=None):
    """
        Функция, которая вычисляет позиции планет после своих знаков управления и суммырует количество таких случаев
        для данного дня

    """

    graha_in_znaks = np_asarray(np_asarray(graha_in_degrees) / SECONDS_IN_ZNAK, dtype='int32')
    scores = 0

    for planet in PLANETS_RANGE:

        graha_in_znak = graha_in_znaks[planet]

        # Каким знаком управляет планета
        for planet_in_znak in PLANET_UPRAV[planet]:

            if np_fmod(graha_in_znak - planet_in_znak + 12, 12) == 1:
                scores += 1

    return scores