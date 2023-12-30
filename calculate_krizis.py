from constants import *

class KrizisData():
    def __init__(self, my_return, retrograd, planets_in_border, planets_in_look_grahas,
                 planets_in_look_aspects,planets_in_znak):
        self.my_return = my_return
        self.retrograd = retrograd
        self.planets_in_border = planets_in_border
        self.planets_in_look_grahas = planets_in_look_grahas
        self.planets_in_look_aspects = planets_in_look_aspects
        self.planets_in_znak = planets_in_znak


def calc_krizis(transit_graha_in_degrees, speed_planet, graha_in_degrees_next=None):
    """
    функция для просчета факта кризиса. возвращает 1 либо 0.
    :param tranzit_in_znak:
    :return:
    """
    my_return = 0
    add_koef = []
    for n in ZODIAK_RANGE:
        add_koef.append(0.0 / (n+1)) # 0.034

    """
        Составление матрицы параметров планет
    """
    planets_in_znak = []
    planets_in_ganda = []
    planets_in_border = []
    planets_in_selfznak = []
    planets_in_look_grahas = []
    planets_in_retrograd = []
    planets_aspects_deg = []
    planets_aspects_znak = []
    planets_alone = []
    planets_in_selfdebilit = []
    planets_in_eksalt = []
    planets_selfznak_under_aspects = []
    planets_in_look_aspects = []
    planets_get_selfaspect = []
    planets_get_eksaltaspect = []
    planets_aspect_selfznak = [] # Планета аспектирует свой собствнный знаk

    degrees_fire = [15, 12, 17, 14, 11, 10, 16, 16, 17]
    gandas = [0, 432000, 864000, 1296000]
    planets_in_borders = np.linspace(0, 1296000, 13, dtype='int32')

    graha_aspects = [[6], [6], [3, 6, 7], [6], [4, 6, 8], [6], [2, 6, 9], [5, 7, 9], [5, 7, 9]]

    for planet in PLANETS_RANGE:

        planets_in_znak.append(int(transit_graha_in_degrees[planet]/SECONDS_IN_ZNAK))
        # planets_in_next_znak.append(int(graha_in_degrees_next[planet] / SECONDS_IN_ZNAK))

        """
            Планета в Ганде
        """
        planets_in_ganda.append(0)
        for ganda in gandas:
            if abs(ganda - transit_graha_in_degrees[planet]) < 10000:
                planets_in_ganda[-1] = 1

        planets_in_border.append(0)
        if planets_in_znak[planet] in [1, 3, 5, 7, 9, 11]:
            planets_in_border[-1] = 1

        """
            Планета находится в собственном знаке или знаке экзальтации
        """
        planets_in_selfznak.append(0)
        for znak in SELF_ZNAKS[planet]:
            if znak * SECONDS_IN_ZNAK < transit_graha_in_degrees[planet] < (znak + 1) * SECONDS_IN_ZNAK:
                planets_in_selfznak[planet] = 1

        """
            С какими планетами соединяется граха
        """
        graha_1_deg = transit_graha_in_degrees[planet]
        connects = []
        planet_alone = True
        for planet_con, graha_2_deg in enumerate(transit_graha_in_degrees[0:9]):
            if planet == planet_con: continue
            lk_down = -SECONDS_HALF_ZNAK
            lk_up = SECONDS_HALF_ZNAK

            diff = graha_2_deg - graha_1_deg
            if diff < -SECONDS_IN_HALF_ZODIAC:
                diff = SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg
            if diff > SECONDS_IN_HALF_ZODIAC:
                diff = -SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg

            if lk_down < diff < lk_up:
                connects.append(planet_con)

            """
                Одиночество планет, вокруг планеты нету никаких планет в пределах полузнака
            """
            if -SECONDS_HALF_ZNAK < diff < SECONDS_HALF_ZNAK: planet_alone = False
        if planet_alone: planets_alone.append(1)
        else: planets_alone.append(0)

        planets_in_look_grahas.append(connects)

        """
            Ретроградность планет
        """
        if planet in [7, 8]:
            planets_in_retrograd.append(1)
        else:
            if speed_planet[planet] <= 0:
                planets_in_retrograd.append(1)
            else:
                planets_in_retrograd.append(0)

        """
            Аспекты планет
        """
        aspects = []
        aspects_znak = []
        for grasp in graha_aspects[planet]:
            diff = grasp * SECONDS_IN_ZNAK - planets_in_retrograd[planet] * SECONDS_IN_ZNAK + transit_graha_in_degrees[planet]
            if diff > SECONDS_IN_ZODIAC:
                diff -= SECONDS_IN_ZODIAC

            aspects.append(diff)
            aspects_znak.append(int(diff/SECONDS_IN_ZNAK))
        planets_aspects_deg.append(aspects)
        planets_aspects_znak.append(aspects_znak)

        """
            Планета которая аспектирует собственный знак
        """
        planets_aspect_selfznak.append(0)
        for self_znak in SELF_ZNAKS[planet]:
            for aspect_znak in planets_aspects_znak[planet]:
                if aspect_znak == self_znak:
                    planets_aspect_selfznak[planet] = 1

        """
            Планеты в дебилитации
        """
        if SELF_DEBILITATION[planet] * SECONDS_IN_ZNAK <= \
            transit_graha_in_degrees[planet] < \
            (SELF_DEBILITATION[planet] + 1) * SECONDS_IN_ZNAK:
            planets_in_selfdebilit.append(1)
        else:
            planets_in_selfdebilit.append(0)

        """
            Планеты в экзальтации
        """
        if EKSATS_PLANETS_IN_ZNAKS[planet] * SECONDS_IN_ZNAK <= \
            transit_graha_in_degrees[planet] < \
            (EKSATS_PLANETS_IN_ZNAKS[planet] + 1) * SECONDS_IN_ZNAK:
            planets_in_eksalt.append(1)
        else:
            planets_in_eksalt.append(0)


    for planet in PLANETS_RANGE:
        """
            Планеты, их собственные знаки аспектируют другие планеты
        """
        selfznak_under_aspects = []
        planet_under_aspects = []
        for n_planet, planet_aspect in enumerate(planets_aspects_deg):
            if planet == n_planet: continue
            for aspect in planet_aspect:
                for self_znak in SELF_ZNAKS[planet]:
                    if (self_znak - add_koef[self_znak]) * SECONDS_IN_ZNAK < aspect < \
                            (self_znak + 1 - add_koef[self_znak]) * SECONDS_IN_ZNAK:
                        selfznak_under_aspects.append(n_planet)

                """
                    Аспекты, которые попадают в поле видимости на планеты от других планет
                """
                graha_2_deg = transit_graha_in_degrees[planet]
                graha_1_deg = aspect

                lk_down = -SECONDS_HALF_ZNAK
                lk_up = SECONDS_HALF_ZNAK

                diff = graha_2_deg - graha_1_deg
                if diff < -SECONDS_IN_HALF_ZODIAC:
                    diff = SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg
                if diff > SECONDS_IN_HALF_ZODIAC:
                    diff = -SECONDS_IN_ZODIAC - graha_1_deg + graha_2_deg
                if lk_down < diff < lk_up:
                    planet_under_aspects.append(n_planet)

        planets_in_look_aspects.append(planet_under_aspects)
        planets_selfznak_under_aspects.append(selfznak_under_aspects)

        """
            Планета, которая находится под аспектом другой планеты, которая в знаке управления первой планеты. Такая
            планета получая аспект из собственного дома нейтрализуются.
        """
        get_selfaspect = []
        for under_aspect in planets_in_look_aspects[planet]:
            for self_znak in SELF_ZNAKS[planet]:
                if (self_znak - add_koef[self_znak]) * SECONDS_IN_ZNAK < \
                        transit_graha_in_degrees[under_aspect] < (self_znak + 1 - add_koef[self_znak]) * SECONDS_IN_ZNAK:
                    get_selfaspect.append(under_aspect)
        planets_get_selfaspect.append(get_selfaspect)

        """
            Планета, которая находится под аспектом другой планеты, которая в знаке экзальтации первой планеты. Такая
            планета получая аспект из собственного дома становится пагубной.
        """
        get_eksaltaspect = []
        for under_aspect in planets_in_look_aspects[planet]:
            eksalt_znak = EKSATS_PLANETS_IN_ZNAKS[planet]
            if (eksalt_znak - add_koef[eksalt_znak]) * SECONDS_IN_ZNAK < \
                    transit_graha_in_degrees[under_aspect] < (eksalt_znak + 1 - add_koef[eksalt_znak]) * SECONDS_IN_ZNAK:
                get_eksaltaspect.append(under_aspect)
        planets_get_eksaltaspect.append(get_eksaltaspect)


    return KrizisData(my_return=my_return, retrograd=planets_in_retrograd, planets_in_border=planets_in_border,
                      planets_in_look_grahas=planets_in_look_grahas,
                      planets_in_look_aspects=planets_in_look_aspects, planets_in_znak=planets_in_znak)
