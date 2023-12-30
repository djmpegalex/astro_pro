import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

import mathCalculateLagna
from dictsData.muhurta_recomendations import etdata
from constants import SUN_PLANET_NUMBER, SECONDS_IN_ZODIAC
from toolkits.date_time_helper import time_to_seconds, seconds_to_strtime

const_uprav = {0: [0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 7, 0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 8],
               1: [1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 7, 1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 8],
               2: [2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 7, 2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 8],
               3: [3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 7, 3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 8],
               4: [4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 7, 4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 8],
               5: [5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 7, 5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 8],
               6: [6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 7, 6, 4, 2, 0, 5, 3, 1, 6, 4, 2, 0, 5, 3, 1, 8]}

x1 = 0
x2 = 0

y1 = 5
y2 = 10
# plt.figure()

dict_powers ={'в экзальтации': 100,
              'в мулатриконе': 90,
              'в собственном': 75,
              'большой друг': 50,
              'в дружественном': 37.5,
              'в нейтральном': 25,
              'во вражеском': 0,
              'большой враг': 0,
              'в дибилитации': 0}

names_pl = ['Su', 'Mo', 'Ma', 'Me', 'Ju', 'Ve', 'Sa', 'Ra', 'Ke']


def get_recomendations(rise_time="05:55:54", set_time="19:23:54", date="2020-12-20", calc_lagna=None, send_moment=None,
                       ltd_degr=59.8564, planets_degrees=None, power_planets=None, speed_moon=48000):

    moon_0 = planets_degrees[1:2][0]

    if send_moment is None:
        calc_lagna = range(30)

    date = date.replace('.', '-')

    zero_day = datetime.fromisoformat(f'{date}T00:00:00')
    zero_nig = datetime.fromisoformat(f'{date}T23:59:59')

    sun_rise = datetime.fromisoformat(f'{date}T{rise_time}')
    sun_set = datetime.fromisoformat(f'{date}T{set_time}')

    n_day = [1,2,3,4,5,6,0][sun_rise.weekday()]

    day_muhurta = ((zero_nig - zero_day) / 30).total_seconds()
    angle_day = day_muhurta / 240  # перевод секунд времени в угловые градусы

    rise_6_00 = seconds_to_strtime((time_to_seconds(str(sun_set.time())) + time_to_seconds(str(sun_rise.time()))) / 2 - 21600)
    sun_rise_6_00 = datetime.fromisoformat(f'{date}T{rise_6_00}')
    print('местные 6-00:', sun_rise_6_00)

    send_time_ = None
    if send_moment is not None:

        if len(send_moment) == 19:
            send_time_ = datetime.fromisoformat(send_moment)

            """
                FIND LAGNA FOR VARIATY TIME
            """
            axise = []
            add_seconds = 0

            for len_muh, tim_muh in zip([angle_day], [day_muhurta]):
                for muhh in range(30):
                    axise.append(360)

                    add_seconds += tim_muh

                    time_muhurta_0 = sun_rise_6_00 + timedelta(seconds=int(add_seconds - tim_muh))
                    time_muhurta_1 = sun_rise_6_00 + timedelta(seconds=int(add_seconds))

                    if time_muhurta_0 <= send_time_ < time_muhurta_1:
                        calc_lagna = [len(axise) - 1]

    func_all = {}

    for lagna in calc_lagna:
        axise = []
        all_angle = 0

        add_seconds = 0
        lagna_angle = None

        time_muhurta_0 = ''
        time_muhurta_1 = ''

        for len_muh, tim_muh in zip([angle_day], [day_muhurta]):
            for muhh in range(30):
                axise.append(360 - all_angle)

                add_seconds += tim_muh

                if lagna == len(axise) - 1:
                    lagna_angle = axise[-1]

                    time_muhurta_0 = sun_rise_6_00 + timedelta(seconds=int(add_seconds - tim_muh))
                    time_muhurta_1 = sun_rise_6_00 + timedelta(seconds=int(add_seconds))

                    """
                        Корректировка положения луны
                    """
                    planets_degrees[1] = np.fmod(moon_0 + (time_muhurta_0 - zero_day).total_seconds() / 86400 * speed_moon, SECONDS_IN_ZODIAC)

                all_angle += len_muh
        axise.append(0)

        """
            Вычисление джанма-лагны для начала и конца времени мухурты
        """
        sun_rise_seconds = int(sun_rise_6_00.hour * 3600 + sun_rise_6_00.minute * 60 + sun_rise_6_00.second)
        b_time_start = int(time_muhurta_0.hour * 3600 + time_muhurta_0.minute * 60 + time_muhurta_0.second)
        sunrise_in_degrees = planets_degrees[SUN_PLANET_NUMBER]
        lagna_in_seconds = mathCalculateLagna.asc_calculate(sunrise_in_degrees, sun_rise_seconds, b_time_start, ltd_degr)

        lagna_in_angle_start = np.fmod(360 - (lagna_in_seconds - planets_degrees[0]) / 3600 - lagna_angle + 360, 360)

        muhurta_angles_bhava = []
        for nn, n in enumerate(axise[:-1]):
            new_angle = np.fmod(n - lagna_angle + 360, 360)

            muhurta_angles_bhava.append(new_angle)

            # cos_a2 = np.cos(np.radians(new_angle))
            # sin_a2 = np.sin(np.radians(new_angle))
            #
            # x_2 = x2 * cos_a2 - y2 * sin_a2
            # y_2 = x2 * sin_a2 + y2 * cos_a2
            #
            # x_1 = x1 * cos_a2 - y1 * sin_a2
            # y_1 = x1 * sin_a2 + y1 * cos_a2
            #
            # cos_at = np.cos(np.radians((n + axise[nn + 1]) / 2 - lagna_angle))
            # sin_at = np.sin(np.radians((n + axise[nn + 1]) / 2 - lagna_angle))
            #
            # x_t = x2 * cos_at - y2 * sin_at
            # y_t = x2 * sin_at + y2 * cos_at
            #
            # x_b = x1 * cos_at - y1 * sin_at
            # y_b = x1 * sin_at + y1 * cos_at
            #
            # plt.plot([x_1, x_2], [y_1, y_2], '--', color='gray', linewidth=.5)
            #
            # if np.fmod(nn - lagna + 30, 30) == 0:
            #     plt.text(x_t, y_t, 'лагна', horizontalalignment='center', verticalalignment='center', color='blue',
            #              size=9)
            # else:
            #     plt.text(x_t, y_t, nn, horizontalalignment='center', verticalalignment='center', color='blue', size=9)
            #
            # plt.text(x_b, y_b, np.fmod(nn - lagna + 30, 30), horizontalalignment='center', verticalalignment='center',
            #          color='red', size=8)

        planets_in_angles = []
        for n, (pl_nm, p_an) in enumerate(zip(names_pl, planets_degrees)):
            angle = np.fmod(360 - (p_an - planets_degrees[0]) / 3600 - lagna_angle + 360, 360)
            planets_in_angles.append(angle)

            # cos_a2 = np.cos(np.radians(angle))
            # sin_a2 = np.sin(np.radians(angle))
            #
            # xpl = 0
            # ypl = 6 + n * .45
            #
            # x_pl = xpl * cos_a2 - ypl * sin_a2
            # y_pl = xpl * sin_a2 + ypl * cos_a2
            #
            # plt.plot(x_pl, y_pl, '.', color='black')
            # plt.text(x_pl, y_pl, pl_nm, color='black', size=7, horizontalalignment='center', verticalalignment='top')

        # plt.title(time_muhurta_0 + ' - ' + time_muhurta_1)

        dict_planets = {}

        muhurta_angles_bhava.append(muhurta_angles_bhava[0])

        for n, planets_in_angle in enumerate(planets_in_angles):
            dict_planets.update(
                {n: {'uprav_muhurta': [], 'in_muhurta': -1, 'in_bhava': -1, 'is_lagnesha': False, 'in_lagna': False, 'is_udaya_lagnesha': False}})

            for nupr, upravs in enumerate(const_uprav[n_day]):
                if upravs == n:
                    dict_planets[n]['uprav_muhurta'].append(nupr)
                    if lagna == nupr:
                        dict_planets[n]['is_lagnesha'] = True

            for n_m, (in_bhava_last, in_bhava_next) in enumerate(
                    zip(muhurta_angles_bhava[:-1], muhurta_angles_bhava[1:])):

                if in_bhava_last >= planets_in_angle > in_bhava_next or (
                        in_bhava_last == 0 and in_bhava_next <= planets_in_angle < 360):
                    dict_planets[n]['in_muhurta'] = n_m
                    dict_planets[n]['in_bhava'] = np.fmod(n_m - lagna + 30, 30)

                    if dict_planets[n]['in_bhava'] == 0: dict_planets[n]['in_lagna'] = True

        for n_m, (in_bhava_last, in_bhava_next) in enumerate(zip(muhurta_angles_bhava[:-1], muhurta_angles_bhava[1:])):

            if in_bhava_last >= lagna_in_angle_start > in_bhava_next or (
                    in_bhava_last == 0 and in_bhava_next <= lagna_in_angle_start < 360):

                udays_ = n_m

                who_uprav_udaya = const_uprav[n_day][n_m]
                dict_planets[who_uprav_udaya]['is_udaya_lagnesha'] = True


        func_all.update({lagna: {'time_start': time_muhurta_0, 'time_finish': time_muhurta_1, 'recomendations': {}}})

        for planet in dict_planets.keys():
            if dict_planets[planet]['is_lagnesha']:

                for data_ in [dict_planets[planet]['in_muhurta'], dict_planets[planet]['in_bhava']] + dict_planets[planet]['uprav_muhurta']:
                    if data_ not in func_all[lagna]['recomendations'].keys():
                        func_all[lagna]['recomendations'].update({data_: dict_powers[power_planets[planet]] * (1.5 * (data_ == 7) * 4)})
                    else:
                        func_all[lagna]['recomendations'][data_] += dict_powers[power_planets[planet]] * (1.5 + (data_ == 7) * 4)

                # if lagna == 8:
                #     print()

            if dict_planets[planet]['in_lagna']:

                for data_ in dict_planets[planet]['uprav_muhurta']:
                    if data_ not in func_all[lagna]['recomendations'].keys():
                        func_all[lagna]['recomendations'].update({data_: dict_powers[power_planets[planet]]})
                    else:
                        func_all[lagna]['recomendations'][data_] += dict_powers[power_planets[planet]]

            if dict_planets[planet]['is_udaya_lagnesha']:

                muhurta_ = dict_planets[planet]['in_muhurta']
                bhava_udaya = np.fmod(muhurta_ - udays_ + 30, 30)

                for data_ in [bhava_udaya, muhurta_, dict_planets[planet]['in_bhava']]:
                    if data_ not in func_all[lagna]['recomendations'].keys():
                        func_all[lagna]['recomendations'].update({data_: dict_powers[power_planets[planet]] * (2.5 + (data_ == 7) * 4)})
                    else:
                        func_all[lagna]['recomendations'][data_] += dict_powers[power_planets[planet]] * (2.5 + (data_ == 7) * 4)

    return func_all


def parse_recomendations(recomendations: dict):
    recomendations_ = {}

    for recomendat in recomendations.keys():
        recomendations_.update({recomendat:
                                {'time_start': recomendations[recomendat]['time_start'],
                                 'time_finish': recomendations[recomendat]['time_finish'],
                                 'recomendations': {}}})

        for rec in recomendations[recomendat]['recomendations'].keys():
            if rec == -1: continue

            for etd in etdata[rec]:

                if etd not in recomendations_[recomendat]['recomendations'].keys():
                    recomendations_[recomendat]['recomendations'].update({etd: recomendations[recomendat]['recomendations'][rec]})
                else:
                    recomendations_[recomendat]['recomendations'][etd] += recomendations[recomendat]['recomendations'][rec]


        delete_keys = []
        for rec in recomendations_[recomendat]['recomendations'].keys():

            if recomendations_[recomendat]['recomendations'][rec] <= 80:
                delete_keys.append(rec)

        for delete_key in delete_keys:
            recomendations_[recomendat]['recomendations'].pop(delete_key)

    return recomendations_
