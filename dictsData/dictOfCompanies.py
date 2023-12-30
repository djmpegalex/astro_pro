import csv

COMPANIES_DATA = 'resources/DatesRegCompany19602030.csv'

COMPANY_NAME_INDEX = 0
COMPANY_SET_UP_DATE_INDEX = 1
COMPANY_LATITUDE_INDEX = 2
COMPANY_LONGITUDE_INDEX = 3
COMPANY_GMT_INDEX = 4
COMPANY_SET_UP_TIME_INDEX = 5
COMPANY_GRAPHIC_INDEX = 6

def get_companies_data():
    """
        Возвращает словарь с данными о компаниях
    :return: словарь с данными о компаниях
    """

    # инициализируем объект с данными о компаниях
    companies_data = dict()

    with open(COMPANIES_DATA) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            company_name = str(row[COMPANY_NAME_INDEX])

            # проверяем есть ли компания в массиве companies_data, если нет то добавляем
            if company_name not in companies_data:
                companies_data[company_name] = CompanyData(company_name,
                                                           str(row[COMPANY_SET_UP_DATE_INDEX]),
                                                           str(row[COMPANY_LONGITUDE_INDEX]),
                                                           str(row[COMPANY_LATITUDE_INDEX]),
                                                           str(row[COMPANY_GMT_INDEX]),
                                                           str(row[COMPANY_SET_UP_TIME_INDEX]),
                                                           str(row[COMPANY_GRAPHIC_INDEX]))
    return companies_data


def get_companies_names(companies_data):
    """
        Возвращает список наименований компаний

        :param companies_data: данные о компаниях
        :return: список наименований компаний
    """
    return list(companies_data.keys())


class CompanyData:
    """
        Класс с данными о компании
    """

    def __init__(self, company_name, set_up_date, longitude, latitude, gmt, set_up_time, graphic):
        """
            Конструктор иницилизирует поля класса

            :param company_name: наименование компании
            :param set_up_date: дата основания
            :param longitude: широта
            :param latitude: долгота
            :param gmt: относитлеьное время по гринвичу
            :param set_up_time: время основания
        """
        self.company_name = company_name
        self.set_up_date = set_up_date
        self.longitude = longitude
        self.latitude = latitude
        self.gmt = gmt
        self.set_up_time = set_up_time
        self.graphic = graphic