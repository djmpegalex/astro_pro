import csv

# COST_COMPANIES_DATA = 'resources/tableSNP500.csv'
COST_COMPANIES_DATA = 'resources/SNP500_VTBR.csv'

COMPANY_DATE_INDEX = 0
COMPANY_SNP500 = 1

def get_companies_data():
    """
        Возвращает словарь с данными о росте цены компании
    :return: словарь с данными о росте компаний
    """

    # инициализируем объект с данными
    cost_companies_data = dict()

    with open(COST_COMPANIES_DATA) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            company_name = str(row[COMPANY_DATE_INDEX])

            # проверяем есть ли компания в массиве cost_companies_data, если нет то добавляем
            if company_name not in cost_companies_data:
                cost_companies_data[company_name] = CompanyData(company_name,
                                                                str(row[COMPANY_SNP500]))
    return cost_companies_data


def get_date_dynamics(companies_data):
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

    def __init__(self, date_company_cost, snp500):
        """
            Конструктор иницилизирует поля класса

            :param company_name: наименование компании

        """
        self.date_company_cost = date_company_cost
        self.snp500 = snp500
