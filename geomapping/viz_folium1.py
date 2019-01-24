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


# == specific imports ==

import folium


# == parameters == 

jobsdatafile = join("data", "cities-and-jobs.csv")
geodatafile = join("data", "geo-de.csv")
mapfile = join("plots", "jobmap1.html")
mapstyle = "Open Street Map" # "Open Street Map" | "Stamen Watercolor" | "Stamen Terrain" | "Stamen Toner"


# == functions == 


def open_datafile(datafile): 
    """
    Reads a CSV file and returns a DataFrame.
    """
    with open(datafile, "r", encoding="utf8") as infile: 
        data = pd.read_table(infile, sep="[\t;]", engine="python")
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
    jobnums = list(jobsdata.loc[:, "jobs"])
    for i in range (0,len(places)): 
        place = places[i]
        jobnum = jobnums[i]
        lat,lon = get_latlon(geodata, place)
        markerdata[place] = {"jobs" : jobnum,
                             "lat" : lat,
                             "lon" : lon}
    print(markerdata)
    return markerdata


def make_map(mapfile, mapstyle): 
    """
    Creates an empty map just with a marker for Trier.
    """
    mymap = folium.Map(location=[51.312801, 9.481544],
        zoom_start=7,
        tiles = mapstyle,
        attr="<a href=\"http://maps.stamen.com/\">Stamen</a> | <a href=\"https://www.openstreetmap.org\">OSM</a> | <a href=\"http://python-visualization.github.io/folium/\">Folium</a>")
    folium.Marker(location=[51.312801, 9.481544], 
        popup="Kassel").add_to(mymap)
    mymap.save(mapfile)
    return mymap


def add_markers(mymap, markerdata, mapfile):
    """
    For each place with any number of jobs, 
    creates a marker in the right location on the map, 
    with the size of the circle showing the number of jobs, 
    and with the popup showing the place name and number of jobs. 
    Saves the map to an HTML file. 
    """
    for place, data in markerdata.items():
        lat = float(data["lat"])
        lon = float(data["lon"])
        label = str(place) + ": " + str(data["jobs"]) + " Stellen"
        radius = int(data["jobs"])
        folium.CircleMarker(
            location=[lat, lon],
            popup = label,
            radius = radius,
            fill = True,
            fill_color='darkblue').add_to(mymap)
    mymap.save(mapfile)


# == main == 

def main(geodatafile, jobsdatafile, mapfile, mapstyle): 
    geodata = open_datafile(geodatafile)
    jobsdata = open_datafile(jobsdatafile)
    markerdata = get_markerdata(geodata, jobsdata)
    mymap = make_map(mapfile, mapstyle)
    add_markers(mymap, markerdata, mapfile)
    
main(geodatafile, jobsdatafile, mapfile, mapstyle)
