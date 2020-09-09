from netCDF4 import Dataset
from datetime import datetime
import numpy as np, pandas as pd, math as m
from cutCoords import cutCoords

def wrfforecast(startDate, endDate, path, prefix, sufix, latbox, lonbox, uvar, vvar, latvar, lonvar, path2save, timevar):
    dayofyr = startDate.timetuple().tm_yday
    daysd = startDate.day
    monthsd = startDate.month
    yearsd = startDate.year
    dayfd = endDate.day
    monthfd = endDate.month
    yearfd = endDate.year
    dayofyrf = endDate.timetuple().tm_yday
    yeardt = yearfd - yearsd
    fileName = path + prefix + str(yearsd) + '-' + '{0:02d}'.format(monthsd) + '-' + '{0:02d}'.format(daysd) + sufix
    coords = cutCoords(fileName, latvar, lonvar, latbox, lonbox, 'depth', 'depthvar', 'wrf')
    latValues = coords[0]
    lonValues = coords[1]
    latminindx = coords[2]
    latmaxindx = coords[3]
    lonminindx = coords[4]
    lonmaxindx = coords[5]
    data = Dataset(fileName, 'r', format='NETCDF4_CLASSIC')
    var = data.variables
    u = var.get(uvar)
    v = var.get(vvar)
    ncTime = var.get(timevar)
    uData = np.zeros((len(ncTime), len(latValues), len(lonValues)))
    vData = np.zeros((len(ncTime), len(latValues), len(lonValues)))
    for hour in range(0, len(ncTime)):
        uData[hour, :, :] = u[hour, latminindx:latmaxindx + 1, lonminindx:lonmaxindx + 1]
        vData[hour, :, :] = v[hour, latminindx:latmaxindx + 1, lonminindx:lonmaxindx + 1]

    fileName = 'WRF_forecast_' + str(yearsd) + '{0:02d}'.format(monthsd) + '{0:02d}'.format(daysd) + '.nc'
    dataset = Dataset((path2save + fileName), 'w', format='NETCDF3_CLASSIC')
    fillValue = 1.267651e+30
    dataset.createDimension('time', None)
    dataset.createDimension('lat', len(latValues))
    dataset.createDimension('lon', len(lonValues))
    time = dataset.createVariable('time', np.float64, ('time', ))
    lon = dataset.createVariable('lon', np.float32, ('lon', ))
    lat = dataset.createVariable('lat', np.float32, ('lat', ))
    u = dataset.createVariable('air_u', (np.float32), ('time', 'lat', 'lon'), fill_value=fillValue)
    v = dataset.createVariable('air_v', (np.float32), ('time', 'lat', 'lon'), fill_value=fillValue)
    dataset.grid_type = 'REGULAR'
    lat.long_name = 'Latitude'
    lat.units = 'degrees_east'
    lat.standard_name = 'latitude'
    lon.long_name = 'Longitude'
    lon.units = 'degrees_north'
    lon.standard_name = 'longitude'
    time.long_name = 'Time'
    time.units = 'hours since ' + str(yearsd) + '-' + str(monthsd) + '-' + str(daysd) + ' 00:00:00'
    time.standard_name = 'time'
    u.long_name = 'Eastward Air Velocity'
    u.standard_name = 'eastward_air_velocity'
    u.units = 'm/s'
    v.long_name = 'Northward Air Velocity'
    v.standard_name = 'northward_air_velocity'
    v.units = 'm/s'
    timenetcdf = [x for x in range(0, len(ncTime))]
    lat[:] = latValues[:]
    lon[:] = lonValues[:]
    time[:] = timenetcdf[:]
    u[:] = uData[:]
    v[:] = vData[:]
    dataset.sync()
    dataset.close()

