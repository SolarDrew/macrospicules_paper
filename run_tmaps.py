from matplotlib import use
use('agg')
import sys
from os.path import join, expanduser
CThome = expanduser(join('~', 'CoronaTemps'))
sys.path.append(CThome)
from temperature import TemperatureMap as TMap
from matplotlib import pyplot as plt
from sunpy.time import parse_time as parse

dates = ['2014-12-15 12:00']

for date in dates:
    thismap = TMap(date, data_dir=join(CThome, 'data'), maps_dir=CThome, verbose=True)
    thismap.save()
    fig = plt.figure(figsize=(32, 24))
    thismap.plot()
    plt.colorbar()
    plt.savefig('t_{:%Y-%m-%d_%H-%M-%S}'.format(parse(thismap.date)))
    plt.close()
