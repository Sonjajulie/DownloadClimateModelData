# DownloadClimateModelData
Python version: python 3.7

library Requirements:
 - numpy
 - netCDF4
 - scipy
 - datetime
 - xarray


Program usage: python3 main.py

Annotations: 

The forecast months are given by numbers (line 50 in main.py), whereas the the forecast reference date ist fiven by a datetimeobject (line 47 in main.py).  This way, if you want to forecast the date April 1990 from January 1990, you have to change the code in the following way:

...

    ...
    
            forecast_reference_time = datetime(start_year+9,1,1,0,0,0)
            # How many months in advance: 
            # Here: sep, oct, dec
            forecastMonths =2
            
...


The nasa_dict is a dictionary and provides the models which are used to download the data.

TODO:
Should also work on NCAR cluster
OpenMP for models, years?
