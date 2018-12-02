# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 16:37:20 2018

@author: Mag
"""
import pandas as pd
import sys
import unidecode
import re

class finder():
    
    def __init__(self):
        """ get data from files and creates cities database """

        try:
            places = pd.read_csv('gps_data\\places.csv', sep=';', header=None)
        except FileNotFoundError:
            print('places.csv file missing in location "gps_data" or location doesn\'t exists')
        else:
            places.columns = ['Place_id', 'State_id', 'Place_name']
            places.Place_name = [unidecode.unidecode(sn).lower() for sn in list(places.Place_name)]
        
        try:
            states = pd.read_csv('gps_data\\provinces.csv', sep=';', header=None)
        except FileNotFoundError:
            print('provinces.csv file missing in location "gps_data" or location doesn\'t exists')
        else:
            states.columns = ['State_id', 'State_name']
            states.State_name = [unidecode.unidecode(sn) for sn in list(states.State_name)]
            
        try:
            self.cities_DB = pd.merge(places, states, how='left', on='State_id')
        except:
            print('Couldn\'t create locations database. One or more files are missing.')

    def get_state(self, location: str):
        """ gets location data from files """
        
        assert (hasattr(self, 'cities_DB')), "No cities database"   
        
        location = unidecode.unidecode(re.sub(r'[\\/;\:]', ',', location).lower())
        location=re.sub('polska', ' ', location)
        location=re.sub('poland', ' ', location)
        location=re.sub('dolny slask', 'dolnoslaskie', location)
        location=re.sub('warsaw', 'warszawa', location).strip()
        #print(location)
    
        loc_parts = location.split(',')
        try:
            s = [part for part in loc_parts if part in list(self.cities_DB.State_name)][0]
        except:
            s= ''
            
        if len(s)==0:
            for part in loc_parts:
                if part in list(self.cities_DB.Place_name):
                    s = self.cities_DB.State_name.loc[self.cities_DB.Place_name==part].values[0]
                    break
                else:
                    location = unidecode.unidecode(re.sub(r'[,-]', ' ', location).lower())
                    loc_parts = location.split(' ')
                    for part in loc_parts:
                        if part.strip() in list(self.cities_DB.Place_name):
                            s = self.cities_DB.State_name.loc[self.cities_DB.Place_name==part.strip()].values[0]
                            break
        
        return s