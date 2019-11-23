#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:45:58 2019

@author: sonja totz
"""

from datetime import datetime
import xarray as xa

class NMME():
    """ class to download data from NMME models"""
    
    def __init__(self,model,url,var):
        """ Initialize model, variable, url for download"""
        self.model = model
        self.url = url
        self.var = var
        self.fullURL = f"{self.url}/.{self.var}/dods"

    def download_data(self,output_label,forecast_reference_time,forecastMonths):
        """ 
        download data for all realization. Forecast Start Time (forecast_reference_time),
        forecast lead (forecast_lead) and months 
        (forecast_months) is specified by user
        """
        print(f"Access {self.var} from model {self.model} via {self.fullURL}")
        with xa.open_dataset(self.fullURL, decode_times=False)  as self.nc:
            #  Check for variable in dataset 
            assert self.var in (self.nc.variables),"Variable not found!"
            
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
            self.m = int(self._date_to_num(forecast_reference_time))
            
            # check whether forecastMonths are in Lead of dataset
            assert set(forecastMonths).issubset(self.nc.L.values), f"Forecast months not found! Only possible forecastmonts are {self.nc.L.values}"
            
            # Get requested data and save data as netcdf
            self.ds = self.nc.sel(S=self.m,L=forecastMonths)
            self.forecast_time = [self._num_to_date(self.m + i) for i in (forecastMonths)]
            self.ds = self.ds.rename({'X': 'longitude','Y': 'latitude'})
            self.ds = (self.ds.assign_coords(L=self.forecast_time))
            self.ds.to_netcdf(path=output_label, engine='scipy')

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


