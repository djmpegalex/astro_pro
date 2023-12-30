import numpy as np

def get_karakas(planets_in_degrees=None):
    """
        planets_in_degrees - угловые градусы от 0 до 1296000 секунд

        return:
        сортированный список по планетам: Атма карака, Аматья карака, Бхрата карака и т.д.
        [0, 2, 5, 3, 1, 4, 6] вывод
        [Солнце, Марс, Венера, Меркурий, Луна, Юпитер, Сатурн] означает
        [АК, АмК, БК, МК, ПК, ГК, ДК] подразумевается
    """

    result = np.asarray(np.fmod(np.array(planets_in_degrees[0:7]), 108000), dtype='int32').tolist()

    result_sorts = np.sort(result)[::-1]

    karakas = []

    for result_sort in result_sorts:
        karakas.append(result.index(result_sort))

    return karakas