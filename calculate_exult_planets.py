from constants import *

#           экзальт   мулатр     собств     собств     дебилет    друг     друг      друг       друг       друг       враг       враг       враг       враг
koef_poz = [1,        1,         1,         1,         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
list_poz = ['exz',    'mula',    'self',     'self',     'deb',       'frd',      'frd',      'frd',      'frd',      'frd', 'enm', 'enm', 'enm', 'enm']

def calc_list_power_planet(power_planet=0, planets_in_angles=None, koef=1):
    for n, planet_angles in enumerate(planets_in_angles[0:7]):
        if planet_angles is None: continue

        for m in np.arange(len(koef_poz)):
            if (planet_angles >= RESULT_EKSALTATION[n][m][0]) and (planet_angles < RESULT_EKSALTATION[n][m][1]):
                power_planet += koef_poz[m] * koef
                if (m >= 4) and (m <= 8): break
                elif (m >= 9) and (m <= 12): break

    return power_planet


def calc_self_aspects(transit_graha_in_degrees, trazit_retrograd):
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    planets_in_angles = np.asarray(np.array(transit_graha_in_degrees) / 3600, dtype='int32')

    """
        Проверка, аспектирует ли планета свой собственный знак
    """
    aspect_planets_angles = []

    for planet in PLANETS_RANGE:
        aspect_planets = []

        for num_asp, aspect in enumerate(ASP_2[planet]):
            retr_algle = 0
            if trazit_retrograd[planet] == 1: retr_algle = -30
            if num_asp == 0: retr_algle = 0

            aspect_planets.append(np.fmod(aspect * 30 + planets_in_angles[planet] + retr_algle + 360, 360))
        for add_none in np.arange(4 - len(ASP_2[planet])):
            aspect_planets.append(None)
        aspect_planets_angles.append(aspect_planets)

    aspect_planets_angles = np.array(aspect_planets_angles).T

    for list_aspects_in_angles in aspect_planets_angles:
        for n, planet_angles in enumerate(list_aspects_in_angles):
            findr = None
            if planet_angles is None:
                continue

            for m in np.arange(len(koef_poz)):
                if (planet_angles >= RESULT_EKSALTATION[n][m][0]) and (planet_angles < RESULT_EKSALTATION[n][m][1]):
                    findr = list_poz[m]
                    if findr == 'self': result[n] = 1

    return result


def calculate_goods_pozition(transit_graha_in_degrees, trazit_retrograd):
    planets_in_angles = np.asarray(np.array(transit_graha_in_degrees) / 3600, dtype='int32')
    power_planet = 0

    """
        Проверка, аспектирует ли планета свой собственный знак
    """
    aspect_planets_angles = []

    for planet in PLANETS_RANGE[0:7]:
        aspect_planets = []

        for num_asp, aspect in enumerate(ASP_2[planet]):
            retr_algle= 0
            if trazit_retrograd[planet] == 1: retr_algle = -30
            if num_asp == 0: retr_algle= 0

            aspect_planets.append(np.fmod(aspect*30 + planets_in_angles[planet] + retr_algle + 360, 360))
        for add_none in np.arange(4 - len(ASP_2[planet])):
            aspect_planets.append(None)
        aspect_planets_angles.append(aspect_planets)

    aspect_planets_angles = np.array(aspect_planets_angles).T
    for n_iter, list_aspects_in_angles in enumerate(aspect_planets_angles):
        if n_iter == 0: koef = 1
        else: koef = .8
        power_planet = calc_list_power_planet(power_planet=power_planet,
                                                planets_in_angles=list_aspects_in_angles, koef=koef)
    return int(power_planet)