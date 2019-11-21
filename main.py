#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:45:58 2019

@author: sonja totz
"""
from download_NMME_data import NMME
from datetime import datetime


if __name__ == '__main__':
    
    URL_PREFIX = "http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME"
    output_label = "model_"
    
    #forecast start date
    forecast_reference_time = datetime(1982,11,1,0,0,0)
    # How many months in advance?
    forecastMonths = [2.5,3.5,4.5]
    #dictionary of all possible NASA models (key: model name, value: model url adress)
    nasa_dict = {
              "NASA-GMAO" :        "/.NASA-GMAO/.MONTHLY",
              "NASA-GMAO-062012" : "/.NASA-GMAO-062012/.MONTHLY",
              "NASA-GEOSS2S":      "/.NASA-GEOSS2S/.HINDCAST/.MONTHLY"
            }
    
    # iterate over all nasa models
    for model,url in nasa_dict.items():
        output_label_full = output_label + model + ".nc"
        print(model,url)
        var = "prec"
        nasa = NMME(model,URL_PREFIX+url,var)
        nasa.download_data(output_label_full,forecast_reference_time,forecastMonths)
