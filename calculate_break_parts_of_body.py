import math
from constants import *

znaks_by_part_body = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      2, 2, 2, 3, 3, 4, 4, 4, 3, 3, 2, 2,
                      5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6]


class choice():
    def __init__(self, ratio_parts_of_body_drakkana, planets_of_znakbody):
        self.ratio_parts_of_body_drakkana = ratio_parts_of_body_drakkana
        self.planets_of_znakbody = planets_of_znakbody


def get_break_parts_of_body(whole_drekkana, graha_in_znak, power_nature_all, aspect):
    break_parts_of_body_drakkana = [0] * 36
    planets_of_znakbody = [-1] * 36
    max_number = -SECONDS_IN_ZNAK
    min_number = SECONDS_IN_ZNAK

    for i in PLANETS_RANGE:
        power_nature_all[i] = (power_nature_all[i] * 60) + (aspect[i] * 5)
        if max_number < power_nature_all[i]:
            max_number = power_nature_all[i]

        if min_number > power_nature_all[i]:
            min_number = power_nature_all[i]

    ratio_power_nature_all = []
    for i in PLANETS_RANGE:
        ratio_power_nature_all.append(math.trunc((power_nature_all[i] - min_number) / (max_number - min_number) * 100))

    for i in PLANETS_RANGE:
        break_parts_of_body_drakkana[whole_drekkana[i]] += (100 - ratio_power_nature_all[i]) * 60

        for x in range(36):
            if znaks_by_part_body[x] == graha_in_znak[i]:
                break_parts_of_body_drakkana[x] += (100 - ratio_power_nature_all[i]) * 60
                planets_of_znakbody[x] = i

    max_number = -SECONDS_IN_ZNAK
    min_number = SECONDS_IN_ZNAK
    for i in range(36):
        if max_number < break_parts_of_body_drakkana[i]:
            max_number = break_parts_of_body_drakkana[i]

        if min_number > break_parts_of_body_drakkana[i]:
            min_number = break_parts_of_body_drakkana[i]

    return choice(list(
        map(lambda x: (math.trunc((x - min_number) / (max_number - min_number) * 100)), break_parts_of_body_drakkana)),
                  planets_of_znakbody)
