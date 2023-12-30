import math
from constants import *
import numpy as np

power_code_of_day = [0, 60, 0, 60, 30, 60, 0, 30, 60]
power_moon_day = [60, 0, 0, 60, 0, 60, 15, 60, 15]

FUNC_VALUES = [9, 0, 0, 0, 0, 1, 2, 4, 7, 9]


def func_values(part_code_day):
    ratio_part_code = FUNC_VALUES[math.trunc(part_code_day * 10)]

    return ratio_part_code


def get_code_of_day(graha_in_degrees, bad_nakshatras, jam_nakshatra):
    strenght_day = 0

    moon_in_nakshatra = graha_in_degrees[MOON_PLANET_NUMBER] / SECONDS_IN_NAKSHATRA

    """
        подсчет группы накшатры относительно положения луны
    """
    code_day = math.fmod((jam_nakshatra + moon_in_nakshatra), NUMBER_OF_PLANETS)
    whole_code_day = int(math.trunc(code_day))
    part_code_day = code_day - whole_code_day
    strenght_day += power_code_of_day[whole_code_day] * (1 - func_values(part_code_day)) + \
                    power_code_of_day[int(math.fmod((whole_code_day + 1), 9))] * func_values(part_code_day)

    """
        подсчет неблагоприятного положения луны в накшатрах
    """
    for i in np.arange(len(bad_nakshatras)):
        if abs(bad_nakshatras[i] - moon_in_nakshatra) <= 0.5:
            strenght_day -= 60 * (1 - abs(bad_nakshatras[i] - moon_in_nakshatra))

    return strenght_day

def code_moon_day(graha_in_degrees, dayweek):
    strenght_day = 0
    moon_in_nakshatra = graha_in_degrees[MOON_PLANET_NUMBER] / SECONDS_IN_NAKSHATRA
    """
        подсчет нумералогического кода дня
    """
    # номер лунного дня
    moon_day_degrees = math.fmod((DEGREES_IN_ZODIAK +
                         ((graha_in_degrees[SUN_PLANET_NUMBER] - graha_in_degrees[MOON_PLANET_NUMBER]) / SECONDS_IN_ZNAK)),
                         DEGREES_IN_ZODIAK)
    moon_day = int(math.fmod(moon_day_degrees / 12, 15))

    moon_nakshatra = int(math.trunc(moon_in_nakshatra))

    moon_in_znak = int(math.trunc(graha_in_degrees[MOON_PLANET_NUMBER] / SECONDS_IN_ZNAK))

    moon_weekday = int(math.trunc(math.fmod((dayweek + 6), 7)))

    strenght_day += power_moon_day[int(math.trunc(math.fmod((moon_day + moon_nakshatra +
                                                             moon_in_znak + moon_weekday), NUMBER_OF_PLANETS)))]

    return strenght_day