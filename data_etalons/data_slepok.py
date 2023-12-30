from data_etalons.diff_oil import etalon_

slepoks = ['Ju.inznak', 'Ma.Ju.diff_inznak', 'Ma.Ke.diff_inznak', 'Me.inznak', 'Sa.innavamsha', 'Sa.inznak', 'Su.Ju.diff_inznak', 'Su.Ke.diff_inznak']
slepok_breaks = ['Mo.phase', 'Mo.speed'] #, 'Me.Ve.diff_inznak', 'Su.Me.diff_inznak', 'Su.Ve.diff_inznak', 'Ma.Me.diff_inznak', 'Ju.Sa.hard.diff_inznak', 'Ma.Ve.diff_inznak', 'Ju.Ra.hard.diff_inznak', 'Ju.Ke.hard.diff_inznak', 'Su.Ma.diff_inznak', 'Su.speed', 'Me.Ju.diff_inznak', 'Ju.Ve.diff_inznak', 'Me.Ra.diff_inznak', 'Me.Ke.diff_inznak']


result = {}

for slepok in slepoks:

    if slepok in etalon_.keys():
        result.update({slepok: etalon_[slepok]})
