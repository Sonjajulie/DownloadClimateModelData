#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:45:58 2019

@author: sonja totz
"""
from download_NMME_data import NMME
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "nmme_download.log"


if __name__ == '__main__':
    URL_PREFIX = "http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME"

    # create logger
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


    # create console handler and file handler and set level to debug and error
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    file_handler = logging.FileHandler("NMME.log")
    file_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter_exact = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")

    # add formatter to console_handler and file_handler
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter_exact)

    # Create logger
    logger = logging.getLogger(__name__)
    # add ch to logger
    logger.addHandler(console_handler)
    logging.info('Start NMME download')
    start_year=1981
    for year in range(1):
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
            logger.info(f"\nDownload data for forecast_reference_time: {forecast_reference_time} and lead: {forecastMonths}")
            # iterate over all nasa models
            for model,url in nasa_dict.items():
                var = "prec"
                output_label_full = f"{output_label}_{model}_{var}.nc"
                nasa = NMME(model,URL_PREFIX+url,var)
                nasa.download_data(output_label_full,forecast_reference_time,forecastMonths)
