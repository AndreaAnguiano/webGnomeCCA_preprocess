import os, time, sys
from datetime import datetime, timedelta
import numpy as np

#setting the domain of your models
latbox = [18.2, 31]
lonbox = [-98, -80]

#date and duration of the data
now = datetime(2020,9,8)
start_time = datetime(now.year,now.month, now.day, 12)
duration = timedelta(days=5)

#adding paths
data_path= 'data/'
sys.path.append('scripts/')

from cutCoords import cutCoords
from hycomforecast_ts import hycomforecast_ts
from wrfforecast import wrfforecast

#select the hydrodynamic model 

hyd_model = 'HYCOM'

#hydrodynamic model variables for pre-processing data
prefhy = 'hycom_gomu_901m000_'
sufhy = '_t000.nc'
uvarhy = 'water_u'
vvarhy = 'water_v'
latvarhy = 'lat'
lonvarhy = 'lon'
depthvarhy = 'depth'
# depths of the hydrodynamic model data (currently only superficial data [depth = 0] )
depths = [0]
#timestep for hydrodynamic data
ts = 1 

#select the atmospheric model
atmos_model = 'WRF'

#atmospheric model variables for pre-processing data
prefw = 'wrfout_d01_'
sufw= '_00.nc'
latvarw = 'XLAT'
lonvarw = 'XLONG'
uvarw = 'U10'
vvarw = 'V10'
timevarw = 'Time'

if hyd_model == 'HYCOM':
    hycomforecast_ts(start_time,start_time+duration, data_path, prefhy, sufhy, latbox, lonbox, depths, uvarhy, vvarhy, latvarhy, lonvarhy, depthvarhy, data_path, ts)


if atmos_model == 'WRF':
    wrfforecast(start_time, start_time+duration, data_path, prefw, sufw, latbox, lonbox, uvarw, vvarw, latvarw, lonvarw, data_path, timevarw)
