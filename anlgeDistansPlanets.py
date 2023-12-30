from constants import *
import numpy as np


def calculateDistansePlanets(Planet, tranzit_absolut_degree):
    plDist = []

    for x_planet in PLANETS_RANGE:
            plDist.append(
                np.trunc(np.modf((tranzit_absolut_degree[x_planet] - tranzit_absolut_degree[Planet] + 360)/360)[0]*360)
            )

    return plDist

def calculateDistansePlanets_scale(Planet1, Planet2, scale=360):
    return np.trunc(np.modf((Planet1 - Planet2 + scale)/scale)[0]*scale)
