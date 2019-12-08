#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:45:58 2019

@author: sonja totz
"""

from datetime import datetime
import xarray as xa
import sys
import logging


logger = logging.getLogger(__name__)


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
        logger.info(f"Access {self.var} from model {self.model} via {self.fullURL}\n")
        try:
            with xa.open_dataset(self.fullURL, decode_times=False)  as self.nc:
                #  Check for variable in dataset 
                assert self.var in (self.nc.variables),logging.error(f"Variable {self.var} not found! Possible variables:\
                                                       self.nc.variables ")
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
                # check whether forecast_reference_time is in dataset
                assert self.m  in (self.nc.S.values), logging.error(f"Forecast reference time not found ({forecast_reference_time})!\
                        Only possible forecast refernce times are\
                        {list(map(lambda x: (self._num_to_date(x)).strftime('%Y-%m-%d'),self.nc.S.values))}")
                # check whether forecastMonths are in dataset
                assert set(forecastMonths).issubset(self.nc.L.values), logging.error(f"Forecast months not found!\
                        Possible forecast months are {self.nc.L.values}")
                logger.debug("Download raw data: {self.nc}")
                # Get requested data and save data as netcdf
                self.ds = self.nc.sel(S=self.m,L=forecastMonths)
                self.forecast_time = [self._num_to_date(self.m + i) for i in (forecastMonths)]
                self.ds = self.ds.rename({'X': 'longitude','Y': 'latitude'})
                self.ds = (self.ds.assign_coords(L=self.forecast_time))
                logger.debug("Download data: {self.ds}")
                self.ds.to_netcdf(path=output_label, engine='scipy')
        except OSError:
            print(f"\nWebsite {self.fullURL} not found!\n")
            sys.exit(-1)
            
    def _num_to_date(self,nMonths):
        """ Helper-function to convert number to date"""
        self.nMonths = int(nMonths)
        self.baseDate = datetime(1960,1,1,0,0,0)
        self.deltayears  = self.nMonths//12
        self.deltamonths = self.nMonths % 12
        self.requestedDate = datetime(self.baseDate.year + self.deltayears, self.baseDate.month + self.deltamonths, 1,0,0,0)
        logger.debug("Date: {self.requestedDate}")
        return self.requestedDate

    def _date_to_num(self,reqDate):
        """ Helper-function to convert date to number"""
        self.baseDate = datetime(1960,1,1,0,0,0)
        self.nMonths  = (reqDate.year - self.baseDate.year) * 12
        self.nMonths += reqDate.month - self.baseDate.month
        logger.debug("Num: {self.requestedDate}")
        return self.nMonths


