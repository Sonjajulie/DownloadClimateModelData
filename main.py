#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:43:02 2019

@author: sonja totz
"""
from download_NASA_data import NMME

if __name__ == '__main__':
    
    URL_PREFIX = "http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME"
    output_label = "test.nc"
    forecast_reference_time=1
    forecast_lead = 0.5
    forecast_months = 1
    #dictionary of all possible NASA models (key: model name, value: model url adress)
    nasa_dict = {
              "NASA-GMAO" : "/.NASA-GMAO/.MONTHLY",
              "NASA-GMAO-062012" : "/.NASA-GMAO-062012/.MONTHLY",
            }
    
    # iterate over all nasa models
    for model,url in nasa_dict.items():
        print(model,url)
        var = "prec"
        nasa = NMME(model,URL_PREFIX+url,var)
        nasa.download_data(output_label,forecast_reference_time,
                                      forecast_lead,forecast_months)