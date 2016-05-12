import numpy as np
import matplotlib.pyplot as plt

import sunpy.map
from sunpy.image import slit

from astropy.io import fits
import astropy.units as u

from glob import glob

files = glob('/storage2/temperature_maps/data/full_gauss/*.fits')
files.sort()

submaps = []

for afile in files[30:130]:
    with fits.open(afile, memmap=True) as f:
        data = f[0].data[..., 0]
        header = dict(f[0].header)
        m = sunpy.map.Map((data, header))
        m.plotsettings = {'cmap':'coolwarm'}
        submaps.append(m.submap((857.9, 957.94)*u.arcsec,
        (-197.92, -297.92)*u.arcsec))


mc = sunpy.map.Map(submaps, cube=True)

image = slit.slit(mc, [915, 911]*u.arcsec, [-246, -241]*u.arcsec, 1, -1, +1)

slit_arr = image[0][0]

temp_K = 10**slit_arr

