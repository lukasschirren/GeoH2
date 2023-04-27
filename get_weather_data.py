# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 15:11:47 2023

@author: Claire Halloran, University of Oxford

get_weather_data.py

This script fetches historical weather data to calculate wind and solar potential
from the ERA-5 reanalysis dataset using Atlite.

Create cutouts with `atlite <https://atlite.readthedocs.io/en/latest/>`_.

For this rule to work you must have

- installed the `Copernicus Climate Data Store <https://cds.climate.copernicus.eu>`_ ``cdsapi`` package  (`install with `pip``) and
- registered and setup your CDS API key as described `on their website <https://cds.climate.copernicus.eu/api-how-to

.. seealso::
    For details on the weather data read the `atlite documentation <https://atlite.readthedocs.io/en/latest/>`_.
    If you need help specifically for creating cutouts `the corresponding section in the atlite documentation <https://atlite.readthedocs.io/en/latest/examples/create_cutout.html>`_ should be helpful.

"""
import logging
import atlite
# import geopandas as gpd
import pandas as pd
# from _helpers import configure_logging

logging.basicConfig(level=logging.INFO)

weather_excel_path = "Data/weather_parameters.xlsx"

weather_parameters = pd.read_excel(weather_excel_path,
                                   index_col = 'Parameters'
                                   ).squeeze('columns')

start_date = weather_parameters['Start date']
end_date = weather_parameters['End date (not inclusive)']
min_lon = weather_parameters['Minimum longitude (deg)']
max_lon = weather_parameters['Maximum longitude (deg)']
min_lat = weather_parameters['Minimum latitude (deg)']
max_lat = weather_parameters['Maximum latitude (deg)']
filename = weather_parameters['Filename']


snapshots = slice(start_date,end_date) # date range to import, end not inclusive

cutout = atlite.Cutout(
    path="Cutouts/" + filename + ".nc",
    module="era5",
    x=slice(min_lon, max_lon),
    y=slice(min_lat, max_lat),
    time=snapshots,
)

cutout.prepare()