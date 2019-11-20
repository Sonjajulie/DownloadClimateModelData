#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:30:33 2019

@author: sonja totz
"""
import numpy as np
import sys
from datetime import datetime, timedelta
from netCDF4 import Dataset,date2num

class NMME():
    """ class to download data from NMME models"""
    
    def __init__(self,model,url,var):
        """ Initialize model, variable, url for download as well as access
        model variable from url"""
        self.model = model
        self.url = url
        self.var = var
        self.fullURL = f"{self.url}/.{self.var}/dods"
        print(f"Access {self.var} from model {self.model} through {self.fullURL}")
        try:
            self.nc = Dataset(self.fullURL)
        except:
            print(f"Could not open THREDDS url {self.fullURL}")
            sys.exit(-1)
        #  Check for variable in dataset 
        assert self.var in (self.nc.variables),"Variable not found!"
        self._get_dimensions_of_var()

    def _num_to_date(self,nMonths):
        """ Helper-function to convert number to date"""
        self.nMonths = int(nMonths)
        self.baseDate = datetime(1960,1,1,0,0,0)
        self.deltayears  = self.nMonths / 12
        self.deltamonths = self.nMonths % 12
        self.requestedDate = datetime(self.baseDate.year + self.deltayears, self.baseDate.month + self.deltamonths, 1,0,0,0)
        return self.requestedDate
    
    def _date_to_num(self,reqDate):
        """ Helper-function to convert date to number"""
        self.baseDate = datetime(1960,1,1,0,0,0)
        self.nMonths  = (reqDate.year - self.baseDate.year) * 12
        self.nMonths += reqDate.month - self.baseDate.month
        return self.nMonths

    def _days_in_month(self,dateObject):
        """ Helper-function to receive the days in 1 month"""
        next_month = dateObject.replace(day=28) + timedelta(days=4)  
        return (next_month - timedelta(days=next_month.day)).day
    
    def _get_dimensions_of_var(self):
        """ Get dimension of variable in netcdf"""
        # netCDF variable of interest is: 
        #
        # float var(S, M, L, Y, X)
        #   where
        #     S : Forecast Start Time (forecast_reference_time)
        #     M : Ensemble Member (realization)
        #     L : Lead (forecast_period)
        #     Y : Latitude (latitude)
        #     X : Longitude (longitude)
        #
        # though for some datasets, M and L are reversed, so we
        # have to explicitly check
        #
        self.dims = self.nc.variables[self.var].dimensions
        # Unicode = u' '
        self.mdim = self.dims.index(u'M')
        #
        #  nm : number of ensemble members
        #  ny : number of latitudes
        #  nx : number of longitudes
        #
        self.nm, self.ny, self.nx = (self.nc.variables[self.var].shape[self.mdim],
            self.nc.variables[self.var].shape[-2],self.nc.variables[self.var].shape[-1])
        self.lats = self.nc.variables['Y'][:]
        self.lons = self.nc.variables['X'][:]

    def _locate_index_of_anaysis_month(self,analysisDate):
        """
           Locate the netCDF index of the analysis month
           if no  variable is found, return AssertError
        """
        self.m = self._date_to_num(analysisDate)
        self.tm = self.nc['S'][:]
        self.listOfMonths = [i for i in range(self.tm.shape[0]) if self.tm[i] == self.m]
        assert len(self.listOfMonths) == 0," variable for specified month not found!"
        self.im = self.listOfMonths[0]
        
    def _get_forecast(self,forecast_reference_time,forecast_lead,forecast_months):
        #  Locate the netCDF index of the analysis month
        #  and if that month does not exist, raise exception
        self. _locate_index_of_anaysis_month(forecast_reference_time)
        self.days = 0
        
        #initialize variable which should be downloaded with number of
        # realization, lons,lats
        self.v = np.zeros((self.nm,self.ny,self.nx))
        for forecastMonth in self.forecastMonths:
            self.desiredDate = self._num_to_date(self.m + self.forecastMonth)
            self.mdays = self._days_in_month(self.desiredDate)
            print ('debug. desiredDate,mdays=',self.desiredDate,self.mdays)
            self.days += self.mdays
            #  check whether M is in the first or second index
            if self.mdim == 1:
                self.v +=  self.nc.variables[self.var][self.im,:,self.forecastMonth,:,:]
            if self.mdim == 2:
                self.v +=  self.nc.variables[self.var][self.im,self.forecastMonth,:,:,:]
        self.nc.close()
    
        return self.lats, self.lons, self.p/float(len(self.forecastMonths))

    def _save_variable_in_nc(self,output_label):
        """Set parameters such as lat,lon, etc for download func"""
        self.dataset =Dataset(output_label,'w') 
        # Create coordinate variables for 4-dimensions
        self.lat = self.dataset.createDimension('lat', 181)
        self.lon= self.dataset.createDimension('lon', 360) 
        self.time1 = self.dataset.createDimension('time', None) 

        self.times = self.dataset.createVariable('time', 'f8', ('time',)) 
        self.latitudes = self.dataset.createVariable('latitude', 'f4', ('lat',))
        self.longitudes = self.dataset.createVariable('longitude', 'f4', ('lon',)) 
        self.var_to_download = self.dataset.createVariable(self.var, 'f4', 
                                                           ('time','lat','lon',)) 
        self.lons = np.arange(0,360.,1.)
        self.lats = np.arange(-90,91.,1.) 
    
        self.latitudes[:] = self.lats 
        self.longitudes[:] = self.lons
        
        self.var_to_download[:,:,:] = self._get_var(self.analysisDate, 
                            self.forecastMonths)
        self.times.units = 'hours since 0001-01-01 00:00:00'  
        self.times.calendar= 'gregorian' 
        self.dates = []
        self.year=1981
        for n in range(self.var_to_download.shape[0]):
            self.year+=1
            self.dates.append(datetime(self.year, 1, 16)) 
        self.times[:] = date2num(self.dates, units = self.times.units,
                  calendar = self.times.calendar) 
        self.dataset.close()

    def download_data(self,output_label,forecast_reference_time,
                                      forecast_lead,forecast_months):
        """ 
        download data for all realization. Forecast Start Time (forecast_reference_time),
        forecast lead (forecast_lead) and how many months should be forecasted 
        (forecast_months) is specified by user
        """
        try:
            self._get_forecast(forecast_reference_time,forecast_lead,forecast_months)
        except:
            print("error!")
        #self._save_variable_in_nc(self,output_label)


