from constants import FORMAT_DATE, FORMAT_TIME
from datetime import datetime

def dt_0_to_00(num_str=None):
    num_str = str(num_str)
    if len(num_str) == 1: num_str = '0' + num_str
    return num_str

def str_to_datetime(date='19.10.1990', time='00:00:00'):
    return datetime.strptime(date + '-' + time, FORMAT_DATE + '-' + FORMAT_TIME)

def diff_between_dates(start_data='01.04.1990', finish_data='01.04.1991'):
    date_form_start = str_to_datetime(start_data)
    date_form_end = str_to_datetime(finish_data)
    return (date_form_end - date_form_start).days + 1

def seconds_to_strtime(seconds_=None):
    hours = int(seconds_/3600)
    minutes = int((seconds_ - hours * 3600) / 60)
    seconds = int(seconds_ - hours * 3600 - minutes * 60)

    return dt_0_to_00(num_str=hours) + ':' + dt_0_to_00(num_str=minutes) + ':' + dt_0_to_00(num_str=seconds)

def datetime_to_strtime(dt=str_to_datetime()):
    return dt_0_to_00(dt.hour) + ':' + dt_0_to_00(dt.minute) + ':' + dt_0_to_00(dt.second)

def datetime_to_strdate(dt=str_to_datetime()):
    return dt_0_to_00(dt.day) + '.' + dt_0_to_00(dt.month) + '.' + dt_0_to_00(dt.year)

def degrees_to_part(lat='59:56:15'):
    lat_ = lat.split(':')
    if len(lat_) < 3:
        lat_ = lat.split('.')

    hour, minute, second = int(lat_[0]), int(lat_[1]), int(lat_[2])
    return (hour * 3600 + minute * 60 + second) / 3600

def time_to_seconds(tim='12:56:15'):
    lat_ = tim.split(':')
    if len(lat_) < 3:
        lat_ = tim.split('.')

    hour, minute, second = int(lat_[0]), int(lat_[1]), int(lat_[2])
    return hour * 3600 + minute * 60 + second