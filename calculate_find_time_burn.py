import beginScript
import math
import numpy as np

def a_delemit_b(a, b):
    if a >= b:
        num_of_matches = (b / a)
    else:
        num_of_matches = (a / b)

    return num_of_matches

def get_time_find(date_but, stat_periods, stat_value, date_f, time_f, txtGTM, txtAltitude, txtLongitude):
    mass_o = int(len(stat_value))

    txt_lastDate = date_but[0]
    txt_nextDate = date_but[7]

    new_command = "ANALIS"
    array_prognozPlanet = beginScript.prognoz_inTime(new_command, date_f, time_f,
                                                     txtGTM, txtAltitude,
                                                     txtLongitude, txt_lastDate,
                                                     txt_nextDate, "dasha",
                                                     "all weekdays")

    astro_periods = array_prognozPlanet.new_period

    """
        проверка на совпадаемость длины планетных периодов, отбор периодов по длине
    """
    num_of_matches = int((a_delemit_b(sum(astro_periods), sum(stat_periods))) * 100)

    """
        отсеивание периодов по совпадаемости каждого отрезка времени
    """
    if num_of_matches > 50:
        # index = 0
        # new_ast_period = []
        # new_stat_value = []
        # n = 0
        #
        # len_stat_periods = len(stat_periods)
        # len_astro_periods = len(astro_periods)
        #
        # if len_stat_periods >= len_astro_periods:
        #     while index < len_astro_periods:
        #         add_periods = [0]
        #         new_stat_value.append(stat_value[n])
        #         while abs(sum(add_periods) - astro_periods[index]) > 10:
        #             add_periods.append(stat_periods[n])
        #             n += 1
        #
        #             if n == (len_stat_periods - 1): break
        #
        #         new_ast_period.append(sum(add_periods))
        #
        #         if n == (len_stat_periods - 1): break
        #         index += 1
        #     last_ast_period = astro_periods
        # else:
        #     while index < len_stat_periods:
        #         add_periods = [0]
        #         while abs(sum(add_periods) - stat_periods[index]) > 10:
        #             add_periods.append(astro_periods[n])
        #             n += 1
        #             if n == (len_stat_periods - 1): break
        #
        #         new_ast_period.append(sum(add_periods))
        #         if n == (len_stat_periods - 1): break
        #         index += 1
        #     last_ast_period = stat_periods
        # """
        #     отсеивание выборок по равной длине и анализ соответствий рядов
        # """
        #
        # if len(new_ast_period) == len(last_ast_period):
        #
        #     num_of_matches = int(a_delemit_b(sum(new_ast_period), sum(last_ast_period)) * 100)
        #
        #     if num_of_matches > 90:
        #         for index in np.arange(len(last_ast_period)):
        #             a = new_ast_period[index]
        #             b = last_ast_period[index]
        #
        #             num_of_matches += a_delemit_b(a, b)
        #
        #         num_of_matches = int(num_of_matches / float(len(last_ast_period) - 1) * 100)
        #
        #         """
        #             отсеивание выборки по установленным и подсчитанным значениям
        #         """
        #         if num_of_matches > 95:


        num_of_matches = 0
        array_value_dashes = beginScript.prognoz_inTime(new_command, date_f, time_f,
                                                         txtGTM, txtAltitude,
                                                         txtLongitude, txt_lastDate,
                                                         txt_nextDate, "dasha",
                                                         "all weekdays")

        astro_periods = array_value_dashes.new_period
        astro_value = array_value_dashes.new_value_of_period

        """
            получение встречного ряда значений
        """
        for i in np.arange(mass_o):
            if astro_value[i] == stat_value[i]:
                num_of_matches += a_delemit_b(stat_periods[i], astro_periods[i])

        num_of_matches = (int(num_of_matches / mass_o * 100))

        #         else:
        #             num_of_matches = 0
        #     else:
        #         num_of_matches = 0
        # else:
        #     num_of_matches = 0
    else:
        num_of_matches = 0

    return num_of_matches
