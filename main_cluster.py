#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:45:58 2019

@author: sonja totz
"""
from download_NMME_data import NMME
from datetime import datetime
import sys

if __name__ == '__main__':
    URL_PREFIX = "http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME"

start_year=1981
year = int(sys.argv[1])
for month in range(3,9):
    output_label = f"/home/sonja/Documents/NASA/NASA-Models/output/model_{month}_{year+start_year}"
    #forecast start date
    forecast_reference_time = datetime(start_year+year,month,1,0,0,0)
    # How many months in advance: 
    # Here: sep, oct, dec
    forecastMonths = [0.5+i + 9-month for i in range(3)]
    #dictionary of all possible NASA models (key: model name, value: model url adress)
    nasa_dict = {
              "NASA-GMAO" :        "/.NASA-GMAO/.MONTHLY",
              "NASA-GMAO-062012" : "/.NASA-GMAO-062012/.MONTHLY",
              "NASA-GEOSS2S":      "/.NASA-GEOSS2S/.HINDCAST/.MONTHLY"
            }
    print(f"\nDownload data for forecast_reference_time: {forecast_reference_time} and lead: {forecastMonths}")
    # iterate over all nasa models
    for model,url in nasa_dict.items():
        var = "prec"
        output_label_full = f"{output_label}_{model}_{var}.nc"
        nasa = NMME(model,URL_PREFIX+url,var)
        nasa.download_data(output_label_full,forecast_reference_time,forecastMonths)
