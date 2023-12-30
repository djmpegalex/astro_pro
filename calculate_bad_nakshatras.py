import math
from constants import *

def get_bad_nakshatras(graha_in_nakshatras):

    return list(map(lambda x: math.fmod(x, NAKSHATRAS_IN_ZODIAK), [graha_in_nakshatras[SATURN_PLANET_NUMBER] + 6,
                              graha_in_nakshatras[SATURN_PLANET_NUMBER] + 19,
                              45 - graha_in_nakshatras[SUN_PLANET_NUMBER] + 18,
                              45 - graha_in_nakshatras[MARS_PLANET_NUMBER] + 18]))
