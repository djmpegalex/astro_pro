import pandas as pd
import numpy as np

df = pd.read_csv("resources/tableOfPlacidus.csv", sep=";")

def asc_calculate(sun_rise_degrees, sun_rise_seconds, born_of_seconds, alt_in):

    part_degrees = alt_in - int(alt_in)
    """
        проверка значения широты на предел
    """
    if alt_in < 0: alt_in = -alt_in
    if alt_in >= 65: alt_in = 64

    alt_inter = [str(int(alt_in)), str(int(alt_in + 1))]

    """
        шаг 1. подсчет сидерического градуса восхода солнца и перевод его в сидерическое время
    """

    if sun_rise_degrees < 0: sun_rise_degrees += 1296000

    degr_inter = [sun_rise_degrees - 50000, sun_rise_degrees + 50000]

    if degr_inter[0] < 0:
        degr_inter[0] = 0
    if degr_inter[1] > 1296000:
        degr_inter[1] = 1296000

    n_fr = [
        (df.loc[(df[alt_inter[0]] >= int(degr_inter[0])) & (df[alt_inter[0]] <= int(degr_inter[1]))][alt_inter[0]].values),
        (df.loc[(df[alt_inter[1]] >= int(degr_inter[0])) & (df[alt_inter[1]] <= int(degr_inter[1]))][alt_inter[1]].values)]

    """
        из всей выборки находим два числа, между которым находится наше значение долготы солнца
    """
    new_variants = []
    m = 0
    lim = np.min([len(n_fr[0]), len(n_fr[1])])
    while m < 2:
        for n in np.arange(lim):
            if n_fr[m][n] <= sun_rise_degrees:
                n += 1
                if n > 11: n = 11
            else:
                break

        new_variants.extend((n_fr[m][n - 1], n_fr[m][n]))

        m += 1

    """
        шаг 2.получаем значение индексов соответствующих нижних значений
    """

    n_time = [df.loc[(df[alt_inter[0]] == int(new_variants[0]))][alt_inter[0]].index.values,
              df.loc[(df[alt_inter[1]] == int(new_variants[2]))][alt_inter[1]].index.values]

    """
        получаем сидерическое время в момент восхода солнца lagna_rise_time
    """

    lagna_rise_time = (n_time[0] + (n_time[1] - n_time[0]) * part_degrees)

    """
        шаг 3. получим разницу во времени рождения и восхода солнца по местному времени и найдем сидерическое время рождения
    """

    delta_bern = (born_of_seconds - sun_rise_seconds) / 60

    summer_time = 0  # поправка на летнее время. Если переводилось на летнее время, то 60 инече 0

    sid_born = delta_bern + sum(list(lagna_rise_time)) + summer_time
    if sid_born >= 1440: sid_born -= 1440
    if sid_born < 0: sid_born += 1440

    """
        по сидерическому времени рождения "sid_born" найдем положение асцендента в момент рождения
    """

    sid_born_part = sid_born - int(sid_born)

    asc_born = df.loc[[int(sid_born), int(sid_born + 1)], alt_inter]

    asc_born = asc_born.values.tolist()
    asc_born = np.ravel(asc_born)
    """
        шаг 4. выведение положения асцендента в момент рождения
    """

    asc_degrees = (asc_born[0] + (asc_born[2] - asc_born[0]) * part_degrees) + (
                (asc_born[1] + (asc_born[3] - asc_born[1]) * part_degrees) - (
                    asc_born[0] + (asc_born[2] - asc_born[0]) * part_degrees)) * sid_born_part

    return asc_degrees