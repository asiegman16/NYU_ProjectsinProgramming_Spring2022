import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import time 
import json 
import urllib.request
import sqlite3
from datetime import datetime

con = sqlite3.connect('/Users/asiegman/Desktop/NYU_ProjectsinProgramming_Spring2022/Class 7/citibikeData2022_class7.db')

while True:
   
    with urllib.request.urlopen("https://gbfs.citibikenyc.com/gbfs/en/station_information.json") as url:
        station_info = json.loads(url.read().decode())
        station_info_values_list = list(station_info.values())
        clean_station_info = station_info_values_list[0]['stations']

    with urllib.request.urlopen("https://gbfs.citibikenyc.com/gbfs/en/station_status.json") as url:
        station_status = json.loads(url.read().decode())
        station_status_values_list = list(station_status.values())
        clean_station_status = station_status_values_list[0]['stations']

    sql = "CREATE TABLE IF NOT EXISTS AllStationData (capacity INTEGER, lat BLOB, lon BLOB, name TEXT, region_id INTEGER, station_type TEXT, is_installed INTEGER, is_renting INTEGER, is_returning INTEGER, num_bikes_available INTEGER, num_bikes_disabled INTEGER, num_docks_available INTEGER, num_docks_disabled INTEGER, num_ebikes_available INTEGER, station_id INTEGER, station_status TEXT );" 

    con.execute(sql)
    con.commit()

    query_template = """INSERT OR IGNORE INTO AllStationData (capacity, lat, lon, name, station_type, is_installed, is_renting, is_returning, num_bikes_available, num_bikes_disabled, num_docks_available, num_docks_disabled, num_ebikes_available, station_id, station_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    for info, status in zip(clean_station_info,clean_station_status):
        
        capacity = info['capacity']
        lat = info['lat']
        lon = info['lon']
        name = info['name']
        station_type = info['station_type']
        is_installed = status['is_installed']
        is_renting = status['is_renting'] 
        is_returning = status['is_returning']
        num_bikes_available = status['num_bikes_available'] 
        num_bikes_disabled = status['num_bikes_disabled']
        num_docks_available = status['num_docks_available']
        num_docks_disabled = status['num_docks_disabled'] 
        num_ebikes_available = status['num_ebikes_available']
        station_id = info['station_id']
        station_status = status['station_status']
                               
        print("Inserting Station:", capacity, lat, lon, name, station_type, is_installed, is_renting, is_returning, num_bikes_available, num_bikes_disabled, num_docks_available, num_docks_disabled, num_ebikes_available, station_id, station_status) 

        query_parameters = (capacity, lat, lon, name, station_type,is_installed, is_renting, is_returning, num_bikes_available, num_bikes_disabled, num_docks_available, num_docks_disabled, num_ebikes_available, station_id, station_status) 
        
        con.execute(query_template, query_parameters)
        
    con.commit()
        
time.sleep(60)