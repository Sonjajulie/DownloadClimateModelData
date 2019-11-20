#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:43:02 2019

@author: sonja totz
"""
from download_NASA_data import NMME
from datetime import datetime


if __name__ == '__main__':
    
    URL_PREFIX = "http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME"
    output_label = "/home/sonja/Documents/NASA/NASA-Models/output/test.nc"
    #forecast start date
    forecast_reference_time = datetime(1982,11,1,0,0,0)

    forecastDates = []
    forecastDates.append(datetime(1982,12,31,0,0,0))
    forecastDates.append(datetime(1982+1,1,31,0,0,0))
    forecastDates.append(datetime(1982+1,2,28,0,0,0))
    #dictionary of all possible NASA models (key: model name, value: model url adress)
    nasa_dict = {
              "NASA-GMAO" : "/.NASA-GMAO/.MONTHLY",
#              "NASA-GMAO-062012" : "/.NASA-GMAO-062012/.MONTHLY",
            }
    
    # iterate over all nasa models
    for model,url in nasa_dict.items():
        print(model,url)
        var = "prec"
        nasa = NMME(model,URL_PREFIX+url,var)
        nasa.download_data(output_label,forecast_reference_time,forecastDates)
        
        
