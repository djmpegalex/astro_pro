import readPlanetInZnake
from constants import*

# данные о силе планет в знаках
planet_in_znak = readPlanetInZnake.get_planet_in_znak()
# коэффициенты силы планеты в знаке
ratio_planets_in_znak = readPlanetInZnake.get_planet_data(planet_in_znak)

ZNAK_DEBILITATION = [6, 7, 3, 11, 9, 5, 0, 7, 1]
ZNAK_EKZALTATION = [0, 1, 9, 5, 3, 11, 6, 1, 7]

def calculate_power_planet_in_znaks_func(positions_in_znak, fire_planets, bala_planets_znak, grahas_degrees):
    power_planets_in_znaks = [float(planet_in_znak.get(positions_in_znak[SUN_PLANET_NUMBER]).ratio_sun),
                              float(planet_in_znak.get(positions_in_znak[MOON_PLANET_NUMBER]).ratio_moon),
                              float(planet_in_znak.get(positions_in_znak[MARS_PLANET_NUMBER]).ratio_mars),
                              float(planet_in_znak.get(positions_in_znak[MERCURY_PLANET_NUMBER]).ratio_mercury),
                              float(planet_in_znak.get(positions_in_znak[JUPITER_PLANET_NUMBER]).ratio_jupiter),
                              float(planet_in_znak.get(positions_in_znak[VENUS_PLANET_NUMBER]).ratio_venus),
                              float(planet_in_znak.get(positions_in_znak[SATURN_PLANET_NUMBER]).ratio_saturn), -1, -1]

    for i in PLANETS_RANGE:
        # перемножаем велечины лучи в знаке друга/врага и лучи в своем положении
        power_planets_in_znaks[i] *= bala_planets_znak[i]
        # умножим промежуточный результат на угловой процент расстояния планеты от дебилитации PERCENT_ANGLE_ZODIAK
        # в расчетах учитываются следующие массивы
        # array_power_planets_in_znaks - КОЛИЧЕСТВО ЛУЧЕЙ ПЛАНЕТЫ В ЗНАКАХ ЗОДИАКА
        # between_planet_angle - БЛИЗОСТЬ ПЛАНЕТЫ К ТОЧКЕ СВОЕЙ ДИБИЛИТАЦИИ
        # array_FireSunPlanets - СТЕПЕНЬ СГОРАНИЯ ПЛАНЕТ
        between_planet_angle = grahas_degrees[i] - ARRAY_BALA_PLANT[i * 2 + 90] + SECONDS_IN_HALF_DEGREE
        viseversa_planet_angle = SECONDS_IN_ZODIAC - between_planet_angle
        if between_planet_angle >= 0 and between_planet_angle <= SECONDS_IN_HALF_ZODIAC:
            power_planets_in_znaks[i] *= (between_planet_angle * PERCENT_ANGLE_ZODIAK)
        elif viseversa_planet_angle >= 0 and viseversa_planet_angle <= SECONDS_IN_HALF_ZODIAC:
            power_planets_in_znaks[i] *= ((viseversa_planet_angle) * PERCENT_ANGLE_ZODIAK) * fire_planets[i]

        if positions_in_znak[i] == ZNAK_DEBILITATION[i]:
            power_planets_in_znaks[i] *= 0.01
        if positions_in_znak[i] == ZNAK_EKZALTATION[i]:
            power_planets_in_znaks[i] *= 3

    return power_planets_in_znaks