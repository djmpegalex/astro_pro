from datetime import datetime
from datetime import timedelta
import numpy as np

from data_etalons.data_slepok import result as resulter_oil
import calculateTranzitMap
from constants import *
from toolkits.math_distance import dist_in_degrees, diagramms_counts

actual_aspects = [[0,1], [0,1], [0,1,2,3], [0,1], [0,1,2,3], [0,1], [0,1,2,3], [0,1,2,3], [0,1,2,3]]


def calc_param_date(dict_params: dict, planet_in_znak=None, graha_speed=None,
                    graha_in_degrees_aspects=None, graha_in_degrees=None, retrograd_planet=None, not_class=False):

    graha_in_navamsha = np.array(np.fmod(np.array(graha_in_degrees[0:9]) / 12000, 9), dtype='int32').tolist()

    # Фазы планет
    for plane in PHASE_PLANETS:
        for planet_ph in range(1, 8):
            dist_M = dist_in_degrees(M=graha_in_degrees[plane],
                                     S=graha_in_degrees[planet_ph], absp=False)
            phase_ = int(dist_M > 648000)

            name_col = nak_nam_pl[planet_ph] + '.phase'

            if name_col not in dict_params.keys():
                dict_params.update({name_col: [phase_]})
            else:
                dict_params[name_col].append(phase_)

    # положение планеты в знаке
    for planet_, planet_znak in enumerate(planet_in_znak[0:9]):
        if planet_ in [1]: continue
        name_col = nak_nam_pl[planet_] + '.inznak'

        if name_col not in dict_params.keys():
            dict_params.update({name_col: [planet_znak]})
        else:
            dict_params[name_col].append(planet_znak)

    # положение планеты в навамше
    for planet_, planet_navamsha in enumerate(graha_in_navamsha):
        if planet_ in [0, 1, 2, 3, 5]: continue
        name_col = nak_nam_pl[planet_] + '.innavamsha'

        if name_col not in dict_params.keys():
            dict_params.update({name_col: [planet_navamsha]})
        else:
            dict_params[name_col].append(planet_navamsha)

    # планета в нескольких знаках от другой планеты
    for planet_1, planet_in_znak_1 in enumerate(planet_in_znak[0:9]):
        if planet_1 in [1, 4, 6, 7, 8]: continue

        for planet_2, planet_in_znak_2 in enumerate(planet_in_znak[0:9]):
            if planet_1 >= planet_2: continue
            if planet_2 in [1, 4, 6, 7, 8]: continue

            name_col = nak_nam_pl[planet_1] + '.' + nak_nam_pl[planet_2] + '.diff_inznak'

            class_data = np.fmod(planet_in_znak_1 - planet_in_znak_2 + 12, 12)

            if name_col not in dict_params.keys():
                dict_params.update({name_col: [class_data]})
            else:
                dict_params[name_col].append(class_data)

    # расстояние между тяжелыми планетами в навамшах
    for planet_1, planet_in_znak_1 in enumerate(graha_in_navamsha):
        if planet_1 in [0, 1, 2, 3, 5]: continue

        for planet_2, planet_in_znak_2 in enumerate(graha_in_navamsha):
            if planet_1 >= planet_2: continue
            if planet_2 in [0, 1, 2, 3, 5]: continue

            name_col = nak_nam_pl[planet_1] + '.' + nak_nam_pl[planet_2] + '.hard.diff_inznak'
            class_data = np.fmod(planet_in_znak_1 - planet_in_znak_2 + 12, 12)

            if name_col not in dict_params.keys():
                dict_params.update({name_col: [class_data]})
            else:
                dict_params[name_col].append(class_data)

    # скорость планеты
    for planet_, planet_speed in enumerate(graha_speed[0:9]):
        if planet_ in [7, 8]: continue

        name_col = nak_nam_pl[planet_] + '.speed'

        if not not_class:
            class_speed = int((MAX_SPEED_PLANETS[planet_] - planet_speed) / (
                        MAX_SPEED_PLANETS[planet_] - MIN_SPEED_PLANETS[planet_]) * 100)
        else:
            if planet_ in [0, 1]:
                class_speed = planet_speed
            else:
                class_speed = retrograd_planet[planet_]

        if name_col not in dict_params.keys():
            dict_params.update({name_col: [class_speed]})
        else:
            dict_params[name_col].append(class_speed)

    # планета под аспектом другой планеты (сходство с расстояниями между планетами)
    degrees_aspects = (np.array(graha_in_degrees_aspects) * 3600).reshape(-1, 7)

    # соединение планет
    for planet_1, degrees_aspect in enumerate(degrees_aspects):
        if planet_1 in [1]: continue

        for planet_2, planet_in_degree in enumerate(graha_in_degrees[0:9]):
            class_aspects = []
            if planet_1 == planet_2: continue
            if planet_2 in [1]: continue

            # Смотрим все три аспекта на планету
            for n_aspect, aspect in enumerate(degrees_aspect[0:1]):
                if n_aspect not in actual_aspects[planet_1]: continue

                dist_class = int(dist_in_degrees(M=aspect, S=planet_in_degree) / 12000)
                if dist_class > 4: continue

                class_aspects.append(0)

            if len(class_aspects) == 0: class_aspect = None
            else: class_aspect = class_aspects[0]
            # planet_1 аспектирует -> planet_2

            name_col = nak_nam_pl[planet_1] + '.' + nak_nam_pl[planet_2] + '.connect'
            if name_col not in dict_params.keys():
                dict_params.update({name_col: [class_aspect]})
            else:
                dict_params[name_col].append(class_aspect)

    # планета под аспетом другой планеты
    for planet_1, degrees_aspect in enumerate(degrees_aspects):
        if planet_1 in [1]: continue

        for planet_2, planet_in_degree in enumerate(graha_in_degrees[0:9]):
            class_aspects = []
            if planet_1 == planet_2: continue
            if planet_2 in [1]: continue

            # Смотрим все три аспекта на планету
            for n_aspect, aspect in enumerate(degrees_aspect[1:4]):
                if n_aspect not in actual_aspects[planet_1]: continue

                dist_class = int(dist_in_degrees(M=aspect, S=planet_in_degree) / 12000)
                if dist_class > 4: continue

                class_aspects.append(0)

            if len(class_aspects) == 0: class_aspect = None
            else: class_aspect = class_aspects[0]
            # planet_1 аспектирует -> planet_2

            name_col = nak_nam_pl[planet_1] + '.' + nak_nam_pl[planet_2] + '.aspect'
            if name_col not in dict_params.keys():
                dict_params.update({name_col: [class_aspect]})
            else:
                dict_params[name_col].append(class_aspect)

    return dict_params


def calculate_parametrs(data_dict_up: dict, data_dict_down: dict):
    """
        data_dict словарь периодов {1: {'start': '01.01.2000', 'finish': '05.01.2000'}, ...}
    """

    dict_load = {'down': data_dict_down, 'up': data_dict_up}
    dist_result = {}
    sizes = {}
    unique_keys = []

    for data_name in dict_load.keys():
        len_size = 0
        dict_params = {}
        data_dict = dict_load[data_name]

        for n_dict in range(len(data_dict)):

            new_date_st, new_date_fn = data_dict[n_dict]['start'], data_dict[n_dict]['finish']

            if len(new_date_st) < 9 or len(new_date_fn) < 9: break

            new_date_start = datetime.strptime(new_date_st, FORMAT_DATE)
            new_date_finish = datetime.strptime(new_date_fn, FORMAT_DATE)

            delta_period = (new_date_finish - new_date_start).days

            if delta_period < 0:
                delta_period = -delta_period
                new_date_start, new_date_finish = new_date_finish, new_date_start

            for n_days in range(delta_period):
                len_size += 1
                new_date_tranzit = new_date_start + timedelta(days=n_days)
                new_date_tranzit = new_date_tranzit.strftime(FORMAT_DATE)

                planet_in_tranzit = calculateTranzitMap.calculate_tranzit_map(new_date_tranzit, "01.01.0001", '00:00:00')
                graha_in_degrees_aspects = planet_in_tranzit.graha_in_degrees_transit

                graha_in_degrees = planet_in_tranzit.graha_in_degrees
                graha_speed = planet_in_tranzit.graha_speed

                planet_in_znak = np.asarray(np.asarray(graha_in_degrees) / 108000, dtype='int8')

                """
                    planet_in_znak, graha_speed, graha_in_degrees, graha_in_retrograd, graha_in_degrees_aspects
                """
                dict_params = calc_param_date(dict_params=dict_params, planet_in_znak=planet_in_znak,
                                graha_speed=graha_speed, graha_in_degrees_aspects=graha_in_degrees_aspects,
                                graha_in_degrees=graha_in_degrees)

        sizes.update({data_name: len_size})

        """
            Проводим анализ данных
        """
        data_aspect_count = []
        for dict_param in dict_params.keys():
            if dict_param.split('.')[-1] in ['aspect']:
                data_aspect_count.append(len(dict_params[dict_param]))
        max_list_count = max(data_aspect_count)

        for dict_param in dict_params.keys():

            if dict_param.split('.')[-1] in ['inznak']:
                dict_params[dict_param] = diagramms_counts(list_for_counts=dict_params[dict_param])
                if dict_param not in unique_keys: unique_keys.append(dict_param)

            if dict_param.split('.')[-1] in ['innavamsha']:
                dict_params[dict_param] = diagramms_counts(list_for_counts=dict_params[dict_param])
                if dict_param not in unique_keys: unique_keys.append(dict_param)

            if dict_param.split('.')[-1] in ['diff_inznak']:
                dict_params[dict_param] = diagramms_counts(list_for_counts=dict_params[dict_param])
                if dict_param not in unique_keys: unique_keys.append(dict_param)

            if dict_param.split('.')[-1] in ['speed']:
                dict_params[dict_param] = diagramms_counts(list_for_counts=dict_params[dict_param])
                if dict_param not in unique_keys: unique_keys.append(dict_param)

            if dict_param.split('.')[-1] in ['aspect']:
                norm_into_group = int(count_not_none(dict_params[dict_param]) * (100 / max_list_count))
                dict_params[dict_param] = {'counts': [count_not_none(dict_params[dict_param])], 'norm_into_group': [norm_into_group], 'last_data': dict_params[dict_param]}
                if dict_param not in unique_keys: unique_keys.append(dict_param)

            if dict_param.split('.')[-1] in ['connect']:
                norm_into_group = int(count_not_none(dict_params[dict_param]) * (100 / max_list_count))
                dict_params[dict_param] = {'counts': [count_not_none(dict_params[dict_param])], 'norm_into_group': [norm_into_group], 'last_data': dict_params[dict_param]}
                if dict_param not in unique_keys: unique_keys.append(dict_param)

        dist_result.update({data_name: dict_params})


    """
        Дополнительный анализ двух словарей роста падения
    """
    diff_dict_etalon = {}

    variant = 'counts'

    for unique_key in unique_keys:
        if unique_key in dist_result['down'].keys() and unique_key in dist_result['up'].keys():

            if len(dist_result['up'][unique_key][variant]) > len(dist_result['down'][unique_key][variant]):
                dist_result['up'][unique_key][variant] = dist_result['up'][unique_key][variant][:len(dist_result['down'][unique_key][variant])]

            elif len(dist_result['up'][unique_key][variant]) < len(dist_result['down'][unique_key][variant]):
                dist_result['down'][unique_key][variant] = dist_result['down'][unique_key][variant][:len(dist_result['up'][unique_key][variant])]

            diff_dict_etalon.update({unique_key:
                                  np.asarray(np.array(dist_result['up'][unique_key][variant]) - np.array(dist_result['down'][unique_key][variant]), dtype='int32').tolist()})


        elif unique_key in dist_result['down'].keys() and unique_key not in dist_result['up'].keys():
            diff_dict_etalon.update({unique_key:
                                  np.asarray(-np.array(dist_result['down'][unique_key][variant]), dtype='int32').tolist()})

        elif unique_key not in dist_result['down'].keys() and unique_key in dist_result['up'].keys():
            diff_dict_etalon.update({unique_key:
                                  np.asarray(np.array(dist_result['up'][unique_key][variant]), dtype='int32').tolist()})

    """
        Извлечение значимых параметров
    """
    scores_dict = {}

    for macth_key in diff_dict_etalon.keys():
        scores = model_verify_parametrs(diff_dict=diff_dict_etalon, dist_result=dist_result, macth_keys=[macth_key], sizes=sizes)

        scores_dict.update({scores: macth_key})

    macth_key_list = sorted([key_ for key_ in scores_dict.keys()])[-20:]

    all_keys = ['']
    for macth_key_lis in macth_key_list:
        if macth_key_lis > 50:
            all_keys.append(scores_dict[macth_key_lis])
            print(f'score: {macth_key_lis} \t\t param: {scores_dict[macth_key_lis]}')

    """
        Перебор значимых параметров
    """
    print(str(diff_dict_etalon))

    max_score = 50.0
    list_keys_calc = []
    for nkey_1, key_1 in enumerate(all_keys):
        for nkey_2, key_2 in enumerate(all_keys):
            if nkey_2 <= nkey_1 and key_1 != '': continue

            for nkey_3, key_3 in enumerate(all_keys):
                if nkey_3 <= nkey_2 and key_2 != '': continue

                for nkey_4, key_4 in enumerate(all_keys):
                    if nkey_4 <= nkey_3 and key_3 != '': continue

                    for nkey_5, key_5 in enumerate(all_keys):
                        if nkey_5 <= nkey_4 and key_4 != '': continue

                        for nkey_6, key_6 in enumerate(all_keys):
                            if nkey_6 <= nkey_5 and key_5 != '': continue

                            for nkey_7, key_7 in enumerate(all_keys):
                                if nkey_7 <= nkey_6 and key_6 != '': continue

                                for nkey_8, key_8 in enumerate(all_keys):
                                    if nkey_8 <= nkey_7 and key_7 != '': continue

                                    for nkey_9, key_9 in enumerate(all_keys):
                                        if nkey_9 <= nkey_8 and key_8 != '': continue

                                        for nkey_10, key_10 in enumerate(all_keys):
                                            if nkey_10 < nkey_9 and key_9 != '': continue

                                            for nkey_11, key_11 in enumerate(all_keys):
                                                if nkey_11 <= nkey_10 and key_10 != '': continue

                                                for nkey_12, key_12 in enumerate(all_keys):
                                                    if nkey_12 <= nkey_11 and key_11 != '': continue

                                                    for nkey_13, key_13 in enumerate(all_keys):
                                                        if nkey_13 <= nkey_12 and key_12 != '': continue

                                                        for nkey_14, key_14 in enumerate(all_keys):
                                                            if nkey_14 <= nkey_13 and key_13 != '': continue

                                                            for nkey_15, key_15 in enumerate(all_keys):
                                                                if nkey_15 < nkey_14 and key_14 != '': continue

                                                                for nkey_16, key_16 in enumerate(all_keys):
                                                                    if nkey_16 < nkey_15 and key_15 != '': continue

                                                                    for nkey_17, key_17 in enumerate(all_keys):
                                                                        if nkey_17 <= nkey_16 and key_16 != '': continue

                                                                        for nkey_18, key_18 in enumerate(all_keys):
                                                                            if nkey_18 <= nkey_17 and key_17 != '': continue

                                                                            for nkey_19, key_19 in enumerate(all_keys):
                                                                                if nkey_19 <= nkey_18 and key_18 != '': continue


                                                                                match_ks = []

                                                                                for keys_ in [key_10, key_1, key_2, key_3, key_4, key_5, key_6,
                                                                                              key_7, key_8, key_9, key_11, key_12, key_13, key_14, key_15,
                                                                                              key_16, key_17, key_18, key_19]:

                                                                                    if keys_ not in match_ks and keys_ != '':
                                                                                        match_ks.append(keys_)

                                                                                match_ks = sorted(match_ks)

                                                                                if match_ks in list_keys_calc: continue
                                                                                else: list_keys_calc.append(match_ks)

                                                                                """
                                                                                    Проверка данных вычисления сколько совпадает, проверка каждого параметра
                                                                                """

                                                                                scores = model_verify_parametrs(diff_dict=diff_dict_etalon, dist_result=dist_result, macth_keys=match_ks, sizes=sizes)
                                                                                if max_score * .98 < scores:
                                                                                    print(f'max_sc {max_score} \t\t\t sc: {scores} \t\t {match_ks}')

                                                                                    if max_score < scores: max_score = scores

    print('complite')

    return diff_dict_etalon


def count_not_none(list_count):
    count_none = 0
    for list_coun in list_count:
        if list_coun is None: count_none += 1

    return len(list_count) - count_none


def model_verify_parametrs(diff_dict=None, dist_result=None, macth_keys=None, sizes=None):
    test_data = {'down': [], 'up': []}

    for dict_load in test_data.keys():

        for date in range(sizes[dict_load]):

            date_params_dict = {}

            for date_param in dist_result[dict_load].keys():

                if date_param in macth_keys:
                    date_params_dict.update({date_param: [dist_result[dict_load][date_param]['last_data'][date]]})

            score_ = get_score_date(etalon=diff_dict, data_dict=date_params_dict)

            if dict_load == 'down':
                if score_ >= 0: test_data['down'].append(0)
                else: test_data['down'].append(1)

            elif dict_load == 'up':
                if score_ <= 0: test_data['up'].append(0)
                else: test_data['up'].append(1)

    count_up = test_data['up'].count(1)
    count_down = test_data['down'].count(1)

    if count_up > 0: up_result = count_up / len(test_data['up'])
    else: up_result = 0

    if count_down > 0: down_result = count_down / len(test_data['down'])
    else: down_result = 0

    return round((up_result + down_result) / .02, 2)


def get_score_date(etalon=resulter_oil, data_dict=None):

    score = 0

    for key_ in data_dict.keys():

        if key_ in etalon.keys() and key_ in data_dict.keys():

            if data_dict[key_][0] is not None:
                try:
                    score += etalon[key_][data_dict[key_][0]]
                except:
                    print()

    return score

