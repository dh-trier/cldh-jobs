#!/usr/bin/env python3

"""
Script for getting metadata from advertisements of openbiblio (https://jobs.openbiblio.eu/) using BeautifulsSoup and json module.
See: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://docs.python.org/2/library/json.html

"""

# === Import statements ===

from bs4 import BeautifulSoup as bs
import glob
import re
import json
import os
from os.path import join


# === Parameters ===

dir=""
htmlpages = join(dir, "html", "*.html")


# === Functions ===

def read_html(file):
    """
    Takes as input a html file, outputs a the parsed html.
    """
    with open(file, "r", encoding="utf8") as infile:
        html = infile.read()
        html = bs(html, "html.parser")
        return html


def get_metadata(html):
    """
    Takes as input a html file, outputs the metadata as string.
    The information are separated by "\t" as delimiter.
    Metadata which can't be extracted from the html file is replaced by "N.A.".
    Exceptions are used when extracting information that isn't found in every advertisement.
    
    The title is printed.
    """
   
    text = str(html.find('script', {'type' : 'application/ld+json'}))        # Suche nach <script type="application/ld+json">
    text = re.sub('</script>', "", text)
    text = re.sub('<script(.*?)>', "", text)
    y = json.loads(text)
    
    title = str(y["title"])
    employer = str(y["identifier"]["name"])
    place = str(y["jobLocation"]["address"]["addressLocality"])
    
    try:
        latitude = str(y["jobLocation"]["geo"]["latitude"])
    except KeyError:
        latitude = "N.A."
    
    try:
        longitude = str(y["jobLocation"]["geo"]["longitude"])
    except:
        longitude = "N.A."
    
    date = str(y["datePosted"])
    deadline = "N.A."                                            
    
    try:                                                         # Informationen sind nicht zu jeder Anzeige verfügbar
        education = str(y["educationRequirements"])
    except KeyError:
        education = "N.A."
        
    try:
        industry = str(y["industry"])              # industry enthält immer eine Liste
        industry = re.sub("[\[\]\']*", "", industry)                   
    except KeyError:
        industry = "N.A."
        
    try:
        type = str(y["employmentType"])            # employmentType enthält immer eine Liste
        type = re.sub("[\[\]\']*", "", type) 
    except KeyError:
       type = "N.A."
       
    
    metadata = title + "\t" + employer + "\t" + place + "\t" + latitude + "\t" + longitude + "\t" + date + "\t" + deadline + "\t" + education + "\t" + industry + "\t" + type 

    print(title)
    
    return metadata
                                        


# === Coordinating function ===

def main(dir, htmlpages):
    """
    Coordinates the saving of metadata for all files contained in the
    folder "htmlpages".
    Opens "metadaten.csv", extracts the id from each html filename and writes it with the metadata string into the csv file.
    Possible errors are catches by exceptions.
    """
    
    with open('metadaten.csv', 'a') as csvfile:     
        
        for file in glob.glob(htmlpages):
            try:
                html = read_html(file)            
                base = os.path.basename(file)                   # trennt Basis vom Dateipfad ab
                id = str(os.path.splitext(base)[0])             # trennt Extension ab
                csvfile.writelines(id + "\t" + get_metadata(html) + "\n")
            except (AttributeError, UnicodeEncodeError, json.decoder.JSONDecodeError):                               # Exceptions, falls Stellenanzeige nicht mehr online ist/ Fehler auftreten
                print("Fehler!")
           
main(dir, htmlpages)
    
