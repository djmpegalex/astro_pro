import math
import numpy as np
from constants import*

def calculate_planet_matrix(graha_in_house, retrogr_planet, hozaeva_in_house):

    bhava_matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for b in ZODIAK_RANGE:
        for p in PLANETS_RANGE:

            if graha_in_house[p] == b:
                bhava_matrix[b][p] += 1  # расположния планет
                if p < 8:
                    bhava_matrix[int(math.fmod(b + 6, 12))][p] += 1  # добавление аспектов на противоположный дом
                    for ml in PLANETS_RANGE:
                        if int(math.fmod(b + 6, 12)) == graha_in_house[ml]:
                            for bh in ZODIAK_RANGE:
                                if ml == hozaeva_in_house[bh]:
                                    bhava_matrix[bh][p] += 1
                                    bhava_matrix[int(math.fmod(b + 6, 12))][ml] += 1
                        # если аспектирует другую планету как хозяина другой бхавы
                if retrogr_planet[p] == 1:
                    bhava_matrix[int(math.fmod(b + 5, 12))][p] += 1
                    for ml in PLANETS_RANGE:
                        if int(math.fmod(b + 5, 12)) == graha_in_house[ml]:
                            for bh in ZODIAK_RANGE:
                                if ml == hozaeva_in_house[bh]:
                                    bhava_matrix[bh][p] += 1
                                    bhava_matrix[int(math.fmod(b + 5, 12))][ml] += 1

                if p == 2:
                    bhava_matrix[int(math.fmod(b + 3, 12))][p] += 1
                    bhava_matrix[int(math.fmod(b + 7, 12))][p] += 1
                    for ml in PLANETS_RANGE:
                        if int(math.fmod(b + 3, 12)) == graha_in_house[ml]:
                            for bh in ZODIAK_RANGE:
                                if ml == hozaeva_in_house[bh]:
                                    bhava_matrix[bh][p] += 1
                                    bhava_matrix[int(math.fmod(b + 3, 12))][ml] += 1
                    for ml in PLANETS_RANGE:
                        if int(math.fmod(b + 7, 12)) == graha_in_house[ml]:
                            for bh in ZODIAK_RANGE:
                                if ml == hozaeva_in_house[bh]:
                                    bhava_matrix[bh][p] += 1
                                    bhava_matrix[int(math.fmod(b + 7, 12))][ml] += 1
                    if retrogr_planet[p] == 1:
                        bhava_matrix[int(math.fmod(b + 2, 12))][p] += 1
                        bhava_matrix[int(math.fmod(b + 6, 12))][p] += 1
                        for ml in PLANETS_RANGE:
                            if int(math.fmod(b + 2, 12)) == graha_in_house[ml]:
                                for bh in ZODIAK_RANGE:
                                    if ml == hozaeva_in_house[bh]:
                                        bhava_matrix[bh][p] += 1
                                        bhava_matrix[int(math.fmod(b + 2, 12))][ml] += 1
                        for ml in PLANETS_RANGE:
                            if int(math.fmod(b + 6, 12)) == graha_in_house[ml]:
                                for bh in ZODIAK_RANGE:
                                    if ml == hozaeva_in_house[bh]:
                                        bhava_matrix[bh][p] += 1
                                        bhava_matrix[int(math.fmod(b + 6, 12))][ml] += 1

                if (p == 4) or (p == 7):
                    bhava_matrix[int(math.fmod(b + 4, 12))][p] += 1
                    bhava_matrix[int(math.fmod(b + 8, 12))][p] += 1
                    for ml in PLANETS_RANGE:
                        if int(math.fmod(b + 4, 12)) == graha_in_house[ml]:
                            for bh in ZODIAK_RANGE:
                                if ml == hozaeva_in_house[bh]:
                                    bhava_matrix[bh][p] += 1
                                    bhava_matrix[int(math.fmod(b + 4, 12))][ml] += 1
                    for ml in PLANETS_RANGE:
                        if int(math.fmod(b + 8, 12)) == graha_in_house[ml]:
                            for bh in ZODIAK_RANGE:
                                if ml == hozaeva_in_house[bh]:
                                    bhava_matrix[bh][p] += 1
                                    bhava_matrix[int(math.fmod(b + 8, 12))][ml] += 1
                    if retrogr_planet[p] == 1:
                        bhava_matrix[int(math.fmod(b + 3, 12))][p] += 1
                        bhava_matrix[int(math.fmod(b + 7, 12))][p] += 1
                        for ml in PLANETS_RANGE:
                            if int(math.fmod(b + 3, 12)) == graha_in_house[ml]:
                                for bh in ZODIAK_RANGE:
                                    if ml == hozaeva_in_house[bh]:
                                        bhava_matrix[bh][p] += 1
                                        bhava_matrix[int(math.fmod(b + 3, 12))][ml] += 1
                        for ml in PLANETS_RANGE:
                            if int(math.fmod(b + 7, 12)) == graha_in_house[ml]:
                                for bh in ZODIAK_RANGE:
                                    if ml == hozaeva_in_house[bh]:
                                        bhava_matrix[bh][p] += 1
                                        bhava_matrix[int(math.fmod(b + 7, 12))][ml] += 1

                if p == 6:
                    bhava_matrix[int(math.fmod(b + 2, 12))][p] += 1
                    bhava_matrix[int(math.fmod(b + 9, 12))][p] += 1
                    for ml in PLANETS_RANGE:
                        if int(math.fmod(b + 2, 12)) == graha_in_house[ml]:
                            for bh in ZODIAK_RANGE:
                                if ml == hozaeva_in_house[bh]:
                                    bhava_matrix[bh][p] += 1
                                    bhava_matrix[int(math.fmod(b + 2, 12))][ml] += 1
                    for ml in PLANETS_RANGE:
                        if int(math.fmod(b + 9, 12)) == graha_in_house[ml]:
                            for bh in ZODIAK_RANGE:
                                if ml == hozaeva_in_house[bh]:
                                    bhava_matrix[bh][p] += 1
                                    bhava_matrix[int(math.fmod(b + 9, 12))][ml] += 1
                    if retrogr_planet[p] == 1:
                        bhava_matrix[int(math.fmod(b + 1, 12))][p] += 1
                        bhava_matrix[int(math.fmod(b + 8, 12))][p] += 1
                        for ml in PLANETS_RANGE:
                            if int(math.fmod(b + 1, 12)) == graha_in_house[ml]:
                                for bh in ZODIAK_RANGE:
                                    if ml == hozaeva_in_house[bh]:
                                        bhava_matrix[bh][p] += 1
                                        bhava_matrix[int(math.fmod(b + 1, 12))][ml] += 1
                        for ml in PLANETS_RANGE:
                            if int(math.fmod(b + 8, 12)) == graha_in_house[ml]:
                                for bh in ZODIAK_RANGE:
                                    if ml == hozaeva_in_house[bh]:
                                        bhava_matrix[bh][p] += 1
                                        bhava_matrix[int(math.fmod(b + 8, 12))][ml] += 1

            if hozaeva_in_house[b] == p: bhava_matrix[b][p] += 1  # планета является хозяином дома
            if int(math.fmod(graha_in_house[p] + 6, 12)) == hozaeva_in_house[b]: bhava_matrix[b][p] += 1  # планета аспектирует владение другой планеты

    return bhava_matrix