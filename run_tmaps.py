from matplotlib import use
use('agg')
import sys
from os.path import join, expanduser
CThome = expanduser(join('~', 'CoronaTemps'))
sys.path.append(CThome)
from temperature import TemperatureMap as TMap
from matplotlib import pyplot as plt
from sunpy.time import parse_time as parse

dates = ['2014-12-15 12:00', '2014-12-15 12:30', '2014-12-15 14:00']

completed = False
while completed == False:
    try:
        for date in dates:
            thismap = TMap(date, data_dir=join(CThome, 'data'), maps_dir=CThome, verbose=True)
            thismap.save()
            #thismap = thismap.submap([-1200, -200], [-500, 500], units='data')
            fig = plt.figure(figsize=(32, 24))
            thismap.plot()
            plt.colorbar()
            plt.savefig('t_{:%Y-%m-%d_%H-%M-%S}'.format(parse(thismap.date)))
            plt.close()
        completed = True
    except:
        print 'Failed - restarting'
