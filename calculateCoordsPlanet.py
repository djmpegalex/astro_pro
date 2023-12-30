import time
from datetime import timedelta
from datetime import datetime
from constants import *
import numpy as np
import pandas as pd

# данные о координатах планет
coords_data = pd.read_csv('resources/tableCoordsPlanets_redact.csv', sep=',')

class CoordsData():
    def __init__(self, coords_time_ratio, graha_in_degrees,
                 sp_strenght_planet, retrogr_planet, speed_planet):
        self.coords_time_ratio = coords_time_ratio
        self.graha_in_degrees = graha_in_degrees
        self.sp_strenght_planet = sp_strenght_planet
        self.retrogr_planet = retrogr_planet
        self.speed_planet = speed_planet


def calculate_coords_planet(first_date, first_time, utc=0, delta=0):
    # time_first_time = time.strptime(first_time, FORMAT_TIME)
    time_first_date = datetime.strptime(f'{first_date} {first_time}', f'{FORMAT_DATE} {FORMAT_TIME}')
    time_first_date = time_first_date - timedelta(hours=int(utc))

    time_first_day = time_first_date.strftime(FORMAT_DATE)

    sp_strenght_planet = []

    select_data = coords_data[coords_data['Date'] == time_first_day]
    coords_last_planets = np.asarray(
        [select_data['Sun'].values[0],
         select_data['Moon'].values[0],
         select_data['Mars'].values[0],
         select_data['Mercury'].values[0],
         select_data['Jupiter'].values[0],
         select_data['Venus'].values[0],
         select_data['Saturn'].values[0],
         select_data['Rahy'].values[0],
         select_data['Kety'].values[0]]) - delta

    d1_next_day = time_first_date + timedelta(days=1)
    d1_next_dayStr = d1_next_day.strftime(FORMAT_DATE)

    select_data_next = coords_data[coords_data['Date'] == d1_next_dayStr]
    coords_next_planets = np.asarray(
        [select_data_next['Sun'].values[0],
         select_data_next['Moon'].values[0],
         select_data_next['Mars'].values[0],
         select_data_next['Mercury'].values[0],
         select_data_next['Jupiter'].values[0],
         select_data_next['Venus'].values[0],
         select_data_next['Saturn'].values[0],
         select_data_next['Rahy'].values[0],
         select_data_next['Kety'].values[0]]) - delta

    # выводим поправочный коэффициент для уточнения положений планет
    coords_time_ratio = ((time_first_date.hour * MINUTS_IN_HOUR * MINUTS_IN_HOUR) + (
            time_first_date.minute * MINUTS_IN_HOUR) + time_first_date.second) / 86400

    sp_grah = []
    for n in PLANETS_RANGE:
        arra = coords_next_planets[n] - coords_last_planets[n]
        if arra > MAXIMUS_SPEED_PLANETS[n]: arra = SECONDS_IN_ZODIAC - arra
        elif arra < -MAXIMUS_SPEED_PLANETS[n]: arra = SECONDS_IN_ZODIAC + arra
        sp_grah.append(arra)

    coords_planets = np.fmod(coords_last_planets + np.asarray(sp_grah) * coords_time_ratio + SECONDS_IN_ZODIAC,SECONDS_IN_ZODIAC)

    """
        Вычисление скоростей движения планет    
    """
    speed_planet = np.asarray(sp_grah)

    """
        вычисление чешта балы, силы движения планет
    """
    retrogr_planet = []

    def retrogr_pl(i):
        if sp_grah[i] < -500000:
            sp_grah[i] += SECONDS_IN_ZODIAC
        elif sp_grah[i] > 500000:
            sp_grah[i] = SECONDS_IN_ZODIAC - sp_grah[i]

        # вычисление ретроградности планеты (обратного хода по зодиаку)
        retrogr_planet.append((sp_grah[i]) < 0)
        sp_grah[i] = abs(sp_grah[i])

        if retrogr_planet[i] == False:
            sp_strenght_planet.append(sp_grah[i] / SP_PLANET_MAX[i] * SP_POWER_VALUE)
            retrogr_planet[i] = 0
        else:
            sp_strenght_planet.append(sp_grah[i] / SP_PLANET_RETR[i] * SP_POWER_RETR)
            retrogr_planet[i] = 1
    list(map(lambda x: retrogr_pl(x), PLANETS_RANGE))

    retrogr_planet[7] = 1
    retrogr_planet[8] = 1
    """
         вычисление точных координат положения планет
    """
    graha_in_degrees = np.concatenate([np.asarray(coords_planets), [0]]).tolist()
    # print(end='')
    return CoordsData(coords_time_ratio, graha_in_degrees,
                      sp_strenght_planet, retrogr_planet, speed_planet)
