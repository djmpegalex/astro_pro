import math
from dictsData import dictOfVargas
import calculateBindy

from constants import *

# сва-вишва для шодаша-варги
D01_BALA_16 = 3.5
D02_BALA_16 = 1.0
D03_BALA_16 = 1.0
D09_BALA_16 = 3.0
D12_BALA_16 = 0.5
D05_BALA_16 = 1.0
D07_BALA_16 = 0.5
D10_BALA_16 = 0.5
D16_BALA_16 = 2.0
D60_BALA_16 = 4.0
D20_BALA_16 = 0.5
D24_BALA_16 = 0.5
D27_BALA_16 = 0.5
D04_BALA_16 = 0.5
D40_BALA_16 = 0.5
D45_BALA_16 = 0.5

# сва-вишва для сапта-варги
D01_BALA_7 = 5.0
D02_BALA_7 = 2.0
D03_BALA_7 = 3.0
D09_BALA_7 = 2.5
D12_BALA_7 = 4.5
D05_BALA_7 = 2.0
D07_BALA_7 = 1.0

# сва-вишва для шад-варги
D01_BALA_6 = 6.0
D02_BALA_6 = 2.0
D03_BALA_6 = 4.0
D09_BALA_6 = 5.0
D12_BALA_6 = 2.0
D05_BALA_6 = 1.0

SHAD_BALA = 20

# данные об времени восхода и захода солнца
vargas_dict = dictOfVargas.get_location_in_varga_data()
# даты
location_varga_znaks = dictOfVargas.get_locate_of_planets(vargas_dict)


def get_whole_drekkana(planet_in_degrees_from_znak, planet_in_znaks):
    whole_drekkana = []

    for planet in PLANETS_RANGE:
        d3_get_local = [vargas_dict.get(planet_in_znaks[planet]).d03_000000_036000,
                        vargas_dict.get(planet_in_znaks[planet]).d03_036000_072000,
                        vargas_dict.get(planet_in_znaks[planet]).d03_072000_108000]
        whole_drekkana.append(d3_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 36000)] +
                              (math.trunc(planet_in_degrees_from_znak[planet] / 36000) * 12))

    return whole_drekkana


def get_calculate_bala_of_planets(planet_in_degrees_from_znak, planet_in_znaks, name_varga,
                                  lagna_in_seconds_znak, polojenie_lagna_rashi):
    bala_planet = []

    if name_varga in [ALL_VARGAS, ALL_VARGAS_PARTS]:
        planet_in_degrees_from_znak.append(lagna_in_seconds_znak)
        planet_in_znaks.append(polojenie_lagna_rashi)

    d1_varga = planet_in_znaks
    d2_varga, d3_varga, d9_varga, d12_varga, d5_varga, d7_varga, d10_varga, d16_varga, d60_varga, d20_varga, \
    d24_varga, d27_varga, d4_varga, d40_varga, d45_varga, d6_varga, \
    d8_varga, d11_varga = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    d2_varga_p, d3_varga_p, d9_varga_p, d12_varga_p, d5_varga_p, d7_varga_p, d10_varga_p, d16_varga_p, \
    d60_varga_p, d20_varga_p, d24_varga_p, d27_varga_p, d4_varga_p, d40_varga_p, d45_varga_p, d6_varga_p, \
    d8_varga_p, d11_varga_p = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    vimhopaka_bala_planets = []
    for planet in range(NUMBER_OF_PLANETS + int(polojenie_lagna_rashi > (-1))):
        # построение D-2 варги: Хора
        if planet_in_znaks[planet] > 11: planet_in_znaks[planet] = int(np.modf(np.modf(planet_in_znaks[planet]/12)[0]*12)[1])
        d2_get_local = [vargas_dict.get(planet_in_znaks[planet]).d02_000000_054000,
                        vargas_dict.get(planet_in_znaks[planet]).d02_054000_108000]

        d2_varga.append(d2_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 54000)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 54000)[0]
        d2_varga_p.append(d2_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 54000)]+partDegrees)

        # построение D-3 варги: Дрекхана
        d3_get_local = [vargas_dict.get(planet_in_znaks[planet]).d03_000000_036000,
                        vargas_dict.get(planet_in_znaks[planet]).d03_036000_072000,
                        vargas_dict.get(planet_in_znaks[planet]).d03_072000_108000]
        d3_varga.append(d3_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 36000)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 36000)[0]
        d3_varga_p.append(d3_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 36000)]+partDegrees)

        # построение D-9 варги: Навамша
        d9_get_local = [vargas_dict.get(planet_in_znaks[planet]).d09_000000_012000,
                        vargas_dict.get(planet_in_znaks[planet]).d09_012000_024000,
                        vargas_dict.get(planet_in_znaks[planet]).d09_024000_036000,
                        vargas_dict.get(planet_in_znaks[planet]).d09_036000_048000,
                        vargas_dict.get(planet_in_znaks[planet]).d09_048000_060000,
                        vargas_dict.get(planet_in_znaks[planet]).d09_060000_072000,
                        vargas_dict.get(planet_in_znaks[planet]).d09_072000_084000,
                        vargas_dict.get(planet_in_znaks[planet]).d09_084000_096000,
                        vargas_dict.get(planet_in_znaks[planet]).d09_096000_108000]
        d9_varga.append(d9_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 12000)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 12000)[0]
        d9_varga_p.append(d9_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 12000)]+partDegrees)

        # построение D-12 варги: Двадашамша
        d12_get_local = [vargas_dict.get(planet_in_znaks[planet]).d12_000000_009000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_009000_018000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_018000_027000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_027000_036000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_036000_045000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_045000_054000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_054000_063000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_063000_072000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_072000_081000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_081000_090000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_090000_099000,
                         vargas_dict.get(planet_in_znaks[planet]).d12_099000_108000]
        d12_varga.append(d12_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 9000)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 9000)[0]
        d12_varga_p.append(d12_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 9000)]+partDegrees)

        # построение D-5 варги: Тримшамша
        #   чтобы построить данную варгу, нужно проверить четность/нечетность знака
        if (math.trunc(planet_in_znaks[planet] / 2)) * 2 == planet_in_znaks[planet]:
            #       если знак четный
            d5_get_local = [vargas_dict.get(planet_in_znaks[planet]).d5c_000000_018000,
                            vargas_dict.get(planet_in_znaks[planet]).d5c_018000_043200,
                            vargas_dict.get(planet_in_znaks[planet]).d5c_043200_072000,
                            vargas_dict.get(planet_in_znaks[planet]).d5c_072000_090000,
                            vargas_dict.get(planet_in_znaks[planet]).d5c_090000_108000]
            if planet_in_degrees_from_znak[planet] < 18000:
                d5_varga.append(d5_get_local[0])
                partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 18000)[0]
                d5_varga_p.append(d5_get_local[0] + partDegrees)

            elif 18000 <= planet_in_degrees_from_znak[planet] < 43200:
                d5_varga.append(d5_get_local[1])
                partDegrees = np.modf((planet_in_degrees_from_znak[planet] - 18000)/25200)[0]
                d5_varga_p.append(d5_get_local[1] + partDegrees)

            elif 43200 <= planet_in_degrees_from_znak[planet] < 72000:
                d5_varga.append(d5_get_local[2])
                partDegrees = np.modf((planet_in_degrees_from_znak[planet] - 43200)/28800)[0]
                d5_varga_p.append(d5_get_local[2] + partDegrees)

            elif 72000 <= planet_in_degrees_from_znak[planet] < 90000:
                d5_varga.append(d5_get_local[3])
                partDegrees = np.modf((planet_in_degrees_from_znak[planet] - 72000)/18000)[0]
                d5_varga_p.append(d5_get_local[3] + partDegrees)

            else:
                d5_varga.append(d5_get_local[4])
                partDegrees = np.modf((planet_in_degrees_from_znak[planet] - 90000)/18000)[0]
                d5_varga_p.append(d5_get_local[4] + partDegrees)

        else:
            #       если знак нечетный
            d5_get_local = [vargas_dict.get(planet_in_znaks[planet]).d5n_000000_018000,
                            vargas_dict.get(planet_in_znaks[planet]).d5n_018000_036000,
                            vargas_dict.get(planet_in_znaks[planet]).d5n_036000_064800,
                            vargas_dict.get(planet_in_znaks[planet]).d5n_064800_090000,
                            vargas_dict.get(planet_in_znaks[planet]).d5n_090000_108000]
            if planet_in_degrees_from_znak[planet] < 18000:
                d5_varga.append(d5_get_local[0])
                partDegrees = np.modf(planet_in_degrees_from_znak[planet]/18000)[0]
                d5_varga_p.append(d5_get_local[0] + partDegrees)

            elif 18000 <= planet_in_degrees_from_znak[planet] < 36000:
                d5_varga.append(d5_get_local[1])
                partDegrees = np.modf((planet_in_degrees_from_znak[planet] - 18000)/18000)[0]
                d5_varga_p.append(d5_get_local[1] + partDegrees)

            elif 36000 <= planet_in_degrees_from_znak[planet] < 64800:
                d5_varga.append(d5_get_local[2])
                partDegrees = np.modf((planet_in_degrees_from_znak[planet] - 36000)/28800)[0]
                d5_varga_p.append(d5_get_local[2] + partDegrees)

            elif 64800 <= planet_in_degrees_from_znak[planet] < 90000:
                d5_varga.append(d5_get_local[3])
                partDegrees = np.modf((planet_in_degrees_from_znak[planet] - 64800)/25200)[0]
                d5_varga_p.append(d5_get_local[3] + partDegrees)

            else:
                d5_varga.append(d5_get_local[4])
                partDegrees = np.modf((planet_in_degrees_from_znak[planet] - 90000)/18000)[0]
                d5_varga_p.append(d5_get_local[4] + partDegrees)

        # построение D-7 варги: Саптамша
        d7_get_local = [vargas_dict.get(planet_in_znaks[planet]).d07_000000_015428,
                        vargas_dict.get(planet_in_znaks[planet]).d07_015428_030857,
                        vargas_dict.get(planet_in_znaks[planet]).d07_030857_046285,
                        vargas_dict.get(planet_in_znaks[planet]).d07_046285_061714,
                        vargas_dict.get(planet_in_znaks[planet]).d07_061714_077142,
                        vargas_dict.get(planet_in_znaks[planet]).d07_077142_092571,
                        vargas_dict.get(planet_in_znaks[planet]).d07_092571_108000]
        d7_varga.append(d7_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 15428.572)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 15428.572)[0]
        d7_varga_p.append(d7_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 15428.572)]+partDegrees)

        # построение D-10 варги: Дашамша
        d10_get_local = [vargas_dict.get(planet_in_znaks[planet]).d10_000000_010800,
                         vargas_dict.get(planet_in_znaks[planet]).d10_010800_021600,
                         vargas_dict.get(planet_in_znaks[planet]).d10_021600_032400,
                         vargas_dict.get(planet_in_znaks[planet]).d10_032400_043200,
                         vargas_dict.get(planet_in_znaks[planet]).d10_043200_054000,
                         vargas_dict.get(planet_in_znaks[planet]).d10_054000_064800,
                         vargas_dict.get(planet_in_znaks[planet]).d10_064800_075600,
                         vargas_dict.get(planet_in_znaks[planet]).d10_075600_086400,
                         vargas_dict.get(planet_in_znaks[planet]).d10_086400_097200,
                         vargas_dict.get(planet_in_znaks[planet]).d10_097200_108000]
        d10_varga.append(d10_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 10800)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 10800)[0]
        d10_varga_p.append(d10_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 10800)]+partDegrees)

        # построение D-16 варги: Каламша (Шодашамша)
        d16_get_local = [vargas_dict.get(planet_in_znaks[planet]).d16_000000_006750,
                         vargas_dict.get(planet_in_znaks[planet]).d16_006750_013500,
                         vargas_dict.get(planet_in_znaks[planet]).d16_013500_020250,
                         vargas_dict.get(planet_in_znaks[planet]).d16_020250_027000,
                         vargas_dict.get(planet_in_znaks[planet]).d16_027000_033750,
                         vargas_dict.get(planet_in_znaks[planet]).d16_033750_040500,
                         vargas_dict.get(planet_in_znaks[planet]).d16_040500_047250,
                         vargas_dict.get(planet_in_znaks[planet]).d16_047250_054000,
                         vargas_dict.get(planet_in_znaks[planet]).d16_054000_060750,
                         vargas_dict.get(planet_in_znaks[planet]).d16_060750_067500,
                         vargas_dict.get(planet_in_znaks[planet]).d16_067500_074250,
                         vargas_dict.get(planet_in_znaks[planet]).d16_074250_081000,
                         vargas_dict.get(planet_in_znaks[planet]).d16_081000_087750,
                         vargas_dict.get(planet_in_znaks[planet]).d16_087750_094500,
                         vargas_dict.get(planet_in_znaks[planet]).d16_094500_101250,
                         vargas_dict.get(planet_in_znaks[planet]).d16_101250_108000]
        d16_varga.append(d16_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 6750)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 6750)[0]
        d16_varga_p.append(d16_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 6750)]+partDegrees)

        # построение D-60 варги: Шаштйамша
        d60_get_local = [vargas_dict.get(planet_in_znaks[planet]).d60_000000_001800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_001800_003600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_003600_005400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_005400_007200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_007200_009000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_009000_010800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_010800_012600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_012600_014400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_014400_016200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_016200_018000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_018000_019800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_019800_021600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_021600_023400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_023400_025200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_025200_027000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_027000_028800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_028800_030600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_030600_032400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_032400_034200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_034200_036000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_036000_037800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_037800_039600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_039600_041400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_041400_043200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_043200_045000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_045000_046800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_046800_048600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_048600_050400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_050400_052200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_052200_054000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_054000_055800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_055800_057600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_057600_059400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_059400_061200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_061200_063000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_063000_064800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_064800_066600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_066600_068400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_068400_070200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_070200_072000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_072000_073800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_073800_075600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_075600_077400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_077400_079200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_079200_081000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_081000_082800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_082800_084600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_084600_086400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_086400_088200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_088200_090000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_090000_091800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_091800_093600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_093600_095400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_095400_097200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_097200_099000,
                         vargas_dict.get(planet_in_znaks[planet]).d60_099000_100800,
                         vargas_dict.get(planet_in_znaks[planet]).d60_100800_102600,
                         vargas_dict.get(planet_in_znaks[planet]).d60_102600_104400,
                         vargas_dict.get(planet_in_znaks[planet]).d60_104400_106200,
                         vargas_dict.get(planet_in_znaks[planet]).d60_106200_108000]
        d60_varga.append(d60_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 1800)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 1800)[0]
        d60_varga_p.append(d60_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 1800)]+partDegrees)

        # построение D-20 варги: Вимшамша
        d20_get_local = [vargas_dict.get(planet_in_znaks[planet]).d20_000000_005400,
                         vargas_dict.get(planet_in_znaks[planet]).d20_005400_010800,
                         vargas_dict.get(planet_in_znaks[planet]).d20_010800_016200,
                         vargas_dict.get(planet_in_znaks[planet]).d20_016200_021600,
                         vargas_dict.get(planet_in_znaks[planet]).d20_021600_027000,
                         vargas_dict.get(planet_in_znaks[planet]).d20_027000_032400,
                         vargas_dict.get(planet_in_znaks[planet]).d20_032400_037800,
                         vargas_dict.get(planet_in_znaks[planet]).d20_037800_043200,
                         vargas_dict.get(planet_in_znaks[planet]).d20_043200_048600,
                         vargas_dict.get(planet_in_znaks[planet]).d20_048600_054000,
                         vargas_dict.get(planet_in_znaks[planet]).d20_054000_059400,
                         vargas_dict.get(planet_in_znaks[planet]).d20_059400_064800,
                         vargas_dict.get(planet_in_znaks[planet]).d20_064800_070200,
                         vargas_dict.get(planet_in_znaks[planet]).d20_070200_075600,
                         vargas_dict.get(planet_in_znaks[planet]).d20_075600_081000,
                         vargas_dict.get(planet_in_znaks[planet]).d20_081000_086400,
                         vargas_dict.get(planet_in_znaks[planet]).d20_086400_091800,
                         vargas_dict.get(planet_in_znaks[planet]).d20_091800_097200,
                         vargas_dict.get(planet_in_znaks[planet]).d20_097200_102600,
                         vargas_dict.get(planet_in_znaks[planet]).d20_102600_108000]
        d20_varga.append(d20_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 5400)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 5400)[0]
        d20_varga_p.append(d20_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 5400)]+partDegrees)

        # построение D-24 варги: Чатурвимшамша
        d24_get_local = [vargas_dict.get(planet_in_znaks[planet]).d24_000000_004500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_004500_009000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_009000_013500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_013500_018000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_018000_022500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_022500_027000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_027000_031500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_031500_036000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_036000_040500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_040500_045000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_045000_049500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_049500_054000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_054000_058500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_058500_063000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_063000_067500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_067500_072000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_072000_076500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_076500_081000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_081000_085500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_085500_090000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_090000_094500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_094500_099000,
                         vargas_dict.get(planet_in_znaks[planet]).d24_099000_103500,
                         vargas_dict.get(planet_in_znaks[planet]).d24_103500_108000]
        d24_varga.append(d24_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 9000)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 9000)[0]
        d24_varga_p.append(d24_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 9000)] + partDegrees)

        # построение D-27 варги: Бхашма (Саптавишамша)
        d27_get_local = [vargas_dict.get(planet_in_znaks[planet]).d27_000000_004000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_004000_008000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_008000_012000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_012000_016000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_016000_020000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_020000_024000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_024000_028000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_028000_032000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_032000_036000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_036000_040000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_040000_044000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_044000_048000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_048000_052000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_052000_056000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_056000_060000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_060000_064000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_064000_068000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_068000_072000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_072000_076000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_076000_080000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_080000_084000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_084000_088000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_088000_092000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_092000_096000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_096000_100000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_100000_104000,
                         vargas_dict.get(planet_in_znaks[planet]).d27_104000_108000]
        d27_varga.append(d27_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 4000)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 4000)[0]
        d27_varga_p.append(d27_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 4000)] + partDegrees)

        # построение D-4 варги: Турйамша (Чатуртхамша)
        d4_get_local = [vargas_dict.get(planet_in_znaks[planet]).d04_000000_027000,
                        vargas_dict.get(planet_in_znaks[planet]).d04_027000_054000,
                        vargas_dict.get(planet_in_znaks[planet]).d04_054000_081000,
                        vargas_dict.get(planet_in_znaks[planet]).d04_081000_108000]
        d4_varga.append(d4_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 27000)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 27000)[0]
        d4_varga_p.append(d4_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 27000)] + partDegrees)

        # построение D-40 варги: Кхаведамша
        d40_get_local = [vargas_dict.get(planet_in_znaks[planet]).d40_000000_002700,
                         vargas_dict.get(planet_in_znaks[planet]).d40_002700_005400,
                         vargas_dict.get(planet_in_znaks[planet]).d40_005400_008100,
                         vargas_dict.get(planet_in_znaks[planet]).d40_008100_010800,
                         vargas_dict.get(planet_in_znaks[planet]).d40_010800_013500,
                         vargas_dict.get(planet_in_znaks[planet]).d40_013500_016200,
                         vargas_dict.get(planet_in_znaks[planet]).d40_016200_018900,
                         vargas_dict.get(planet_in_znaks[planet]).d40_018900_021600,
                         vargas_dict.get(planet_in_znaks[planet]).d40_021600_024300,
                         vargas_dict.get(planet_in_znaks[planet]).d40_024300_027000,
                         vargas_dict.get(planet_in_znaks[planet]).d40_027000_029700,
                         vargas_dict.get(planet_in_znaks[planet]).d40_029700_032400,
                         vargas_dict.get(planet_in_znaks[planet]).d40_032400_035100,
                         vargas_dict.get(planet_in_znaks[planet]).d40_035100_037800,
                         vargas_dict.get(planet_in_znaks[planet]).d40_037800_040500,
                         vargas_dict.get(planet_in_znaks[planet]).d40_040500_043200,
                         vargas_dict.get(planet_in_znaks[planet]).d40_043200_045900,
                         vargas_dict.get(planet_in_znaks[planet]).d40_045900_048600,
                         vargas_dict.get(planet_in_znaks[planet]).d40_048600_051300,
                         vargas_dict.get(planet_in_znaks[planet]).d40_051300_054000,
                         vargas_dict.get(planet_in_znaks[planet]).d40_054000_056700,
                         vargas_dict.get(planet_in_znaks[planet]).d40_056700_059400,
                         vargas_dict.get(planet_in_znaks[planet]).d40_059400_062100,
                         vargas_dict.get(planet_in_znaks[planet]).d40_062100_064800,
                         vargas_dict.get(planet_in_znaks[planet]).d40_064800_067500,
                         vargas_dict.get(planet_in_znaks[planet]).d40_067500_070200,
                         vargas_dict.get(planet_in_znaks[planet]).d40_070200_072900,
                         vargas_dict.get(planet_in_znaks[planet]).d40_072900_075600,
                         vargas_dict.get(planet_in_znaks[planet]).d40_075600_078300,
                         vargas_dict.get(planet_in_znaks[planet]).d40_078300_081000,
                         vargas_dict.get(planet_in_znaks[planet]).d40_081000_083700,
                         vargas_dict.get(planet_in_znaks[planet]).d40_083700_086400,
                         vargas_dict.get(planet_in_znaks[planet]).d40_086400_089100,
                         vargas_dict.get(planet_in_znaks[planet]).d40_089100_091800,
                         vargas_dict.get(planet_in_znaks[planet]).d40_091800_094500,
                         vargas_dict.get(planet_in_znaks[planet]).d40_094500_097200,
                         vargas_dict.get(planet_in_znaks[planet]).d40_097200_099900,
                         vargas_dict.get(planet_in_znaks[planet]).d40_099900_102600,
                         vargas_dict.get(planet_in_znaks[planet]).d40_102600_105300,
                         vargas_dict.get(planet_in_znaks[planet]).d40_105300_108000]
        d40_varga.append(d40_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 2700)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 2700)[0]
        d40_varga_p.append(d40_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 2700)] + partDegrees)

        # построение D-45 варги: Акшаведамша
        d45_get_local = [vargas_dict.get(planet_in_znaks[planet]).d45_000000_002400,
                         vargas_dict.get(planet_in_znaks[planet]).d45_002400_004800,
                         vargas_dict.get(planet_in_znaks[planet]).d45_004800_007200,
                         vargas_dict.get(planet_in_znaks[planet]).d45_007200_009600,
                         vargas_dict.get(planet_in_znaks[planet]).d45_009600_012000,
                         vargas_dict.get(planet_in_znaks[planet]).d45_012000_014400,
                         vargas_dict.get(planet_in_znaks[planet]).d45_014400_016800,
                         vargas_dict.get(planet_in_znaks[planet]).d45_016800_019200,
                         vargas_dict.get(planet_in_znaks[planet]).d45_019200_021600,
                         vargas_dict.get(planet_in_znaks[planet]).d45_021600_024000,
                         vargas_dict.get(planet_in_znaks[planet]).d45_024000_026400,
                         vargas_dict.get(planet_in_znaks[planet]).d45_026400_028800,
                         vargas_dict.get(planet_in_znaks[planet]).d45_028800_031200,
                         vargas_dict.get(planet_in_znaks[planet]).d45_031200_033600,
                         vargas_dict.get(planet_in_znaks[planet]).d45_033600_036000,
                         vargas_dict.get(planet_in_znaks[planet]).d45_036000_038400,
                         vargas_dict.get(planet_in_znaks[planet]).d45_038400_040800,
                         vargas_dict.get(planet_in_znaks[planet]).d45_040800_043200,
                         vargas_dict.get(planet_in_znaks[planet]).d45_043200_045600,
                         vargas_dict.get(planet_in_znaks[planet]).d45_045600_048000,
                         vargas_dict.get(planet_in_znaks[planet]).d45_048000_050400,
                         vargas_dict.get(planet_in_znaks[planet]).d45_050400_052800,
                         vargas_dict.get(planet_in_znaks[planet]).d45_052800_055200,
                         vargas_dict.get(planet_in_znaks[planet]).d45_055200_057600,
                         vargas_dict.get(planet_in_znaks[planet]).d45_057600_060000,
                         vargas_dict.get(planet_in_znaks[planet]).d45_060000_062400,
                         vargas_dict.get(planet_in_znaks[planet]).d45_062400_064800,
                         vargas_dict.get(planet_in_znaks[planet]).d45_064800_067200,
                         vargas_dict.get(planet_in_znaks[planet]).d45_067200_069600,
                         vargas_dict.get(planet_in_znaks[planet]).d45_069600_072000,
                         vargas_dict.get(planet_in_znaks[planet]).d45_072000_074400,
                         vargas_dict.get(planet_in_znaks[planet]).d45_074400_076800,
                         vargas_dict.get(planet_in_znaks[planet]).d45_076800_079200,
                         vargas_dict.get(planet_in_znaks[planet]).d45_079200_081600,
                         vargas_dict.get(planet_in_znaks[planet]).d45_081600_084000,
                         vargas_dict.get(planet_in_znaks[planet]).d45_084000_086400,
                         vargas_dict.get(planet_in_znaks[planet]).d45_086400_088800,
                         vargas_dict.get(planet_in_znaks[planet]).d45_088800_091200,
                         vargas_dict.get(planet_in_znaks[planet]).d45_091200_093600,
                         vargas_dict.get(planet_in_znaks[planet]).d45_093600_096000,
                         vargas_dict.get(planet_in_znaks[planet]).d45_096000_098400,
                         vargas_dict.get(planet_in_znaks[planet]).d45_098400_100800,
                         vargas_dict.get(planet_in_znaks[planet]).d45_100800_103200,
                         vargas_dict.get(planet_in_znaks[planet]).d45_103200_105600,
                         vargas_dict.get(planet_in_znaks[planet]).d45_105600_108000]
        d45_varga.append(d45_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 2400)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 2400)[0]
        d45_varga_p.append(d45_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 2400)] + partDegrees)

        # построение D-6 варги
        d06_get_local = [vargas_dict.get(planet_in_znaks[planet]).D06_000000_018000,
                         vargas_dict.get(planet_in_znaks[planet]).D06_018000_036000,
                         vargas_dict.get(planet_in_znaks[planet]).D06_036000_054000,
                         vargas_dict.get(planet_in_znaks[planet]).D06_054000_072000,
                         vargas_dict.get(planet_in_znaks[planet]).D06_072000_090000,
                         vargas_dict.get(planet_in_znaks[planet]).D06_090000_108000]
        d6_varga.append(d06_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 18000)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 18000)[0]
        d6_varga_p.append(d06_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 18000)] + partDegrees)

        # построение D-8 варги
        d08_get_local = [vargas_dict.get(planet_in_znaks[planet]).D08_000000_013500,
                         vargas_dict.get(planet_in_znaks[planet]).D08_013500_027000,
                         vargas_dict.get(planet_in_znaks[planet]).D08_027000_040500,
                         vargas_dict.get(planet_in_znaks[planet]).D08_040500_054000,
                         vargas_dict.get(planet_in_znaks[planet]).D08_054000_067500,
                         vargas_dict.get(planet_in_znaks[planet]).D08_067500_081000,
                         vargas_dict.get(planet_in_znaks[planet]).D08_081000_094500,
                         vargas_dict.get(planet_in_znaks[planet]).D08_094500_108000]
        d8_varga.append(d08_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 13500)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 13500)[0]
        d8_varga_p.append(d08_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 13500)] + partDegrees)

        # построение D-11 варги
        d11_get_local = [vargas_dict.get(planet_in_znaks[planet]).D11_000000_009818,
                         vargas_dict.get(planet_in_znaks[planet]).D11_009818_019636,
                         vargas_dict.get(planet_in_znaks[planet]).D11_019636_029454,
                         vargas_dict.get(planet_in_znaks[planet]).D11_029454_039272,
                         vargas_dict.get(planet_in_znaks[planet]).D11_039272_049090,
                         vargas_dict.get(planet_in_znaks[planet]).D11_049090_058908,
                         vargas_dict.get(planet_in_znaks[planet]).D11_058908_068726,
                         vargas_dict.get(planet_in_znaks[planet]).D11_068726_078544,
                         vargas_dict.get(planet_in_znaks[planet]).D11_078544_088362,
                         vargas_dict.get(planet_in_znaks[planet]).D11_088362_098180,
                         vargas_dict.get(planet_in_znaks[planet]).D11_098182_108000]
        d11_varga.append(d11_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 9818.182)])

        partDegrees = np.modf(planet_in_degrees_from_znak[planet] / 9818.182)[0]
        d11_varga_p.append(d11_get_local[math.trunc(planet_in_degrees_from_znak[planet] / 9818.182)] + partDegrees)

        # оценка силы планет в варгах
        if name_varga == VARGA_SHODASHA:
            bala_planet = (D01_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                WHO_UPRAVLAET_ZNAKOM[d1_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D02_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d2_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D03_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d3_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D09_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d9_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D12_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d12_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D05_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d5_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D07_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d7_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D10_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d10_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D16_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d16_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D60_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d60_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D20_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d20_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D24_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d24_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D27_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d27_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D04_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d4_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D40_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d40_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D45_BALA_16 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d45_varga[planet]] + (planet * NUMBER_OF_GRAHAS)]) / SHAD_BALA

        if name_varga == VARGA_SAPTA:
            bala_planet = (D01_BALA_7 * RAPPORT_PLANETS_SHODAHA[
                WHO_UPRAVLAET_ZNAKOM[d1_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D02_BALA_7 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d2_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D03_BALA_7 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d3_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D09_BALA_7 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d9_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D12_BALA_7 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d12_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D05_BALA_7 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d5_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D07_BALA_7 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d7_varga[planet]] + (planet * NUMBER_OF_GRAHAS)]) / SHAD_BALA

        if name_varga == VARGA_SHAD:
            bala_planet = (D01_BALA_6 * RAPPORT_PLANETS_SHODAHA[
                WHO_UPRAVLAET_ZNAKOM[d1_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D02_BALA_6 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d2_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D03_BALA_6 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d3_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D09_BALA_6 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d9_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D12_BALA_6 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d12_varga[planet]] + (planet * NUMBER_OF_GRAHAS)] \
                           + D05_BALA_6 * RAPPORT_PLANETS_SHODAHA[
                               WHO_UPRAVLAET_ZNAKOM[d5_varga[planet]] + (planet * NUMBER_OF_GRAHAS)]) / SHAD_BALA

        if name_varga == EVEN_ODD:
            bala_planet = (RAPPORT_EVEN_ODD[d1_varga[planet] + (planet * ZNAKS_IN_ZODIAK)] \
                           + RAPPORT_EVEN_ODD[d9_varga[planet] + (planet * ZNAKS_IN_ZODIAK)]) / 60

        vimhopaka_bala_planets.append(bala_planet)

    """
        оценка благотворности грах
    """
    if name_varga == BINDY_VARGA_CHARITY:
        bindy_d1 = calculateBindy.calculate_bindy_vargas(d1_varga, [0])
        bindy_d2 = calculateBindy.calculate_bindy_vargas(d2_varga, [0])
        bindy_d3 = calculateBindy.calculate_bindy_vargas(d3_varga, [0])
        bindy_d5 = calculateBindy.calculate_bindy_vargas(d5_varga, [0])
        bindy_d9 = calculateBindy.calculate_bindy_vargas(d9_varga, [0])
        bindy_d7 = calculateBindy.calculate_bindy_vargas(d7_varga, [0])
        bindy_d12 = calculateBindy.calculate_bindy_vargas(d12_varga, [0])

        vimhopaka_bala_planets = [0] * 12

        for planets_varga in PLANETS_RANGE:
            vimhopaka_bala_planets[planets_varga] += bindy_d1[d1_varga[planets_varga]]
            vimhopaka_bala_planets[planets_varga] += bindy_d2[d2_varga[planets_varga]]
            vimhopaka_bala_planets[planets_varga] += bindy_d3[d3_varga[planets_varga]]
            vimhopaka_bala_planets[planets_varga] += bindy_d5[d5_varga[planets_varga]]
            vimhopaka_bala_planets[planets_varga] += bindy_d9[d9_varga[planets_varga]]
            vimhopaka_bala_planets[planets_varga] += bindy_d7[d7_varga[planets_varga]]
            vimhopaka_bala_planets[planets_varga] += bindy_d12[d12_varga[planets_varga]]

            vimhopaka_bala_planets[planets_varga] /= 180
            vimhopaka_bala_planets[planets_varga] -= 1

    if name_varga == ALL_VARGAS:
        return [d1_varga, d2_varga, d3_varga, d4_varga, d5_varga, d6_varga, d7_varga, d8_varga, d9_varga, d10_varga,
                d11_varga, d12_varga, d16_varga, d20_varga, d24_varga, d27_varga, d40_varga, d45_varga, d60_varga]

    if name_varga == ALL_VARGAS_PARTS:
        return [d2_varga_p, d3_varga_p, d4_varga_p, d5_varga_p, d6_varga_p, d7_varga_p, d8_varga_p, d9_varga_p, d10_varga_p,
                d11_varga_p, d12_varga_p, d16_varga_p, d20_varga_p, d24_varga_p, d27_varga_p, d40_varga_p, d45_varga_p, d60_varga_p]

    return vimhopaka_bala_planets
