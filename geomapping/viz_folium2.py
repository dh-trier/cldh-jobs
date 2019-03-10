#!/usr/bin/env python3

"""
Script to demonstrate mapping using folium.
Documentaiton: http://python-visualization.github.io/folium/
"""

# == general-purpose imports ==

import glob
import re
import os
from os.path import join
import pandas as pd
import numpy as np
import Radius



# == specific imports ==

import folium


# == parameters == 

jobsdatafile = join("data", "cities-and-jobs.csv")
geodatafile = join("data", "geo-de-org.csv")
mapfile = join("plots", "jobmap_10.03.2019.html")
mapstyle = "Open Street Map" # "Stamen Toner" | "Stamen Watercolor" | "Stamen Terrain" | "Stamen Toner"


# == functions == 
#Leere Liste fuer die Jobanzahl
max_jobs = []

def open_datafile(datafile): 
    """
    Reads a CSV file and returns a DataFrame.
    """
    with open(datafile, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep=";")  #NEU/GEÄNDERT 30.1.2018
        #print(data.head())
        return data


def get_latlon(geodata, place): 
    """
    For a given placename, extracts the latitude and longitude.
    Gives them back separately.
    """
    #print(place)
    row = geodata[geodata["name"] == place]
    #print(row)
    lat = list(row.loc[:,"lat"])[0]
    if not lat: 
        lat = list(row.loc[:,"lat"])[1]        
    if not lat: 
        lat = list(row.loc[:,"lat"])[2]        
    lon = list(row.loc[:,"lon"])[0]
    if not lon: 
        lon = list(row.loc[:,"lon"])[1]
    if not lon: 
        lon = list(row.loc[:,"lon"])[2]
    #print(lat, lon)
    return lat, lon


def get_markerdata(geodata, jobsdata):
    """
    Pulls together the place name, number of jobs, 
    latitude and longitude of each place name,
    and puts them together in a dictionary. 
    Calls get_latlon for each place. 
    """
    markerdata = {}
    places = list(jobsdata.loc[:,"place"])
    #print(places)
    jobnumsALL = list(jobsdata.loc[:, "jobs"])
    jobnumsCL = list(jobsdata.loc[:, "jobs-cl"])
    jobnumsDH = list(jobsdata.loc[:, "jobs-dh"])

    #Jobanzahl wird in die Liste hinzugefuegt. Dies wird fuer die Formel, die Radiusgroesse berechnet, verwendet.
    max_jobs.extend(jobnumsALL)
    

    for i in range (0,len(places)): 
        place = places[i]
        jobnumALL = jobnumsALL[i]
        jobnumCL = jobnumsCL[i]
        jobnumDH = jobnumsDH[i]
        try:                         #NEU/GEÄNDERT 30.1.2018
            lat,lon = get_latlon(geodata, place)
            #print(lat,lon)
        except: 
            print("No geodata for this location:", place)
            lat, lon = 51.16, 10.45
            #print(lat, lon)
        markerdata[place] = {"jobs-all" : jobnumALL,
                             "jobs-cl" : jobnumCL,
                             "jobs-dh" : jobnumDH,
                             "lat" : lat,
                             "lon" : lon}
    #print(markerdata)
    return markerdata


def make_map(mapfile, mapstyle): 
    """
    Creates an empty map just with a marker for Trier.
    """
    mymap = folium.Map(location=[51.312801, 9.481544],
        zoom_start=7,
        tiles = mapstyle,
        attr="<a href=\"http://maps.stamen.com/\">Stamen</a> | <a href=\"https://www.openstreetmap.org\">OSM</a> | <a href=\"http://python-visualization.github.io/folium/\">Folium</a>")
    folium.Marker(location=[49.75,6.63333], popup="Trier").add_to(mymap)
    mymap.save(mapfile)
    return mymap



def methode_rosch(total_jobs):
    #Verteilt die Werte zwischen 4 und 50.
    # x == groesste Stellenanzahl
    x=max(max_jobs)
    #print(x)
    radius = float((total_jobs - 1) * 46 / ((x - 1) - 1) + 4)
    return radius


def add_markers(mymap, markerdata, mapfile):
    """
    For each place with any number of jobs, 
    creates a marker in the right location on the map, 
    with the size of the circle showing the number of jobs, 
    and with the popup showing the place name and number of jobs. 
    Saves the map to an HTML file. 
    """
    for place, data in markerdata.items():       #NEU/GEÄNDERT 30.1.2019
        lat = float(data["lat"])
        lon = float(data["lon"])
        label = str(place) + ": " + str(data["jobs-all"]) + " CL/DH-Stellen"
        #print(lat,lon,label)
        #print(data["jobs-all"])
        radius = methode_rosch(data["jobs-all"])#NEU/GEÄNDERT 10.02.2019
        #radius = Radius.methode_schoech(data["jobs-all"])#NEU/GEÄNDERT 04.1.2019
        #if data["jobs-all"] > 10:
        #    print(data["jobs-all"], radius)
        folium.CircleMarker(
            location=[lat, lon],
            popup = label,
            radius = radius,
            fill = True,
            fill_color='darkgreen').add_to(mymap)
    """
    for place, data in markerdata.items():
        lat = float(data["lat"])
        lon = float(data["lon"])
        label = str(place) + ": " + str(data["jobs-cl"]) + " CL-Stellen"
        radius = int(data["jobs-cl"]*2)
        folium.CircleMarker(
            location=[lat, lon],
            popup = label,
            radius = radius,
            fill = True,
            fill_color='darkblue').add_to(mymap)
    for place, data in markerdata.items():
        lat = float(data["lat"])
        lon = float(data["lon"])
        label = str(place) + ": " + str(data["jobs-dh"]) + " DH-Stellen"
        radius = int(data["jobs-dh"]*2)
        folium.CircleMarker(
            location=[lat, lon],
            popup = label,
            radius = radius,
            fill = True,
            fill_color='darkred').add_to(mymap)
    """
    mymap.save(mapfile)


# == main == 

def main(geodatafile, jobsdatafile, mapfile, mapstyle): 
    geodata = open_datafile(geodatafile)
    jobsdata = open_datafile(jobsdatafile)
    markerdata = get_markerdata(geodata, jobsdata)
    mymap = make_map(mapfile, mapstyle)
    add_markers(mymap, markerdata, mapfile)
    
main(geodatafile, jobsdatafile, mapfile, mapstyle)
