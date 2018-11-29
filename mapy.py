# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 20:54:02 2018

@author: Mag
"""

import googlemaps as gm
import geocoder
import requests

gmaps = gm.Client(key=open('gm_api_key.txt','r').read())
dir(gmaps)

a = gmaps.geocode('Warszawa')
b = gmaps.geocode('Wroclaw')

key=open('gm_api_key.txt','r').read()
address='Warszawa'
geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
geocode_url = geocode_url + "&key={}".format(key)
        
results = requests.get(geocode_url)
    # Results will be in JSON format - convert to dict using requests functionality
results = results.json()

import geocoder as geo

g = geo.google('Warszawa')
g.latlng