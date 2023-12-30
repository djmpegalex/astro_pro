import math

from constants import MOON_PLANET_NUMBER
from constants import SUN_PLANET_NUMBER
from constants import KETY_PLANET_NUMBER
from constants import MERCURY_PLANET_NUMBER

from constants import SECONDS_IN_ZODIAC
from constants import SECONDS_OF_ASPECT
from constants import MOON_DAY_IN_DEGREES
from constants import DAYS_IN_MOON_MONTH
from constants import PLANETS_RANGE

KETY_START_EXALTATION_DEGREE = 756000
KETY_END_EXALTATION_DEGREE = 863940

class PlanetNatureCalculator:

    def __init__(self):
        pass

    def calculate(self, planets_in_degree_locations):
        # print('planets_in_degree_locations',planets_in_degree_locations)
        rashi_beleficial_ids = []

        # Солнце всегда идентифицируется как зловещая планета
        rashi_beleficial_ids.append(-1)

        moon_degree_location = planets_in_degree_locations[MOON_PLANET_NUMBER]
        sun_degree_location = planets_in_degree_locations[SUN_PLANET_NUMBER]
        kety_degree_location = planets_in_degree_locations[KETY_PLANET_NUMBER]

        moon_sun_diff_in_degrees = moon_degree_location - sun_degree_location
        moon_day = moon_sun_diff_in_degrees / MOON_DAY_IN_DEGREES
        if moon_day < 0:
            if DAYS_IN_MOON_MONTH - (moon_day) >= 8 and DAYS_IN_MOON_MONTH - (moon_day) <= 23:
                rashi_beleficial_ids.append(1)  # Луна возрастает, идентифицируется как благотворная планета
            else:
                rashi_beleficial_ids.append(-1)  # Луна убывает, идентифицируется как зловещая планета
        else:
            if moon_day >= 8 and moon_day <= 23:
                # Луна возрастает, идентифицируется как благотворная планета
                rashi_beleficial_ids.append(1)
            else:
                # Луна убывает, идентифицируется как зловещая планета
                rashi_beleficial_ids.append(-1)

        rashi_beleficial_ids.append(-2)  # Марс всегда идентифицируется как зловещая планета
        rashi_beleficial_ids.append(0)  # Меркурий изначально нейтральный по природе, но меняктся при наличии планет в соединении
        rashi_beleficial_ids.append(2)  # Юпитер всегда идентифицируется как благотворная планета
        rashi_beleficial_ids.append(2)  # Венера всегда идентифицируется как благотворная планета
        rashi_beleficial_ids.append(-2)  # Сатурн всегда идентифицируется как зловещая планета
        rashi_beleficial_ids.append(-2)  # Раху всегда идентифицируется как зловещая планета

        if kety_degree_location > KETY_START_EXALTATION_DEGREE and kety_degree_location < KETY_END_EXALTATION_DEGREE:
            # Кету в положени в экзальтации идентифицируется как благотворная планета
            rashi_beleficial_ids.append(1)
        else:
            # Кету в остальных случаях идентифицируется как зловещая планета
            rashi_beleficial_ids.append(-1)

        for position in PLANETS_RANGE:
            if position != MERCURY_PLANET_NUMBER:

                diff_between_mercury = planets_in_degree_locations[MERCURY_PLANET_NUMBER] - planets_in_degree_locations[position]
                sum_between_mercury = rashi_beleficial_ids[MERCURY_PLANET_NUMBER] + (rashi_beleficial_ids[position])

                if diff_between_mercury < 0 and (
                        (SECONDS_IN_ZODIAC - diff_between_mercury <= SECONDS_OF_ASPECT) or (-diff_between_mercury <= SECONDS_OF_ASPECT)):
                    # Идентифицируется по планетам с которыми соединяестся
                    rashi_beleficial_ids[MERCURY_PLANET_NUMBER] = sum_between_mercury
                elif diff_between_mercury <= SECONDS_OF_ASPECT:
                    # Идентифицируется по планетам с которыми соединяется
                    rashi_beleficial_ids[MERCURY_PLANET_NUMBER] = sum_between_mercury

        self.cast_planet_value(rashi_beleficial_ids, MERCURY_PLANET_NUMBER)

        return rashi_beleficial_ids

    def cast_planet_value(self, identificators, planet_number):
        if identificators[planet_number] == 0:
            identificators[planet_number] = 1
        else:
            identificators[planet_number] = identificators[planet_number] / abs(identificators[planet_number])
