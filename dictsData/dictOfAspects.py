import csv

DEGREES_DATA = 'resources/tableOfAspectsPlanets.csv'

START_ASPECT_INDEX = 0
END_ASPECT_INDEX = 1
SUN_STRENGHT_INDEX = 2
MOON_STRENGHT_INDEX = 3
MARS_STRENGHT_INDEX = 4
MERCURY_STRENGHT_INDEX = 5
JUPITER_STRENGHT_INDEX = 6
VENUS_STRENGHT_INDEX = 7
SATURN_STRENGHT_INDEX = 8
RAHY_STRENGHT_INDEX = 9
KETY_STRENGHT_INDEX = 10

BREAK_DEGREES_INDEX = 11


def get_aspects_strenght_data():
    """
        Возвращает словарь с данными о силе аспектов
    :return: словарь с данными о аспектах
    """

    # инициализируем объект с данными о баллах аспектов
    aspect_stranght_data = dict()

    with open(DEGREES_DATA) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            aspect_degree = float(row[START_ASPECT_INDEX])

            # проверяем есть градус аспекта в массиве aspect_stranght_data, если нет то добавляем
            if aspect_degree not in aspect_stranght_data:
                aspect_stranght_data[aspect_degree] = AspectFromPlanet(aspect_degree,
                                                                       float(row[END_ASPECT_INDEX]),
                                                                       float(row[SUN_STRENGHT_INDEX]),
                                                                       float(row[MOON_STRENGHT_INDEX]),
                                                                       float(row[MARS_STRENGHT_INDEX]),
                                                                       float(row[MERCURY_STRENGHT_INDEX]),
                                                                       float(row[JUPITER_STRENGHT_INDEX]),
                                                                       float(row[VENUS_STRENGHT_INDEX]),
                                                                       float(row[SATURN_STRENGHT_INDEX]),
                                                                       float(row[RAHY_STRENGHT_INDEX]),
                                                                       float(row[KETY_STRENGHT_INDEX]),
                                                                       float(row[BREAK_DEGREES_INDEX]))
    return aspect_stranght_data


def get_aspects_degrees(aspects_data):
    """
        Возвращает список градусов аспетов

        :param aspects_data: данные о аспектах
        :return: список аспектов поланет
    """
    return list(aspects_data.keys())


class AspectFromPlanet:
    """
        Класс с данными о аспектах
    """

    def __init__(self, start_aspect, end_aspect, sun_strenght, moon_strenght, mars_strenght, mercury_strenght, jupiter_strenght,
                 venus_strenght, saturn_strenght, rahy_strenght, kety_strenght, break_gegrees):
        """
            Конструктор иницилизирует поля класса

            :param company_name: наименование компании
            :param set_up_date: дата основания
            :param longitude: широта
            :param latitude: долгота
            :param gmt: относитлеьное время по гринвичу
            :param set_up_time: время основания
        """
        self.start_aspect = start_aspect
        self.end_aspect = end_aspect
        self.sun_strenght = sun_strenght
        self.moon_strenght = moon_strenght
        self.mars_strenght = mars_strenght
        self.mercury_strenght = mercury_strenght
        self.jupiter_strenght = jupiter_strenght
        self.venus_strenght = venus_strenght
        self.saturn_strenght = saturn_strenght
        self.rahy_strenght = rahy_strenght
        self.kety_strenght = kety_strenght
        self.break_gegrees = break_gegrees
