import csv

DASHAS_DATA = 'resources/tableOfDahasChakras.csv'

DAY_NUMBER_INDEX = 0
DASH_UPRAV_INDEX = 1
ANTAR_UPRAV_INDEX = 2
PRATIA_UPRAV_INDEX = 3
SYKSHM_UPRAV_INDEX = 4
DASH_PERCENT_INDEX = 5
ANTAR_PERCENT_INDEX = 6
PRATIA_PERCENT_INDEX = 7


def get_dasha_data():
    """
        Возвращает словарь с данными о координатах планет и поправках
    :return: словарь с данными о координатах планет и поправках
    """

    # инициализируем объект с данными о координатах планет и поправках
    dict_of_dashas = dict()

    with open(DASHAS_DATA) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            dasha_date = int(row[DAY_NUMBER_INDEX])

            # проверяем есть ли дата в массиве dict_dashas, если нет то добавляем
            if dasha_date not in dict_of_dashas:
                dict_of_dashas[dasha_date] = UpravPlanetDate(dasha_date,
                                                             int(row[DASH_UPRAV_INDEX]),
                                                             int(row[ANTAR_UPRAV_INDEX]),
                                                             int(row[PRATIA_UPRAV_INDEX]),
                                                             int(row[SYKSHM_UPRAV_INDEX]),
                                                             float(row[DASH_PERCENT_INDEX]),
                                                             float(row[ANTAR_PERCENT_INDEX]),
                                                             float(row[PRATIA_PERCENT_INDEX]))
    return dict_of_dashas


def get_dasha_uprav(dasha_new):
    """
        Возвращает список дат и позиций планет

        :param dict_dashas_new: данные о датах и позиций планет
        :return: список данных координат планет и поправок
    """
    return list(dasha_new.keys())


class UpravPlanetDate:
    """
        Класс с данными о планетах
    """

    def __init__(self, day_up, maha_d, antar_d, pratia_d, sykshm_d, maha_per, antar_per, pratia_per):
        """
            Конструктор иницилизирует поля класса

            :param day_up:
            :param maha_d:
            :param antar_d:
            :param pratia_d:
            :param sykshm_d:
            :param maha_per:
            :param antar_per:
            :param pratia_per:
        """
        self.day_up = day_up
        self.maha_d = maha_d
        self.antar_d = antar_d
        self.pratia_d = pratia_d
        self.sykshm_d = sykshm_d

        self.maha_per = maha_per
        self.antar_per = antar_per
        self.pratia_per = pratia_per

