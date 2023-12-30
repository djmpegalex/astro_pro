from calculator_aspects_planet import *
from constants import *

# данные об аспектах планет, взависимости от удаления от аспектирующей планеты
aspect_dict = dictOfAspects.get_aspects_strenght_data()
# градусы
degrees_aspect_dict = dictOfAspects.get_aspects_degrees(aspect_dict)

G_TRANZ = [1283400, 12600, 419400, 444600, 851400, 876600]
MOONG_TRANZ = [1292000, 7400, 428000, 439400, 856000, 871400]
RATIO = [.4, .1, .5, .2, .7, .3, 1, .5, .4]
RATIO_M = [.1, .9, .2, .2, .7, .2, .7, .3, .3]

def get_power_calculate_degress(tranzit_in_degrees, array_bindy, graha_in_chandra_degrees, tranzit_retrograd, PLANETS_RANGE_TR=PLANETS_RANGE):

    power_break_ganda = [0] * 9
    for planet_x in PLANETS_RANGE_TR:
        differense = get_pozitiv_number(tranzit_in_degrees[planet_x], graha_in_chandra_degrees[MOON_PLANET_NUMBER])
        planet_in_house = math.trunc(differense/SECONDS_IN_ZNAK)

        power_break_ganda[planet_x] += (array_bindy[planet_in_house])

        for i in range(3):
            if tranzit_in_degrees[planet_x] >= G_TRANZ[i * 2] and tranzit_in_degrees[planet_x] <= G_TRANZ[i * 2 +1]:
                percent = 1 - ((math.fmod((tranzit_in_degrees[planet_x] + SECONDS_IN_ZODIAC) - G_TRANZ[i], SECONDS_IN_ZODIAC)) / 12600)
                power_break_ganda[planet_x] *= (percent * RATIO[planet_x])

                if tranzit_in_degrees[planet_x] >= MOONG_TRANZ[i * 2] and tranzit_in_degrees[planet_x] <= MOONG_TRANZ[i * 2 +1]:
                    power_break_ganda[planet_x] += (RATIO_M[planet_x]*50)

        if tranzit_retrograd[planet_x] == 1:
            power_break_ganda[planet_x] *= (1 - RATIO[planet_x])
    return power_break_ganda
