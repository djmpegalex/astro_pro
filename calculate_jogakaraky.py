from constants import *
import math

ekzalt, self, drug, neitral, vrag = 1, 1, 1, 0, 0



RELAT_GRAH = [ekzalt, neitral, self, neitral, drug, neitral, vrag, vrag, drug,
              vrag, ekzalt, neitral, drug, vrag, self, drug, drug, drug,
              neitral, drug, vrag, self, vrag, drug, drug, neitral, neitral,
              drug, self, drug, vrag, ekzalt, vrag, vrag, vrag, vrag,
              self, drug, drug, drug, drug, vrag, vrag, vrag, vrag,
              neitral, drug, vrag, ekzalt, vrag, drug, drug, neitral, neitral,
              vrag, neitral, neitral, drug, vrag, self, ekzalt, drug, drug,
              drug, neitral, self, neitral, drug, neitral, vrag, vrag, self,
              drug, neitral, drug, neitral, self, neitral, neitral, drug, neitral,
              vrag, neitral, ekzalt, neitral, neitral, drug, self, drug, drug,
              vrag, neitral, neitral, neitral, neitral, drug, self, drug, drug,
              drug, neitral, drug, neitral, self, ekzalt, neitral, self, neitral]



PLANET_UPRAV = [[4], [3], [0, 7], [2, 5], [8, 11], [1, 6], [9, 10], [10], [7]]


class Choosen():
    def __init__(self, relate_jogakaraka, list_good_planets_joga, list_joga):
        self.relate_jogakaraka = relate_jogakaraka
        self.list_good_planets_joga = list_good_planets_joga
        self.list_joga = list_joga


def get_calculate_jogakaraky(graha_in_znak, polojenie_lagna_rashi, ret_planet, planet_nature_and_rising_sign):
    """
        вычисление триконов и кендр в знаках
    :param graha_in_znak: массив планет, расположенные в знаках
    :param polojenie_lagna_rashi: в каком знаке лагна
    :return: значение благотворности планет по функции йогакараки
    """

    planet_in_house = list(map(lambda x: int(math.fmod(graha_in_znak[x] - polojenie_lagna_rashi + 12, 12)), PLANETS_RANGE))

    relate_planets = list(map(lambda x: RELAT_GRAH_T[int(int(graha_in_znak[x]) * 9) + x], PLANETS_RANGE))

    kendra = list(map(lambda x: int(math.fmod(x + polojenie_lagna_rashi, 12)), [0, 3, 6, 9]))
    trikon = list(map(lambda x: int(math.fmod(x + polojenie_lagna_rashi, 12)), [0, 4, 8]))
    ran_k = len(kendra)
    ran_t = len(trikon)

    graha_uprav_house, uprav_house = [], []
    for n in PLANETS_RANGE:
        for m in range(len(PLANET_UPRAV[n])):
            uprav_house.append(int(math.fmod(PLANET_UPRAV[n][m] - polojenie_lagna_rashi + 12, 12)))
        graha_uprav_house.append(uprav_house)
        uprav_house = []
    # print("graha_uprav_house", graha_uprav_house)

    list_radja_joga = []
    list_laksmi_joga = []
    list_jewelry_joga = []
    list_good_planets_joga = []
    list_parvata_joga = []
    list_gadja_keshari_joga = []

    list_amala_joga = []
    list_khala_joga = []
    list_chamara_joga = []

    relate_jogakaraka = list(map(lambda x: RELAT_GRAH[int(int(graha_in_znak[x]) * 9) + x], PLANETS_RANGE))
    # print("relate_jogakaraka", relate_jogakaraka)
    # происходит взаимный обмен кендрой и триконой n
    for n in PLANETS_RANGE:
        for m in range(len(PLANET_UPRAV[n])):
            """
                управитель 10го дома является йога-каракой
            """
            if PLANET_UPRAV[n][m] == kendra[3]: relate_jogakaraka[n] += 1

            for t in range(ran_t):
                """
                    установим является ли планета правителем трикона t
                """
                if PLANET_UPRAV[n][m] == trikon[t]:

                    """
                        проверка на взаимные аспекты правителей триконы n и кендры x
                    """
                    for casp_n in range(len(ASP[n])):
                        if ASP[n][casp_n] > 0:
                            for ret_n in range(ret_planet[n] + 1):
                                for x in PLANETS_RANGE:
                                    """
                                        проверка на наличие планеты, куда идет аспект с учетом признака ретроградности
                                    """
                                    if int(math.fmod(graha_in_znak[n] + ASP[n][casp_n] - ret_n + 12, 12)) == graha_in_znak[x]:
                                        """
                                            проверка, является ли граха управителем кендры
                                        """
                                        for r in range(len(PLANET_UPRAV[x])):
                                            for s in range(ran_k):
                                                if PLANET_UPRAV[x][r] == kendra[s]:
                                                    """
                                                        проверка взаимного аспекта аспектируемой грахи
                                                    """
                                                    for casp_x in range(len(ASP[x])):
                                                        if ASP[x][casp_x] > 0:
                                                            for ret_x in range(ret_planet[x] + 1):
                                                                if int(math.fmod(graha_in_znak[x] + ASP[x][casp_x] - ret_x + 12, 12)) == \
                                                                        graha_in_znak[n]:
                                                                    relate_jogakaraka[n] += 1
                                                                    list_radja_joga.append([n, x])

                    """
                        если является управителем триконы, тогда проверяем находится ли граха в кендре k
                    """
                    for k in range(ran_k):
                        if graha_in_znak[n] == kendra[k]:
                            """
                                проверяем правление другой грахи над занятой кендрой x, находится ли она в триконе t
                            """
                            for x in PLANETS_RANGE:
                                for y in range(len(PLANET_UPRAV[x])):
                                    for z in range(ran_k):
                                        if (PLANET_UPRAV[x][y] == kendra[z]) and (x != n) and (graha_in_znak[x] == t):
                                            relate_jogakaraka[n] += 1
                                            list_radja_joga.append([n, x])

                    """
                        установим соединяется ли n граха с другой грахой p
                    """
                    for p in PLANETS_RANGE:
                        if (graha_in_znak[n] == graha_in_znak[p]) and (n != p):
                            """
                                если граха n соединяется с грахой p, то проверим является граха p правителем кендры
                            """
                            for r in range(len(PLANET_UPRAV[p])):
                                for s in range(ran_k):
                                    if PLANET_UPRAV[p][r] == kendra[s]:
                                        relate_jogakaraka[n] += 1
                                        list_radja_joga.append([n, p])

                    """
                        проверим расположение правителя трикона в кендре
                    """
                    for k in range(ran_k):
                        if graha_in_znak[n] == kendra[k]:
                            relate_jogakaraka[n] += 1

                    """
                        является ли планета также правителем кендры
                    """
                    for k in range(ran_k):
                        if PLANET_UPRAV[n][m] == kendra[k]:
                            relate_jogakaraka[n] += 1

            """
                выясним правителя кендры в расположении триконы
            """
            for k in range(ran_k):
                if PLANET_UPRAV[n][m] == kendra[k]:

                    """
                        проверка на взаимные аспекты правителей триконы n и кендры x
                    """
                    for casp_n in range(len(ASP[n])):
                        if ASP[n][casp_n] > 0:
                            for ret_n in range(ret_planet[n] + 1):
                                for x in PLANETS_RANGE:
                                    """
                                        проверка на наличие планеты, куда идет аспект без учета признака ретроградности
                                    """
                                    if int(math.fmod(graha_in_znak[n] + ASP[n][casp_n] - ret_n + 12, 12)) == graha_in_znak[x]:
                                        """
                                            проверка, является ли граха управителем кендры
                                        """
                                        for r in range(len(PLANET_UPRAV[x])):
                                            for s in range(ran_t):
                                                if PLANET_UPRAV[x][r] == trikon[s]:
                                                    """
                                                        проверка взаимного аспекта аспектируемой грахи
                                                    """
                                                    for casp_x in range(len(ASP[x])):
                                                        if ASP[x][casp_x] > 0:
                                                            for ret_x in range(ret_planet[x] + 1):
                                                                if int(math.fmod(graha_in_znak[x] + ASP[x][casp_x] - ret_x + 12, 12)) == \
                                                                        graha_in_znak[n]:
                                                                    relate_jogakaraka[n] += 1
                                                                    list_radja_joga.append([n, x])

                    for t in range(ran_t):
                        if graha_in_znak[n] == trikon[t]:
                            relate_jogakaraka[n] += 1

                    """
                        если является управителем кендры, тогда проверяем находится ли граха в триконе
                    """
                    for t in range(ran_t):
                        if graha_in_znak[n] == trikon[t]:
                            """
                                проверяем правление другой грахи над занятой триконом, находится ли она в кендре
                            """
                            for x in PLANETS_RANGE:
                                for y in range(len(PLANET_UPRAV[x])):
                                    for z in range(ran_t):
                                        if (PLANET_UPRAV[x][y] == trikon[z]) and (x != n) and (graha_in_znak[x] == k):
                                            relate_jogakaraka[n] += 1
                                            list_radja_joga.append([n, x])

                    """
                        установим соединяется ли n граха с другой грахой p
                    """
                    for p in PLANETS_RANGE:
                        if (graha_in_znak[n] == graha_in_znak[p]) and (n != p):
                            """
                                если граха n соединяется с грахой p, то проверим является граха p правителем триконы
                            """
                            for r in range(len(PLANET_UPRAV[p])):
                                for s in range(ran_t):
                                    if PLANET_UPRAV[p][r] == trikon[s]:
                                        relate_jogakaraka[n] += 1
                                        list_radja_joga.append([n, p])

    """
        установим планеты, которые расположены в 11 и есть ли аспект на 2ю бхаву. каждая планета должна управлять кендрой или триконом
    """
    for pl_1 in PLANETS_RANGE:
        if planet_in_house[pl_1] == 10:
            """
                проверка аспекта на 2й дом
            """
            for casp_1 in range(len(ASP[pl_1])):
                if ASP[pl_1][casp_1] > 0:
                    for ret_1 in range(ret_planet[pl_1] + 1):
                        done = 0
                        """
                            проверка на наличие аспета планеты pl_1 на 2й дом, куда идет аспект с учетом признака ретроградности
                        """
                        if int(math.fmod(planet_in_house[pl_1] + ASP[pl_1][casp_1] - ret_1 + 12, 12)) == 1:
                            """
                                если есть аспект на 2й дом, то смотрим, есть ли наличие планеты во втором доме
                            """
                            for pl_2 in PLANETS_RANGE:
                                if planet_in_house[pl_2] == 1:
                                    """
                                        проверка аспекта на 10й дом
                                    """
                                    for casp_2 in range(len(ASP[pl_2])):
                                        if ASP[pl_2][casp_2] > 0:
                                            for ret_2 in range(ret_planet[pl_2] + 1):
                                                """
                                                    проверка на наличие аспета планеты pl_2 на 11й дом, куда идет аспект с учетом признака ретроградности
                                                """
                                                if int(math.fmod(planet_in_house[pl_2] + ASP[pl_2][casp_2] - ret_2 + 12, 12)) == 10:
                                                    """
                                                        если есть аспект на 11й дом, то устанавливается связь между планетами pl_1 и pl_2. убедимся в том, что 
                                                        каждая планета управляет домами кендры либо триконы
                                                        проверка, является ли граха управителем кендры
                                                    """
                                                    pl_1_k, pl_1_t, pl_2_k, pl_2_t = 0, 0, 0, 0

                                                    for r in range(len(PLANET_UPRAV[pl_1])):
                                                        for s in range(ran_k):
                                                            if PLANET_UPRAV[pl_1][r] == kendra[s]:
                                                                pl_1_k = 1
                                                        for s in range(ran_t):
                                                            if PLANET_UPRAV[pl_1][r] == trikon[s]:
                                                                pl_1_t = 1

                                                    for r in range(len(PLANET_UPRAV[pl_2])):
                                                        for s in range(ran_k):
                                                            if PLANET_UPRAV[pl_2][r] == kendra[s]:
                                                                pl_2_k = 1
                                                        for s in range(ran_t):
                                                            if PLANET_UPRAV[pl_2][r] == trikon[s]:
                                                                pl_2_t = 1

                                                    if ((pl_1_k > 0) and (pl_2_t > 0)) or ((pl_2_k > 0) and (pl_1_t > 0)):
                                                        list_jewelry_joga.append([pl_1, pl_2])
                                                        done = 1
                                                if done == 1: break
                                        if done == 1: break
                                if done == 1: break

    """
        случай, когда управители 2го и 11го домов соединяются в кендре или триконе
    """
    # находим управителя 2го дома и управителя 11го дома
    uprpl, aspect_pl = [], 0
    # print("graha_uprav_house", graha_uprav_house)
    for x in PLANETS_RANGE:
        for r in range(len(graha_uprav_house[x])):
            for s in [1, 10]:
                if graha_uprav_house[x][r] == s:
                    uprpl.append(x)
                    if len(uprpl) == 2:
                        if (planet_in_house[uprpl[0]] == planet_in_house[uprpl[1]]) and (planet_in_house[uprpl[1]] in [0, 3, 4, 6, 8, 9]):
                            list_jewelry_joga.append(uprpl)

                        """
                            взаимный аспект правителей 2 и 11 бхав
                        """
                        aspect_pl = []
                        for tt in [0, 1]:
                            for casp_x in range(len(ASP[uprpl[tt]])):
                                if ASP[uprpl[tt]][casp_x] > 0:
                                    for ret_x in range(ret_planet[uprpl[tt]] + 1):
                                        if int(math.fmod(planet_in_house[uprpl[tt]] + ASP[uprpl[tt]][casp_x] - ret_x + 12, 12)) == \
                                                planet_in_house[uprpl[tt * (-1) + 1]]:
                                            aspect_pl.append(uprpl[tt])
                                            uprplpp = []
                                            if len(aspect_pl) == 2:
                                                for xx in aspect_pl:
                                                    for npp in range(len(graha_uprav_house[xx])):
                                                        for ss in [1, 10]:
                                                            if graha_uprav_house[xx][npp] == ss:
                                                                uprplpp.append(xx)
                                                                if (len(uprplpp) == 2):
                                                                    if uprplpp[0] != uprplpp[1]:
                                                                        list_jewelry_joga.append(uprplpp)
                                                                        aspect_pl = []

                            """
                                взаимное расположение в домах друг друга
                            """
                            for rr1 in range(len(graha_uprav_house[uprpl[tt]])):
                                for rr2 in range(len(graha_uprav_house[uprpl[tt * (-1) + 1]])):
                                    if (graha_uprav_house[uprpl[tt]][rr1] == 1) and (graha_uprav_house[uprpl[tt * (-1) + 1]][rr2] == 10) and (
                                            planet_in_house[uprpl[tt]] == 10) and (planet_in_house[uprpl[tt * (-1) + 1]] == 1):
                                        list_jewelry_joga.append(uprpl)
                        uprpl = []

    """
        проверка гороскопа на наличие йоги Лакшми
    """
    for x in PLANETS_RANGE:
        for r in range(len(graha_uprav_house[x])):
            if graha_uprav_house[x][r] == 8:
                if (planet_in_house[x] == 8) and (graha_in_znak[3] == 5): list_laksmi_joga.append([x, 3])
                if (graha_in_znak[x] == 11) & (graha_in_znak[5] == 11) & (planet_in_house[6] == 2): list_laksmi_joga.extend(([x, 5], [x, 6]))

    """
        нахождение хозяев 6, 8, 12 домов в этих домах дает благотворность неблаготворной планете, и пагубность 
    """
    for x in PLANETS_RANGE:
        if planet_nature_and_rising_sign[x] < 0:
            # проверка, является ли планета правителем одного из предложенных домов
            for r in range(len(graha_uprav_house[x])):
                for hous_uprav in [5, 7, 11]:
                    if graha_uprav_house[x][r] == hous_uprav:
                        # проверка нахождения правителя одного из указанных домов в указанном доме
                        for hous_local in [5, 7, 11]:
                            if planet_in_house[x] == hous_local:
                                # пагубная планета управляющая 6, 8, 12 домом и находящаяся там становится благотворной
                                list_good_planets_joga.append([x, 1])
                # проверка, правители других домов (не апоклимы)
                for hous_uprav in [0, 1, 2, 3, 4, 6, 8, 9, 10]:
                    if (graha_uprav_house[x][r] == hous_uprav) and ((graha_uprav_house[x][r] in [5, 7, 11]) == False):
                        # проверка нахождения правителя одного из указанных домов в указанном доме
                        for hous_local in [5, 7, 11]:
                            if planet_in_house[x] == hous_local:
                                # любая планета находящаяся в 6, 8, 12 домах становится пагубной
                                list_good_planets_joga.append([x, -1])

    """
        Парвата-йога
    """
    n_bad_planet_kendr = 0
    n_good_planet_kendr = 0
    n_bad_planet_7bhava = 0
    n_bad_planet_8bhava = 0
    n_good_planet_7bhava = 0
    n_good_planet_8bhava = 0
    n_bad_planet_6bhava = 0
    n_good_planet_6bhava = 0
    n_bad_planet_12bhava = 0
    n_good_planet_12bhava = 0
    for x in PLANETS_RANGE:
        # проверка на предмет отсутсвия пагубных планет и присутствия благотворных планет в кендрах
        if (planet_nature_and_rising_sign[x] < 0) and (planet_in_house[x] in [0, 3, 6, 9]): n_bad_planet_kendr += 1
        if (planet_nature_and_rising_sign[x] >= 0) and (planet_in_house[x] in [0, 3, 6, 9]): n_good_planet_kendr += 1
        if (planet_nature_and_rising_sign[x] < 0) and (planet_in_house[x] in [6]): n_bad_planet_7bhava += 1
        if (planet_nature_and_rising_sign[x] >= 0) and (planet_in_house[x] in [6]): n_good_planet_7bhava += 1
        if (planet_nature_and_rising_sign[x] < 0) and (planet_in_house[x] in [7]): n_bad_planet_8bhava += 1
        if (planet_nature_and_rising_sign[x] >= 0) and (planet_in_house[x] in [7]): n_good_planet_8bhava += 1
        if (planet_nature_and_rising_sign[x] < 0) and (planet_in_house[x] in [5]): n_bad_planet_6bhava += 1
        if (planet_nature_and_rising_sign[x] >= 0) and (planet_in_house[x] in [5]): n_good_planet_6bhava += 1
        if (planet_nature_and_rising_sign[x] < 0) and (planet_in_house[x] in [11]): n_bad_planet_12bhava += 1
        if (planet_nature_and_rising_sign[x] >= 0) and (planet_in_house[x] in [11]): n_good_planet_12bhava += 1

    if (n_bad_planet_kendr == 0) and (n_good_planet_kendr > 0):
        # проверка 2х следующих условий.
        # 1. 7, 8 бхавы пустые или хотя бы одна занята только благотворной бхавой
        if ((n_good_planet_7bhava + n_good_planet_8bhava) >= 0) and ((n_bad_planet_7bhava + n_bad_planet_8bhava) == 0):
            # при наличии такой йоги идет выстраивание вязей между планетами
            for x in PLANETS_RANGE:
                for y in PLANETS_RANGE:
                    if (planet_in_house[x] in [0, 3, 6, 7, 9]) and (planet_in_house[y] in [0, 3, 6, 7, 9]) and (x != y):
                        list_parvata_joga.append([x, y])

        if ((n_good_planet_8bhava + n_good_planet_12bhava + n_bad_planet_8bhava + n_bad_planet_12bhava) == 0) and (n_good_planet_kendr > 1):
            for x in PLANETS_RANGE:
                for y in PLANETS_RANGE:
                    if (planet_in_house[x] in [0, 3, 6, 9]) and (planet_in_house[y] in [0, 3, 6, 9]) and (x != y):
                        list_parvata_joga.append([x, y])

        if ((n_good_planet_6bhava > 0) and (n_good_planet_8bhava > 0)) and ((n_bad_planet_6bhava + n_bad_planet_8bhava) == 0):
            for x in PLANETS_RANGE:
                for y in PLANETS_RANGE:
                    if (planet_in_house[x] in [0, 3, 6, 9, 5, 7]) and (planet_in_house[y] in [0, 3, 6, 9, 5, 7]) and (x != y):
                        list_parvata_joga.append([x, y])

    """
        гаджа-кешари йога
    """
    if (planet_in_house[JUPITER_PLANET_NUMBER] in [0, 3, 6, 9]) or (planet_in_house[JUPITER_PLANET_NUMBER] in [planet_in_house[MOON_PLANET_NUMBER],
                                                                                                               int(math.fmod(planet_in_house[MOON_PLANET_NUMBER] + 3, 12)),
                                                                                                               int(math.fmod(planet_in_house[MOON_PLANET_NUMBER] + 6, 12)),
                                                                                                               int(math.fmod(planet_in_house[MOON_PLANET_NUMBER] + 9, 12))]):
        if (relate_planets[JUPITER_PLANET_NUMBER] in [ekzaltt, neitralt, selft, drugt]) and (planet_in_house[JUPITER_PLANET_NUMBER] != planet_in_house[SUN_PLANET_NUMBER]):

            for x in PLANETS_RANGE:
                if planet_nature_and_rising_sign[x] >= 0:
                    for casp in np.arange(len(ASP[x])):
                        for ret in [ret_planet[x] + 1]:
                            if int(math.fmod(planet_in_house[x] + ASP[x][casp] - ret + 12, 12)) == planet_in_house[JUPITER_PLANET_NUMBER]:
                                list_gadja_keshari_joga.extend(([x, JUPITER_PLANET_NUMBER], [x, MOON_PLANET_NUMBER], [JUPITER_PLANET_NUMBER, MOON_PLANET_NUMBER]))

    if planet_in_house[JUPITER_PLANET_NUMBER] in [planet_in_house[MOON_PLANET_NUMBER],
                                                  int(math.fmod(planet_in_house[MOON_PLANET_NUMBER] + 3, 12)),
                                                  int(math.fmod(planet_in_house[MOON_PLANET_NUMBER] + 6, 12)),
                                                  int(math.fmod(planet_in_house[MOON_PLANET_NUMBER] + 9, 12))]:
        for x in [MERCURY_PLANET_NUMBER, VENUS_PLANET_NUMBER, JUPITER_PLANET_NUMBER]:
            if planet_nature_and_rising_sign[x] >= 0:
                for casp in np.arange(len(ASP[x])):
                    for ret in [ret_planet[x] + 1]:
                        if int(math.fmod(planet_in_house[x] + ASP[x][casp] - ret + 12, 12)) == planet_in_house[MOON_PLANET_NUMBER]:

                            if (relate_planets[x] in [ekzaltt, neitralt, selft, drugt]) and (planet_in_house[x] != planet_in_house[SUN_PLANET_NUMBER]):
                                list_gadja_keshari_joga.extend(([x, MOON_PLANET_NUMBER], [x, JUPITER_PLANET_NUMBER], [JUPITER_PLANET_NUMBER, MOON_PLANET_NUMBER]))

    num_pl = 0
    for x in [MERCURY_PLANET_NUMBER, VENUS_PLANET_NUMBER, JUPITER_PLANET_NUMBER]:
        if planet_nature_and_rising_sign[x] >= 0:
            for casp in np.arange(len(ASP[x])):
                for ret in [ret_planet[x] + 1]:
                    if int(math.fmod(planet_in_house[x] + ASP[x][casp] - ret + 12, 12)) == planet_in_house[MOON_PLANET_NUMBER]:
                        if (relate_planets[x] in [ekzaltt, neitralt, selft, drugt]) and (planet_in_house[x] != planet_in_house[SUN_PLANET_NUMBER]):
                            num_pl += 1
                            if num_pl == 3: list_gadja_keshari_joga.extend(([VENUS_PLANET_NUMBER, JUPITER_PLANET_NUMBER],
                                                                            [VENUS_PLANET_NUMBER, MOON_PLANET_NUMBER],
                                                                            [VENUS_PLANET_NUMBER, MERCURY_PLANET_NUMBER],
                                                                            [JUPITER_PLANET_NUMBER, MOON_PLANET_NUMBER],
                                                                            [JUPITER_PLANET_NUMBER, MERCURY_PLANET_NUMBER],
                                                                            [MOON_PLANET_NUMBER, MERCURY_PLANET_NUMBER]))

    """
        Амала-йога
    """
    bad_grah_lg = 0
    good_grah_lg = 0
    bad_grah_ch = 0
    good_grah_ch = 0
    for planet1 in PLANETS_RANGE:

        if planet_in_house[planet1] == 9:
            if planet_nature_and_rising_sign[planet1] >= 0:
                good_grah_lg += 1
            else:
                bad_grah_lg += 1

        if planet_in_house[planet1] == int(
                math.fmod(planet_in_house[MOON_PLANET_NUMBER] + 9, 12)):
            if planet_nature_and_rising_sign[planet1] >= 0:
                good_grah_ch += 1
            else:
                bad_grah_ch += 1

    for planet1 in PLANETS_RANGE:
        if RELAT_GRAH_T[int(int(graha_in_znak[planet1]) * 9) + planet1] in [ekzaltt, neitralt, selft, drugt]:
            if (bad_grah_lg == 0) and (good_grah_lg > 0):
                if planet_in_house[planet1] == 9:
                    for n in PLANETS_RANGE:
                        for m in range(len(graha_uprav_house[n])):
                            if graha_uprav_house[n][m] == 9:
                                list_amala_joga.append([planet1, n])
                                n_010 = n
                            if graha_uprav_house[n][m] == 0:
                                list_amala_joga.append([planet1, n])
                                n_01 = n
                                if ('n_010' in locals()) and ('n_01' in locals()): list_amala_joga.append([n_010, n_01])

            if (bad_grah_ch == 0) and (good_grah_ch > 0):
                if planet_in_house[planet1] == int(
                        math.fmod(planet_in_house[MOON_PLANET_NUMBER] + 9, 12)):
                    for n in PLANETS_RANGE:
                        for m in range(len(PLANET_UPRAV[n])):
                            if graha_uprav_house[n][m] == int(
                                    math.fmod(planet_in_house[MOON_PLANET_NUMBER] + 9, 12)):
                                list_amala_joga.append([planet1, n])
                                n_10 = n
                            if graha_uprav_house[n][m] == planet_in_house[MOON_PLANET_NUMBER]:
                                list_amala_joga.append([planet1, n])
                                n_1 = n
                            if ('n_10' in locals()) and ('n_1' in locals()): list_amala_joga.append([n_10, n_1])

    """
        Кхала-йога
    """
    for pravitel_4bh in PLANETS_RANGE:
        for pravitel_1bh in PLANETS_RANGE:
            if pravitel_4bh != pravitel_1bh:
                for arr_4bh in np.arange(len(graha_uprav_house[pravitel_4bh])):
                    # выясним правителя 4й бхавы
                    if graha_uprav_house[pravitel_4bh][arr_4bh] == 3:
                        # является ли управитель 4й бхавы сильным
                        # print('pravitel_4bh', pravitel_4bh)
                        # print('graha_in_znak[pravitel_4bh]', graha_in_znak[pravitel_4bh])
                        # print('int(graha_in_znak[pravitel_4bh] * 9)', int(graha_in_znak[pravitel_4bh] * 9))
                        # print('int(graha_in_znak[pravitel_4bh] * 9) + pravitel_4bh', int(graha_in_znak[pravitel_4bh] * 9) + pravitel_4bh)
                        # print('len(RELAT_GRAH_T)', len(RELAT_GRAH_T))
                        if RELAT_GRAH_T[np.fmod(int(graha_in_znak[pravitel_4bh] * 9) + pravitel_4bh, 108)] in [ekzaltt, neitralt, selft, drugt]:
                            # выясним правителя 1й бхавы
                            for arr_1bh in np.arange(len(graha_uprav_house[pravitel_1bh])):
                                if graha_uprav_house[pravitel_1bh][arr_1bh] == 0:
                                    # является ли управитель 1й бхавы сильным
                                    if RELAT_GRAH_T[np.fmod(int(graha_in_znak[pravitel_1bh] * 9) + pravitel_1bh, 108)] in [ekzaltt, neitralt, selft, drugt]:

                                        # является ли положение правителя 4й бхавы и юпитера во взаимных кендрах
                                        if (planet_in_house[pravitel_4bh] in [0, 3, 6, 9]) and (
                                                planet_in_house[JUPITER_PLANET_NUMBER] in [0, 3, 6, 9]):
                                            list_khala_joga.extend(([pravitel_4bh, pravitel_1bh],
                                                                    [JUPITER_PLANET_NUMBER, pravitel_4bh],
                                                                    [JUPITER_PLANET_NUMBER, pravitel_1bh]))

                        for arr_1bh in np.arange(len(graha_uprav_house[pravitel_1bh])):
                            # правитель 10го дома сильный
                            if graha_uprav_house[pravitel_1bh][arr_1bh] == 9:
                                if RELAT_GRAH_T[np.fmod(int(graha_in_znak[pravitel_1bh] * 9) + pravitel_1bh, 108)] in [ekzaltt, neitralt, selft, drugt]:
                                    # оба правителя соеденены или аспектируют друг друга
                                    if planet_in_house[pravitel_1bh] == planet_in_house[pravitel_4bh]:
                                        list_khala_joga.append([pravitel_4bh, pravitel_1bh])
                                        # правитель того дома, в котором планеты соединяются
                                        for planet in PLANETS_RANGE:
                                            for arr_pl in np.arange(len(graha_uprav_house[planet])):
                                                if planet_in_house[pravitel_1bh] == graha_uprav_house[planet][arr_pl]:
                                                    list_khala_joga.extend(([pravitel_1bh, planet], [pravitel_4bh, planet]))

                                    #   или правители друг друга аспектируют
                                    for casp in np.arange(len(ASP[pravitel_1bh])):
                                        for ret in [ret_planet[pravitel_1bh] + 1]:
                                            if int(math.fmod(planet_in_house[pravitel_1bh] + ASP[pravitel_1bh][casp] - ret + 12, 12)) == planet_in_house[pravitel_4bh]:
                                                for casp_2 in np.arange(len(ASP[pravitel_4bh])):
                                                    for ret in [ret_planet[pravitel_4bh] + 1]:
                                                        if int(math.fmod(planet_in_house[pravitel_4bh] + ASP[pravitel_4bh][casp_2] - ret + 12, 12)) == planet_in_house[pravitel_1bh]:
                                                            list_khala_joga.append(([pravitel_1bh, pravitel_4bh]))


                        for arr_1bh in np.arange(len(graha_uprav_house[pravitel_1bh])):
                            if graha_uprav_house[pravitel_1bh][arr_1bh] == 8:
                                # является ли управитель 1й бхавы сильным
                                if RELAT_GRAH_T[np.fmod(int(graha_in_znak[pravitel_1bh] * 9) + pravitel_1bh, 108)] in [ekzaltt, neitralt, selft, drugt]:

                                    # является ли положение правителя 4й бхавы и юпитера во взаимных кендрах
                                    if (planet_in_house[pravitel_4bh] in [0, 3, 6, 9]) and (
                                            planet_in_house[pravitel_1bh] in [0, 3, 6, 9]):
                                        list_khala_joga.append([pravitel_4bh, pravitel_1bh])
                                        # условие соединения двух рассматриваемых планет
                                        if planet_in_house[pravitel_4bh] == planet_in_house[pravitel_1bh]:
                                            for planet in PLANETS_RANGE:
                                                for arr_pl in np.arange(len(graha_uprav_house[planet])):
                                                    if planet_in_house[pravitel_1bh] == graha_uprav_house[planet][arr_pl]:
                                                        list_khala_joga.extend(([pravitel_1bh, planet], [pravitel_4bh, planet]))

    """
        чамара йога
    """
    # правитель лагны в кендре и сильный
    for pravitel_1bh in PLANETS_RANGE:
        for arr_1bh in np.arange(len(graha_uprav_house[pravitel_1bh])):
            if (graha_uprav_house[pravitel_1bh][arr_1bh] == 0) and (RELAT_GRAH_T[np.fmod(int(
                    graha_in_znak[pravitel_1bh] * 9) + pravitel_1bh, 108)] in [ekzaltt, neitralt, selft, drugt]):

                for casp_1 in range(len(ASP_2[JUPITER_PLANET_NUMBER])):
                    if ASP_2[JUPITER_PLANET_NUMBER][casp_1] > 0:
                        for ret_1 in range(ret_planet[JUPITER_PLANET_NUMBER] + 1):
                            """
                                проверка на наличие аспета планеты pl_1 на 2й дом, куда идет аспект с учетом признака ретроградности
                            """
                            if (int(math.fmod(planet_in_house[JUPITER_PLANET_NUMBER] +
                                              ASP_2[JUPITER_PLANET_NUMBER][casp_1] - ret_1, 12)) == planet_in_house[pravitel_1bh]) or (
                                    planet_in_house[JUPITER_PLANET_NUMBER] == planet_in_house[pravitel_1bh]):
                                list_chamara_joga.append([pravitel_1bh, JUPITER_PLANET_NUMBER])

    for graha_in_1bh in PLANETS_RANGE:
        for graha_in_9bh in PLANETS_RANGE:
            if planet_nature_and_rising_sign[graha_in_1bh] and planet_nature_and_rising_sign[graha_in_9bh]:
                if planet_in_house[graha_in_1bh] != planet_in_house[graha_in_9bh]:
                    if (planet_in_house[graha_in_1bh] == 0) and (planet_in_house[graha_in_9bh] == 8):
                        list_chamara_joga.append([graha_in_1bh, graha_in_9bh])
                    if (planet_in_house[graha_in_1bh] == 9) and (planet_in_house[graha_in_9bh] == 6):
                        list_chamara_joga.append([graha_in_1bh, graha_in_9bh])

    for planet in PLANETS_RANGE:
        if planet_nature_and_rising_sign[planet] > 0:
            for casp_1 in range(len(ASP_2[planet])):
                if ASP_2[planet][casp_1] > 0:
                    for ret_1 in range(ret_planet[planet] + 1):
                        """
                            проверка на наличие аспета планеты pl_1 на 2й дом, куда идет аспект с учетом признака ретроградности
                        """
                        if (int(math.fmod(planet_in_house[planet] +
                                          ASP_2[planet][casp_1] - ret_1, 12)) == 0) or (
                                planet_in_house[planet] == 0):
                            for upr_1bh in PLANETS_RANGE:
                                for arr_upr_1bh in np.arange(len(graha_uprav_house[upr_1bh])):
                                    if graha_uprav_house[upr_1bh][arr_upr_1bh] == 0:
                                        if (graha_uprav_house[upr_1bh] in [0, 3, 4, 6, 8, 9]) and (
                                                RELAT_GRAH_T[int(graha_in_znak[upr_1bh] * 9) + upr_1bh] in [ekzaltt, neitralt, selft, drugt]):
                                            list_chamara_joga.append([planet, upr_1bh])

    if len(list_radja_joga) > 0: list_radja_joga = np.unique(list(map(lambda x: np.sort(list_radja_joga[x]), np.arange(len(list_radja_joga)))), axis=0)
    if len(list_jewelry_joga) > 0: list_jewelry_joga = np.unique(list(map(lambda x: np.sort(list_jewelry_joga[x]), np.arange(len(list_jewelry_joga)))), axis=0)
    if len(list_laksmi_joga) > 0: list_laksmi_joga = np.unique(list(map(lambda x: np.sort(list_laksmi_joga[x]), np.arange(len(list_laksmi_joga)))), axis=0)
    if len(list_parvata_joga) > 0: list_parvata_joga = np.unique(list(map(lambda x: np.sort(list_parvata_joga[x]), np.arange(len(list_parvata_joga)))), axis=0)
    if len(list_gadja_keshari_joga) > 0: list_gadja_keshari_joga = np.unique(list(map(lambda x: np.sort(list_gadja_keshari_joga[x]), np.arange(len(list_gadja_keshari_joga)))), axis=0)
    if len(list_amala_joga) > 0: list_amala_joga = np.unique(list(map(lambda x: np.sort(list_amala_joga[x]), np.arange(len(list_amala_joga)))), axis=0)
    if len(list_khala_joga) > 0: list_khala_joga = np.unique(list(map(lambda x: np.sort(list_khala_joga[x]), np.arange(len(list_khala_joga)))), axis=0)
    if len(list_chamara_joga) > 0: list_chamara_joga = np.unique(list(map(lambda x: np.sort(list_chamara_joga[x]), np.arange(len(list_chamara_joga)))), axis=0)

    # print("planet_nature_and_rising_sign", planet_nature_and_rising_sign)
    # print("graha_uprav_house", graha_uprav_house)
    # print("relate_jogakaraka", relate_jogakaraka)
    # print("planet_in_house", planet_in_house)
    # print("list_radja_joga", list_radja_joga)
    # print("list_jewelry_joga", list_jewelry_joga)
    # print("list_laksmi_joga", list_laksmi_joga)
    # print("list_parvata_joga", list_parvata_joga)
    # print("list_good_planets_joga", list_good_planets_joga)
    # print("list_gadja_keshari_joga", list_gadja_keshari_joga)
    # print("list_amala_joga", list_amala_joga)
    # print("list_khala_joga", list_khala_joga)
    # print("list_chamara_joga", list_chamara_joga)
    # print("--------------------------------")

    list_joga = [list_jewelry_joga, list_laksmi_joga, list_radja_joga, list_parvata_joga, list_gadja_keshari_joga, list_amala_joga, list_khala_joga, list_chamara_joga]

    return Choosen(relate_jogakaraka, list_good_planets_joga, list_joga)
