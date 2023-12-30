import math

import numpy as np
from datetime import timedelta, date
from datetime import datetime
import pandas as pd

from dictsData.nakshatras_recomend import *

import calculate_sunrise_time
from constants import *
from toolkits.date_time_helper import dt_0_to_00, str_to_datetime, diff_between_dates, datetime_to_strtime, \
    datetime_to_strdate, seconds_to_strtime, degrees_to_part


def get_calculate_planet_time(start_data, finish_data, UTC=0, planet_1=MOON_PLANET_NUMBER, planet_2=SUN_PLANET_NUMBER):
    '''
    :param first_date: дата для которой вычисляется положение одной планеты оносительно другой
    :param end_date: конечная дата
    :param planet_1: планета первая
    :param planet_2: планета вторая

    speed_main_planet - более медленая планета (например Солнце)
    speed_scnd_planet - более быстрая планета (например Луна) - сколько градусов зодиака прошла планета за сутки


    angle_distanse_second_day - угловое расстояние пройденное за сутки быстрой планеты от главной main планеты

    функция принимает значения о положении планет
    возможно подсчитать день одной планеты относительно другой в данный момент времени

    :return: время начала дня и окончания дня, а также какая планета более медленная, какой у нее день по счету
            относительно другой планеты.
    '''

    if SP_PLANET_MEDDLE[planet_1] >= SP_PLANET_MEDDLE[planet_2]: main_planet, scnd_planet = planet_2, planet_1
    else: main_planet, scnd_planet = planet_1, planet_2

    df = pd.read_csv('resources/tableCoordsPlanets_redact.csv', sep=',')
    df.columns = ['SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN',
                  'URANUS', 'NEPTUNE', 'PLUTO', 'RAHY', 'KETY', 'DATE']


    date_form_period = diff_between_dates(start_data=start_data, finish_data=finish_data)

    data_output = []
    data_output_nakshatra = []
    data_output_znak = []
    tithi_start = 0
    nakshatra_start = 0
    znak_start = 0
    for day in np.arange(0, date_form_period):

        data_new = str_to_datetime(start_data) + timedelta(days=int(day))
        data_str = dt_0_to_00(data_new.day) + '.' + dt_0_to_00(data_new.month) + '.' + str(data_new.year)

        first_date_index = df[df['DATE'] == data_str].index.tolist()[0]

        coord_1_first = df.loc[first_date_index, NAME_PLANET_TIME[main_planet]]
        coord_2_first = df.loc[first_date_index + 1, NAME_PLANET_TIME[main_planet]]
        coord_aianamsha = SURIA_SIDDHANTA_AINAMSHA

        speed_main_planet = np.sum([-coord_1_first, coord_2_first])
        if speed_main_planet < 0: speed_main_planet += SECONDS_IN_ZODIAC
        if speed_main_planet > 100000: speed_main_planet = SECONDS_IN_ZODIAC - coord_2_first + coord_1_first

        coord_1_second = df.loc[first_date_index, NAME_PLANET_TIME[scnd_planet]]
        coord_2_second = df.loc[first_date_index + 1, NAME_PLANET_TIME[scnd_planet]]
        speed_scnd_planet = np.sum([-coord_1_second, coord_2_second])
        if speed_scnd_planet < 0: speed_scnd_planet += SECONDS_IN_ZODIAC
        if speed_scnd_planet > 100000: speed_scnd_planet = SECONDS_IN_ZODIAC - coord_2_second + coord_1_second

        angle_distanse_first_day = coord_1_second - coord_1_first
        if angle_distanse_first_day < 0: angle_distanse_first_day += SECONDS_IN_ZODIAC

        angle_distanse_second_day = coord_2_second - coord_2_first
        if angle_distanse_second_day < 0: angle_distanse_second_day += SECONDS_IN_ZODIAC

        delta_angle_distanse_in_day = angle_distanse_second_day - angle_distanse_first_day
        if delta_angle_distanse_in_day < -100000: delta_angle_distanse_in_day += SECONDS_IN_ZODIAC

        """
            Вычисление накшатры
        """
        coord_1_second_ayanamsha = coord_1_second - coord_aianamsha
        if coord_1_second_ayanamsha < 0: coord_1_second_ayanamsha = SECONDS_IN_ZODIAC + coord_1_second_ayanamsha

        angle_zodiak_seconds_in_second = speed_scnd_planet / SECONDS_IN_DAY

        seconds_to_next_nakshatra = (SECONDS_IN_NAKSHATRA - np.fmod(coord_1_second_ayanamsha, SECONDS_IN_NAKSHATRA))

        sun_time_to_next_nakshatra = seconds_to_next_nakshatra * angle_zodiak_seconds_in_second

        nakshatra_first_day = int(np.modf(coord_1_second_ayanamsha / SECONDS_IN_NAKSHATRA)[1])
        if day == 0: nakshatra_start = nakshatra_first_day

        seconds_to_last_nakshatra = np.fmod(coord_1_second_ayanamsha, SECONDS_IN_NAKSHATRA)
        sun_time_to_last_nakshatra = seconds_to_last_nakshatra * angle_zodiak_seconds_in_second

        time_last_nakshatra = data_new - timedelta(seconds=int(-sun_time_to_last_nakshatra)) - timedelta(days=1) + timedelta(hours=UTC)
        time_new_nakshatra = data_new + timedelta(seconds=int(sun_time_to_next_nakshatra)) - timedelta(days=1) + timedelta(hours=UTC)

        data_output_nakshatra.append([nakshatra_first_day, time_last_nakshatra, time_new_nakshatra])

        """
            Вычисление знака
        """
        coord_1_second_ayanamsha = coord_1_second - coord_aianamsha
        if coord_1_second_ayanamsha < 0: coord_1_second_ayanamsha = SECONDS_IN_ZODIAC + coord_1_second_ayanamsha

        angle_zodiak_seconds_in_second = speed_scnd_planet / SECONDS_IN_DAY

        seconds_to_next_znak = (SECONDS_IN_ZNAK - np.fmod(coord_1_second_ayanamsha, SECONDS_IN_ZNAK))

        sun_time_to_next_znak = seconds_to_next_znak * angle_zodiak_seconds_in_second

        znak_first_day = int(np.modf(coord_1_second_ayanamsha / SECONDS_IN_ZNAK)[1])
        if day == 0: znak_start = znak_first_day

        seconds_to_last_znak = np.fmod(coord_1_second_ayanamsha, SECONDS_IN_ZNAK)
        sun_time_to_last_znak = seconds_to_last_znak * angle_zodiak_seconds_in_second

        time_last_znak = data_new - timedelta(seconds=int(-sun_time_to_last_znak)) - timedelta(days=1) + timedelta(hours=UTC)
        time_new_znak = data_new + timedelta(seconds=int(sun_time_to_next_znak)) - timedelta(days=1) + timedelta(hours=UTC)

        data_output_znak.append([znak_first_day, time_last_znak, time_new_znak])

        """
            Вычисления титхи
        """
        angle_seconds_in_second = delta_angle_distanse_in_day / SECONDS_IN_DAY

        seconds_to_next_tithi = (((int(
            angle_distanse_first_day / SECONDS_IN_TITHI) + 1) * 12) - angle_distanse_first_day / SECONDS_IN_HOUR) * SECONDS_IN_HOUR


        tithi_first_day = int(np.modf(angle_distanse_first_day / SECONDS_IN_TITHI)[1])
        if day == 0: tithi_start = tithi_first_day

        tithi_first_day_part = np.modf(angle_distanse_first_day / SECONDS_IN_TITHI)[0]
        if delta_angle_distanse_in_day < .01: continue

        sun_time_to_next_tithi = seconds_to_next_tithi / angle_seconds_in_second

        seconds_to_last_tithi = tithi_first_day_part * SECONDS_IN_TITHI
        sun_time_to_last_tithi = seconds_to_last_tithi / angle_seconds_in_second

        time_last_tithi = data_new - timedelta(seconds=int(-sun_time_to_last_tithi)) - timedelta(days=1) + timedelta(hours=UTC)
        time_new_tithi = data_new + timedelta(seconds=int(sun_time_to_next_tithi)) - timedelta(days=1) + timedelta(hours=UTC)

        data_output.append([tithi_first_day, time_last_tithi, time_new_tithi])

    """
        Tithi
    """
    analis_result = []
    for tithi_mass in data_output:
        tithi, last_time, next_time = tithi_mass[0], tithi_mass[1], tithi_mass[2]
        tithi_str = TITHI_NAME[tithi]
        if tithi - tithi_start == 1 or tithi - tithi_start == -29:
            analis_result.append([tithi, next_time, tithi_str])
            tithi_start = tithi
        elif tithi - tithi_start == 2 or tithi - tithi_start == -28:
            analis_result.append([tithi, last_time, TITHI_NAME[tithi]])
            analis_result.append([tithi, next_time, tithi_str])
            tithi_start = tithi
        elif tithi - tithi_start == 0:
            if len(analis_result) == 0:
                analis_result.append([tithi, next_time, tithi_str])

    """
        Nakshatra
    """
    analis_result_nakshatra = []
    for nakshatra_mass in data_output_nakshatra:
        nakshatra, last_time, next_time = nakshatra_mass[0], nakshatra_mass[1], nakshatra_mass[2]
        nakshatra_str = NAME_NAKSHATRAS[nakshatra]
        if nakshatra - nakshatra_start == 1 or nakshatra - nakshatra_start == -26:
            analis_result_nakshatra.append([nakshatra, next_time, nakshatra_str])
            nakshatra_start = nakshatra
        elif nakshatra - nakshatra_start == 2 or nakshatra - nakshatra_start == -25:
            analis_result_nakshatra.append([nakshatra, last_time, NAME_NAKSHATRAS[nakshatra]])
            analis_result_nakshatra.append([nakshatra, next_time, nakshatra_str])
            nakshatra_start = nakshatra
        elif nakshatra - nakshatra_start == 0:
            if len(analis_result_nakshatra) == 0:
                analis_result_nakshatra.append([nakshatra, next_time, nakshatra_str])

    """
        Znak
    """
    analis_result_znak = []
    for znak_mass in data_output_znak:
        znak, last_time, next_time = znak_mass[0], znak_mass[1], znak_mass[2]
        znak_str = NAME_ZNAKS[znak]
        if znak - znak_start == 1 or znak - znak_start == -max(ZODIAK_RANGE):
            analis_result_znak.append([znak, next_time, znak_str])
            znak_start = znak
        elif znak - znak_start == 2 or znak - znak_start == -max(ZODIAK_RANGE) + 1:
            analis_result_znak.append([znak - 1, last_time, ZODIAK_RANGE[znak - 1]])
            analis_result_znak.append([znak, next_time, znak_str])
            znak_start = znak
        elif znak - znak_start == 0:
            if len(analis_result_znak) == 0:
                analis_result_znak.append([znak, next_time, znak_str])

    return analis_result[1:], analis_result_nakshatra[1:], analis_result_znak[1:]

def calc_surise(ltd_degr=59.37, lng_degr=37.96, UTC=0, str_date='02.02.1998', data='sunrise'):
    how_date = str_to_datetime(str_date)

    """
        Time Sunrise
    """
    s_day, s_month, s_year = how_date.day, how_date.month, how_date.year

    sun_rise, sun_set = calculate_sunrise_time.get_calculate_sunrise(ltd_degr, lng_degr,
                                                                     s_day, s_month, s_year, UTC)

    sun_rise, sun_set = int(sun_rise), int(sun_set)

    def calculate_set_sun(sun_time=None, s_day=None, s_month=None, s_year=None):
        sunrise_hour = sun_time / SECONDS_IN_HOUR
        sunrise_minute = (sunrise_hour - math.trunc(sunrise_hour)) * MINUTS_IN_HOUR
        sunrise_second = (sunrise_minute - math.trunc(sunrise_minute)) * MINUTS_IN_HOUR

        s_day, s_month, s_year, s_hour, s_minute, s_second = dt_0_to_00(s_day), dt_0_to_00(s_month), dt_0_to_00(s_year), \
                                                             dt_0_to_00(int(sunrise_hour)), dt_0_to_00(int(sunrise_minute)), dt_0_to_00(int(sunrise_second))

        sun_date = s_day + '.' + s_month + '.' + s_year
        sun_time = s_hour + ':' + s_minute + ':' + s_second

        return datetime.strptime(sun_date + '-' + sun_time, FORMAT_DATE + '-' + FORMAT_TIME)

    if data == 'sunrise': return calculate_set_sun(sun_time=sun_rise, s_day=s_day, s_month=s_month, s_year=s_year)
    else: return calculate_set_sun(sun_time=sun_set, s_day=s_day, s_month=s_month, s_year=s_year)

def calculate_moon_day(start_data='27.05.2021', finish_data='25.07.2021', utc=3, ltd=59.37, lng=37.96):

    analis_result_tithi, analis_result_nakshatra, analis_result_znak = get_calculate_planet_time(start_data, finish_data, UTC=utc)

    """
        Создание общего словаря данных по датам
    """
    result_dict = {}

    for result_tnz, name_tnz in zip([analis_result_tithi, analis_result_nakshatra, analis_result_znak],
                                    ['tithi', 'nakshatra', 'znak']):

        for tnz in result_tnz:
            day, month = dt_0_to_00(tnz[1].day), dt_0_to_00(tnz[1].month)
            date_key_tithi = day+'.'+month+'.'+str(tnz[1].year)

            if date_key_tithi not in result_dict.keys():
                result_dict.update({date_key_tithi: {'tithi': None, 'nakshatra': None, 'znak': None,
                                                     'sunrise': None, 'sunset': None}})

            result_dict[date_key_tithi][name_tnz] = tnz

            if result_dict[date_key_tithi]['sunrise'] is None:
                result_dict[date_key_tithi]['sunrise'] = calc_surise(ltd_degr=ltd, lng_degr=lng, UTC=utc, str_date=date_key_tithi, data='sunrise')

            if result_dict[date_key_tithi]['sunset'] is None:
                result_dict[date_key_tithi]['sunset'] = calc_surise(ltd_degr=ltd, lng_degr=lng, UTC=utc, str_date=date_key_tithi, data='sunset')

    """
        Автозаполнение пропусков в данных
    """
    total_result_dict = {}
    date_form_period = diff_between_dates(start_data=start_data, finish_data=finish_data)

    for day in np.arange(1, date_form_period):

        data_lst = str_to_datetime(start_data) + timedelta(days=int(day-1))
        data_new = str_to_datetime(start_data) + timedelta(days=int(day))

        data_newstr = dt_0_to_00(data_new.day) + '.' + dt_0_to_00(data_new.month) + '.' + str(data_new.year)
        data_lststr = dt_0_to_00(data_lst.day) + '.' + dt_0_to_00(data_lst.month) + '.' + str(data_lst.year)

        if data_newstr in result_dict.keys():

            if data_newstr not in total_result_dict.keys():
                total_result_dict.update({data_newstr: {'tithi': None, 'nakshatra': None, 'znak': None,
                                                        'sunrise': None, 'sunset': None, 'weekday': None}})

            for type_tnz in ['tithi', 'nakshatra', 'znak']:

                if result_dict[data_newstr][type_tnz] is None:
                    result_dict[data_newstr][type_tnz] = result_dict[data_lststr][type_tnz]

                """
                    Окончательное сведение данных по восходу Солнца
                """
                if result_dict[data_lststr][type_tnz] is not None:
                    if result_dict[data_newstr][type_tnz][1] > result_dict[data_newstr]['sunrise']:
                        total_result_dict[data_newstr][type_tnz] = [result_dict[data_lststr][type_tnz][0],
                                                                    result_dict[data_lststr][type_tnz][2]]

                    else:
                        total_result_dict[data_newstr][type_tnz] = [result_dict[data_newstr][type_tnz][0],
                                                                    result_dict[data_newstr][type_tnz][2]]
                else:
                    total_result_dict[data_newstr][type_tnz] = [None, 'None']

            total_result_dict[data_newstr]['sunrise'] = result_dict[data_newstr]['sunrise']
            total_result_dict[data_newstr]['sunset'] = result_dict[data_newstr]['sunset']

            total_result_dict[data_newstr]['weekday'] = [str_to_datetime(date=data_newstr).weekday(),
                                                         WEEKDAYS[str_to_datetime(date=data_newstr).weekday()]]

    return total_result_dict

def filter_zachatie(ldf=None, man_jnakshatra=9, woman_jnakshatra=18, date_minstr='07.04.2022', finish_data=None):

    if ldf is None: ldf = calculate_moon_day(start_data=date_minstr, finish_data=finish_data, utc=3, ltd=59.37, lng=37.96)

    bad_nakhatras = np.fmod(np.array([man_jnakshatra, man_jnakshatra+9, man_jnakshatra+18,
                     woman_jnakshatra, woman_jnakshatra+9, woman_jnakshatra+18]), 27).tolist() + [1,2,5,6,8,9,10,12,15,17,19,24]
    bad_tithi = [14, 29, 3, 7, 8, 18, 22, 23]
    bad_weekdays = []#[1, 5, 6]

    good_day_far_minstr = [5, 9, 11, 13, 4, 14, 15,16,17,18,19,20,21,22,23]

    filter_data = {}

    for good_day_far in good_day_far_minstr:
        good_day_far_minstr_dt = datetime_to_strdate(dt=str_to_datetime(date=date_minstr) + timedelta(days=good_day_far))

        if ((ldf[good_day_far_minstr_dt]['tithi'][0] not in bad_tithi) and
           (ldf[good_day_far_minstr_dt]['nakshatra'][0] not in bad_nakhatras) and
           (ldf[good_day_far_minstr_dt]['weekday'][0] not in bad_weekdays)):

            add_280_days = datetime_to_strdate(dt=str_to_datetime(date=date_minstr) + timedelta(days=280))
            filter_data.update({good_day_far_minstr_dt: ldf[good_day_far_minstr_dt].update({'add_280': add_280_days, 'good_day_far':good_day_far})})

    return filter_data

date_minstr_ = '01.12.2025' #'12.09.2021'

start = datetime_to_strdate(dt=str_to_datetime(date=date_minstr_) - timedelta(days=5))
finish = datetime_to_strdate(dt=str_to_datetime(date=date_minstr_) + timedelta(days=50))

moon_days_ldf = calculate_moon_day(start_data=start, finish_data=finish, utc=3,
                                   ltd=degrees_to_part(lat='59:56:15'), lng=degrees_to_part(lat='30:30:55'))

filter_data = filter_zachatie(ldf=moon_days_ldf, man_jnakshatra=9, woman_jnakshatra=18,
                              date_minstr=date_minstr_, finish_data=finish)

print(date_minstr_)
for moon_day in filter_data.keys():

    end_timeday = str_to_datetime(date=datetime_to_strdate(dt=moon_days_ldf[moon_day]['sunrise']), time='23:59:59')
    night_dt = end_timeday - moon_days_ldf[moon_day]['sunset'] + moon_days_ldf[moon_day]['sunrise']

    nmyh = 25 - 15
    night_sec_1 = int((night_dt.hour*3600+night_dt.minute*60+night_dt.second) / 15) * nmyh
    calc_time1 = moon_days_ldf[moon_day]['sunset'] + timedelta(seconds=night_sec_1)

    night_sec_2 = int((night_dt.hour*3600+night_dt.minute*60+night_dt.second) / 15) * (nmyh+1)
    calc_time2 = moon_days_ldf[moon_day]['sunset'] + timedelta(seconds=night_sec_2)

    print(moon_day, datetime_to_strtime(dt=moon_days_ldf[moon_day]['sunrise']), datetime_to_strtime(dt=moon_days_ldf[moon_day]['sunset']),
          '\t\t<<<', calc_time1.time(), '-', calc_time2.time(), '>>>\t',
          moon_days_ldf[moon_day]['tithi'][1], moon_days_ldf[moon_day]['nakshatra'][1],
          moon_days_ldf[moon_day]['znak'][1], moon_days_ldf[moon_day]['weekday'][1], moon_days_ldf[moon_day]['add_280'], 'day:',moon_days_ldf[moon_day]['good_day_far'])

print()

for moon_day in moon_days_ldf.keys():
    print(f"{moon_day} {datetime_to_strtime(dt=moon_days_ldf[moon_day]['sunrise'])} {moon_days_ldf[moon_day]['tithi'][1]} "
          f"{moon_days_ldf[moon_day]['nakshatra'][1]} {moon_days_ldf[moon_day]['znak'][1]} "
          f"{moon_days_ldf[moon_day]['weekday'][1]}", end=' -----> ')

    for key in dict_data.keys():

        parkey = key.split('.')

        if len(parkey) == 1:
            if moon_days_ldf[moon_day]['nakshatra'][1] == parkey[0]:
                print(dict_data[key], end=' ')

        elif len(parkey) == 2:
            if moon_days_ldf[moon_day]['nakshatra'][1] == parkey[0] and TITHI_NAME[int(parkey[1])] == moon_days_ldf[moon_day]['tithi'][1]:
                print(dict_data[key], end=' ')

    print()