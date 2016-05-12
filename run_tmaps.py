from matplotlib import use
use('agg')
import sys
from os.path import join, expanduser
paperhome = expanduser(join('~', 'macrospicules_paper'))
CThome = join(paperhome, 'CoronaTemps')
sys.path.append(CThome)
from temperature import TemperatureMap as TMap
from matplotlib import pyplot as plt
import matplotlib.animation as anim
from sunpy.time import parse_time as parse
import datetime as dt
import astropy.units as u
Writer = anim.writers['ffmpeg']
writer = Writer(fps=15, bitrate=1800)

t0 = parse('2012-06-21 07:28')#6:00')
#t0 = parse('2012-06-21 07:50')
dates = [t0]
while t0 < parse('2012-06-21 08:00'):
    t0 += dt.timedelta(seconds=12)
    dates.append(t0)
print dates

map_path = join('/fastdata', 'sm1ajl', 'macrospicules', 'temperature_maps', 'data', '{:%Y-%m-%dT%H_%M_%S}.fits')
data_path = join('/fastdata', 'sm1ajl', 'macrospicules', 'aia*{w}a_{d.year}_{d.month:02d}_{d.day:02d}?{d.hour:02d}_{d.minute:02d}_{d.second:02d}*.fits')
image_dir = join('/fastdata', 'sm1ajl', 'macrospicules', 'temperature_maps', 'images')
x, y = 907.943, -247.942

thismap = TMap(dates[0], data_path=data_path, map_path=map_path.format(dates[0]))
thismap = thismap.submap([x-75, x+75], [y-75, y+75], units='data')
#thismap.save(thismap.map_path.replace('/data', '/crop/data'))

fig, ax = plt.subplots(figsize=(20, 15))
plot = thismap.plot(vmin=6.0, vmax=6.16)
#plt.xlim(*thismap.xrange)
#plt.ylim(*thismap.yrange)
plt.colorbar()

#for date in dates[1:]:
def nextmap(t):
    #thismap = TMap(date, data_path=data_path, map_path=map_path.format(date))#, verbose=True)#, n_params=3)
    thismap = TMap(dates[t], data_path=data_path, map_path=map_path.format(dates[t]))
    #thismap = thismap.save()
    #thismap = thismap.submap([660, 1160], [-500, 0], units='data')
    thismap = thismap.submap([x-75, x+75], [y-75, y+75], units='data')
    #thismap.save(thismap.map_path.replace('/data', '/crop/data'))
    """fig = plt.figure(figsize=(20, 15))
    thismap.plot(vmin=6.0, vmax=6.16)
    #plt.plot(907.943, -247.924, 'o', color='white')
    plt.xlim(*thismap.xrange)
    plt.ylim(*thismap.yrange)
    plt.colorbar()
    if thismap.n_params == 1:
        plt.savefig(join(image_dir, 't_{:%Y-%m-%d_%H-%M-%S}'.format(parse(thismap.date))))
    else:
        plt.savefig(join(image_dir, 't_{:%Y-%m-%d_%H-%M-%S}_full'.format(parse(thismap.date))))
    plt.close()"""
    plot.set_data(thismap.data)
    return plot

animap = anim.FuncAnimation(fig, nextmap, interval=100, repeat=False, frames=len(dates))
animap.save('temperature_map.mp4', writer=writer)
fig.close()
