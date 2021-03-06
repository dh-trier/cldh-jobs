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
    The title is printed.
    """
    text = str(html.find_all('script', {'type' : 'application/ld+json'})[-2])   # Infos zu Anzeige im vorletztem <script type="application/ld+json">
    text = re.sub('</script>', "", text)
    text = re.sub('<script(.*?)>', "", text)
    data = json.loads(text)
    
    title = str(data["title"])
    employer = str(data["hiringOrganization"]["name"])
    place = str(data["jobLocation"]["address"]["addressLocality"])
    latitude = "N.A."
    longitude = "N.A."
    date = str(data["datePosted"])
    deadline = "N.A."                                             
    education = "N.A."
    industry = "N.A."
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
            except (AttributeError, UnicodeEncodeError, json.decoder.JSONDecodeError):           # Exceptions, falls Stellenanzeige nicht mehr online ist/ Fehler auftreten
                print("Fehler!")
           
main(dir, htmlpages)
    
