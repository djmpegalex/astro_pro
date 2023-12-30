from constants import *
import numpy as np

class Choise():

    def __init__(self, filtr_scores_varga, bindy_scores_sarva):
        self.filtr_scores_varga = filtr_scores_varga
        self.bindy_scores_sarva = bindy_scores_sarva

def get_bindy_scores(planets_in_znaks, lagna_in_znak):

    moon_in_znak = planets_in_znaks[MOON_PLANET_NUMBER]
    znaks_range = np.arange(ZNAKS_IN_ZODIAK).tolist()
    znaks_range = znaks_range[moon_in_znak:] + znaks_range[:moon_in_znak]

    bindy_znaks = planets_in_znaks[:7] + [lagna_in_znak]

    bindy_scores_varga, filtr_scores_varga = [], []

    for planet_1 in np.arange(len(bindy_znaks)-1):
        sample_scores = []
        for planet_2 in np.arange(len(bindy_znaks)):
            sample_scores.append(BINDY_POLINTS[planet_1][planet_2][bindy_znaks[planet_1]:] + \
                                BINDY_POLINTS[planet_1][planet_2][:bindy_znaks[planet_1]])

        sample_scores = np.sum(sample_scores, axis=0).tolist()
        bindy_scores_varga.append(sample_scores)

        filtr_scores_varga.append(filter_ashtaka_varga(planet_1, znaks_range, sample_scores))
    bindy_scores_sarva = np.sum(bindy_scores_varga, axis=0).tolist()

    return Choise(filtr_scores_varga, bindy_scores_sarva)


def filter_ashtaka_varga(planet, znaks_range, sample_scores):
    """
        Отмечаем пагубные и благотворные дома, транзиты каждой планеты будут благотворными
    """

    for upachaya_znak in UPACHAYA:
        upach_in_blago = False
        upach = znaks_range[upachaya_znak] # номер упачая знака

        """
            Проверяем попадается ли в упачая знак в собственный или знак экзальтации
        """
        if (upach == EKSATS_PLANETS_IN_ZNAKS[planet]) or \
                (upach in SELF_ZNAKS[planet]): upach_in_blago = True

        # """
        #     Попадает ли упачая в дружественный знак
        # """
        elif FRND == RELATION_PLANETS_START[planet][WHO_UPRAVLAET_ZNAKOM[upach]]: upach_in_blago = True

        if not upach_in_blago: sample_scores[upachaya_znak] = 4

    """
        Неблагоприятные транзиты
    """
    for apachaya_znak in APACHAYA:
        apach_in_not_blago = False
        apach = znaks_range[apachaya_znak] # номер упачая знака

        """
            Проверяем попадается ли в упачая знак в собственный или знак экзальтации
        """
        if apach == SELF_DEBILITATION[planet]: apach_in_not_blago = True

        # """
        #     Попадает ли упачая в дружественный знак
        # """
        elif ENEM == RELATION_PLANETS_START[planet][WHO_UPRAVLAET_ZNAKOM[apach]]: apach_in_not_blago = True

        if not apach_in_not_blago: sample_scores[apachaya_znak] = 4

    return sample_scores

