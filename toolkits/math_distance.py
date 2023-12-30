from constants import SECONDS_IN_HALF_ZODIAC, SECONDS_IN_ZODIAC
import numpy as np

def dist_in_degrees(M=None, S=None, absp=True):
    """
    Инструмент позволяющий вычислить расстояние между двумя планетами в секундах
    :param S second: угловые секунды планеты 2
    :param M main: угловые секунды планеты 1
    :param not_abs: флаг для уточнения абсолютности расстояний.
    Если True, то расстояния будут считаться без учета последовательности расположения планет
    Если False - расстояния будут вычислены с учетом главной main планеты
    :return: угловое расстояние моежду 2мя планетами в секундах
    """

    dist = M - S
    if absp:
        dist = abs(dist)
        if dist>SECONDS_IN_HALF_ZODIAC: dist = SECONDS_IN_ZODIAC - dist
    else:
        if dist < 0: dist = S - M
        else: dist = SECONDS_IN_ZODIAC - M + S

    return dist

def sum_in_degrees(M=None, S=None):
    """
    Инструмент получения кшетры-спхуты, сложения угловых координа двух планет
    :param M:
    :param S:
    :return: угловая координата кшетра-спхуты двух планет
    """

    kshetra_sphuta = M+S
    if kshetra_sphuta > SECONDS_IN_ZODIAC:
        kshetra_sphuta -= SECONDS_IN_ZODIAC

    return kshetra_sphuta

def diagramms_counts(list_for_counts: list):

    list_count = []
    dict_count = {}
    list_unique = np.unique(list_for_counts)

    for uniq_counts in list_unique:

        while len(list_count) < uniq_counts:
            list_count.append(0)

        list_count.append(list_for_counts.count(uniq_counts))

    dict_count.update({'counts': list_count})

    list_count = np.array(list_count)

    norm_into_group = np.asarray((list_count * (100 / np.max(list_count))), dtype='int32').tolist()
    # for n_group, norm_into in enumerate(norm_into_group):
    #     if norm_into < 50: norm_into_group[n_group] = 0

    dict_count.update({'norm_into_group': norm_into_group, 'last_data': list_for_counts})

    return dict_count