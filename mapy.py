# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 20:54:02 2018

@author: Mag
"""

import googlemaps as gm

gmaps = gm.Client(key=open('gm_api_key.txt','r').read())

a = gm.geocode('Warszawa')