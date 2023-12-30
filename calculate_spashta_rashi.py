import numpy as np
import pandas as pd

def calc_spashta(ltd_degr):
    """
    :param ltd_degr: широта рождения в градусах с дробным числом
    :return: спашты (долготы) начала для каждого знака (список)
    """
    ltd_degr_int = int(ltd_degr)
    part = ltd_degr - ltd_degr_int

    data_spasha = pd.read_csv("resources/tableOfSpashta.csv", sep=";")
    data_spasha.columns = np.arange(67)

    data_spasha_last = np.asarray(data_spasha[ltd_degr_int].tolist())
    data_spasha_next = np.asarray(data_spasha[ltd_degr_int+1].tolist())

    angles = data_spasha_last + (data_spasha_next - data_spasha_last) * part

    return np.concatenate([angles[-3:], angles[0:-3]])


def calc_spashta_planets(spashta_rashi, graha_in_degrees):
    """

    :param spashta_rashi: Угловые секунды начала каждогого раши
    :param graha_in_degrees: Положение планет в угловых секундах
    :return: locate_planets_in_spashta - список углов спашт, где расположены планеты
            planets_in_spashta - расположение планеты в спаште
    """
    spashta_rashi = np.concatenate([spashta_rashi, [spashta_rashi[0]]])
    locate_planets_in_spashta = []
    planets_in_spashta = []

    for graha in graha_in_degrees:
        for spashta_number, (spashta_last, spashta_next) in enumerate(zip(spashta_rashi[0:-1], spashta_rashi[1:])):
            if spashta_next == 0: spashta_next = 1296000
            if (graha >= spashta_last) and (graha < spashta_next):
                locate_planets_in_spashta.append(spashta_last)
                planets_in_spashta.append(spashta_number)
                break

    return locate_planets_in_spashta, planets_in_spashta
