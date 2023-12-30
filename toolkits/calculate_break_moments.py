from datetime import datetime
from datetime import timedelta
import numpy as np

import calculateTranzitMap
from constants import FORMAT_DATE
from data_etalons.data_slepok import slepok_breaks
from toolkits.calculate_parameters import calc_param_date


def analis_break_data(dict_params=None, dict_results=None):

    for dict_param in dict_params.keys():

        col_list = dict_param.split('.')

        if col_list[0] in ['Su', 'Mo'] and col_list[-1] == 'speed':
            d_lst = dict_params[dict_param]
            d_lst_new = []

            for n1, n2 in zip(d_lst[1:], d_lst[:-1]):
                if n1 > n2:
                    d_lst_new.append(0)
                else:
                    d_lst_new.append(1)

            d_lst_new.append(d_lst_new[-1])
            dict_params[dict_param] = d_lst_new

        if col_list[-1] in ['connect', 'aspect']:
            d_lst = dict_params[dict_param]
            d_lst_new = []

            for n1 in d_lst:
                if n1 is None:
                    d_lst_new.append(0)
                else:
                    d_lst_new.append(1)

            dict_params[dict_param] = d_lst_new

        result_p = int(len(np.unique(dict_params[dict_param])) != 1)

        if dict_param not in dict_results.keys():
            dict_results.update({dict_param: [result_p]})
        else:
            dict_results[dict_param].append(result_p)

    return dict_results


def get_filter_data(dict_data=None):
    """
        Фильтрация данных для приведения специальных условий
    """
    if dict_data['Mo.speed'] == [0]: dict_data['Mo.phase'] = [0]

    return dict_data


def get_break_data_analis(data_break_moments: list, delta=0):
    dict_results = {}

    for data_break in data_break_moments:

        new_date_st, new_date_fn = data_break, data_break

        new_date_start = datetime.strptime(new_date_st, FORMAT_DATE)
        new_date_finish = datetime.strptime(new_date_fn, FORMAT_DATE)

        new_date_start = new_date_start + timedelta(days=-2)
        new_date_finish = new_date_finish + timedelta(days=2)

        delta_period = (new_date_finish - new_date_start).days

        if delta_period < 0:
            delta_period = -delta_period
            new_date_start, new_date_finish = new_date_finish, new_date_start

        dict_params = {}

        for n_days in range(delta_period):

            new_date_tranzit = new_date_start + timedelta(days=n_days)
            new_date_tranzit = new_date_tranzit.strftime(FORMAT_DATE)

            planet_in_tranzit = calculateTranzitMap.calculate_tranzit_map(new_date_tranzit, "01.01.0001", '00:00:00', delta=delta)
            graha_in_degrees_aspects = planet_in_tranzit.graha_in_degrees_transit

            graha_in_degrees = planet_in_tranzit.graha_in_degrees
            graha_speed = planet_in_tranzit.graha_speed

            retrograd_planet = planet_in_tranzit.graha_in_retrograd

            planet_in_znak = np.asarray(np.asarray(graha_in_degrees) / 108000, dtype='int8')

            """
                planet_in_znak, graha_speed, graha_in_degrees, graha_in_retrograd, graha_in_degrees_aspects
            """
            dict_params = calc_param_date(dict_params=dict_params, planet_in_znak=planet_in_znak,
                            graha_speed=graha_speed, graha_in_degrees_aspects=graha_in_degrees_aspects,
                            graha_in_degrees=graha_in_degrees, retrograd_planet=retrograd_planet, not_class=True)

        """
            Поправка на скорость для Солнца и Луны и соединений с аспектами
        """
        dict_results = analis_break_data(dict_params=dict_params, dict_results=dict_results)

        dict_results = get_filter_data(dict_data=dict_results)

    return dict_results


def get_break_moments(data_break_moments: list, delta=0):

    dict_results = get_break_data_analis(data_break_moments=data_break_moments, delta=delta)

    data_value = []
    for dict_result in dict_results.keys():
        all_len = len(dict_results[dict_result])
        data_value.append(round(sum(dict_results[dict_result])/all_len*100, 1))
        dict_results[dict_result] = data_value[-1]

    all_results = {}
    slepok_break = []
    for value_ in sorted(data_value)[::-1][:15]:
        for dict_result in dict_results.keys():

            if value_ == dict_results[dict_result] and dict_result not in all_results.keys():
                slepok_break.append(dict_result)
                all_results.update({dict_result: value_})


    print(str(all_results))


def get_break_recomendation(data_slepok=slepok_breaks, data_dict=None):

    score = 0

    for data_slep in data_slepok:

        if data_slep in data_dict.keys():

            score += data_dict[data_slep][0]

    return score
