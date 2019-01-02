#!/usr/bin/env python3

"""
Script for getting metadata from advertisements of openbiblio (https://jobs.openbiblio.eu/) using BeautifulsSoup.
See: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

"""

# === Import statements ===

from bs4 import BeautifulSoup as bs
import glob
import re
from os.path import join
import os


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


def get_title(html):
    """
    Takes as input a html file, outputs the title of the advertisement as string.
    """
    title = html.find('title').get_text()
    title = re.sub(" - (.*?) - Indeed.com", "", title)
    title = re.sub(" \| Indeed.com", " ", title)
    return title


def get_employer(html):
    """
    Takes as input a html file, outputs the employer of the advertisement as string.
    """
    employer = html.find('div', {'class' : 'icl-u-lg-mr--sm icl-u-xs-mr--xs'})
    try:
        employer = employer.get_text()
    except AttributeError:
        employer = "N.A."
    print(employer)
    return employer



def get_place(html):
    """
    Takes as input a html file, outputs the place as string.
    """
    place = html.find('title').get_text()
    try:
        place = re.search(" - (.*?) - ", place).group()
        place = re.sub("- ", "", place)
        place = re.sub(" -", "", place)
        place = re.sub("[0-9]*", "", place)
        place = place.strip()                      # Entfernung Whitespace vor und hinter dem String
    except AttributeError:
        place = "N.A."
    return place


def get_date(html):
    """
    Takes as input a html file, outputs the date of publication of the advertisement as string.
    """
    date = html.find('div', {'class' : 'jobsearch-JobMetadataFooter'})
    date = date.get_text()
    date = re.search("- vor(.*?)Tagen -", date).group()
    date = re.sub("-", "", date)
    return date


def get_metadata(html):
    
    """
    Takes as input a html file, outputs the metadata as string.
    The information are separated by "\t" as delimiter.
    Metadata which can't be extracted from the html file is replaced by "N.A.".
    
    The title is printed.
    """
    
    latitude = "N.A."
    longitude = "N.A."                                
    deadline = "N.A."                                             
    education = "N.A."
    industry = "N.A."
    type = "N.A."
    
    metadata = get_title(html) + "\t" + get_employer(html) + "\t" + get_place(html) + "\t" + latitude + "\t" + longitude + "\t" + get_date(html) + "\t" + deadline + "\t" + education + "\t" + industry + "\t" + type 

    print(get_title(html))
    
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
            except (AttributeError, UnicodeEncodeError):                               # Exceptions, falls Stellenanzeige nicht mehr online ist/ Fehler auftreten
                print("Fehler!")
           
main(dir, htmlpages)
    
