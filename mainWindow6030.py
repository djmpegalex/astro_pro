import tkinter
import math
import io
import time as timet

import calculate_sunrise_time
import window_of_first_date
from anlgeDistansPlanets import calculateDistansePlanets_scale
from calculate_exult_planets import calc_self_aspects
from bhava_aspects_calculate import bhava_aspec
from calculate_muhurta import *
from data_etalons.collections_data import oil_break
from dictsData import dictOfCompanies
# import calculate_find_time_burn
import beginScript
import calculate_karakas
import beginScriptOutData
import matplotlib
import calculateTranzitMap
import calculate_relations_betwen_planets
# import calculate_lights_planets
from calculateBindy import calculate_bindy_vargas
from calculatePlanetsTime import get_calculate_planet_time
import pandas as pd

from toolkits.calculate_break_moments import get_break_moments
from toolkits.calculate_parameters import calculate_parametrs
from toolkits.date_time_helper import degrees_to_part
from toolkits.math_distance import sum_in_degrees

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from constants import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import *

COLOR_LABL = ['#ffffff', '#ff0000', '#00ff00']
array_prognozPlanet = [] is globals()
array_prognozPlanet2 = []
newLabel = ""
array_dashaRatioX = []
xxx = 0
multiMonth = 1

y_labl = 35
x_b_to = 150

x_b_fr = x_b_to + 120
x_b_va = x_b_to + 60

y_butt = y_labl + 15

new_date_search = ''

new_command = ""
retrogr_planet = None
delta = 0

TODAY_TIME = datetime.today()
# today_year = int(TODAY_TIME.year)
# simple_date = TODAY_TIME
# past_date = TODAY_TIME + timedelta(days=-5)
# next_ates = TODAY_TIME + timedelta(days=5)

# TODAY_TIME = datetime.strptime('27.07.2013', FORMAT_DATE)
today_year = int(TODAY_TIME.year)
simple_date = TODAY_TIME
past_date = TODAY_TIME + timedelta(days=-100)
next_ates = TODAY_TIME + timedelta(days=900)

next_ates = next_ates.strftime(FORMAT_DATE)
past_date = past_date.strftime(FORMAT_DATE)
today_date = TODAY_TIME.strftime(FORMAT_DATE)

value_but = [0]*10

next_ates = str(next_ates)
past_date = str(past_date)

# данные о компаниях
companies_data = dictOfCompanies.get_companies_data()
# наименования компаний
companies_names = dictOfCompanies.get_companies_names(companies_data)
companies_names_1 = dictOfCompanies.get_companies_names(companies_data)
companies_names_2 = dictOfCompanies.get_companies_names(companies_data)

days_range = list(np.arange(1, 32))
month_range = list(np.arange(1, 13))
year_range = list(np.arange(today_year - 15, today_year + 1))

output_ratio_matrix_vargas = io.StringIO()
output_map_vargas_str = io.StringIO()

lagna_in_znak = None

def company_get_grahic(c_name, graphic_date):
    pass

"""
    periods scrolling
"""
def scroll_periods(days):
    last_date = txt_lastDate.get()
    last_date = datetime.strptime(last_date, FORMAT_DATE)

    ext_dates = txt_nextDate.get()
    ext_dates = datetime.strptime(ext_dates, FORMAT_DATE)

    last_date += timedelta(days=days)
    last_date = last_date.strftime(FORMAT_DATE)
    last_date = str(last_date)
    txt_lastDate.delete(0, END)
    txt_lastDate.insert(0, last_date)

    ext_dates += timedelta(days=days)
    ext_dates = ext_dates.strftime(FORMAT_DATE)
    ext_dates = str(ext_dates)
    txt_nextDate.delete(0, END)
    txt_nextDate.insert(0, ext_dates)

    xxx1_dateCall()


def button_time_scroll_diff_one_year(event):
    scroll_periods(-1092)

def button_time_scroll_diff_one_mmm(event):
    scroll_periods(-91)


def button_time_scroll_diff_three_month(event):
    scroll_periods(-366)

def button_time_scroll_diff_three_mmm(event):
    scroll_periods(-36)


def button_time_scroll_diff_one_month(event):
    scroll_periods(-4400)


def button_time_scroll_add_one_year(event):
    scroll_periods(1092)

def button_time_scroll_add_one_mmm(event):
    scroll_periods(91)

def button_time_scroll_add_three_mmm(event):
    scroll_periods(36)

def button_time_scroll_add_three_month(event):
    scroll_periods(366)


def button_time_scroll_add_one_month(event):
    scroll_periods(4400)


def new_time_date(n_day, n_hour, n_min):
    time_jam = txtTime.get()
    time_jam = datetime.strptime(time_jam, FORMAT_TIME)

    date_jam = txtDate.get()
    date_jam = datetime.strptime(date_jam, FORMAT_DATE)

    tim_dat_jam = datetime(date_jam.year, date_jam.month, date_jam.day, time_jam.hour, time_jam.minute, time_jam.second)
    tim_dat_jam += timedelta(days=n_day, hours=n_hour, minutes=n_min)

    next_time_jam = tim_dat_jam.strftime(FORMAT_TIME)
    next_time_jam = str(next_time_jam)

    next_date_jam = tim_dat_jam.strftime(FORMAT_DATE)
    next_date_jam = str(next_date_jam)

    txtTime.delete(0, END)
    txtTime.insert(0, next_time_jam)

    txtDate.delete(0, END)
    txtDate.insert(0, next_date_jam)

    xxx1_dateCall()


"""
    events buttons datetime
"""


def button_time_add_hour(event):
    new_time_date(0, 1, 0)


def button_time_add_minute(event):
    new_time_date(0, 0, 10)


def button_time_diff_hour(event):
    new_time_date(0, -1, 0)


def button_time_diff_minute(event):
    new_time_date(0, 0, -10)


def button_time_add_day(event):
    new_time_date(1, 0, 0)


def button_time_add_month(event):
    new_time_date(30, 0, 0)


def button_time_diff_day(event):
    new_time_date(-1, 0, 0)


def button_time_diff_month(event):
    new_time_date(-30, 0, 0)


"""
    find burn of time
"""


def find_time_of_burn_func(event):
    find_nbGraphic.place(x=0, y=0)
    tranzit_nbGraphic.place(x=2000, y=26)


"""
    функция вызова поиска времени
"""
def add_new_event(event):

    # date_but = [labl_bfrom_00.cget("text"),labl_bfrom_01.cget("text"),labl_bfrom_02.cget("text"),
    #             labl_bfrom_03.cget("text"),labl_bfrom_04.cget("text"),labl_bfrom_05.cget("text"),
    #             labl_bfrom_06.cget("text"), labl_bfrom_07.cget("text"),labl_bfrom_08.cget("text"),
    #             labl_bfrom_09.cget("text"),labl_bfrom_10.cget("text")]
    #
    # value_buttun = [labl_b_00.cget("text"),labl_b_01.cget("text"),labl_b_02.cget("text"),labl_b_03.cget("text"),
    #                 labl_b_04.cget("text"),labl_b_05.cget("text"),labl_b_06.cget("text"),labl_b_07.cget("text"),
    #                 labl_b_08.cget("text"),labl_b_09.cget("text")]
    #
    # print(value_buttun)

    # value_but_num = []
    date_period = []
    # for perio in np.arange(10):
    #     if value_buttun[perio] == "up":
    #         value_but_num.append(1)
    #     else:
    #         value_but_num.append(0)
    #
    #     date_one = datetime.strptime(date_but[perio], FORMAT_DATE)
    #     date_two = datetime.strptime(date_but[perio + 1], FORMAT_DATE)
    #
    #     date_period.append((date_two - date_one).days)

    # print(date_period, sum(date_period))
    # print(value_but_num)

    max_per_matches = 0
    first_date = txtDate.get()
    first_date = datetime.strptime(first_date, FORMAT_DATE)
    first_date = first_date + timedelta(days=25)
    find_time = datetime(first_date.year, first_date.month, first_date.day)
    list_find.delete(0, 'end')
    d_time = 0
    date_f_best = 0
    time_f_best = 0
    ss_burn = []
    ss_zach = []
    while d_time < 72000:
        d_time += 1
        find_time = find_time - timedelta(minutes=1)
        date_f = str(find_time.strftime(FORMAT_DATE))
        time_f = str(find_time.strftime(FORMAT_TIME))

        new_command = "ANALIS"

        aianamsa = days_name_combobox.get()

        array_prognozPlanet = beginScript.prognoz_inTime(new_command, date_f, time_f,
                                                         txtGTM.get(), txtAltitude.get(),
                                                         txtLongitude.get(), txt_lastDate.get(),
                                                         txt_nextDate.get(), "dasha_yeartable",
                                                         aianamsa)
        time_burn_date = datetime.strptime(date_f + '-' + time_f, FORMAT_DATE + '-' + FORMAT_TIME)
        time_in_zachatie = array_prognozPlanet.time_in_zachatie
        # print(str(time_burn_date),str(time_in_zachatie), str(d_time))
        ss_burn.append(str(time_burn_date))
        ss_zach.append(str(time_in_zachatie))

        if (int(len(ss_burn) / 10000))*10000 == len(ss_burn):
            print('save df')
            df = pd.DataFrame({'burn': ss_burn, 'zach': ss_zach})
            df.to_csv('DATA12345', index_label=False)
        # num_of_matches = calculate_find_time_burn.get_time_find(date_but, date_period, value_but_num, date_f, time_f, txtGTM.get(),
        #                                                         txtAltitude.get(), txtLongitude.get())
        #
        # if num_of_matches > (max_per_matches * .7):
        #     if num_of_matches > max_per_matches:
        #         max_per_matches = num_of_matches
        #         date_f_best = date_f
        #         time_f_best = time_f
        #         # find_time = find_time + timedelta(seconds=100)
        #     print("complete:  " + str(math.trunc(d_time / 5000000
        #                                          * 100)) + " %", date_f, time_f, num_of_matches, max_per_matches, "best:", date_f_best, time_f_best)
        # else:
        #     find_time = find_time - timedelta(seconds=300)


"""
    calling grafics functions
"""


def xxx1_dateCall():
    xxx = 1
    button_lastDate_clicked(xxx)


def xxx2_dateCall():
    xxx = 2
    button_lastDate_clicked(xxx)


def button_lastDate_clicked(xxx):
    t0 = datetime.today()
    # print("----", graphic_name_combobox.get())

    global delta
    aianamsa = days_name_combobox.get()
    if aianamsa == 'lahiri':delta = 0
    elif aianamsa == 'surya siddhanta':delta = SURIA_SIDDHANTA_AINAMSHA

    if graphic_name_combobox.get() == NAME_GRAPHICS[OUTPUT_DATA]:
        # print()
        # print("Start!")


        beginScriptOutData.prognoz_inTime_data(new_command, txtDate.get(), txtTime.get(),
                                                         txtGTM.get(), txtAltitude.get(),
                                                         txtLongitude.get(), txt_lastDate.get(),
                                                         txt_nextDate.get(), graphic_name_combobox.get(),
                                                         aianamsa)
        # print()
        print("Complite!")
        xxx=0
    name_graphics = graphic_name_combobox.get()

    if (xxx == 1) and name_graphics == NAME_GRAPHICS[PLAN_BABY]:
        baby_nbGraphic.place(x=-180, y=30)

        canvasAgg_baby.draw()
        canvas_baby = canvasAgg_baby.get_tk_widget()
        canvas_baby.pack(fill=BOTH, expand=1)
        frm_baby.pack(fill=BOTH, expand=1)
    else:
        baby_nbGraphic.place(x=2400, y=30)

    if (xxx == 1) and name_graphics in [NAME_GRAPHICS[HOROSCOP], NAME_GRAPHICS[DASHA_YEARTABLE]]:
        newWindow.title(company_name_combobox.get())
        ax.cla()
        fig.canvas.draw()
        fig.canvas.flush_events()

        array_prognozPlanet = beginScript.prognoz_inTime(new_command, txtDate.get(), txtTime.get(),
                                                         txtGTM.get(), txtAltitude.get(),
                                                         txtLongitude.get(), txt_lastDate.get(),
                                                         txt_nextDate.get(), graphic_name_combobox.get(),
                                                         aianamsa)

        t1 = datetime.today()
        txtDateqLast = txt_lastDate.get()
        txtDateqNext = txt_nextDate.get()
        txtDateqLast = datetime.strptime(txtDateqLast, FORMAT_DATE)
        txtDateqNext = datetime.strptime(txtDateqNext, FORMAT_DATE)

        array_dashaRatioX = array_prognozPlanet.general_OXresult

        speed_planet_tranzit_days = array_prognozPlanet.speed_planet_tranzit_days

        OX_coords = array_prognozPlanet.OX_coords
        OY_coords = array_prognozPlanet.OY_coords

        graha_in_degrees = array_prognozPlanet.graha_in_degrees

        baby_sa_ju = array_prognozPlanet.baby_sa_ju

        number_of_yogas = array_prognozPlanet.number_of_yogas

        obmen_znakami = array_prognozPlanet.obmen_znakami

        data_snp500 = array_prognozPlanet.data_snp500
        data_snp500_ = []
        for data_snp in data_snp500:
            if data_snp == -1: continue
            else: data_snp500_.append(data_snp)

        if len(data_snp500_):
            snp500_max, snp500_min = max(data_snp500_), min(data_snp500_)
            data_snp500 = (np.array(data_snp500) - snp500_min) * 100 / (snp500_max - snp500_min)

        global retrogr_planet
        retrogr_planet = array_prognozPlanet.retrogr_planet

        phase_moon = array_prognozPlanet.phase_moon
        scala_time = array_prognozPlanet.general_OZresult

        tr_maha_dasha = array_prognozPlanet.general_maha_dasha
        tr_antar_dasha = array_prognozPlanet.general_antar_dasha
        tr_pratia_dasha = array_prognozPlanet.general_pratia_dasha

        event_for_maha = array_prognozPlanet.event_for_maha
        event_for_antar = array_prognozPlanet.event_for_antar
        event_for_pratia = array_prognozPlanet.event_for_pratia

        dr_planets = array_prognozPlanet.whole_drekkana
        dr_drekkans = array_prognozPlanet.planets_parts_of_body
        dr_bab_balls = array_prognozPlanet.break_parts_of_body_balls

        planets_in_degrees_transit = array_prognozPlanet.planets_in_degrees_transit

        value_joga = array_prognozPlanet.value_joga

        ratio_of_good_planet = array_prognozPlanet.ratio_of_good_planet
        ratio_of_good_bhavas = array_prognozPlanet.ratio_of_good_bhavas
        polojenie_lagna_rashi = array_prognozPlanet.polojenie_lagna_rashi

        time_in_zachatie = array_prognozPlanet.time_in_zachatie
        days_in_utroba = array_prognozPlanet.days_in_utroba

        data_level_Sa_Ju = array_prognozPlanet.data_level_Sa_Ju

        planets_in_znak = array_prognozPlanet.planets_in_znak
        coef_relations = array_prognozPlanet.coef_relations
        trazit_retrograd = array_prognozPlanet.trazit_retrograd

        scores_rajya = array_prognozPlanet.scores_rajya

        ashtaka_varga = array_prognozPlanet.ashtaka_varga
        sarva_ashtaka = array_prognozPlanet.sarva_ashtaka

        bhava_aspects_rashi = array_prognozPlanet.bhava_aspects_rashi

        num_exalt_planets_days = array_prognozPlanet.num_exalt_planets_days
        light_transit_tr = array_prognozPlanet.light_transit_tr

        map_vargas = array_prognozPlanet.map_vargas
        ratio_matrix_vargas = array_prognozPlanet.ratio_matrix_vargas
        moon_in_nakshatra = array_prognozPlanet.moon_in_nakshatra

        words_base_astrology = array_prognozPlanet.words_base_astrology

        scores = array_prognozPlanet.scores

        ratio_matrix_vargas_str = str(ratio_matrix_vargas)
        map_vargas_str = str(map_vargas)
        ratio_matrix_vargas_str = ratio_matrix_vargas_str[1:-1]   #[1:(len(ratio_matrix_vargas_str) - 1)]
        map_vargas_str = map_vargas_str[1:-1]  #[1:(len(map_vargas_str) - 1)]
        planets_in_avasths = array_prognozPlanet.planets_in_avasths

        global output_ratio_matrix_vargas
        global output_map_vargas_str

        global lagna_in_znak

        output_ratio_matrix_vargas.close()
        output_map_vargas_str.close()

        output_ratio_matrix_vargas = io.StringIO()
        output_map_vargas_str = io.StringIO()

        output_ratio_matrix_vargas.write(ratio_matrix_vargas_str)
        output_map_vargas_str.write(map_vargas_str)

        lagna_in_znak = polojenie_lagna_rashi

        """
            добавление данных по трактовкам гороскопа
        """
        ax_t.cla()
        ax_t.axis('off')
        ax_t.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_t.plot(400, 1900, '-b', linewidth=0.1, markersize=0)

        ylen = 2

        if name_graphics == NAME_GRAPHICS[HOROSCOP]:
            for y, keyn in enumerate(words_base_astrology.keys()):
                oy_crd = 2000 - y * 6

                ax_t.text(0, oy_crd, keyn, color="black", size=8)

                nx = -110

                yfill = [oy_crd - ylen + 1, oy_crd - ylen + 1, oy_crd + ylen + 1, oy_crd + ylen + 1]

                for key_planet in words_base_astrology[keyn].keys():

                    if key_planet == 'Sum': continue
                    count_per = words_base_astrology[keyn][key_planet]

                    xfill = [nx, nx + count_per, nx + count_per, nx]
                    color_k = COLOR_PLANET_DICT[key_planet]

                    ax_t.fill(xfill, yfill, color=color_k)

                    nx += count_per

        canvasAgg_t.draw()
        canvas_t = canvasAgg_t.get_tk_widget()
        canvas_t.pack(fill=BOTH, expand=1)

        canvas_box.create_window(0, 0, window=frame_t, anchor='nw')
        good_planets_nbGraphic.update()
        canvas_box.config(scrollregion=(0, 1550, 1000, 8500))



        """
            Построение карт
        """

        ax_sud.cla()
        ax_nat.cla()
        ax_nat.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_nat.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        min_sarva_ashtaka = min(sarva_ashtaka)
        max_sarva_ashtaka = max(sarva_ashtaka)

        for bhava, coords in enumerate(COORDS_BHAVAS):
            if sarva_ashtaka[bhava] < 24:
                x_, y_ = [], []
                for x, y in coords:
                    x_.append(x)
                    y_.append(y)
                ax_nat.fill(x_, y_, color='red', alpha=.1)
            elif sarva_ashtaka[bhava] > 29:
                x_, y_ = [], []
                for x, y in coords:
                    x_.append(x)
                    y_.append(y)
                ax_nat.fill(x_, y_, color='green', alpha=.3)

            if sarva_ashtaka[bhava] == min_sarva_ashtaka and min_sarva_ashtaka >= 24:
                x_, y_ = [], []
                for x, y in coords:
                    x_.append(x)
                    y_.append(y)
                ax_nat.fill(x_, y_, color='orange', alpha=.3)
            elif sarva_ashtaka[bhava] == max_sarva_ashtaka and max_sarva_ashtaka <= 29:
                x_, y_ = [], []
                for x, y in coords:
                    x_.append(x)
                    y_.append(y)
                ax_nat.fill(x_, y_, color='blue', alpha=.5)

        for i in MAP_RANGE:
            l = mlines.Line2D([BRILLANT_MAP_X[i * 2], BRILLANT_MAP_X[i * 2 + 1]],
                              [BRILLANT_MAP_Y[i * 2], BRILLANT_MAP_Y[i * 2 + 1]], linewidth=1.0)
            l.set_color("blue")
            ax_nat.add_line(l)

        l = mlines.Line2D(COORDS_BHAVAS_X, COORDS_BHAVAS_Y, linewidth=1.0)
        l.set_color("blue")
        ax_nat.add_line(l)

        for nm in ASPECTS_RANGE:

            n = int(nm / 7)

            n_aspect = np.fmod(nm, 7)
            if retrogr_planet[n] == 1:
                if n_aspect in [1, 2, 3]: continue
            if retrogr_planet[n] == 0:
                if n_aspect in [4, 5, 6]: continue

            house = math.trunc(bhava_aspects_rashi[nm] / DEGREES_IN_ZNAK)
            i = (bhava_aspects_rashi[nm] - (house * DEGREES_IN_ZNAK)) * 3

            point_OX = COORDS_BHAVAS_X[house]
            point_OY = COORDS_BHAVAS_Y[house]
            radius = 14 + (n * 1.5)
            angle = ANGLES[house]

            if next_range[house] == 0:
                x = (radius * math.sin(math.radians(i + angle))) + point_OX
                y = (radius * math.cos(math.radians(i + angle))) + point_OY
            else:
                x = (radius * math.cos(math.radians(i + angle))) + point_OX
                y = (radius * math.sin(math.radians(i + angle))) + point_OY

            delta_OX = DELTA_OX_TEXT[house]
            delta_OY = DELTA_OY_TEXT[house]

            if (int(nm / 7)) == (nm / 7):
                ax_nat.text(x + delta_OX - .4, y + delta_OY - .4, NAME_PLANETS[n], color="black",
                            size=8)
                ax_nat.text(x + delta_OX, y + delta_OY, NAME_PLANETS[n], color=COLOR_PLANET[n], size=8)

                l = mlines.Line2D([x, x + .1], [y, y + .1], linewidth=3)
                l.set_color("black")
                ax_nat.add_line(l)
            else:
                l = mlines.Line2D([x, x + .1], [y, y + .1], linewidth=1)
                l.set_color("gray")
                ax_nat.add_line(l)
                ax_nat.text(x + delta_OX - .4, y + delta_OY - .4, NAME_PLANETS[n], color="gray",
                            size=8)
                ax_nat.text(x + delta_OX, y + delta_OY, NAME_PLANETS[n], color=COLOR_PLANET_ASPECT[n], size=8)

        """
            информация о домах
        """

        ax_inf.cla()
        ax_inf.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_inf.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        for i in PLANETS_RANGE:
            oy = 100 - i * 12.3
            l = mlines.Line2D([0, ratio_of_good_planet[i] + 1], [oy, oy], linewidth=15.0, alpha=.5)
            l.set_color(COLOR_PLANET[i])
            ax_inf.add_line(l)
            avastha_name = LIST_AVASTH_NAME[planets_in_avasths[i]]
            ax_inf.text(1, oy-2, avastha_name, size=8)

        ax_bh.cla()
        ax_bh.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_bh.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        for i in ZODIAK_RANGE:
            number_znak = int(math.fmod((polojenie_lagna_rashi[0] + i), ZNAKS_IN_ZODIAK))
            number_znak_sud = int(math.fmod((polojenie_lagna_rashi[1] + i), ZNAKS_IN_ZODIAK))
            OX = HOUSE_OX[i]
            OY = HOUSE_OY[i]

            ax_nat.text(OX + DELTA_P[number_znak], OY, str(number_znak + 1), color="black", size=10)
            ax_nat.text(OX + .4 + DELTA_P[number_znak], OY + .4, str(number_znak + 1),
                        color=COLOR_ELEMENTS_ZNAK[number_znak], size=10)

            ax_sud.text(OX + DELTA_P[number_znak_sud], OY, str(number_znak_sud + 1), color="black", size=10)
            ax_sud.text(OX + .4 + DELTA_P[number_znak_sud], OY + .4, str(number_znak_sud + 1),
                        color=COLOR_ELEMENTS_ZNAK[number_znak_sud], size=10)



            l = mlines.Line2D([i * 9, i * 9], [0, ratio_of_good_bhavas[number_znak] + 1], linewidth=10.0)
            l.set_color(COLOR_ZNAK[number_znak])
            ax_bh.text(i * 9 - 1.5, 0, str(number_znak + 1), color="black", size=6)
            ax_bh.text(i * 9 - 1.5, 100, str(i + 1), color="black", size=9)
            ax_bh.add_line(l)

        for na in np.arange(18):
            ax_bh.text(106, na * 5.26+5.26, VARGA_TXT[na], size=8)
        """
            построение легенды по обозначении йог
        """
        ax_sud.cla()
        ax_sud.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_sud.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        time_in_zachatie_str = 'время зачатия ' + str(time_in_zachatie)
        days_in_utroba_str = 'дней проведенных в лоне ' + str(days_in_utroba)
        moon_in_nakshatra_str = 'луна в накшатре ' + str(NAME_NAKSHATRAS[int(moon_in_nakshatra)]) + ' #' + str(int(moon_in_nakshatra))
        info_gradus_planets_str = 'Информация по планетам:'

        for planet, degrees in enumerate(graha_in_degrees[0:9]):
            degree_str = str(round(degrees/3600, 1))

            info_gradus_planets_str += '\n' + NAME_PLANETS_DREK[planet] + ' - ' + degree_str + '°'

        ax_sud.text(0, 48, info_gradus_planets_str, size=8)

        ax_sud.text(0, 16, moon_in_nakshatra_str, size=8)
        ax_sud.text(0, 8, days_in_utroba_str, size=8)
        ax_sud.text(0, 0, time_in_zachatie_str, size=8)


        joga_unique = np.unique(value_joga)[1:]
        for poz, jog in enumerate(joga_unique):
            l = mlines.Line2D([5, 15], [95 - poz * 9, 95 - poz * 9], linewidth=5)
            l.set_color(JOGA_COLOR[jog[0]])
            ax_sud.add_line(l)
            ax_sud.text(20, 95 - poz * 9, NAME_JOGA[jog[0]], size=8)

        """
            построение проблем в физическом теле
        """
        ax_peo.cla()
        ax_peo.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_peo.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        l = mlines.Line2D(COUNTER_MAN_OX_1, COUNTER_MAN_OY_1, linewidth=1.0)
        ax_peo.add_line(l)
        l = mlines.Line2D(COUNTER_MAN_OX_2, COUNTER_MAN_OY_2, linewidth=1.0)
        ax_peo.add_line(l)
        l = mlines.Line2D(COUNTER_MAN_OX_1_0, COUNTER_MAN_OY_1, linewidth=1.0)
        ax_peo.add_line(l)
        l = mlines.Line2D(COUNTER_MAN_OX_2_0, COUNTER_MAN_OY_2, linewidth=1.0)
        ax_peo.add_line(l)

        """
            проецирование планет на части тела
        """
        planet_of_part_people = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                                 [], [], [], [], [],
                                 [], [], [], [], [], [], [], [], []]
        for i in PLANETS_RANGE:
            oy = i * 12.2
            ax_peo.text(0, oy, NAME_PLANETS_DREK[i], rotation=0, size=8)

            OXX = DREKKANA_OX[dr_planets[i]]
            OYY = DREKKANA_OY[dr_planets[i]]
            l = mlines.Line2D([8, OXX], [oy, OYY], linewidth=0.5)
            l.set_color(COLOR_ELEMENTS_PLANETS[i])
            ax_peo.add_line(l)

            l = mlines.Line2D([OXX, OXX + .5], [OYY, OYY + .5], linewidth=2.0)
            ax_peo.add_line(l)

            planet_of_part_people[dr_planets[i]].append(i)

            for pp in np.arange(36):
                if dr_drekkans[pp] == i:
                    OXX = DREKKANA_OX[pp]
                    OYY = DREKKANA_OY[pp]
                    l = mlines.Line2D([8, OXX], [oy, OYY], linewidth=0.5)
                    l.set_color(COLOR_ELEMENTS_PLANETS[i])
                    ax_peo.add_line(l)

                    l = mlines.Line2D([OXX, OXX + .5], [OYY, OYY + .5], linewidth=2.5)
                    ax_peo.add_line(l)

                    planet_of_part_people[pp].append(dr_drekkans[pp])

        if name_graphics == NAME_GRAPHICS[HOROSCOP]:
            # распределим очередность заполнения полей
            next_p1, next_p2, next_p3 = [], [], []
            for pp in np.arange(36):
                if dr_bab_balls[pp] <= 30:
                    next_p1.append(pp)
                elif 30 < dr_bab_balls[pp] <= 60:
                    next_p2.append(pp)
                else:
                    next_p3.append(pp)

                l = mlines.Line2D([54, 54], [0, 100], linewidth=5.0)
                l.set_color(LEVEL_COLOR[0])
                ax_peo.add_line(l)

                if len(planet_of_part_people[pp]) > 0:
                    for oo in np.arange(len(planet_of_part_people[pp])):
                        plant = planet_of_part_people[pp][oo]
                        oo_text = NAME_PLANETS_DREK[plant]
                        ax_peo.text(58 + (plant * 5), DREKKANA_OY[pp], oo_text, color=COLOR_PLANET[SATURN_PLANET_NUMBER],
                                    size=5)

            for i in next_p2:
                l = mlines.Line2D([54, 54], [DREKKANA_OY[i] - 1, DREKKANA_OY[i] + 1], linewidth=5.0)
                l.set_color(LEVEL_COLOR[1])
                ax_peo.add_line(l)

                l = mlines.Line2D([DREKKANA_OX[i], DREKKANA_OX[i] + .5], [DREKKANA_OY[i], DREKKANA_OY[i] + .5],
                                  linewidth=2.5)
                l.set_color(LEVEL_COLOR[1])
                ax_peo.add_line(l)

            for i in next_p3:
                l = mlines.Line2D([54, 54], [DREKKANA_OY[i] - 1, DREKKANA_OY[i] + 1], linewidth=5.0)
                l.set_color(LEVEL_COLOR[2])
                ax_peo.add_line(l)

                l = mlines.Line2D([DREKKANA_OX[i], DREKKANA_OX[i] + .5], [DREKKANA_OY[i], DREKKANA_OY[i] + .5],
                                  linewidth=2.5)
                l.set_color(LEVEL_COLOR[2])
                ax_peo.add_line(l)
            t2 = datetime.today()
        """
            построение графиков
        """

        ymini, ymaxi = ax_inf.get_ybound()
        ax_inf.text(50, ymaxi, "СИЛА ПЛАНЕТ", rotation=0, size=10, horizontalalignment='center', verticalalignment='bottom')
        ymini, ymaxi = ax_bh.get_ybound()
        ax_bh.text(50, ymaxi, "СИЛА СФЕР ЖИЗНИ", rotation=0, size=10, horizontalalignment='center', verticalalignment='bottom')
        ymini, ymaxi = ax_peo.get_ybound()
        ax_peo.text(50, ymaxi, "ПРЕДРАСПОЛОЖЕННОСТИ", rotation=0, size=10, horizontalalignment='center', verticalalignment='bottom')
        ymini, ymaxi = ax_nat.get_ybound()
        ax_nat.text(50, ymaxi, "НАТАЛЬНАЯ КAРТА", rotation=0, size=10, horizontalalignment='center', verticalalignment='bottom')
        ymini, ymaxi = ax_sud.get_ybound()
        ax_sud.text(50, ymaxi, "ЙОГИ", rotation=0, size=10, horizontalalignment='center', verticalalignment='bottom')

        ax.cla()

        lenght_graphic = len(scala_time) - 2

        if graphic_name_combobox.get() != "no graphics":

            ax.plot(np.min(OX_coords), np.min(OY_coords), '-b', linewidth=0.5, markersize=0)
            ax.plot(np.max(OX_coords), np.max(OY_coords), '-b', linewidth=0.5, markersize=0)

            ymin, ymax = ax.get_ybound()

            ax.plot(0, ymin - (ymax - ymin) * .15, '-b', linewidth=0.5, markersize=0)
            xmin, xmax = ax.get_xbound()
            ymin, ymax = ax.get_ybound()
            ymean = (ymax + ymin)/3

            ax_legend.plot(0, ymin, '-w', linewidth=0.5, markersize=0)
            ax_legend.plot(1, ymax, '-w', linewidth=0.5, markersize=0)

            label_company = str(company_name_combobox.get()) + "     " + str(txtDate.get()) + "     " + str(
                txtTime.get()) + "     GTM:" + str(
                txtGTM.get()) + "     Alt:" + str(txtAltitude.get()) + "     Long:" + str(txtLongitude.get())
            ax.text(0, ymax + (ymax - ymin) * 0.02,
                    "     Period: " + str(txt_lastDate.get()) + " - " + str(txt_nextDate.get()), size=15)
            ax.text(0, ymax + (ymax - ymin) * 0.10, label_company, rotation=0, size=10)
            lock = True

            ax.text(xmin + (xmax - xmin) * 0.005, ymin + (ymax - ymin) * 0.97, scala_time[0].tm_year,
                    rotation=ROTATE_LABEL, size=10)
            ax.text(xmin + (xmax - xmin) * 0.025, ymin + (ymax - ymin) * 0.95,
                    NAME_MONTH[int(scala_time[0].tm_mon) - 1], rotation=0,
                    size=8)

            up_line = .945
            koef_line = .024

            OX_OY = list(map(lambda x: ymin + (ymax - ymin) * (up_line - koef_line * x), np.arange(int(up_line/koef_line))))
            len_ = abs(OX_OY[12] - OX_OY[13]) / 2
            ratio_q = (ymax - ymin) * 0.010
            lx = -14

            if name_graphics == NAME_GRAPHICS[HOROSCOP]:

                ax.text(lx, OX_OY[-1] - ratio_q, "пратья", rotation=0, size=6)
                ax.text(lx, OX_OY[-2] - ratio_q, "антар", rotation=0, size=6)
                ax.text(lx, OX_OY[-3] - ratio_q, "маха", rotation=0, size=6)

                ax.text(lx, OX_OY[0] - ratio_q, "взлеты", rotation=0, size=6)

                ax.text(lx, OX_OY[18] - ratio_q, "силаD1", rotation=0, size=6)
                ax.text(lx, OX_OY[19] - ratio_q, "лучи", rotation=0, size=6)

                ax.text(lx, OX_OY[23] - ratio_q, "йоги", rotation=0, size=6)
                ax.text(lx, OX_OY[24] - ratio_q, "Su варги", rotation=0, size=6)
                ax.text(lx, OX_OY[25] - ratio_q, "Mo варги", rotation=0, size=6)
                ax.text(lx, OX_OY[26] - ratio_q, "Ma варги", rotation=0, size=6)
                ax.text(lx, OX_OY[27] - ratio_q, "Ju варги", rotation=0, size=6)
                ax.text(lx, OX_OY[28] - ratio_q, "Ve варги", rotation=0, size=6)
                ax.text(lx, OX_OY[29] - ratio_q, "Sa варги", rotation=0, size=6)


            for new_time in np.arange(2, lenght_graphic)[:-3]:

                len_ = abs(OX_OY[12] - OX_OY[13])/2
                len_ox = OX_coords[new_time] - OX_coords[new_time - 1]
                xfill = [OX_coords[new_time], OX_coords[new_time] + len_ox, OX_coords[new_time] + len_ox, OX_coords[new_time]]

                if name_graphics == NAME_GRAPHICS[DASHA_YEARTABLE]:
                    # """
                    #     Вывод данных параметров дня по слепкам и эталону
                    # """
                    # score = scores[new_time]
                    # if score != scores[new_time-1]:
                    #     if score > 1:
                    #         color_k, oy_crd = 'blue', OX_OY[36]
                    #         len_2 = abs(OX_OY[20] - OX_OY[18])
                    #         yfill = [oy_crd - len_2, oy_crd - len_2, oy_crd + len_2, oy_crd + len_2]
                    #         ax.fill(xfill, yfill, color=color_k)
                    #     elif score > 0:
                    #         color_k, oy_crd = 'green', OX_OY[36]
                    #         len_2 = abs(OX_OY[20] - OX_OY[18])
                    #         yfill = [oy_crd - len_2, oy_crd - len_2, oy_crd + len_2, oy_crd + len_2]
                    #         ax.fill(xfill, yfill, color=color_k, alpha=.6)

                    # """
                    #     Обозначение скоростей планет на графиках в процентах
                    # """
                    # speed_sums_next = speed_planet_tranzit_days[new_time][SATURN_PLANET_NUMBER] - speed_planet_tranzit_days[new_time][JUPITER_PLANET_NUMBER]
                    # speed_sums_last = speed_planet_tranzit_days[new_time - 1][SATURN_PLANET_NUMBER] - speed_planet_tranzit_days[new_time - 1][JUPITER_PLANET_NUMBER]
                    #
                    # # Набор планет для подсчета суммарной скорости
                    # sp_1 = (speed_sums_next - MIN_SPEED_PLANETS[JUPITER_PLANET_NUMBER]) / (
                    #         MAX_SPEED_PLANETS[JUPITER_PLANET_NUMBER] - MIN_SPEED_PLANETS[JUPITER_PLANET_NUMBER])
                    # sp_2 = (speed_sums_last - MIN_SPEED_PLANETS[JUPITER_PLANET_NUMBER]) / (
                    #         MAX_SPEED_PLANETS[JUPITER_PLANET_NUMBER] - MIN_SPEED_PLANETS[JUPITER_PLANET_NUMBER])
                    #
                    # color_k, oy_crd = 'lightgreen', OX_OY[25]
                    # len_sp = abs(OX_OY[20] - OX_OY[10])
                    # ax.plot([new_time-1, new_time], [sp_2 * len_sp + oy_crd, sp_1 * len_sp + oy_crd], color='black')

                    # """
                    #     Обозначение титхи Юпитер - Сатурн
                    # """
                    # angle = calculateDistansePlanets_scale(
                    #                                     Planet1=planets_in_degrees_transit[new_time][JUPITER_PLANET_NUMBER],
                    #                                     Planet2=planets_in_degrees_transit[new_time][SATURN_PLANET_NUMBER],
                    #                                     scale=SECONDS_IN_ZODIAC
                    # )
                    #
                    # jupiter_tithi = int(np.fmod(angle / 43200, 15))
                    #
                    # color_k = ['gold', 'gray', 'red', 'limegreen', 'darkorange', 'hotpink', '#8500ff', 'blue',
                    #            'darkred', 'y', 'black', 'orangered', 'lime', 'goldenrod', 'deeppink'][jupiter_tithi]
                    #
                    # oy_crd = OX_OY[5]
                    # yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    # ax.fill(xfill, yfill, color=color_k)


                    # """
                    #     Phases if MOON
                    # """
                    # for npl, planets in enumerate(PHASE_PLANETS):
                    #
                    #     if phase_moon[new_time-1][npl] != phase_moon[new_time][npl]:
                    #
                    #         if phase_moon[new_time][npl] == 3:
                    #             yyy = OX_OY[26 + npl]
                    #             ax.plot([OX_coords[new_time], OX_coords[new_time]],[ymin, ymax], color='green', alpha=.6)
                    #             ax.plot(OX_coords[new_time], yyy, marker='o', markersize=8, color=COLOR_PLANET[MOON_PLANET_NUMBER])
                    #
                    #         elif phase_moon[new_time][npl] == 4:
                    #             yyy = OX_OY[14 + npl]
                    #             ax.plot([OX_coords[new_time], OX_coords[new_time]], [ymin, ymax], color='green', alpha=.4, linewidth=0.2)
                    #             ax.plot(OX_coords[new_time], yyy, marker='o', markersize=8, color=COLOR_PLANET[MOON_PLANET_NUMBER])
                    #             ax.plot(OX_coords[new_time] + (OX_coords[new_time] - OX_coords[new_time-1])*.3, yyy, marker='o', markersize=7, color='white')
                    #
                    #         elif phase_moon[new_time][npl] == 1:
                    #             yyy = OX_OY[2 + npl]
                    #             ax.plot([OX_coords[new_time], OX_coords[new_time]], [ymin, ymax], color='green', alpha=.6)
                    #             ax.plot(OX_coords[new_time], yyy, marker='o', markersize=8, color=COLOR_PLANET[MOON_PLANET_NUMBER])
                    #             ax.plot(OX_coords[new_time], yyy, marker='o', markersize=7, color='white')
                    #
                    #         elif phase_moon[new_time][npl] == 2:
                    #             yyy = OX_OY[14 + npl]
                    #             ax.plot([OX_coords[new_time], OX_coords[new_time]], [ymin, ymax], color='green', alpha=.4, linewidth=0.2)
                    #             ax.plot(OX_coords[new_time], yyy, marker='o', markersize=8, color=COLOR_PLANET[MOON_PLANET_NUMBER])
                    #             ax.plot(OX_coords[new_time] - (OX_coords[new_time] - OX_coords[new_time-1])*.3, yyy, marker='o', markersize=7, color='white')
                    #
                    #     if phase_moon[new_time][npl] in [1,2]:
                    #         color_k = 'gray'
                    #         yfill = [ymax, ymax, ymin, ymin]
                    #         ax.fill(xfill, yfill, color=color_k, alpha=.1)

                    """
                        Вывод данных о Юпитере, влияния о него
                    """
                    # delta_rel = []
                    # for num, rel in enumerate(coef_relations[new_time]):
                    #     point_1 = (oy_coords_max - coef_relations[new_time-1][num]) / (oy_coords_max - oy_coords_min)*ymax
                    #     point_2 = (oy_coords_max - coef_relations[new_time][num]) / (oy_coords_max - oy_coords_min)*ymax
                    #
                    #     if point_1 != point_2: delta_rel.append(1)
                    #
                    #     l = mlines.Line2D([OX_coords[new_time], OX_coords[new_time], OX_coords[new_time]+len_ox],
                    #                       [point_1, point_2, point_2], linewidth=1.0)
                    #     l.set_color(COLOR_PLANET[num])
                    #     ax.add_line(l)

                    """
                        Вывод ретроградности Юпитера и Меркурия
                    """
                    delta_rel = []
                    planets = [MARS_PLANET_NUMBER, MERCURY_PLANET_NUMBER, JUPITER_PLANET_NUMBER,
                               VENUS_PLANET_NUMBER, SATURN_PLANET_NUMBER]
                    colols = ['tomato', 'mediumseagreen', 'goldenrod', 'orchid', 'deepskyblue']

                    for n_planet, planet_ in enumerate(planets):
                        point_1 = trazit_retrograd[new_time][planet_]
                        point_2 = trazit_retrograd[new_time-1][planet_]
                        if point_1 != point_2: delta_rel.append(1)

                        if point_2 == 1:
                            color_k, oy_crd = colols[n_planet], OX_OY[2+n_planet]
                            yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                            ax.fill(xfill, yfill, color=color_k)

                    """
                        Вывод смены планеты знака
                    """
                    # if len(delta_rel) > 0:
                    #     color_k, oy_crd = 'black', OX_OY[28]
                    #     yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    #     ax.fill(xfill, yfill, color=color_k)

                    """
                        Вывод реальных кризисных данных
                    """
                    if data_snp500[new_time - 1] >= 0 and data_snp500[new_time] >= 0:

                        ysnp_1 = (data_snp500[new_time - 1])*ymax/100
                        ysnp_2 = (data_snp500[new_time]*ymax/100)

                        if ysnp_1 > ysnp_2:
                            color_k = 'red'
                            yfill = [ysnp_1, ysnp_1, ysnp_2, ysnp_2]
                            ax.fill(xfill, yfill, color=color_k, alpha=.8)
                        else:
                            color_k = 'green'
                            yfill = [ysnp_1, ysnp_1, ysnp_2, ysnp_2]
                            ax.fill(xfill, yfill, color=color_k, alpha=.8)


                if name_graphics == NAME_GRAPHICS[HOROSCOP]:

                    """
                        обозначение махадаш
                    """
                    oy_crd = OX_OY[-3]
                    yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    ax.fill(xfill, yfill, color=COLOR_PLANET[tr_maha_dasha[new_time]])

                    if event_for_maha[new_time] != 0:
                        if int(new_time / 2)*2 == new_time:
                            ax.fill(xfill, yfill, color='black', alpha=event_for_maha[new_time])
                        else:
                            ax.fill(xfill, yfill, color='white', alpha=event_for_maha[new_time])

                    """
                        обозначение антардаш
                    """
                    oy_crd = OX_OY[-2]
                    yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    ax.fill(xfill, yfill, color=COLOR_PLANET[tr_antar_dasha[new_time]])

                    if event_for_antar[new_time] != 0:
                        if int(new_time / 2) * 2 == new_time:
                            ax.fill(xfill, yfill, color='black', alpha=event_for_antar[new_time])
                        else:
                            ax.fill(xfill, yfill, color='white', alpha=event_for_antar[new_time])

                    """
                        обозначение пратьядаш
                    """
                    oy_crd = OX_OY[-1]
                    yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    ax.fill(xfill, yfill, color=COLOR_PLANET[tr_pratia_dasha[new_time]])

                    if event_for_pratia[new_time] != 0:
                        if int(new_time / 2) * 2 == new_time:
                            ax.fill(xfill, yfill, color='black', alpha=event_for_pratia[new_time])
                        else:
                            ax.fill(xfill, yfill, color='white', alpha=event_for_pratia[new_time])


                    """
                        построение времени действия йог
                    """
                    if new_time < len(value_joga):
                        joga_planet = [value_joga[new_time]]
                        for plan in np.arange(len(joga_planet)):
                            oy_crd = OX_OY[23 - plan]

                            if len(joga_planet[plan]) > 0:
                                yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                                ax.fill(xfill, yfill, color=JOGA_COLOR[joga_planet[plan][0]])

                    """
                        построение обмена между планетами
                    """
                    for ncolor, planet_str in enumerate(NAME_PLANETS_DREK):

                        try:
                            if obmen_znakami[planet_str][new_time] == 1:
                                oy_crd = OX_OY[ncolor + 9]
                                yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                                ax.fill(xfill, yfill, color=COLOR_PLANET[ncolor])
                        except:
                            pass

                    # """
                    #     построение раджа йог
                    # """
                    # try:
                    #     if scores_rajya[new_time] >= 2:
                    #         oy_crd = OX_OY[4]
                    #         ncolor = ['', '', 'yellow', 'aqua', 'green', 'violet', 'black', 'black', 'black'][scores_rajya[new_time]]
                    #         yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    #         ax.fill(xfill, yfill, color=ncolor)
                    # except:
                    #     pass


            for new_time in np.arange(1, lenght_graphic):
                ox_line = array_dashaRatioX[new_time]
                ox_line_l = array_dashaRatioX[new_time - 1]

                len_ox = OX_coords[new_time] - OX_coords[new_time - 1]
                xfill = [OX_coords[new_time], OX_coords[new_time] + len_ox, OX_coords[new_time] + len_ox,
                         OX_coords[new_time]]

                delta_line_mon = ox_line + abs(ox_line_l - ox_line)

                if name_graphics == NAME_GRAPHICS[HOROSCOP]:
                    """
                        Отображение двойного транзита Sa и Ju на 10ю бхаву
                    """

                    # for pol in [0,1]:
                    #     if data_level_Sa_Ju[new_time][pol] > 0:
                    #             collor = COLOR_CLASS_NY[pol][data_level_Sa_Ju[new_time][pol]]
                    #             oy_crd = OX_OY[pol]
                    #             yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    #             ax.fill(xfill, yfill, color=collor)
                    #
                    # if len(light_transit_tr) > 0 and len(num_exalt_planets_days) > 0:
                    #
                    #     """
                    #         Обозначение Д1 Д9 лучшие положения планет
                    #     """
                    #     oy_crd = OX_OY[18]
                    #     yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    #     x_color = num_exalt_planets_days[new_time]*2
                    #     if x_color > xmax_color: x_color = xmax_color
                    #     ax.fill(xfill, yfill, color=COLOR_CLASS_BRN[0][x_color])
                    #
                    #     oy_crd = OX_OY[19]
                    #     yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    #     x_color = light_transit_tr[new_time] ** 3 / 6000
                    #     if x_color > xmax_color: x_color = xmax_color
                    #     ax.fill(xfill, yfill, color=COLOR_CLASS_BRN[0][int(x_color)])
                    #

                    """
                        планета на участке в знаке, который более 29 рекх или менее
                    """
                    for plan in np.arange(NUMBER_OF_GRAHAS):
                        oy_crd = OX_OY[24 + plan]
                        yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                        ax.fill(xfill, yfill,
                                color=COLOR_ASHTAKA[plan][COLOR_INDEX_ASHTAKA[ashtaka_varga[plan][planets_in_znak[new_time][plan]]]])

                if (scala_time[new_time].tm_year != scala_time[new_time - 1].tm_year):
                    ax.text(ox_line, ymin + (ymax - ymin) * 0.97, scala_time[new_time].tm_year, rotation=ROTATE_LABEL,
                            size=10)
                    l = mlines.Line2D([ox_line_l, ox_line_l], [ymin, ymax], linewidth=0.6)
                    ax.add_line(l)

                if (scala_time[new_time].tm_mon != scala_time[new_time - 1].tm_mon) and (
                        (txtDateqNext - txtDateqLast).days < 1310):
                    ax.text(delta_line_mon, ymin + (ymax - ymin) * 0.968,
                            NAME_MONTH[int(scala_time[new_time].tm_mon) - 1], rotation=0,
                            size=8)
                    l = mlines.Line2D([ox_line_l, ox_line_l], [ymin, ymax], linewidth=0.3)
                    ax.add_line(l)

                if (scala_time[new_time].tm_mday != scala_time[new_time - 1].tm_mday) and (
                        (txtDateqNext - txtDateqLast).days < 150):
                    ax.text(ox_line_l + len_/2, ymin + (ymax - ymin) * 0.050, scala_time[new_time+1].tm_mday, rotation=ROTATE_LABEL,
                            size=9)
                    l = mlines.Line2D([ox_line_l, ox_line_l], [ymin, ymax], linewidth=0.1)
                    ax.add_line(l)

                if name_graphics == NAME_GRAPHICS[HOROSCOP]:

                    if lock:
                        if int(scala_time[new_time].tm_year) >= int(TODAY_TIME.year) and \
                                int(scala_time[new_time].tm_mon) >= int(TODAY_TIME.month) and \
                                int(scala_time[new_time].tm_mday) >= int(TODAY_TIME.day):
                            lock = False
                            l = mlines.Line2D([ox_line_l, ox_line_l], [ymin, ymax], linewidth=0.7)
                            l.set_color("red")
                            ax.add_line(l)


            """
                вывод данных легенды
            """
            len_x = 5
            for pol in [0,1]:
                for nn, nc in enumerate(COLOR_CLASS_NY[pol]):
                    oy_crd = OX_OY[pol]
                    xfill = [nn*len_x, nn*len_x + len_x,
                             nn*len_x + len_x, nn*len_x]
                    yfill = [oy_crd - len_, oy_crd - len_, oy_crd + len_, oy_crd + len_]
                    ax_legend.fill(xfill, yfill, color=nc)

            canvasAgg.draw()
            canvas = canvasAgg.get_tk_widget()
            canvas.pack(fill=BOTH, expand=1)
            frm.pack(fill=BOTH, expand=1)

        canvasAgg_legend.draw()
        canvas_legend = canvasAgg_legend.get_tk_widget()
        canvas_legend.pack(fill=BOTH, expand=1)
        frm_legend.pack(fill=BOTH, expand=1)

        canvasAgg_bh.draw()
        canvas_bh = canvasAgg_bh.get_tk_widget()
        canvas_bh.pack(fill=BOTH, expand=1)
        frm_bh.pack(fill=BOTH, expand=1)

        canvasAgg_inf.draw()
        canvas_inf = canvasAgg_inf.get_tk_widget()
        canvas_inf.pack(fill=BOTH, expand=1)
        frm_inf.pack(fill=BOTH, expand=1)

        canvasAgg_sud.draw()
        canvas_sud = canvasAgg_sud.get_tk_widget()
        canvas_sud.pack(fill=BOTH, expand=1)
        frm_sud.pack(fill=BOTH, expand=1)

        canvasAgg_peo.draw()
        canvas_peo = canvasAgg_peo.get_tk_widget()
        canvas_peo.pack(fill=BOTH, expand=1)
        frm_peo.pack(fill=BOTH, expand=1)

        canvasAgg_nat.draw()
        canvas_nat = canvasAgg_nat.get_tk_widget()
        canvas_nat.pack(fill=BOTH, expand=1)
        frm_nat.pack(fill=BOTH, expand=1)
        t3 = datetime.today()

        # print('--- TIMERS ---')
        # print('Вычисление астроданных: ', t1 - t0, 'сек.')
        # print('Построение астрологических карт: ', t2 - t1, 'сек.')
        # print('Визуализация данных: ', t3 - t2, 'сек.')
    if xxx == 2:
        if str(txt_intervalSaveDay.get()) == "0":
            fig.savefig(
                'C:/Projects/' + str(company_name_combobox.get()) + '_' + str(txt_lastDate.get()) + '-' + str(
                    txt_nextDate.get()) + '.png')
            fig.set_size_inches(18, 4, forward=True)


def new_date_func():
    """
        открывает окно для редактирования, удаления и добавления новых данных по дате рождения
    """
    window_of_first_date.get_window_of_first_date()


def companies_selector_handler(event):
    """
        Обработчик селектора выбора компаний
        :param event: событие
    """
    company_data = companies_data.get(company_name_combobox.get())
    txtDate.delete(0, END)
    txtTime.delete(0, END)
    txtGTM.delete(0, END)
    txtAltitude.delete(0, END)
    txtLongitude.delete(0, END)
    txtDate.insert(0, company_data.set_up_date)
    txtTime.insert(0, company_data.set_up_time)
    txtGTM.insert(0, company_data.gmt)
    txtAltitude.insert(0, company_data.latitude)
    txtLongitude.insert(0, company_data.longitude)

def calculate_baby(event):
    day_bestday = partner_day_combobox.get()
    month_bestday = partner_month_combobox.get()
    years_bestday = partner_years_combobox.get()

    day_moon = partner_day_moon.get()
    month_moon = partner_month_moon.get()
    years_moon = partner_years_moon.get()

    day_bestday = ('0' + day_bestday)[-2:]
    day_moon = ('0' + day_moon)[-2:]
    month_bestday = ('0' + month_bestday)[-2:]
    month_moon = ('0' + month_moon)[-2:]

    time_bestday = day_bestday + '.' + month_bestday + '.' + years_bestday
    time_bestday = datetime.strptime(time_bestday, FORMAT_DATE)
    time_bestday_next = time_bestday + timedelta(days=15)
    time_bestday_last = time_bestday - timedelta(days=15)

    time_bestday_next_str = ('0' + str(time_bestday_next.day))[-2:]

    time_moon = day_moon + '.' + month_moon + '.' + years_moon
    time_moon = datetime.strptime(time_moon, FORMAT_DATE)

    analis_result_tithi, analis_result_nakshatra, analis_result_znak = get_calculate_planet_time('25.03.2021',
                                                                                                 '25.05.2021', UTC=3)



def back_baby(event):
    baby_nbGraphic.place(x=2400, y=30)


def find_time_of_muhurts(event):
    tranzit_nbGraphic.place(x=2000, y=26)
    good_planets_nbGraphic.place(x=2000, y=30)
    data_of_muhurts.place(x=0, y=26)
    print('call "button_muhurts"')


def button_strenght_planet(event):
    """
    появление окна good_planets_nbGraphic которое предназначено для подробного вычисления временных отрезков
    например, лунный день, лунный сутки, совмещение графиков для всех временных промежутков по дням недели
    """
    tranzit_nbGraphic.place(x=2000, y=26)
    good_planets_nbGraphic.place(x=0, y=30)
    data_of_muhurts.place(x=2000, y=26)
    print('call "button_strenght_planet"')


def good_planets_out(event):
    """
    скрытие окна для вычисления более подробных промежутков времени good_planets_nbGraphic
    """
    good_planets_nbGraphic.place(x=2000, y=26)
    tranzit_nbGraphic.place(x=-190, y=30)
    data_of_muhurts.place(x=2000, y=26)
    print('call "good_planets_out"')


def find_time_func(event):
    find_nbGraphic.place(x=2000, y=26)
    tranzit_nbGraphic.place(x=-190, y=30)


def coords_date(x_tranzit):
    if (x_tranzit >= 0) and (x_tranzit < 1400):
        last_num = txt_lastDate.get()
        next_num = txt_nextDate.get()

        last_num = datetime.strptime(last_num, FORMAT_DATE)
        next_num = datetime.strptime(next_num, FORMAT_DATE)

        date_num_period = (next_num - last_num).days
        date_percent = int(x_tranzit / 1300 * date_num_period)
    else:
        date_percent = -1

    return date_percent

def text_filter(my_string):
    if len(my_string)>0:
        if my_string[0] == "[":
            my_string = my_string[1:]
        elif my_string[len(my_string) - 1] == "]":
            my_string = my_string[:len(my_string) - 1]
        if my_string[len(my_string) - 2] == ".":
            my_string = my_string[:len(my_string) - 2]

    return my_string


def trnzit_gog(x_tranzit, hour_str='00'):

    if 0 <= x_tranzit <= 1300:

        global lagna_in_znak
        t0 = timet.time()
        date_percent = coords_date(x_tranzit)

        last_num = txt_lastDate.get()
        last_num = datetime.strptime(last_num, FORMAT_DATE)

        next_num = txt_nextDate.get()
        next_num = datetime.strptime(next_num, FORMAT_DATE)

        delta_date = last_num + timedelta(days=date_percent)

        delta_period = (next_num - last_num).days

        one_day = 1317 / delta_period
        labl_poz.place(x=93 + one_day * date_percent, y=78, width=1, height=308)

        new_date_tranzit = str(delta_date.day) + "." + str(delta_date.month) + "." + str(delta_date.year)

        def format_date(strnumber: str = None):
            if len(strnumber) == 1: strnumber = '0'+strnumber
            return strnumber

        new_date_tranzit_str = format_date(str(delta_date.day)) + "." + \
                               format_date(str(delta_date.month)) + "." + str(delta_date.year)

        new_date_tranzit_dt = datetime.strptime(new_date_tranzit, FORMAT_DATE)
        new_date_tranzit = new_date_tranzit_dt.strftime(FORMAT_DATE)

        hour_str = hour_str + ':00:00'
        planet_in_tranzit = calculateTranzitMap.calculate_tranzit_map(
            new_date_tranzit, txtDate.get(), hour_str, lagna=lagna_in_znak[0], delta=delta)

        graha_in_degrees_transit = planet_in_tranzit.graha_in_degrees_transit

        graha_in_retrograd = planet_in_tranzit.graha_in_retrograd
        graha_in_degrees = planet_in_tranzit.graha_in_degrees
        graha_speed = planet_in_tranzit.graha_speed

        planet_in_znak = np.asarray(np.asarray(graha_in_degrees) / 108000, dtype='int8')
        natal_moon = int(planet_in_tranzit.natal_moon_degrees / 108000) #

        graha_in_znak_algle = np.fmod(np.asarray(graha_in_degrees), 108000)

        planets_in_nakshatras = np.asarray(np.asarray(graha_in_degrees) / 48000, dtype='int8')
        planets_in_parts_naks = np.asarray(np.modf(np.asarray(graha_in_degrees) / 48000)[0] * 4, dtype='int8')

        utc, ltd_degr, lng_degr = txtGTM.get(), txtAltitude.get(), txtLongitude.get()

        sun_rise, sun_set = calculate_sunrise_time.get_calculate_sunrise(degrees_to_part(ltd_degr),
                                                                         degrees_to_part(lng_degr),
                                                                         new_date_tranzit_dt.day,
                                                                         new_date_tranzit_dt.month,
                                                                         new_date_tranzit_dt.year, int(utc))

        sun_rise_t = str((new_date_tranzit_dt + timedelta(seconds=sun_rise)).time())
        sun_set_t = str((new_date_tranzit_dt + timedelta(seconds=sun_set)).time())

        """
            построение карты транзитов по накшатрам
        """
        t1 = timet.time()
        ax_bh.cla()
        ax_bh.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_bh.plot(1, 1, '-b', linewidth=0.1, markersize=0)

        for x1, y1, z1, x2, y2 in zip(nak_x, nak_y, nak_z, nak_xl, nak_yl):
            ax_bh.plot([0, x1], [0, y1], color='blue', lw=.2)
            ax_bh.text(x2, y2, '%d' % (int(z1 + 1)), horizontalalignment='center',
                     verticalalignment='center', rotation=0, color=nak_clrr[nak_ccc[z1] + 1], size=8)

        for dgr, nam, r in zip(graha_in_degrees, nak_nam_pl, nak_rr):
            dgr0 = dgr / 1296000 * 2 * 3.141
            xx = np.cos(dgr0) * r
            yy = np.sin(dgr0) * r
            ax_bh.plot(xx, yy, '.', color='black', lw=.2)
            ax_bh.text(xx - abs(xx * .02), yy + abs(yy * .03), nam, verticalalignment='bottom',
                     horizontalalignment='center', size=6)

        ymin, ymax = ax_bh.get_ybound()

        for yn in PLANETS_RANGE:
            ynak = ymin + (ymax - ymin)/10 * (9-yn)
            txt_n = str(planets_in_nakshatras[yn]+1)
            ax_bh.text(1.095, ynak+.005, txt_n, color='black', size=8)
            ax_bh.text(1.10, ynak, txt_n, color=COLOR_PLANET[yn], size=8)
            txt_p = str(planets_in_parts_naks[yn]+1)
            ax_bh.text(1.245, ynak+.005, txt_p, color='black', size=8)
            ax_bh.text(1.25, ynak, txt_p, color=COLOR_PLANET[yn], size=8)
        t2 = timet.time()
        """
            Подсчет видимости планет
        """
        # planets_look_grahas = []
        # planets_aspects_znaks = [[],[],[],[],[],[],[],[],[]]
        #
        # for nm in ASPECTS_RANGE:
        #
        #     n = int(nm / 7)
        #     if n == (nm / 7):
        #         looks = []
        #
        #         for n2 in PLANETS_RANGE:
        #             if n == n2: continue
        #             graha_1_deg = graha_in_degrees[n]
        #             graha_2_deg = graha_in_degrees[n2]
        #             diff = graha_2_deg - graha_1_deg
        #             if diff < -36000:
        #                 diff = SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg
        #             if diff > 36000:
        #                 diff = -SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg
        #
        #             if abs(diff) < 36000:
        #                 looks.append(n2)
        #         planets_look_grahas.append(looks)
        #
        #     n_aspect = np.fmod(nm, 7)
        #     if graha_in_retrograd[n] == 1:
        #         if n_aspect in [1, 2, 3]: continue
        #     if graha_in_retrograd[n] == 0:
        #         if n_aspect in [4, 5, 6]: continue
        #
        #     if n_aspect in [1, 2, 3][0:NUMBER_OF_ASPECTS[n]] or n_aspect in [4, 5, 6][0:NUMBER_OF_ASPECTS[n]]:
        #         znak_und_aspect = math.trunc(graha_in_degrees_transit[nm] / DEGREES_IN_ZNAK)
        #         planets_aspects_znaks[n].append(znak_und_aspect)
        """
            построение поля характеристик планет в D1 и D9
        """

        ax_peo.cla()
        ax_peo.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_peo.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        planet_angles = np.array(graha_in_degrees) / 3600
        planet_balaAvastha = np.asarray(np.fmod(planet_angles, 30)/30*100, dtype='int16')
        planet_chet_ntchet = np.asarray(np.asarray(np.array(graha_in_degrees)/108000, dtype='int16')/2)

        planet_angles_nava = np.fmod(np.array(graha_in_degrees)/12000, 12) * 30
        planet_in_znak_nava = np.asarray(planet_angles_nava/30, dtype='int16')

        list_planets_in_otnoseniya_data = calculate_relations_betwen_planets.calc_rel_planets(planet_angles, planet_in_znak)

        list_planets_in_start_otnosheniya = list_planets_in_otnoseniya_data.list_planets_in_start_otnosheniya
        list_planets_in_otnoseniya = list_planets_in_otnoseniya_data.list_planets_in_otnoseniya
        # list_planets_in_znak = list_planets_in_otnoseniya_data.list_planets_in_znak
        t3 = timet.time()
        if on_muhurta.get() == 1:
            """
                Расчет мухурт на весь день
            """
            recomendations = parse_recomendations(
                recomendations=get_recomendations(rise_time=sun_rise_t, set_time=sun_set_t,
                                                  date=str(new_date_tranzit_dt.date()),
                                                  ltd_degr=degrees_to_part(ltd_degr),
                                                  planets_degrees=graha_in_degrees, power_planets=list_planets_in_otnoseniya,
                                                  speed_moon=graha_speed[1]))
            """
                добавление данных по трактовкам гороскопа
            """
            ax_muh.cla()
            ax_muh.axis('off')
            ax_muh.plot(0, 0, '-b', linewidth=0.1, markersize=0)
            ax_muh.plot(400, 4000, '-b', linewidth=0.1, markersize=0)

            ylen = 2
            count_str = 0
            for keyn in recomendations.keys():

                count_str += 4
                oy_crd = 4000 - count_str * 6
                time_str = f"мухурта {keyn + 1}: {MUHURTA_NAME[keyn]} ----- {recomendations[keyn]['time_start'].date()} {recomendations[keyn]['time_start'].time()} -> {recomendations[keyn]['time_finish'].date()} {recomendations[keyn]['time_finish'].time()}"

                ax_muh.text(0, oy_crd, time_str, color="black", size=8)
                count_str += 1

                for rec in recomendations[keyn]['recomendations'].keys():

                    count_str += 1
                    oy_crd = 4000 - count_str * 6
                    ax_muh.text(0, oy_crd, rec, color="black", size=8)

                    yfill = [oy_crd - ylen + 1, oy_crd - ylen + 1, oy_crd + ylen + 1, oy_crd + ylen + 1]

                    count_per = int(recomendations[keyn]['recomendations'][rec] / 15)
                    xfill = [-10, -10 - count_per, -10 - count_per, -10]

                    if count_per >= len(COLOR_CLASS_BRN[0]):
                        count_per = len(COLOR_CLASS_BRN[0]) - 1

                    color_k = COLOR_CLASS_BRN[0][count_per]
                    ax_muh.fill(xfill, yfill, color=color_k)


            canvasAgg_muh.draw()
            canvas_muh = canvasAgg_muh.get_tk_widget()
            canvas_muh.pack(fill=BOTH, expand=1)

            canvas_muhurts.create_window(0, 0, window=frame_muh, anchor='nw')
            data_of_muhurts.update()
            canvas_muhurts.config(scrollregion=(0, 1550, 0, 1550 + count_str * 10.6))

        # bad_good_data = calculate_relations_betwen_planets.calc_rel_connect_planets(planets_look_grahas,
        #                                     list_planets_in_start_otnosheniya, list_planets_in_znak, planet_in_znak,
        #                                                                             planets_aspects_znaks, graha_in_retrograd)

        list_planets_in_otnoseniya_nava_data = calculate_relations_betwen_planets.calc_rel_planets(
            planet_angles_nava, planet_in_znak_nava)
        list_planets_in_otnoseniya_nava = list_planets_in_otnoseniya_nava_data.list_planets_in_otnoseniya


        for n in PLANETS_RANGE[0:9]:
            if int(planet_chet_ntchet[n]) == planet_chet_ntchet[n]:
                bala_planet = planet_balaAvastha[n]
            else:
                bala_planet = 100 - planet_balaAvastha[n]

            for to_, do_ in zip(AVASTHA_INTERVALS[0:-1], AVASTHA_INTERVALS[1:]):
                if (bala_planet >= to_) and (bala_planet <= do_):
                    bala_planet = int(AVASTHA_RESULTS[int(to_/10)] + (
                            (bala_planet - to_)/10*(AVASTHA_RESULTS[int(do_/10)]-AVASTHA_RESULTS[int(to_/10)])))
                    break

            oy = 95 - (n * 9)
            ax_peo.text(5, oy, NAME_PLANETS_DREK[n], size=8)
            ax_peo.text(50, oy, str(bala_planet), size=8)

            for list_otnoseniya, oxpl in zip([list_planets_in_otnoseniya[n], list_planets_in_otnoseniya_nava[n]],
                                    [14, 60]):
                ax_peo.text(oxpl, oy, list_otnoseniya, size=6)
                color_ = COLOR_BALA[list_otnoseniya]
                l = mlines.Line2D([oxpl+3, oxpl+33], [oy+1, oy+1], linewidth=10.0, alpha=.6)
                l.set_color(color_)
                ax_peo.add_line(l)

        t4 = timet.time()
        # """
        #     Лунa
        # """
        #
        # data_transits = np.arange(0, 390, 30)
        #
        # for n_gegr, degr in enumerate(np.linspace(0, 100, 36)):
        #
        #     l = mlines.Line2D([degr, degr], [5, 20], linewidth=0.1)
        #     l.set_color("blue")
        #     ax_peo.add_line(l)
        #
        #     if abs(n_gegr - 18) < 10 or abs(n_gegr - 18) in [11, 13, 15]:
        #         ax_peo.text(degr - 3, 0, abs(n_gegr - 18), color='black', size=6)


        # for indx, transit in enumerate(data_transits):
        #     diff_planet = data_transits[indx] - graha_in_degrees[MOON_PLANET_NUMBER]/SECONDS_IN_DEGREE
        #
        #     if diff_planet > DEGREES_IN_ZODIAK:
        #         diff_planet -= DEGREES_IN_ZODIAK
        #     # elif diff_planet < 0:
        #     #     diff_planet += DEGREES_IN_ZODIAK
        #
        #     if -18 < diff_planet < 18:
        #         per_poz = (diff_planet + 18) / 36
        #
        #         name_planet = '|'
        #
        #         l = mlines.Line2D([per_poz*100, per_poz*100 + .1], [4, 4 + .1], linewidth=1)
        #         l.set_color("black")
        #         ax_peo.add_line(l)
        #         ax_peo.text(per_poz*100 - .4, 8 - 1 - .4, name_planet, color="black",
        #                     size=8)
        #         ax_peo.text(per_poz*100, 8 - 1, name_planet, color='black', size=8)

        """
            просчет планет караки
        """
        # karaka_planets = np.asarray(graha_in_znak_algle)
        for mm in PLANETS_RANGE:
            oy = 95 - (mm*9)
            if graha_in_retrograd[mm] == 1:
                # karaka_planets[mm] = 108000 - graha_in_znak_algle[mm]
                ax_peo.text(-2, oy, 'R', size=6)

        """
            Построение градусов планет в крайнем окне
        """
        ax_dpl.cla()
        ax_dpl.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_dpl.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        data_karakas = calculate_karakas.get_karakas(planets_in_degrees=graha_in_degrees)
        str_karakas = ['АК', 'АмК', 'БК', 'МК', 'ПУ', 'ГК', 'ДК']
        t5 = timet.time()
        for planetes, degreses in enumerate(graha_in_degrees[0:9]):
            y = 100 - planetes * 8
            angle = round(degreses / 3600, 1)
            angle_str = str(angle) + '°'

            angle_in_znak = round(np.fmod(degreses, 108000) / 3600, 1)
            angle_in_znak_str = str(angle_in_znak) + '°'

            in_znak = int(degreses/108000)

            ax_dpl.text(3.2, y, NAME_PLANETS_DREK[planetes], color='black', size=8)
            ax_dpl.text(3, y, NAME_PLANETS_DREK[planetes], color=COLOR_PLANET[planetes], size=8)

            try:
                if planetes < 7:
                    ax_dpl.text(15.2, y, str_karakas[data_karakas.index(planetes)], size=8, multialignment='center')
                    ax_dpl.text(15, y, str_karakas[data_karakas.index(planetes)], size=8,
                                multialignment='center', color=COLOR_PLANET[data_karakas.index(planetes)])
            except:
                pass

            ax_dpl.text(26, y, angle_str, size=8, multialignment='center')
            ax_dpl.text(46, y, NAME_ZNAKS[in_znak], size=8, multialignment='center')
            ax_dpl.text(75, y, angle_in_znak_str, size=8)

            planest_list = []
            for planets2, degreses2 in enumerate(graha_in_degrees[0:9]):
                if planets2 != planetes and planets2 != 1 and planetes != 1:
                    angle_in_znak2 = round(np.fmod(degreses2, 108000) / 3600, 1)
                    diff_planet = abs(angle_in_znak2 - angle_in_znak)

                    if diff_planet > 15.5:
                        diff_planet = 30 - angle_in_znak2 + angle_in_znak
                    elif diff_planet < 13.5:
                        diff_planet = 30 - angle_in_znak2 + angle_in_znak

                    if 13.5 <= diff_planet <= 15.5:
                        planest_list.append(planets2)
                        ax_dpl.text(75 + len(planest_list) * 5, y, NAME_PLANETS[planets2],
                                    color=COLOR_PLANET[planets2], size=8)

        canvasAgg_dpl.draw()
        canvas_dpl = canvasAgg_dpl.get_tk_widget()
        canvas_dpl.pack(fill=BOTH, expand=1)
        frm_dpl.pack(fill=BOTH, expand=1)
        t6 = timet.time()
        ax_inf.cla()
        ax_inf.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_inf.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        def brilliant_map(i):
            l = mlines.Line2D([BRILLANT_MAP_X[i * 2], BRILLANT_MAP_X[i * 2 + 1]],
                              [BRILLANT_MAP_Y[i * 2], BRILLANT_MAP_Y[i * 2 + 1]], linewidth=1.0)
            l.set_color("blue")
            ax_inf.add_line(l)

        list(map(lambda u: brilliant_map(u), MAP_RANGE))

        l = mlines.Line2D(COORDS_BHAVAS_X, COORDS_BHAVAS_Y, linewidth=1.0)
        l.set_color("blue")
        ax_inf.add_line(l)

        """
            построение положения планет в транзитах относительно положения луны
        """
        ax_sud.cla()
        ax_sud.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_sud.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        def brilliant_map(i):
            l = mlines.Line2D([BRILLANT_MAP_X[i * 2], BRILLANT_MAP_X[i * 2 + 1]],
                              [BRILLANT_MAP_Y[i * 2], BRILLANT_MAP_Y[i * 2 + 1]], linewidth=1.0)
            l.set_color("blue")
            ax_sud.add_line(l)

        list(map(lambda u: brilliant_map(u), MAP_RANGE))

        l = mlines.Line2D(COORDS_BHAVAS_X, COORDS_BHAVAS_Y, linewidth=1.0)
        l.set_color("blue")
        ax_sud.add_line(l)

        """
            Обозначение проблемных знаков
        """
        bindy_scores_data = calculate_bindy_vargas(planet_in_znak, [0, 0])
        bindy_scores_planets = bindy_scores_data.planet_in_goods_location

        # krizis_data = KrizisData(graha_in_degrees, graha_speed)

        """
            Подсчет в каком знаке находится планета, в знаке друга, в знаке врага
        """
        list_simple_otnoseniya = list_planets_in_otnoseniya_data.list_in_simple_otnosheniya

        """
            Подсчет взаимоотношений планет, когда они соединяются
        """

        bad_good_planets = []
        for planet in PLANETS_RANGE:

            bad_good_planets.append(list_simple_otnoseniya[planet])


        # bindy_scores = []


        """
           Построение планет и аспектов 
        """
        x_planets = []
        y_planets = []

        planets_angle_aspects = [[],[],[],[],[],[],[],[],[]]
        x_planets_aspects = [[],[],[],[],[],[],[],[],[]]
        y_planets_aspects = [[],[],[],[],[],[],[],[],[]]
        planets_angle_planets = []
        t7 = timet.time()
        # graha_in_degrees_transit_D9 = bhava_aspec(np.array(planet_angles_nava)*3600, 0, graha_in_retrograd)

        for variant, graha_in_degrees_transit_D, ax_ in zip([True, False], [graha_in_degrees_transit, np.fmod(np.array(graha_in_degrees_transit)*3600/12000, 12) * 30],
                                                            [ax_sud, ax_inf]):
            for nm in ASPECTS_RANGE:

                n = int(nm / 7)
                if n == (nm / 7) and variant:
                    planets_angle_planets.append(graha_in_degrees_transit_D[nm])

                n_aspect = np.fmod(nm, 7)
                if graha_in_retrograd[n] == 1:
                    if n_aspect in [1, 2, 3]: continue
                if graha_in_retrograd[n] == 0:
                    if n_aspect in [4, 5, 6]: continue

                house = math.trunc(graha_in_degrees_transit_D[nm] / DEGREES_IN_ZNAK)
                i = (graha_in_degrees_transit_D[nm] - (house * DEGREES_IN_ZNAK)) * 3

                point_OX = COORDS_BHAVAS_X[house]
                point_OY = COORDS_BHAVAS_Y[house]
                radius = 14 + (n * 1.5)
                angle = ANGLES[house]

                if next_range[house] == 0:
                    x = (radius * math.sin(math.radians(i + angle))) + point_OX
                    y = (radius * math.cos(math.radians(i + angle))) + point_OY
                else:
                    x = (radius * math.cos(math.radians(i + angle))) + point_OX
                    y = (radius * math.sin(math.radians(i + angle))) + point_OY
                delta_OX = DELTA_OX_TEXT[house]
                delta_OY = DELTA_OY_TEXT[house]

                if n == (nm / 7):
                    ax_.text(x + delta_OX - .4, y + delta_OY - .4, NAME_PLANETS[n], color="black",
                                size=8)
                    ax_.text(x + delta_OX, y + delta_OY, NAME_PLANETS[n], color=COLOR_PLANET[n], size=8)

                    ax_.plot([x, x + .1], [y, y + .1], '.', color='black', markersize=8)
                    ax_.plot([x, x + .1], [y, y + .1], '.', color='white', markersize=1)

                    if variant:
                        x_planets.append(x)
                        y_planets.append(y)
                else:
                    if variant:
                        x_planets_aspects[n].append(x)
                        y_planets_aspects[n].append(y)
                        planets_angle_aspects[n].append(graha_in_degrees_transit_D[nm])

                    ax_.plot([x, x + .1], [y, y + .1], '.', color='gray', markersize=1)
                    ax_.text(x + delta_OX - .4, y + delta_OY - .4, NAME_PLANETS[n], color="gray",
                                size=8)
                    ax_.text(x + delta_OX, y + delta_OY, NAME_PLANETS[n], color=COLOR_PLANET_ASPECT[n], size=8)

            def text_znak(i):
                if variant: nmpl = natal_moon
                else: nmpl = 0
                number_znak_sud = int(math.fmod((nmpl + i), ZNAKS_IN_ZODIAK))
                OX = HOUSE_OX[i]
                OY = HOUSE_OY[i]
                ax_.text(OX + DELTA_P[number_znak_sud], OY, str(number_znak_sud + 1), color="black", size=10)
                ax_.text(OX + .4 + DELTA_P[number_znak_sud], OY + .4, str(number_znak_sud + 1),
                            color=COLOR_ELEMENTS_ZNAK[number_znak_sud], size=10)

            list(map(lambda x: text_znak(x), ZODIAK_RANGE))
        t8 = timet.time()
        # for planet in [4]:
        #     if (bad_good_data[planet][0] - bad_good_data[planet][1]) == 0: coef = 0
        #         coef = int(round(bad_good_data[planet][0] / (bad_good_data[planet][0] - bad_good_data[planet][1]), 2) * 100)
        #
        #     ax_sud.text(0, 100 - planet * 10, NAME_PLANETS_DREK[planet], color='black', size=8)
        #     ax_sud.text(10, 100 - planet * 10, coef, color='black', size=8)
        #     ax_sud.text(20, 100 - planet * 10, int(bad_good_data[planet][0]/10), color='black', size=8)
        """
            Поиск аспектов, которые видят планеты
        """
        for graha in PLANETS_RANGE:
            for planet, (a_planet, x_planet, y_planet) in enumerate(zip(planets_angle_aspects, x_planets_aspects, y_planets_aspects)):
                if graha == planet: continue

                for a_plan, x_plan, y_plan in zip(a_planet, x_planet, y_planet):

                    graha_1_deg = planets_angle_planets[graha]
                    graha_2_deg = a_plan
                    diff = graha_2_deg - graha_1_deg
                    if diff < -10:
                        diff = DEGREES_IN_ZODIAK - graha_1_deg + graha_2_deg
                    if diff > 10:
                        diff = -DEGREES_IN_ZODIAK - graha_1_deg + graha_2_deg

                    """
                        Вывод линии от планеты до аспекта
                    """

                    if abs(diff) < 10:
                        l = mlines.Line2D([x_planets[graha], x_plan],
                                          [y_planets[graha], y_plan], linewidth=.3)
                        l.set_color('blue')
                        ax_sud.add_line(l)

        """
            Вывод взаимосвязей планет
        """

        # for planet in PLANETS_RANGE:
        #     for look_planets in planets_look_grahas[planet]:
        #         l = mlines.Line2D([x_planets[planet], x_planets[look_planets]],
        #                           [y_planets[planet], y_planets[look_planets]], linewidth=.3)
        #         l.set_color("blue")
        #         ax_sud.add_line(l)

        labl_tranzit.config(text=new_date_tranzit)
        lx_tranzit.delete(0, END)
        lx_tranzit.insert(0, x_tranzit)
        t9 = timet.time()
        # добавляем дату транзитов
        ymini, ymaxi = ax_sud.get_ybound()
        ax_sud.text(50, ymaxi, new_date_tranzit_str, rotation=0, size=10, horizontalalignment='center',
                    verticalalignment='bottom')

        ymini, ymaxi = ax_inf.get_ybound()
        ax_inf.text(50, ymaxi, 'ТРАНЗИТНАЯ D9', rotation=0, size=10, horizontalalignment='center',
                    verticalalignment='bottom')

        canvasAgg_inf.draw()
        canvas_inf = canvasAgg_inf.get_tk_widget()
        canvas_inf.pack(fill=BOTH, expand=1)
        frm_inf.pack(fill=BOTH, expand=1)

        canvasAgg_peo.draw()
        canvas_peo = canvasAgg_peo.get_tk_widget()
        canvas_peo.pack(fill=BOTH, expand=1)
        frm_peo.pack(fill=BOTH, expand=1)

        canvasAgg_sud.draw()
        canvas_sud = canvasAgg_sud.get_tk_widget()
        canvas_sud.pack(fill=BOTH, expand=1)
        frm_sud.pack(fill=BOTH, expand=1)

        canvasAgg_bh.draw()
        canvas_bh = canvasAgg_bh.get_tk_widget()
        canvas_bh.pack(fill=BOTH, expand=1)
        frm_bh.pack(fill=BOTH, expand=1)
        t10 = timet.time()


def vargas_show(event):
    y_vargas = int((canvas_bh.winfo_pointery() - 492)/11.36)
    global retrogr_planet
    if 0<=y_vargas<=18:

        contents = output_map_vargas_str.getvalue()
        str_map_vargas_str = list(contents.split(', '))
        int_map_vargas_str = list(map(lambda x: float(text_filter(x)), str_map_vargas_str))
        int_map_vargas_str = np.reshape(int_map_vargas_str, (int(len(int_map_vargas_str) / 10), 10))


        ax_inf.cla()
        ax_inf.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_inf.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        ymin, ymax = ax_inf.get_ybound()

        str_map = "КАРТА ДЕЛЕНИЯ: " + str(VARGA_TXT[18 - y_vargas-1])

        ymini, ymaxi = ax_inf.get_ybound()
        ax_inf.text(50, ymaxi, str_map, rotation=0, size=10, horizontalalignment='center', verticalalignment='bottom')

        def brilliant_map(i):
            l = mlines.Line2D([BRILLANT_MAP_X[i * 2], BRILLANT_MAP_X[i * 2 + 1]],
                              [BRILLANT_MAP_Y[i * 2], BRILLANT_MAP_Y[i * 2 + 1]], linewidth=1.0)
            l.set_color("blue")
            ax_inf.add_line(l)

        list(map(lambda u: brilliant_map(u), MAP_RANGE))

        l = mlines.Line2D(COORDS_BHAVAS_X, COORDS_BHAVAS_Y, linewidth=1.0)
        l.set_color("blue")
        ax_inf.add_line(l)

        planet_angles = []
        for nm in PLANETS_RANGE:
            planet_angles.append(int_map_vargas_str[y_vargas][nm] * 30)

            for aspects in ASPECTS_FOR_YOGA[nm]:

                if aspects != 0:
                    try:
                        delta_ = aspects - retrogr_planet[nm]
                    except:
                        pass
                else:
                    delta_ = 0

                graha_in_degrees = int_map_vargas_str[y_vargas][nm] - int(int_map_vargas_str[y_vargas][nm])
                house = int(math.fmod(int_map_vargas_str[y_vargas][nm] - int(int_map_vargas_str[y_vargas][9]) + delta_ + 12, 12))

                i = graha_in_degrees * 90

                point_OX = COORDS_BHAVAS_X[house]
                point_OY = COORDS_BHAVAS_Y[house]
                radius = 14 + (nm * 1.5)
                angle = ANGLES[house]

                if next_range[house] == 0:
                    x = (radius * math.sin(math.radians(i + angle))) + point_OX
                    y = (radius * math.cos(math.radians(i + angle))) + point_OY
                else:
                    x = (radius * math.cos(math.radians(i + angle))) + point_OX
                    y = (radius * math.sin(math.radians(i + angle))) + point_OY
                delta_OX = DELTA_OX_TEXT[house]
                delta_OY = DELTA_OY_TEXT[house]

                if aspects == 0:
                    l = mlines.Line2D([x, x + .1], [y, y + .1], linewidth=3)
                    l.set_color("black")
                    ax_inf.add_line(l)

                    ax_inf.text(x + delta_OX - .4, y + delta_OY - .4, NAME_PLANETS[nm], color="black",
                                size=8)
                    ax_inf.text(x + delta_OX, y + delta_OY, NAME_PLANETS[nm], color=COLOR_PLANET[nm], size=8)
                else:
                    if delta_ == 6 and nm in [7, 8]: continue

                    """
                        adding aspects
                    """
                    l = mlines.Line2D([x, x + .1], [y, y + .1], linewidth=1)
                    l.set_color("gray")
                    ax_inf.add_line(l)
                    ax_inf.text(x + delta_OX - .4, y + delta_OY - .4, NAME_PLANETS[nm], color="gray",
                                size=8)
                    ax_inf.text(x + delta_OX, y + delta_OY, NAME_PLANETS[nm], color=COLOR_PLANET_ASPECT[nm], size=8)

        """
            построение поля характеристик планет в D1 и D9
        """
        ax_peo.cla()
        ax_peo.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_peo.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        ymini, ymaxi = ax_peo.get_ybound()
        ax_peo.text(50, ymaxi, str_map, rotation=0, size=10, horizontalalignment='center', verticalalignment='bottom')

        planet_in_znak = np.asarray(np.array(planet_angles) / 30, dtype='int8')
        graha_in_degrees = np.array(planet_angles) * 3600
        planet_balaAvastha = np.asarray(np.fmod(planet_angles, 30) / 30 * 100, dtype='int16')
        planet_chet_ntchet = np.asarray(np.asarray(np.array(graha_in_degrees) / 108000, dtype='int16') / 2)

        list_planets_in_otnoseniya = calculate_relations_betwen_planets.calc_rel_planets(planet_angles,
                                                                                         planet_in_znak)

        for mm in PLANETS_RANGE:
            oy = 95 - (mm*9)
            if retrogr_planet[mm] == 1:
                ax_peo.text(-2, oy, 'R', size=6)

        self_aspects = calc_self_aspects(graha_in_degrees, retrogr_planet)

        for mm in PLANETS_RANGE:
            oy = 95 - (mm*9)
            if self_aspects[mm] == 1:
                ax_peo.text(60, oy, 'o', size=9, color='green')


        for n in PLANETS_RANGE[0:9]:
            if int(planet_chet_ntchet[n]) == planet_chet_ntchet[n]:
                bala_planet = planet_balaAvastha[n]
            else:
                bala_planet = 100 - planet_balaAvastha[n]

            for to_, do_ in zip(AVASTHA_INTERVALS[0:-1], AVASTHA_INTERVALS[1:]):
                if (bala_planet >= to_) and (bala_planet <= do_):
                    bala_planet = int(AVASTHA_RESULTS[int(to_ / 10)] + (
                            (bala_planet - to_) / 10 * (
                                AVASTHA_RESULTS[int(do_ / 10)] - AVASTHA_RESULTS[int(to_ / 10)])))
                    break

            oy = 95 - (n * 9)
            ax_peo.text(5, oy, NAME_PLANETS_DREK[n], size=8)
            ax_peo.text(50, oy, str(bala_planet), size=8)

            for list_otnoseniya, oxpl in zip([list_planets_in_otnoseniya.list_planets_in_otnoseniya[n]],
                                             [14, 60]):
                ax_peo.text(oxpl, oy, list_otnoseniya, size=6)
                color_ = COLOR_BALA[list_otnoseniya]
                l = mlines.Line2D([oxpl + 3, oxpl + 33], [oy + 1, oy + 1], linewidth=10.0, alpha=.6)
                l.set_color(color_)
                l.set_color(color_)
                ax_peo.add_line(l)

        def text_znak(i):
            number_znak_sud = int(math.fmod((i + int_map_vargas_str[y_vargas][9] + 12), ZNAKS_IN_ZODIAK))
            OX = HOUSE_OX[i]
            OY = HOUSE_OY[i]
            ax_inf.text(OX + DELTA_P[number_znak_sud], OY, str(number_znak_sud + 1), color="black", size=10)
            ax_inf.text(OX + .4 + DELTA_P[number_znak_sud], OY + .4, str(number_znak_sud + 1),
                        color=COLOR_ELEMENTS_ZNAK[number_znak_sud], size=10)

        list(map(lambda x: text_znak(x), ZODIAK_RANGE))

        canvasAgg_inf.draw()
        canvas_inf = canvasAgg_sud.get_tk_widget()
        canvas_inf.pack(fill=BOTH, expand=1)
        frm_inf.pack(fill=BOTH, expand=1)

        canvasAgg_peo.draw()
        canvas_peo = canvasAgg_sud.get_tk_widget()
        canvas_peo.pack(fill=BOTH, expand=1)
        frm_peo.pack(fill=BOTH, expand=1)

def find_time_of_burn_3days(event):
    ax.cla()
    fig.canvas.draw()
    fig.canvas.flush_events()

    data_med = labl_tranzit.cget('text')
    data_med = datetime.strptime(data_med, FORMAT_DATE)

    planets_look_grahas_full = [[0]]
    planets_in_znaks_info_full = []
    situation_info_all = []
    planets_pipe = []
    datas = []

    for day in [-1, 0, 1]:
        new_date = data_med + timedelta(days=day)

        new_date_tranzit = str(new_date.day) + "." + str(new_date.month) + "." + str(new_date.year)
        datas.append(new_date_tranzit)

        new_date_tranzit = datetime.strptime(new_date_tranzit, FORMAT_DATE)
        new_date_tranzit = new_date_tranzit.strftime(FORMAT_DATE)

        for hour in np.arange(HOURS_IN_DAY):
            situation_info = []

            hour_s = str(hour)
            if len(hour_s) == 1: hour_s = '0' + hour_s

            hour_str = hour_s + ':00:00'
            planet_in_tranzit = calculateTranzitMap.calculate_tranzit_map(new_date_tranzit, txtDate.get(), hour_str, delta=delta)
            graha_in_degrees_transit = planet_in_tranzit.graha_in_degrees_transit

            graha_in_retrograd = planet_in_tranzit.graha_in_retrograd
            graha_in_degrees = planet_in_tranzit.graha_in_degrees

            planets_in_znaks_info = np.asarray(np.asarray(graha_in_degrees) / SECONDS_IN_ZNAK, dtype='int32')

            """
                Подсчет видимости планет
            """
            looks = []
            planets_look_grahas = []
            planets_aspects_znaks = [[], [], [], [], [], [], [], [], []]
            for nm in ASPECTS_RANGE:
                n = int(nm / 7)
                if n == (nm / 7):
                    for n2 in PLANETS_RANGE:
                        if n >= n2: continue
                        graha_1_deg = graha_in_degrees[n]
                        graha_2_deg = graha_in_degrees[n2]
                        diff = graha_2_deg - graha_1_deg
                        if diff < -36000:
                            diff = SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg
                        if diff > 36000:
                            diff = -SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg

                        if abs(diff) < 36000:
                            planets_look_grahas.append(1)
                            situation_info.append(NAME_PLANETS_DREK[n] + ' - ' + NAME_PLANETS_DREK[n2] + ' соединение')
                        else:
                            planets_look_grahas.append(0)
                            situation_info.append('')

                n_aspect = np.fmod(nm, 7)
                if graha_in_retrograd[n] == 1:
                    if n_aspect in [1, 2, 3]: continue
                if graha_in_retrograd[n] == 0:
                    if n_aspect in [4, 5, 6]: continue

                if n_aspect in [1, 2, 3][0:NUMBER_OF_ASPECTS[n]] or n_aspect in [4, 5, 6][0:NUMBER_OF_ASPECTS[n]]:
                    znak_und_aspect = math.trunc(graha_in_degrees_transit[nm] / DEGREES_IN_ZNAK)
                    planets_aspects_znaks[n].append(znak_und_aspect)

            """
               Построение планет и аспектов 
            """
            x_planets = []
            y_planets = []
            looks = []
            planets_angle_aspects = [[], [], [], [], [], [], [], [], []]
            x_planets_aspects = [[], [], [], [], [], [], [], [], []]
            y_planets_aspects = [[], [], [], [], [], [], [], [], []]
            planets_angle_planets = []

            for nm in ASPECTS_RANGE:
                n = int(nm / 7)
                if n == (nm / 7):
                    planets_angle_planets.append(graha_in_degrees_transit[nm])

                n_aspect = np.fmod(nm, 7)
                if graha_in_retrograd[n] == 1:
                    if n_aspect in [1, 2, 3]: continue
                if graha_in_retrograd[n] == 0:
                    if n_aspect in [4, 5, 6]: continue

                house = math.trunc(graha_in_degrees_transit[nm] / DEGREES_IN_ZNAK)
                i = (graha_in_degrees_transit[nm] - (house * DEGREES_IN_ZNAK)) * 3

                point_OX = COORDS_BHAVAS_X[house]
                point_OY = COORDS_BHAVAS_Y[house]
                radius = 14 + (n * 1.5)
                angle = ANGLES[house]

                if next_range[house] == 0:
                    x = (radius * math.sin(math.radians(i + angle))) + point_OX
                    y = (radius * math.cos(math.radians(i + angle))) + point_OY
                else:
                    x = (radius * math.cos(math.radians(i + angle))) + point_OX
                    y = (radius * math.sin(math.radians(i + angle))) + point_OY

                if n == (nm / 7):
                    x_planets.append(x)
                    y_planets.append(y)
                else:
                    x_planets_aspects[n].append(x)
                    y_planets_aspects[n].append(y)
                    planets_angle_aspects[n].append(graha_in_degrees_transit[nm])

            """
                Поиск аспектов, которые видят планеты
            """
            for graha in PLANETS_RANGE:
                for planet, (a_planet, x_planet, y_planet) in enumerate(
                        zip(planets_angle_aspects, x_planets_aspects, y_planets_aspects)):
                    if graha >= planet: continue

                    for a_plan, x_plan, y_plan in zip(a_planet, x_planet, y_planet):
                        graha_1_deg = planets_angle_planets[graha]
                        graha_2_deg = a_plan
                        diff = graha_2_deg - graha_1_deg
                        if diff < -10:
                            diff = DEGREES_IN_ZODIAK - graha_1_deg + graha_2_deg
                        if diff > 10:
                            diff = -DEGREES_IN_ZODIAK - graha_1_deg + graha_2_deg

                        """
                            Вывод линии от планеты до аспекта
                        """
                        if abs(diff) < 10:
                            planets_look_grahas.append(1)
                            serch_n = NAME_PLANETS_DREK[graha] + ' - ' + NAME_PLANETS_DREK[planet] + ' аспект'
                            if serch_n in situation_info:
                                situation_info.append('')
                            else:
                                situation_info.append(serch_n)
                        else:
                            planets_look_grahas.append(0)
                            situation_info.append('')

            """
                Поиск переходит ли планета в другой знак
            """
            if len(planets_in_znaks_info_full) > 0:
                for graha in PLANETS_RANGE:
                    planets_look_grahas.append(planets_in_znaks_info[graha])
                    if planets_in_znaks_info_full[-1][graha] != planets_in_znaks_info[graha]:
                        str_per = NAME_PLANETS_DREK[graha] + ' переход в ' + str(planets_in_znaks_info[graha] + 1) + ' знак'
                        if str_per in situation_info_all[-1]:
                            situation_info.append('')
                        else:
                            situation_info.append(str_per)
                    else:
                        situation_info.append('')
            else:
                for graha in PLANETS_RANGE:
                    planets_look_grahas.append(planets_in_znaks_info[graha])
                    situation_info.append('')

            situation_info_all.append(situation_info)
            planets_in_znaks_info_full.append(planets_in_znaks_info)
            planets_pipe.append(planets_look_grahas_full[-1] == planets_look_grahas)
            planets_look_grahas_full.append(planets_look_grahas)

    """
        построение почасового графика изменений ситуации
    """
    ONE_DAYS = 1300 / 72
    ymin, ymax = ax.get_ybound()
    ax.plot(1300, ymax)
    ax.plot(1300, ymin)

    count_connects = 0
    for ox in np.arange(1, 71):
        ox_ = ox * ONE_DAYS + ONE_DAYS * .5
        oxn = ox * ONE_DAYS

        if not planets_pipe[ox]:
            l = mlines.Line2D([ox_, ox_],
                              [ymax * .21, ymax * .99], linewidth=10)
            l.set_color("silver")
            ax.add_line(l)

            for last, next in zip(situation_info_all[ox-1], situation_info_all[ox]):
                if last != next:
                    if len(last) == 0: iterpls = [next]
                    elif len(next) == 0: iterpls = [last]
                    else: iterpls = [next, last]
                    for iterpl in iterpls:
                        count_connects += 1
                        ystr = 1-count_connects*.05
                        ax.text(oxn, ymax * ystr, iterpl, fontsize=8, horizontalalignment='left', fontweight='bold')

        l = mlines.Line2D([oxn, oxn],
                          [ymax * .2, ymax], linewidth=.5)
        l.set_color("blue")
        ax.add_line(l)

        hour_p = int(np.fmod(ox, 24))
        ax.text(oxn, ymax * .05, str(hour_p), fontsize=8, horizontalalignment='center')

        if ox in [1, 24, 48]:
            l = mlines.Line2D([oxn, oxn],
                              [ymax * .15, ymax], linewidth=1)
            l.set_color("blue")
            ax.add_line(l)

            data_str = datas[int(ox / 24)]
            ax.text(oxn, ymax * .15, data_str, fontsize=8, horizontalalignment='left')


    canvasAgg.draw()
    canvas = canvasAgg.get_tk_widget()
    canvas.pack(fill=BOTH, expand=1)
    frm.pack(fill=BOTH, expand=1)

def button_tranzit(event):
    x_tranzit = canvas.winfo_pointerx() - 103 - newWindow.winfo_x()
    trnzit_gog(x_tranzit)

def calc_date_per():
    lx_val = int(lx_tranzit.get())

    last_num = txt_lastDate.get()
    next_num = txt_nextDate.get()

    last_num = datetime.strptime(last_num, FORMAT_DATE)
    next_num = datetime.strptime(next_num, FORMAT_DATE)

    date_num_period = (next_num - last_num).days
    date_percent = int(1310 / date_num_period)
    return lx_val, date_percent

def button_tranzit_bring_closer(event=None, keyys=False, lx_val=None, date_percent=None, event_scroll=None):

    if not keyys:
        event_scroll = int(event.delta/120)
        lx_val, date_percent = calc_date_per()

    """
        Проверка на флаг
    """
    if button_checkbox_var.get() == 1:
        n_hour = int(labl_tranzit_hour.cget('text'))
        n_hour += event_scroll

        date_per = 0

        if n_hour < 0:
            n_hour = 23
            date_per = -date_percent
        if n_hour > 23:
            n_hour = 0
            date_per = date_percent

        labl_tranzit_hour.config(text=str(n_hour))

        hour_s = str(n_hour)
        if len(hour_s) == 1: hour_s = '0' + hour_s

        trnzit_gog(lx_val + date_per, hour_str=hour_s)
    else:
        if event_scroll == 1:
            trnzit_gog(lx_val + date_percent)
        else:
            trnzit_gog(lx_val - date_percent)

def button_tranzit_bring_left(event):
    lx_val, date_percent = calc_date_per()
    button_tranzit_bring_closer(keyys=True, lx_val=lx_val, date_percent=date_percent, event_scroll=-1)

def button_tranzit_bring_right(event):
    lx_val, date_percent = calc_date_per()
    button_tranzit_bring_closer(keyys=True, lx_val=lx_val, date_percent=date_percent, event_scroll=1)

"""
    periods dates
"""
def new_date(days, to_day=False):
    if not to_day: tranzit_num = labl_tranzit.cget("text")
    else:
        to_date = datetime.today()
        dayt = str(to_date.day)
        mont = str(to_date.month)
        yeat = str(to_date.year)
        if len(dayt) == 1: dayt = '0' + dayt
        if len(mont) == 1: mont = '0' + mont
        tranzit_num = dayt+'.'+mont+'.'+yeat

    tranzit_num = datetime.strptime(tranzit_num, FORMAT_DATE)

    tranzit_num_d = date(tranzit_num.year, tranzit_num.month, tranzit_num.day)

    last_date = tranzit_num_d + timedelta(days=-days)
    next_new_date = tranzit_num_d + timedelta(days=days)

    last_date = last_date.strftime(FORMAT_DATE)
    last_date = str(last_date)
    txt_lastDate.delete(0, END)
    txt_lastDate.insert(0, last_date)

    next_new_date = next_new_date.strftime(FORMAT_DATE)
    next_new_date = str(next_new_date)
    txt_nextDate.delete(0, END)
    txt_nextDate.insert(0, next_new_date)



    xxx1_dateCall()


def button_time_diff_one_week(event):
    new_date(5)

def button_time_diff_one_month(event):
    new_date(15)


def button_time_diff_fix_month(event):
    new_date(46)

def button_tranzit_3_mounth(event):
    new_date(46)

def button_tranzit_1_year(event):
    new_date(549)

def button_time_diff_one_year(event):
    new_date(91)


def button_time_diff_five_years(event):
    new_date(183)


def button_time_diff_ten_years(event):
    new_date(549)


def button_time_a_today(event):

    new_date(183, to_day=True)

"""
    Create new window
"""
newWindow = tkinter.Tk()
newWindow.title("ALL FROM YOU")
newWindow.geometry('1828x720+40+0')

button_aripmethicAstrology = Button(newWindow, text='result', font='Arial 12', command=xxx1_dateCall)
button_aripmethicAstrology.place(x=710, y=6, width=LONG_LABEL, height=HIGH_LABEL)

button_new_date = Button(newWindow, text='new date', font='Arial 12', command=new_date_func)
button_new_date.place(x=815, y=6, width=LONG_LABEL, height=HIGH_LABEL)

button_intervalAstrology = Button(newWindow, text='save pic', font='Arial 12', command=xxx2_dateCall)
button_intervalAstrology.place(x=242, y=6, width=LONG_LABEL, height=HIGH_LABEL)

txt_lastDate = Entry(newWindow, font='Arial 12')
txt_lastDate.insert(0, past_date)
txt_lastDate.place(x=10, y=6, width=LONG_LABEL, height=HIGH_LABEL)

txt_nextDate = Entry(newWindow, font='Arial 12')
txt_nextDate.insert(0, next_ates)
txt_nextDate.place(x=102, y=6, width=LONG_LABEL, height=HIGH_LABEL)

txt_intervalSaveDay = Entry(newWindow, font='Arial 12')
txt_intervalSaveDay.insert(0, "0")
txt_intervalSaveDay.place(x=110 + LONG_LABEL, y=6, width=LONG_LABEL / 2, height=HIGH_LABEL)

company_name_combobox = ttk.Combobox(newWindow, values=companies_names)
company_name_combobox.place(x=335, y=6, width=150, height=HIGH_LABEL)
company_name_combobox.current()
company_name_combobox.set("00000000")
company_name_combobox.bind_all('<<ComboboxSelected>>', companies_selector_handler)

graphic_name_combobox = ttk.Combobox(newWindow, values=NAME_GRAPHICS)
graphic_name_combobox.place(x=487, y=6, width=100, height=HIGH_LABEL)
graphic_name_combobox.current()
graphic_name_combobox.set(NAME_GRAPHICS[DASHA_YEARTABLE])

days_name_combobox = ttk.Combobox(newWindow, values=DAYS_OUTPUT)
days_name_combobox.place(x=593, y=6, width=110, height=HIGH_LABEL)
days_name_combobox.current()
days_name_combobox.set("lahiri")

tranzit_nbGraphic = Notebook(newWindow, width=1900, height=400)
tranzit_nbGraphic.pack(expand=1, fill='both')
tranzit_nbGraphic.place(x=-190, y=30)

"""
    output information baby - Graphic
"""
baby_nbGraphic = Notebook(newWindow, width=2400, height=500)
baby_nbGraphic.pack(expand=1, fill='both')
baby_nbGraphic.place(x=2400, y=30)

frm_baby = Frame(baby_nbGraphic)
fig_baby = plt.figure(facecolor='white', figsize=(22, 4.2))
ax_baby = fig_baby.add_subplot(111)
canvasAgg_baby = FigureCanvasTkAgg(fig_baby, master=frm_baby)
canvas_baby = canvasAgg_baby.get_tk_widget()
xax_baby = ax_baby.xaxis
ax_baby.get_xaxis().set_visible(False)
ax_baby.get_yaxis().set_visible(False)

"""
    output information LEGEND
"""
legend_nbGraphic = Notebook(newWindow, width=200, height=500)
legend_nbGraphic.pack(expand=1, fill='both')
legend_nbGraphic.place(x=1480, y=30)

frm_legend = Frame(legend_nbGraphic)
fig_legend = plt.figure(facecolor='white', figsize=(1.2, 4))
ax_legend = fig_legend.add_subplot(111)
canvasAgg_legend = FigureCanvasTkAgg(fig_legend, master=frm_legend)
canvas_legend = canvasAgg_legend.get_tk_widget()
xax_legend = ax_legend.xaxis
ax_legend.get_xaxis().set_visible(False)
ax_legend.get_yaxis().set_visible(False)

"""
    buttons baby
"""
labl_poz_1 = Label(baby_nbGraphic)
labl_poz_1.place(x=275, y=5, width=75, height=HIGH_LABEL)
labl_poz_1.config(text='мужчина', bg='#FFFFFF')
partner_1_combobox = ttk.Combobox(baby_nbGraphic, values=companies_names)
partner_1_combobox.place(x=275+75+15, y=5, width=150, height=HIGH_LABEL)
partner_1_combobox.current()
partner_1_combobox.set("00000000")

labl_poz_2 = Label(baby_nbGraphic)
labl_poz_2.place(x=275, y=25, width=75, height=HIGH_LABEL)
labl_poz_2.config(text='женщина', bg='#FFFFFF')
partner_2_combobox = ttk.Combobox(baby_nbGraphic, values=companies_names)
partner_2_combobox.place(x=275+75+15, y=25, width=150, height=HIGH_LABEL)
partner_2_combobox.current()
partner_2_combobox.set("00000000")

labl_poz_moon = Label(baby_nbGraphic)
labl_poz_moon.place(x=275+75+15+150+15, y=5, width=120, height=HIGH_LABEL)
labl_poz_moon.config(text='дата начала лунных', bg='#FFFFFF')
partner_day_moon = ttk.Combobox(baby_nbGraphic, values=DAYS)
partner_day_moon.place(x=275+75+15+150+15, y=25, width=35, height=HIGH_LABEL)
partner_day_moon.current()
partner_day_moon.set("30")
partner_month_moon = ttk.Combobox(baby_nbGraphic, values=MONTH)
partner_month_moon.place(x=275+75+15+150+15+30+5, y=25, width=35, height=HIGH_LABEL)
partner_month_moon.current()
partner_month_moon.set("12")
partner_years_moon = ttk.Combobox(baby_nbGraphic, values=YEARS)
partner_years_moon.place(x=275+75+15+150+15+30+5+30+5, y=25, width=50, height=HIGH_LABEL)
partner_years_moon.current()
partner_years_moon.set("2040")

labl_poz_s = Label(baby_nbGraphic)
labl_poz_s.place(x=275+75+15+150+15+30+5+30+5+50+15, y=5, width=120, height=HIGH_LABEL)
labl_poz_s.config(text='дата рождения', bg='#FFFFFF')
partner_day_combobox = ttk.Combobox(baby_nbGraphic, values=DAYS)
partner_day_combobox.place(x=275+75+15+150+15+30+5+30+5+50+15, y=25, width=35, height=HIGH_LABEL)
partner_day_combobox.current()
partner_day_combobox.set("30")
partner_month_combobox = ttk.Combobox(baby_nbGraphic, values=MONTH)
partner_month_combobox.place(x=275+75+15+150+15+30+5+30+5+50+15+30+5, y=25, width=35, height=HIGH_LABEL)
partner_month_combobox.current()
partner_month_combobox.set("12")
partner_years_combobox = ttk.Combobox(baby_nbGraphic, values=YEARS)
partner_years_combobox.place(x=275+75+15+150+15+30+5+30+5+50+15+30+5+30+5, y=25, width=50, height=HIGH_LABEL)
partner_years_combobox.current()
partner_years_combobox.set("2040")

button_time_d_h = Button(baby_nbGraphic, text='расчет')
button_time_d_h.place(x=275+75+15+150+15+30+5+30+5+50+15+30+5+30+5+50+15, y=25, width=50, height=HIGH_LABEL)
button_time_d_h.bind('<Button-1>', calculate_baby)

button_time_d_h = Button(baby_nbGraphic, text='< назад')
button_time_d_h.place(x=225, y=15, width=50, height=HIGH_LABEL)
button_time_d_h.bind('<Button-1>', back_baby)

"""
    buttons
"""

txtDate = Entry(newWindow, font='Arial 12')
txtDate.insert(0, "01.01.0001")
txtDate.place(x=1130, y=6, width=LONG_LABEL, height=HIGH_LABEL)

txtTime = Entry(newWindow, font='Arial 12')
txtTime.insert(0, "09:30:00")
txtTime.place(x=1225, y=6, width=LONG_LABEL, height=HIGH_LABEL)

txtGTM = Entry(newWindow, font='Arial 12')
txtGTM.insert(0, "0")
txtGTM.place(x=1320, y=6, width=HIGH_LABEL, height=HIGH_LABEL)

txtAltitude = Entry(newWindow, font='Arial 12')
txtAltitude.insert(0, "60.00.00")
txtAltitude.place(x=1347, y=6, width=70, height=HIGH_LABEL)

txtLongitude = Entry(newWindow, font='Arial 12')
txtLongitude.insert(0, "00.00.00")
txtLongitude.place(x=1430, y=6, width=70, height=HIGH_LABEL)

"""
    add control buttons time
"""
button_time_a_h = Button(newWindow, text='ПЕРИОДЫ')
button_time_a_h.place(x=1530, y=8, width=70, height=HIGH_BUTTON)
button_time_a_h.bind('<Button-1>', good_planets_out)

button_time_a_h = Button(newWindow, text='h>')
button_time_a_h.place(x=1045, y=8, width=LONG_BUTTON, height=HIGH_BUTTON)
button_time_a_h.bind('<Button-1>', button_time_add_hour)

button_time_a_m = Button(newWindow, text='m>')
button_time_a_m.place(x=1020, y=8, width=LONG_BUTTON, height=HIGH_BUTTON)
button_time_a_m.bind('<Button-1>', button_time_add_minute)

button_time_d_h = Button(newWindow, text='<h')
button_time_d_h.place(x=960, y=8, width=LONG_BUTTON, height=HIGH_BUTTON)
button_time_d_h.bind('<Button-1>', button_time_diff_hour)

button_time_d_m = Button(newWindow, text='<m')
button_time_d_m.place(x=985, y=8, width=LONG_BUTTON, height=HIGH_BUTTON)
button_time_d_m.bind('<Button-1>', button_time_diff_minute)

"""
    add control buttons date
"""
button_time_a_day = Button(newWindow, text='d>')
button_time_a_day.place(x=1070, y=8, width=LONG_BUTTON, height=HIGH_BUTTON)
button_time_a_day.bind('<Button-1>', button_time_add_day)

button_time_a_month = Button(newWindow, text='M>')
button_time_a_month.place(x=1095, y=8, width=LONG_BUTTON, height=HIGH_BUTTON)
button_time_a_month.bind('<Button-1>', button_time_add_month)

button_time_d_day = Button(newWindow, text='<d')
button_time_d_day.place(x=935, y=8, width=LONG_BUTTON, height=HIGH_BUTTON)
button_time_d_day.bind('<Button-1>', button_time_diff_day)

button_time_d_month = Button(newWindow, text='<M')
button_time_d_month.place(x=910, y=8, width=LONG_BUTTON, height=HIGH_BUTTON)
button_time_d_month.bind('<Button-1>', button_time_diff_month)

"""
    Research kind dates
    поиск общех закономерностей между рядом событий, или между периодами
"""

def research_dates_periods(event):
    # Вычисление таблицы параметров по датам выбранных периодов
    data_dicts = {}
    for n in range(18):

        data_dicts.update({n: {'start': None, 'finish': None}})

        for label_event, name_event in zip([start_event, finish_event], ['start', 'finish']):
            data_dicts[n][name_event] = label_event[n].get()

    # переломные моменты графика
    collection_break_moments = []

    for n_dict in range(len(data_dicts)):
        new_date_st, new_date_fn = data_dicts[n_dict]['start'], data_dicts[n_dict]['finish']

        if len(new_date_st) != 10 or len(new_date_fn) != 10: continue

        collection_break_moments.extend((new_date_st, new_date_fn))

    print(str(collection_break_moments))

    button_time_d_month.configure(text='-----')
    newWindow.update()

    global delta
    aianamsa = days_name_combobox.get()
    if aianamsa == 'lahiri':
        delta = 0
    elif aianamsa == 'surya siddhanta':
        delta = SURIA_SIDDHANTA_AINAMSHA

    # parametrs_dict = calculate_parametrs(data_dict_up=data_dicts, data_dict_down=data_dicts)
    parametrs_dict = get_break_moments(data_break_moments=collection_break_moments, delta=delta) #oil_break

    button_time_d_month.configure(text='Поиск')
    newWindow.update()


def get_verify_date(event):
    if event.keycode != 8:
        for n in range(18):
            for label_event in [start_event, finish_event]:
                text_ = label_event[n].get()
                if len(text_) > 1:
                    text_ = text_[:10]
                    label_event[n].delete(0, END)
                    label_event[n].insert(0, text_)

                if len(text_) == 2:
                    label_event[n].insert(2, '.')

                if len(text_) == 5:
                    label_event[n].insert(5, '.')

def get_date_from_graphic(event):

    break_flag = False
    for n in range(18):
        for label_event in [start_event, finish_event]:

            if len(label_event[n].get()) == 0:
                break_flag = True
                label_event[n].insert(0, new_date_search)
                break

        if break_flag: break

def get_pozition_from_graphic(event):
    global new_date_search

    x_tranzit = canvas.winfo_pointerx() - 103 - newWindow.winfo_x()

    if 0 <= x_tranzit <= 1300:
        date_percent = coords_date(x_tranzit)

        last_num = txt_lastDate.get()
        last_num = datetime.strptime(last_num, FORMAT_DATE)

        next_num = txt_nextDate.get()
        next_num = datetime.strptime(next_num, FORMAT_DATE)

        delta_period = (next_num - last_num).days

        delta_date = last_num + timedelta(days=date_percent)

        one_day = 1317 / delta_period
        labl_poz.place(x=93 + one_day * date_percent, y=78, width=1, height=308)

        def format_date(strnumber: str = None):
            if len(strnumber) == 1: strnumber = '0'+strnumber
            return strnumber

        new_date_search = format_date(str(delta_date.day)) + "." + \
                            format_date(str(delta_date.month)) + "." + str(delta_date.year)

start_event = {}
finish_event = {}

for n in range(18):
    start_event.update({n: Entry(newWindow, font='Arial 10')})
    start_event[n].insert(0, "")
    start_event[n].place(x=1670, y=30 + n * 22, width=70, height=HIGH_LABEL)
    start_event[n].bind('<Key>', get_verify_date)

    finish_event.update({n: Entry(newWindow, font='Arial 10')})
    finish_event[n].insert(0, "")
    finish_event[n].place(x=1750, y=30 + n * 22, width=70, height=HIGH_LABEL)
    finish_event[n].bind('<Key>', get_verify_date)

button_time_d_month = Button(newWindow, text='Поиск')
button_time_d_month.place(x=1670, y=8, width=70, height=HIGH_BUTTON)
button_time_d_month.bind('<Button-1>', research_dates_periods)

"""
    panel information grahas
"""

inform_nbGraphic = Notebook(newWindow, width=300, height=300)
inform_nbGraphic.pack(expand=1, fill='both')
inform_nbGraphic.place(x=0, y=420)

"""
    panel information people
"""

people_nbGraphic = Notebook(newWindow, width=300, height=300)
people_nbGraphic.pack(expand=1, fill='both')
people_nbGraphic.place(x=1220, y=420)

"""
    output information people
"""

frm_peo = Frame(people_nbGraphic)
fig_peo = plt.figure(facecolor='white', figsize=(3.1, 3.1))
ax_peo = fig_peo.add_subplot(111)
canvasAgg_peo = FigureCanvasTkAgg(fig_peo, master=frm_peo)
canvas_peo = canvasAgg_peo.get_tk_widget()
xax_peo = ax_peo.xaxis
ax_peo.get_xaxis().set_visible(False)
ax_peo.get_yaxis().set_visible(False)

"""
    panel information sydarshana-chakra
"""

sydarshana_nbGraphic = Notebook(newWindow, width=300, height=300)
sydarshana_nbGraphic.pack(expand=1, fill='both')
sydarshana_nbGraphic.place(x=915, y=420)

"""
    output information sydarshana-chakra
"""

frm_sud = Frame(sydarshana_nbGraphic)
fig_sud = plt.figure(facecolor='white', figsize=(3.1, 3.1))
ax_sud = fig_sud.add_subplot(111)
canvasAgg_sud = FigureCanvasTkAgg(fig_sud, master=frm_sud)
canvas_sud = canvasAgg_sud.get_tk_widget()
xax_sud = ax_sud.xaxis
ax_sud.get_xaxis().set_visible(False)
ax_sud.get_yaxis().set_visible(False)

"""
    panel information bhavas
"""

bhava_nbGraphic = Notebook(newWindow, width=300, height=300)
bhava_nbGraphic.pack(expand=1, fill='both')
bhava_nbGraphic.place(x=305, y=420)

"""
    output tranzit
"""

frm = Frame(tranzit_nbGraphic)
fig = plt.figure(facecolor='white', figsize=(18.5, 4))
ax = fig.add_subplot(111)
canvasAgg = FigureCanvasTkAgg(fig, master=frm)
canvas = canvasAgg.get_tk_widget()
xax = ax.xaxis
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
canvas.bind('<Button-1>', button_tranzit)

canvas.bind('<Double-Button-1>', button_tranzit_3_mounth)
canvas.bind('<Double-Button-3>', button_time_diff_five_years)

canvas.bind('<MouseWheel>', button_tranzit_bring_closer)

canvas.bind('<Control-Button-1>', get_date_from_graphic)
canvas.bind('<Control-Motion>', get_pozition_from_graphic)

newWindow.bind('<Left>', button_tranzit_bring_left)
newWindow.bind('<Right>', button_tranzit_bring_right)

"""
    panel natal map
"""

natal_nbGraphic = Notebook(newWindow, width=300, height=300)
natal_nbGraphic.pack(expand=1, fill='both')
natal_nbGraphic.place(x=610, y=420)

frm_nat = Frame(natal_nbGraphic)
fig_nat = plt.figure(facecolor='white', figsize=(3.1, 3.1))
ax_nat = fig_nat.add_subplot(111)
canvasAgg_nat = FigureCanvasTkAgg(fig_nat, master=frm_nat)
canvas_nat = canvasAgg_nat.get_tk_widget()
xax_nat = ax_nat.xaxis
ax_nat.get_xaxis().set_visible(False)
ax_nat.get_yaxis().set_visible(False)

"""
    panel natal map
"""

dataplanets_nbGraphic = Notebook(newWindow, width=300, height=300)
dataplanets_nbGraphic.pack(expand=1, fill='both')
dataplanets_nbGraphic.place(x=1525, y=420)

frm_dpl = Frame(dataplanets_nbGraphic)
fig_dpl = plt.figure(facecolor='white', figsize=(3.1, 3.1))
ax_dpl = fig_dpl.add_subplot(111)
canvasAgg_dpl = FigureCanvasTkAgg(fig_dpl, master=frm_dpl)
canvas_dpl = canvasAgg_dpl.get_tk_widget()
xax_dpl = ax_dpl.xaxis
ax_dpl.get_xaxis().set_visible(False)
ax_dpl.get_yaxis().set_visible(False)

"""
    output god bhavas
"""

frm_bh = Frame(bhava_nbGraphic)
fig_bh = plt.figure(facecolor='white', figsize=(3.1, 3.1))
ax_bh = fig_bh.add_subplot(111)
canvasAgg_bh = FigureCanvasTkAgg(fig_bh, master=frm_bh)
canvas_bh = canvasAgg_bh.get_tk_widget()
xax_bh = ax_bh.xaxis
ax_bh.get_xaxis().set_visible(False)
ax_bh.get_yaxis().set_visible(False)
canvas_bh.bind('<Button-1>', vargas_show)

"""
    output panel strenght planet
"""
frm_inf = Frame(inform_nbGraphic)
fig_inf = plt.figure(facecolor='white', figsize=(3.1, 3.1))
ax_inf = fig_inf.add_subplot(111)
canvasAgg_inf = FigureCanvasTkAgg(fig_inf, master=frm_inf)
canvas_inf = canvasAgg_inf.get_tk_widget()
xax_inf = ax_inf.xaxis
ax_inf.axis('off')
ax_inf.get_xaxis().set_visible(False)
ax_inf.get_yaxis().set_visible(False)
canvas_inf.bind('<Button-1>', button_strenght_planet)

scroll_nbGraphic = Notebook(canvas, width=1900, height=20)
scroll_nbGraphic.pack(expand=1, fill='both')
scroll_nbGraphic.place(x=0, y=357)

"""
    add buttons periods past
"""
button_time_d_one_week = Button(scroll_nbGraphic, text='1 week')
button_time_d_one_week.place(x=510, y=6, width=50, height=HIGH_BUTTON)
button_time_d_one_week.bind('<Button-1>', button_time_diff_one_week)

button_time_d_one_month = Button(scroll_nbGraphic, text='1 month')
button_time_d_one_month.place(x=450, y=6, width=50, height=HIGH_BUTTON)
button_time_d_one_month.bind('<Button-1>', button_time_diff_one_month)

button_time_d_fix_month = Button(scroll_nbGraphic, text='3 month')
button_time_d_fix_month.place(x=390, y=6, width=50, height=HIGH_BUTTON)
button_time_d_fix_month.bind('<Button-1>', button_time_diff_fix_month)

button_time_d_one_year = Button(scroll_nbGraphic, text='6 month')
button_time_d_one_year.place(x=330, y=6, width=50, height=HIGH_BUTTON)
button_time_d_one_year.bind('<Button-1>', button_time_diff_one_year)

button_time_d_five_years = Button(scroll_nbGraphic, text='1 year')
button_time_d_five_years.place(x=270, y=6, width=50, height=HIGH_BUTTON)
button_time_d_five_years.bind('<Button-1>', button_time_diff_five_years)

button_time_d_ten_years = Button(scroll_nbGraphic, text='3 years')
button_time_d_ten_years.place(x=210, y=6, width=50, height=HIGH_BUTTON)
button_time_d_ten_years.bind('<Button-1>', button_time_diff_ten_years)

button_time_today = Button(scroll_nbGraphic, text='today')
button_time_today.place(x=760, y=6, width=50, height=HIGH_BUTTON)
button_time_today.bind('<Button-1>', button_time_a_today)

"""
    add buttons controll reriods
"""
button_time_scroll_d_one_year = Button(scroll_nbGraphic, text='<---3y')
button_time_scroll_d_one_year.place(x=600, y=6, width=50, height=HIGH_BUTTON)
button_time_scroll_d_one_year.bind('<Button-1>', button_time_scroll_diff_one_year)
button_time_scroll_d_one_year.bind('<Button-3>', button_time_scroll_diff_one_mmm)

button_time_scroll_d_three_month = Button(scroll_nbGraphic, text='<--1y')
button_time_scroll_d_three_month.place(x=650, y=6, width=50, height=HIGH_BUTTON)
button_time_scroll_d_three_month.bind('<Button-1>', button_time_scroll_diff_three_month)
button_time_scroll_d_three_month.bind('<Button-3>', button_time_scroll_diff_three_mmm)

button_time_scroll_d_one_month = Button(scroll_nbGraphic, text='<12y')
button_time_scroll_d_one_month.place(x=700, y=6, width=50, height=HIGH_BUTTON)
button_time_scroll_d_one_month.bind('<Button-1>', button_time_scroll_diff_one_month)

button_time_scroll_a_one_month = Button(scroll_nbGraphic, text='12y>')
button_time_scroll_a_one_month.place(x=820, y=6, width=50, height=HIGH_BUTTON)
button_time_scroll_a_one_month.bind('<Button-1>', button_time_scroll_add_one_month)

button_time_scroll_a_three_month = Button(scroll_nbGraphic, text='1y-->')
button_time_scroll_a_three_month.place(x=870, y=6, width=50, height=HIGH_BUTTON)
button_time_scroll_a_three_month.bind('<Button-1>', button_time_scroll_add_three_month)
button_time_scroll_a_three_month.bind('<Button-3>', button_time_scroll_add_three_mmm)

button_time_scroll_a_one_year = Button(scroll_nbGraphic, text='3y--->')
button_time_scroll_a_one_year.place(x=920, y=6, width=50, height=HIGH_BUTTON)
button_time_scroll_a_one_year.bind('<Button-1>', button_time_scroll_add_one_year)
button_time_scroll_a_one_year.bind('<Button-3>', button_time_scroll_add_one_mmm)

lx_tranzit = Entry(scroll_nbGraphic, font='Arial 12')
lx_tranzit.insert(0, "0")
lx_tranzit.place(x=1100, y=3, width=70, height=HIGH_LABEL)

labl_tranzit = Label(scroll_nbGraphic)
labl_tranzit.place(x=1100, y=3, width=80, height=HIGH_LABEL)
labl_tranzit.config(bg=COLOR_LABL[0], text=today_date)

labl_poz = Label(newWindow)
labl_poz.place(x=2103, y=260, width=4, height=200)
labl_poz.config(bg='#000000')

labl_poz.bind('<Button-1>', button_tranzit)
labl_poz.bind('<Double-Button-1>', button_tranzit_3_mounth)
labl_poz.bind('<Double-Button-3>', button_time_diff_five_years)
labl_poz.bind('<MouseWheel>', button_tranzit_bring_closer)
labl_poz.bind('<Control-Button-1>', get_date_from_graphic)

button_time_of_burn = Button(scroll_nbGraphic, text='find time of burn')
button_time_of_burn.place(x=990, y=6, width=100, height=HIGH_BUTTON)
button_time_of_burn.bind('<Button-1>', find_time_of_burn_func)

labl_tranzit_hour = Label(scroll_nbGraphic)
labl_tranzit_hour.place(x=1210, y=3, width=20, height=HIGH_LABEL)
labl_tranzit_hour.config(bg=COLOR_LABL[0], text='0')

button_checkbox_var = IntVar()
button_checkbox = Checkbutton(scroll_nbGraphic, text='Дата / Час', variable=button_checkbox_var, onvalue=1, offvalue=0)
button_checkbox.place(x=1250, y=6, width=100, height=HIGH_BUTTON)
button_checkbox.config(bg='#FFFFFF')

button_time_of_3days = Button(scroll_nbGraphic, text='подробнее')
button_time_of_3days.place(x=1390, y=6, width=100, height=HIGH_BUTTON)
button_time_of_3days.bind('<Button-1>', find_time_of_burn_3days)

on_muhurta = BooleanVar()
on_muhurta.set(0)
check_muhurts = Checkbutton(scroll_nbGraphic, text='', variable=on_muhurta, onvalue=1, offvalue=0)
check_muhurts.place(x=1520, y=3)
check_muhurts.config(bg='#FFFFFF')

button_muhurts = Button(scroll_nbGraphic, text='мухурты')
button_muhurts.place(x=1540, y=6, width=100, height=HIGH_BUTTON)
button_muhurts.bind('<Button-1>', find_time_of_muhurts)

"""
    window good effect planets
"""
good_planets_nbGraphic = Frame(newWindow, width=1900, height=710)
good_planets_nbGraphic.pack(expand=1, fill='both')
good_planets_nbGraphic.place(x=2000, y=0)
good_planets_nbGraphic.bind('<Button-1>', good_planets_out)

"""
    Scroll data
"""
scroll_base_data = Scrollbar(good_planets_nbGraphic)
canvas_box = Canvas(good_planets_nbGraphic, bg='#FFFFFF', yscrollcommand=scroll_base_data.set, width=1900, height=710)

scroll_base_data.config(command=canvas_box.yview)
scroll_base_data.pack(side=LEFT, fill=Y)

frame_t = Frame(canvas_box)
canvas_box.pack(side='left', fill='both', expand=True)
canvas_box.create_window(0, 0, window=frame_t, anchor='nw')

"""
    good_planets_nbGraphic Astrology base
"""
fig_t = plt.figure(facecolor='white', figsize=(10, 100), edgecolor='white')
ax_t = fig_t.add_subplot(111)
canvasAgg_t = FigureCanvasTkAgg(fig_t, master=frame_t)
canvas_t = canvasAgg_t.get_tk_widget()
ax_t.get_xaxis().set_visible(False)
ax_t.get_yaxis().set_visible(False)

good_planets_nbGraphic.update()
canvas_box.config(scrollregion=canvas_box.bbox('all'))

"""
    MUHURTS
"""
data_of_muhurts = Notebook(newWindow, width=1900, height=900)
data_of_muhurts.pack(expand=1, fill='both')
data_of_muhurts.place(x=2000, y=30)

scroll_muhurts = Scrollbar(data_of_muhurts)
canvas_muhurts = Canvas(data_of_muhurts, bg='#FFFFFF', yscrollcommand=scroll_muhurts.set, width=1900, height=710)

scroll_muhurts.config(command=canvas_muhurts.yview)
scroll_muhurts.pack(side=LEFT, fill=Y)

frame_muh = Frame(canvas_muhurts)
canvas_muhurts.pack(side='left', fill='both', expand=True)
canvas_muhurts.create_window(0, 0, window=frame_muh, anchor='nw')

"""
    good_planets_nbGraphic Astrology base
"""
fig_muh = plt.figure(facecolor='white', figsize=(10, 100), edgecolor='white')
ax_muh = fig_muh.add_subplot(111)
canvasAgg_muh = FigureCanvasTkAgg(fig_muh, master=frame_muh)
canvas_muh = canvasAgg_muh.get_tk_widget()
ax_muh.get_xaxis().set_visible(False)
ax_muh.get_yaxis().set_visible(False)

data_of_muhurts.update()
canvas_muhurts.config(scrollregion=canvas_muhurts.bbox('all'))

"""
    window for find bern time
"""
find_nbGraphic = Notebook(newWindow, width=1600, height=382)
find_nbGraphic.pack(expand=1, fill='both')
find_nbGraphic.place(x=2000, y=0)

find_b_quit = Button(find_nbGraphic, text='<<<')
find_b_quit.place(x=10, y=6, width=60, height=HIGH_LABEL)
find_b_quit.bind('<Button-1>', find_time_func)

find_b_add_event = Button(find_nbGraphic, text='find time')
find_b_add_event.place(x=74, y=6, width=60, height=HIGH_LABEL)
find_b_add_event.bind('<Button-1>', add_new_event)

list_book = Notebook(find_nbGraphic, width=350, height=682)
list_book.pack(expand=1, fill='both')
list_book.place(x=10, y=45)

list_find = Listbox(list_book)
list_find.pack(expand=1, fill='both')

"""
    добавление множества кнопок
"""

days_combobox = ttk.Combobox(find_nbGraphic, values=days_range)
days_combobox.place(x=x_b_to + 120 * 9, y=6, width=60, height=HIGH_LABEL)
days_combobox.current()
days_combobox.set("Day")

month_combobox = ttk.Combobox(find_nbGraphic, values=month_range)
month_combobox.place(x=x_b_va + 120 * 9, y=6, width=60, height=HIGH_LABEL)
month_combobox.current()
month_combobox.set("Month")

year_combobox = ttk.Combobox(find_nbGraphic, values=year_range)
year_combobox.place(x=x_b_fr + 120 * 9, y=6, width=60, height=HIGH_LABEL)
year_combobox.current()
year_combobox.set("Year")



def newdate_find():
    d_ = days_combobox.get()
    m_ = month_combobox.get()
    y_ = year_combobox.get()
    new_date_panel_str = d_ + "." + m_ + "." + y_
    new_date_panel_time = datetime.strptime(new_date_panel_str, FORMAT_DATE)

    new_date_panel_str = new_date_panel_time.strftime(FORMAT_DATE)
    return new_date_panel_str

def date_button_from_00(event):
    labl_bfrom_00.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 9, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 9, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 9, y=6, width=60, height=HIGH_LABEL)

find_bfrom_00 = Button(find_nbGraphic, text="from date")
find_bfrom_00.place(x=x_b_to, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_00.bind('<Button-1>', date_button_from_00)

labl_bfrom_00 = Label(find_nbGraphic)
labl_bfrom_00.place(x=x_b_to, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_00.config(bg=COLOR_LABL[0])

labl_b_00 = Label(find_nbGraphic)
labl_b_00.place(x=x_b_va, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_00.config(bg=COLOR_LABL[value_but[0]])

def date_button_from_01(event):
    labl_bfrom_01.config(text=newdate_find())

    days_combobox.place(x=x_b_to, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr, y=6, width=60, height=HIGH_LABEL)

find_bfrom_01 = Button(find_nbGraphic, text="from date")
find_bfrom_01.place(x=x_b_to+120, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_01.bind('<Button-1>', date_button_from_01)

labl_bfrom_01 = Label(find_nbGraphic)
labl_bfrom_01.place(x=x_b_to+120, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_01.config(bg=COLOR_LABL[0])

labl_b_01 = Label(find_nbGraphic)
labl_b_01.place(x=x_b_va+120, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_01.config(bg=COLOR_LABL[value_but[1]])

def date_button_from_02(event):
    labl_bfrom_02.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 1, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 1, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 1, y=6, width=60, height=HIGH_LABEL)

find_bfrom_02 = Button(find_nbGraphic, text="from date")
find_bfrom_02.place(x=x_b_to+120*2, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_02.bind('<Button-1>', date_button_from_02)

labl_bfrom_02 = Label(find_nbGraphic)
labl_bfrom_02.place(x=x_b_to+120*2, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_02.config(bg=COLOR_LABL[0])

labl_b_02 = Label(find_nbGraphic)
labl_b_02.place(x=x_b_va+120*2, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_02.config(bg=COLOR_LABL[value_but[2]])

def date_button_from_03(event):
    labl_bfrom_03.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 2, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 2, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 2, y=6, width=60, height=HIGH_LABEL)

find_bfrom_03 = Button(find_nbGraphic, text="from date")
find_bfrom_03.place(x=x_b_to+120*3, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_03.bind('<Button-1>', date_button_from_03)

labl_bfrom_03 = Label(find_nbGraphic)
labl_bfrom_03.place(x=x_b_to+120*3, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_03.config(bg=COLOR_LABL[0])

labl_b_03 = Label(find_nbGraphic)
labl_b_03.place(x=x_b_va+120*3, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_03.config(bg=COLOR_LABL[value_but[3]])

def date_button_from_04(event):
    labl_bfrom_04.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 3, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 3, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 3, y=6, width=60, height=HIGH_LABEL)

find_bfrom_04 = Button(find_nbGraphic, text="from date")
find_bfrom_04.place(x=x_b_to+120*4, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_04.bind('<Button-1>', date_button_from_04)

labl_bfrom_04 = Label(find_nbGraphic)
labl_bfrom_04.place(x=x_b_to+120*4, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_04.config(bg=COLOR_LABL[0])

labl_b_04 = Label(find_nbGraphic)
labl_b_04.place(x=x_b_va+120*4, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_04.config(bg=COLOR_LABL[value_but[4]])

def date_button_from_05(event):
    labl_bfrom_05.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 4, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 4, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 4, y=6, width=60, height=HIGH_LABEL)

find_bfrom_05 = Button(find_nbGraphic, text="from date")
find_bfrom_05.place(x=x_b_to+120*5, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_05.bind('<Button-1>', date_button_from_05)

labl_bfrom_05 = Label(find_nbGraphic)
labl_bfrom_05.place(x=x_b_to+120*5, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_05.config(bg=COLOR_LABL[0])

labl_b_05 = Label(find_nbGraphic)
labl_b_05.place(x=x_b_va+120*5, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_05.config(bg=COLOR_LABL[value_but[5]])

def date_button_from_06(event):
    labl_bfrom_06.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 5, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 5, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 5, y=6, width=60, height=HIGH_LABEL)

find_bfrom_06 = Button(find_nbGraphic, text="from date")
find_bfrom_06.place(x=x_b_to+120*6, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_06.bind('<Button-1>', date_button_from_06)

labl_bfrom_06 = Label(find_nbGraphic)
labl_bfrom_06.place(x=x_b_to+120*6, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_06.config(bg=COLOR_LABL[0])

labl_b_06 = Label(find_nbGraphic)
labl_b_06.place(x=x_b_va+120*6, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_06.config(bg=COLOR_LABL[value_but[6]])

def date_button_from_07(event):
    labl_bfrom_07.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 6, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 6, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 6, y=6, width=60, height=HIGH_LABEL)

find_bfrom_07 = Button(find_nbGraphic, text="from date")
find_bfrom_07.place(x=x_b_to+120*7, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_07.bind('<Button-1>', date_button_from_07)

labl_bfrom_07 = Label(find_nbGraphic)
labl_bfrom_07.place(x=x_b_to+120*7, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_07.config(bg=COLOR_LABL[0])

labl_b_07 = Label(find_nbGraphic)
labl_b_07.place(x=x_b_va+120*7, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_07.config(bg=COLOR_LABL[value_but[7]])

def date_button_from_08(event):
    labl_bfrom_08.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 7, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 7, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 7, y=6, width=60, height=HIGH_LABEL)

find_bfrom_08 = Button(find_nbGraphic, text="from date")
find_bfrom_08.place(x=x_b_to+120*8, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_08.bind('<Button-1>', date_button_from_08)

labl_bfrom_08 = Label(find_nbGraphic)
labl_bfrom_08.place(x=x_b_to+120*8, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_08.config(bg=COLOR_LABL[0])

labl_b_08 = Label(find_nbGraphic)
labl_b_08.place(x=x_b_va+120*8, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_08.config(bg=COLOR_LABL[value_but[8]])

def date_button_from_09(event):
    labl_bfrom_09.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 8, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 8, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 8, y=6, width=60, height=HIGH_LABEL)

def find_button_09(event):
    value_but[9] += 1
    value_but[9] = math.trunc(math.fmod(value_but[9], 3))

    if value_but[9] == 1:
        value_but[8] = 2
    elif value_but[9] == 2:
        value_but[8] = 1
    else:
        value_but[8] = 0

    value_but[7] = value_but[9]
    value_but[5] = value_but[9]
    value_but[3] = value_but[9]
    value_but[1] = value_but[9]

    value_but[6] = value_but[8]
    value_but[4] = value_but[8]
    value_but[2] = value_but[8]
    value_but[0] = value_but[8]

    labl_b_00.config(bg=COLOR_LABL[value_but[0]], text=TEXT_LABL[value_but[0]])
    labl_b_01.config(bg=COLOR_LABL[value_but[1]], text=TEXT_LABL[value_but[1]])
    labl_b_02.config(bg=COLOR_LABL[value_but[2]], text=TEXT_LABL[value_but[2]])
    labl_b_03.config(bg=COLOR_LABL[value_but[3]], text=TEXT_LABL[value_but[3]])
    labl_b_04.config(bg=COLOR_LABL[value_but[4]], text=TEXT_LABL[value_but[4]])
    labl_b_05.config(bg=COLOR_LABL[value_but[5]], text=TEXT_LABL[value_but[5]])
    labl_b_06.config(bg=COLOR_LABL[value_but[6]], text=TEXT_LABL[value_but[6]])
    labl_b_07.config(bg=COLOR_LABL[value_but[7]], text=TEXT_LABL[value_but[7]])
    labl_b_08.config(bg=COLOR_LABL[value_but[8]], text=TEXT_LABL[value_but[8]])
    labl_b_09.config(bg=COLOR_LABL[value_but[9]], text=TEXT_LABL[value_but[9]])

find_bfrom_09 = Button(find_nbGraphic, text="from date")
find_bfrom_09.place(x=x_b_to+120*9, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_09.bind('<Button-1>', date_button_from_09)

labl_bfrom_09 = Label(find_nbGraphic)
labl_bfrom_09.place(x=x_b_to+120*9, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_09.config(bg=COLOR_LABL[0])

find_b_09 = Button(find_nbGraphic, text="< >")
find_b_09.place(x=x_b_va+120*9, y=y_butt, width=60, height=HIGH_LABEL)
find_b_09.bind('<Button-1>', find_button_09)

labl_b_09 = Label(find_nbGraphic)
labl_b_09.place(x=x_b_va+120*9, y=y_labl, width=60, height=HIGH_LABEL)
labl_b_09.config(bg=COLOR_LABL[value_but[9]])

def date_button_from_10(event):
    labl_bfrom_10.config(text=newdate_find())

    days_combobox.place(x=x_b_to + 120 * 9, y=6, width=60, height=HIGH_LABEL)
    month_combobox.place(x=x_b_va + 120 * 9, y=6, width=60, height=HIGH_LABEL)
    year_combobox.place(x=x_b_fr + 120 * 9, y=6, width=60, height=HIGH_LABEL)

find_bfrom_10 = Button(find_nbGraphic, text="to date")
find_bfrom_10.place(x=x_b_to+120*10, y=y_butt, width=60, height=HIGH_LABEL)
find_bfrom_10.bind('<Button-1>', date_button_from_10)

labl_bfrom_10 = Label(find_nbGraphic)
labl_bfrom_10.place(x=x_b_to+120*10, y=y_labl, width=60, height=HIGH_LABEL)
labl_bfrom_10.config(bg=COLOR_LABL[0])

newWindow.mainloop()
