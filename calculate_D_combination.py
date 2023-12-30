import numpy as np
from constants import *
import bhava_aspects_calculate

def calculate_new_D_combination(natal_map, map_vargas, retrogr_planet):
    """
    params:
    natal_map - даные натальной карты (граха в знаке)
    map_vargas - массив всех положений планет по варгам + лагна (граха в знаке)
    retrogr_planet - данные о ретроградности планет в момент рождения

    Функция вычисляет все возможные комбинации по каждой из дробных карт


    return:
    возвращает комбинации планет в трехмерном массиве
    [ вмещает в себя все варги
     [ в пределах одной карты (учитывается последовательность карт
     D1, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D16, D20, D24, D30, D45, D60) расположены влияние планет на знаки
      [ комбинация влияющих планет

    """

    map_vargas[0] = natal_map
    '''
        вычисление аспектов планет в каждой из дробных карт с учетом их пограничных положений
    '''
    total_D_combination = []

    for map_count, number_map in enumerate(map_vargas):
        all_data = []
        '''
            Сбор данных обо всех аспектах планет, информация нужна чтобы выяснить на какой знак имеются аспекты
        '''
        for planet in PLANETS_RANGE:
            datas = []
            for koef in [-.2333, 0, .2333]:
                number_mapKoef = np.fmod(np.asarray(number_map) + koef + 11, 11)

                graha_in_degrees = list(map(lambda x: x * 108000, number_mapKoef))
                polojenie_lagna_rashi = int(map_vargas[map_count][-1])
                bhava_aspects_rashi = bhava_aspects_calculate.bhava_aspec(graha_in_degrees, polojenie_lagna_rashi,
                                                                          retrogr_planet)

                map_onevarga = list(map(lambda x: int(x), number_mapKoef))
                aspects_varga = list(
                    map(lambda x: np.fmod(int(x / 30) + number_mapKoef[-1], 12), bhava_aspects_rashi))

                aspects_varga_planet = np.asarray(np.concatenate([np.asarray(aspects_varga[planet*7:planet*7+7]), [map_onevarga[planet]]]))
                aspects_varga_planet = list(map(lambda x: int(x), aspects_varga_planet))
                aspects_varga_planet.append(int(number_mapKoef[planet])+100) #расположение планеты в знаке
                datas.append(aspects_varga_planet)
            all_data.append(np.unique(datas).tolist())

        # print('map_count',map_count)
        '''
            Распределение влияние планет на каждый знак карты
        '''
        all_znaks = []
        # print('all_data aspects', all_data)
        for znak in ZODIAK_RANGE:
            znak_data = []
            # print('znak',znak+1,end='')
            for planet, data_planets in enumerate(all_data):

                if (znak + 100) in data_planets: znak_data.append(planet+100)
                if znak in data_planets: znak_data.append(planet)

            znak_data.extend(np.asarray(np.asarray(WHO_UPRAVLAET_ZNAKOM_LI[znak])+1000).tolist())
            znak_data = np.array(znak_data)
            all_znaks.append(znak_data.tolist())
            # print(all_znaks[-1])

        total_D_combination.append(all_znaks)
    # print()
    return total_D_combination




