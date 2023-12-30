import csv

DASHAS_DATA = 'resources/tableOfKalaChakraDashes.csv'

DAY_NUMBER_INDEX = 0
DASH_RASHI_INDEX = 1


def get_kala_dasha_data():
    """
        Возвращает словарь с данными о координатах планет и поправках
    :return: словарь с данными о координатах планет и поправках
    """

    # инициализируем объект с данными периодах раши
    dict_of_dashas = dict()

    with open(DASHAS_DATA) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            dasha_date = int(row[DAY_NUMBER_INDEX])

            # проверяем есть ли дата в массиве dict_dashas, если нет то добавляем
            if dasha_date not in dict_of_dashas:
                dict_of_dashas[dasha_date] = UpravPlanetDate(dasha_date,
                                                             int(row[DASH_RASHI_INDEX]))
    return dict_of_dashas


def get_kala_dasha_rashi(dasha_new):
    """
        Возвращает список дат и позиций планет

        :param dict_dashas_new: данные о влиянии периодов накшатр
        :return: список влияния накшатр (раши)
    """
    return list(dasha_new.keys())


class UpravPlanetDate:
    """
        Класс с данными о периодах накшатр
    """

    def __init__(self, day_up_kala, maha_d_kala):
        """
            Конструктор иницилизирует поля класса

            :param day_up_kala: день влияния даш
            :param maha_d_kala: даша раши
            :param antar_d_kala: антардаша раши
            :param pratia_d_kala: пратьядаша раши
            :param sykshm_d_kala: сукшмадаша раши
        """
        self.day_up_kala = day_up_kala
        self.maha_d_kala = maha_d_kala

