import csv

ZNAK_DATA = 'resources/planetsInZnake.csv'

ZNAK_NUMBER_PLANET_INDEX = 0
ZNAK_SUN_INDEX = 1
ZNAK_MOON_INDEX = 2
ZNAK_MARS_INDEX = 3
ZNAK_MERCURY_INDEX = 4
ZNAK_JUPITER_INDEX = 5
ZNAK_VENERA_INDEX = 6
ZNAK_SATURN_INDEX = 7

def get_planet_in_znak():
    """
        Возвращает словарь с данными о коэффициентах силы планет в позициях знаков
    :return: словарь с данными о коэффициентах силы планет в знаках
    """

    # инициализируем объект с данными коэффициентах
    planet_in_znak = dict()

    with open(ZNAK_DATA) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            number_of_planet = int(row[ZNAK_NUMBER_PLANET_INDEX])

            # проверяем есть ли дата в массиве planet_in_znak, если нет то добавляем
            if number_of_planet not in planet_in_znak:
                planet_in_znak[number_of_planet] = planet_data(number_of_planet,
                                                               float(row[ZNAK_SUN_INDEX]),
                                                               float(row[ZNAK_MOON_INDEX]),
                                                               float(row[ZNAK_MARS_INDEX]),
                                                               float(row[ZNAK_MERCURY_INDEX]),
                                                               float(row[ZNAK_JUPITER_INDEX]),
                                                               float(row[ZNAK_VENERA_INDEX]),
                                                               float(row[ZNAK_SATURN_INDEX]))
    return planet_in_znak


def get_planet_data(data_from_planet):
    """
        Возвращает список планет

        :param data_from_planet: данные о коэффициентах планет по знакам
        :return: список данных коэффициентов планет
    """
    return list(data_from_planet.keys())


class planet_data:
    """
        Класс с данными о коэффициентах планет
    """

    def __init__(self, znak_up, ratio_sun, ratio_moon, ratio_mars, ratio_mercury, ratio_jupiter, ratio_venus, ratio_saturn):
        """
            Конструктор иницилизирует поля класса

            :param znak_up: знак, нахождение планеты в котором, дает коэффициенты этой планете
            :param ratio_sun: коэффициент силы солнца
            :param ratio_moon: коэффициент силы луны
            :param ratio_mars: коэффициент силы марса
            :param ratio_mercury: коэффициент силы меркурия
            :param ratio_jupiter: коэффициент силы юпитера
            :param ratio_venus: коэффициент силы венеры
            :param ratio_saturn: коэффициент силы сатурна
        """
        self.znak_up = znak_up
        self.ratio_sun = ratio_sun
        self.ratio_moon = ratio_moon
        self.ratio_mars = ratio_mars
        self.ratio_mercury = ratio_mercury
        self.ratio_jupiter = ratio_jupiter
        self.ratio_venus = ratio_venus
        self.ratio_saturn = ratio_saturn
