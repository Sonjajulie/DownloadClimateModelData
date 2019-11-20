#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:30:33 2019

@author: sonja totz
"""
import numpy as np
import sys
from datetime import datetime, timedelta
#from netCDF4 import Dataset,date2num as netCDF4
import netCDF4

class NMME():
    """ class to download data from NMME models"""
    
    def __init__(self,model,url,var):
        """ Initialize model, variable, url for download as well as access
        model variable from url"""
        self.model = model
        self.url = url
        self.var = var
        self.fullURL = f"{self.url}/.{self.var}/dods"

#    def __enter__(self):
#        self.nc = netCDF4.Dataset(self.fullURL)
#        return self
#
#    def __exit__(self, *args):
#        self.nc.close()

    def _num_to_date(self,nMonths):
        """ Helper-function to convert number to date"""
        self.nMonths = int(nMonths)
        self.baseDate = datetime(1960,1,1,0,0,0)
        self.deltayears  = self.nMonths//12
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

    def _locate_index_of_reference_time(self,forecast_reference_time):
        """
           Locate the netCDF index of the analysis month
           if no  variable is found, return AssertError
        """
        self.m = int(self._date_to_num(forecast_reference_time))
        self.tm = (self.nc['S'][:]).astype(int)
        # take only those indeces, where specified date occurs
        self.list_of_months = [i for i in range(self.tm.shape[0]) if self.tm[i] == self.m]
        assert len(self.list_of_months) != 0,f" {len(self.list_of_months)}"
        # assign first index, where spcified date occurs
        self.im = self.list_of_months[0]

    def _get_forecast(self,forecast_reference_time,forecastDates):
        """ 
            get forecast for specified reference time,
             and forecast_months
        """
        print(f"Access {self.var} from model {self.model} through {self.fullURL}")
        with netCDF4.Dataset(self.fullURL) as self.nc:
            #  Check for variable in dataset 
            assert self.var in (self.nc.variables),"Variable not found!"
            self._get_dimensions_of_var()
            
            self.forecastDates_nums = []
            self.sm = self._date_to_num(forecast_reference_time)
    
            for forecast_month in forecastDates:
                self.dm = self._date_to_num(forecast_month)
                #gives 1,2,3  for 1,2,3 months in advance
                self.forecastDates_nums.append(self.dm-self.sm)
    
            #  Locate the netCDF index of the analysis month
            #  and if date does not exist, raise exception
            self._locate_index_of_reference_time(forecast_reference_time)
            self.days = 0
    
            #initialize variable which should be downloaded with number of months,
            # of realization, lons,lats
            self.v = np.zeros((len(forecastDates),self.nm,self.ny,self.nx))
    
            for i in range(len(self.forecastDates_nums)):
                print("desired date: ",self.m + self.forecastDates_nums[i])
                self.desired_date = self._num_to_date(self.m + self.forecastDates_nums[i])
                print(self.desired_date)
                self.mdays = self._days_in_month(self.desired_date)
                print ('debug. desiredDate,mdays=',self.desired_date,self.mdays)
                self.days += self.mdays
                #  check whether M is in the first or second index
                if self.mdim == 1:
                    self.v[i] = self.nc.variables[self.var][self.im,:, self.forecastDates_nums[i],:,:]
                if self.mdim == 2:
                    self.v[i] = self.nc.variables[self.var][self.im, self.forecastDates_nums[i],:,:,:]
            return self.lats, self.lons, self.v

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

    def _save_variable_in_nc(self,output_label):
        """
        Set parameters such as lat,lon, etc for download func and save data
        in netCDF
        """
        with netCDF4.Dataset(output_label,'w') as self.ds:
            # Create coordinate variables for 4-dimensions
            self.lat = self.ds.createDimension('lat', 181)
            self.lon= self.ds.createDimension('lon', 360) 
            self.lon= self.ds.createDimension('m', None) 
            self.time1 = self.ds.createDimension('time', None) 
#    
#            self.times = self.ds.createVariable('time', 'f8', ('time',)) 
#            self.latitudes = self.ds.createVariable('latitude', 'f4', ('lat',))
#            self.longitudes = self.ds.createVariable('longitude', 'f4', ('lon',)) 
#            self.realizations = self.ds.createVariable('realization', 'f4', ('m',)) 
#            self.var_to_download = self.ds.createVariable(self.var, 'f4', 
#                                                               ('time','realization','lat','lon',)) 
#            self.lons = np.arange(0,360.,1.)
#            self.lats = np.arange(-90,91.,1.) 
#        
#            self.latitudes[:] = self.lats 
#            self.longitudes[:] = self.lons
#            
#            self.var_to_download[:,:,:,:] = self.v
#            self.times.units = 'hours since 0001-01-01 00:00:00'  
#            self.times.calendar= 'gregorian' 
#            self.dates = []
#            # extract year from analyzed date?
#            self.year=1981
#            for n in range(self.var_to_download.shape[0][0]):
#                self.year+=1
#                self.dates.append(datetime(self.year, 1, 15)) 
#            self.times[:] = date2num(self.dates, units = self.times.units,
#                      calendar = self.times.calendar) 
#        print("ready!")

    def download_data(self,output_label,forecast_reference_time,forecastDates):
        """ 
        download data for all realization. Forecast Start Time (forecast_reference_time),
        forecast lead (forecast_lead) and how many months should be forecasted 
        (forecast_months) is specified by user
        """
        self._get_forecast(forecast_reference_time,forecastDates)
        self._save_variable_in_nc(output_label)


