from constants import *
import numpy as np

def calculate_balls_kepper_house(hozaeva_in_house, power_to_aspects):
    balls_for_keeper_grahas = [0] * 9
    for planet in PLANETS_RANGE:
        for house in ZODIAK_RANGE:
            if planet == hozaeva_in_house[house]:
                balls_for_keeper_grahas[hozaeva_in_house[house]] += power_to_aspects[planet]

    return balls_for_keeper_grahas