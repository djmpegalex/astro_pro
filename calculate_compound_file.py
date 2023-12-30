import math

from calculator_aspects_planet import *
from constants import *


def calculate_compound_grahas(tranzit_in_degrees):
    d_moon = tranzit_in_degrees[1]
    d_sun = tranzit_in_degrees[0]
    negative = []
    positive = []

    if d_sun >= d_moon:
        differense = int((SECONDS_IN_ZODIAC - d_sun + d_moon) / 43200)
    else:
        differense = int((d_moon - d_sun) / 43200)

    if differense >= 15:
        negative.append(1)
    else:
        positive.append(1)

    negative.extend((0, 2, 6, 7, 8))
    positive.extend((3, 4, 5))

    output_strenght = []

    for negative_1 in negative:
        for negative_2 in negative:
            if negative_1 != negative_2:
                differense = get_pozitiv_number(tranzit_in_degrees[negative_1], tranzit_in_degrees[negative_2])
                if differense <= SECONDS_IN_DEGREE * 1.5:
                    output_strenght.append(-60)

    for negative_1 in negative:
        for positive_1 in positive:
            differense = get_pozitiv_number(tranzit_in_degrees[negative_1], tranzit_in_degrees[positive_1])
            if differense <= SECONDS_IN_DEGREE * 1.5:
                output_strenght.append(-30)

    for positive_1 in positive:
        for positive_2 in positive:
            if positive_1 != positive_2:
                differense_n_n = get_pozitiv_number(tranzit_in_degrees[positive_1], tranzit_in_degrees[positive_2])
                if differense_n_n <= SECONDS_IN_DEGREE * 1.5:
                    output_strenght.append(60)

    return output_strenght
