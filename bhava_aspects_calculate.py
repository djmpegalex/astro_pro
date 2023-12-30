import numpy as np
from constants import *

def bhava_aspec(graha_in_degrees, polojenie_lagna_rashi, retrogr_planet):
    """
        params:
        graha_in_degrees - данные о пложении планет в карте (в угловых секундах) 0 - 1296000
        polojenie_lagna_rashi - положение лагны в знаке
        retrogr_planet - данные о ретроградности планет

        return:
        данные об аспектах каждой из планет в угловых градусах 0 - 360
    """
    graha_in_degrees_rashi_as = list(
        map(lambda x: int(np.fmod(x / 3600 - (polojenie_lagna_rashi * 30) + 360, 360)), graha_in_degrees))

    bhava_aspects_rashi = list(map(lambda x: 0, np.arange(63)))

    for n in PLANETS_RANGE:
        poz = int(n * 7)

        bhava_aspects_rashi[poz] = graha_in_degrees_rashi_as[n]
        bhava_aspects_rashi[poz + 1] = np.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3] * 30), 360)
        bhava_aspects_rashi[poz + 2] = np.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3 + 1] * 30), 360)
        bhava_aspects_rashi[poz + 3] = np.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3 + 2] * 30), 360)

        if retrogr_planet[n] == 1:
            bhava_aspects_rashi[poz + 4] = np.fmod((graha_in_degrees_rashi_as[n] + (DPLA[n * 3] - 1) * 30), 360)
            bhava_aspects_rashi[poz + 5] = np.fmod((graha_in_degrees_rashi_as[n] + (DPLA[n * 3 + 1] - 1) * 30), 360)
            bhava_aspects_rashi[poz + 6] = np.fmod((graha_in_degrees_rashi_as[n] + (DPLA[n * 3 + 2] - 1) * 30), 360)
        else:
            bhava_aspects_rashi[poz + 4] = np.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3] * 30), 360)
            bhava_aspects_rashi[poz + 5] = np.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3 + 1] * 30), 360)
            bhava_aspects_rashi[poz + 6] = np.fmod((graha_in_degrees_rashi_as[n] + DPLA[n * 3 + 2] * 30), 360)

    return bhava_aspects_rashi