import numpy as np
from constants import *

def calc_lights(graha_in_znaks, list_planets_in_otnoseniya, retrograd_planets):
    """
    :param graha_in_znaks: планеты в знаках с дробной частью
    :param list_planets_in_otnoseniya: состояния планет, согласно константе NAME_LIGHT_TR
    :return: суммарное число лучей при данном положении планет
    """

    # вычисление долготы до глубокой точки дебилитации * лучевые константы
    full_lights = np.abs(np.asarray(graha_in_znaks[0:7]) - POINT_DEB_ZNAK)
    for i, n in enumerate(full_lights):
        if n > 6: full_lights[i] = 12 - full_lights[i]

    # вводим поправку на сжигание солнцем (исключаем Su, Me, Ve) - если сжигает, аннулируем результат
    planets_distanse_to_sun = np.abs(np.asarray(graha_in_znaks[0:7]) - graha_in_znaks[0])
    for i, n in enumerate(full_lights):
        if n > 6: planets_distanse_to_sun[i] = 12 - planets_distanse_to_sun[i]
    for planet in [1, 2, 4, 6]:
        if planets_distanse_to_sun[planet] < FIRE_SUN_ANGLE[planet]: full_lights[planet] = 0

    # вводим поправочные коэффициенты на ретроградность и на планетные коэффициенты
    full_lights *= LIGHTS_PLANET * (1 - np.array(retrograd_planets[0:7])*.1)

    # делаем поправку, взависимости от состояния планеты
    for planet, otnoseniya in enumerate(list_planets_in_otnoseniya[0:7]):
        for name_otnoseniya, ratio in zip(NAME_LIGHT_TR, RATIO_LIGHT_TR):
            if otnoseniya == name_otnoseniya:
                full_lights[planet] = round(full_lights[planet] * ratio, 2)
                break

    return np.sum(full_lights, dtype='int16')
