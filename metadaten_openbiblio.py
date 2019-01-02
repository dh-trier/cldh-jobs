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
    title = html.find('h1', {'class' : 'single-title custom-post-type-title'})
    title = title.get_text()
    title = re.sub("[\,].*", "", title)
    return title


def get_employer(html):
    """
    Takes as input a html file, outputs the employer of the advertisement as string.
    """
    employer = html.find('section', {'class' : 'entry-content clearfix'})
    employer = employer.find('p').get_text()
    employer = re.sub('\| Bewerbungsfrist: \d{2}.\d{2}.\d{4}', "", employer)                     
    return employer


def get_date(html):
    """
    Takes as input a html file, outputs the date of publication of the advertisement as string.
    """
    date = html.find('footer', {'class' : 'article-footer'})
    date = date.find_all('p')[1].get_text()                   # 2. p-element innerhalb des gesuchten footer-Elements
    date = re.sub("(.*?)Veröffentlicht am", "", date)
    date = re.sub("von anonym.", "", date)
    date = date.strip()
    return date


def get_deadline(html):
    """
    Takes as input a html file, outputs the deadline of the advertisement as string.
    """
    deadline = html.find('section', {'class' : 'entry-content clearfix'})
    deadline = deadline.find('p').get_text()
    deadline = re.sub('(.*?) \| Bewerbungsfrist:', "", deadline)
    deadline = deadline.strip()
    return deadline


def get_metadata(html):
    """
    Takes as input a html file, outputs the metadata as string.
    The information are separated by "\t" as delimiter.
    Metadata which can't be extracted from the html file is replaced by "N.A.".
    The title is printed.
    """
    place = "N.A."
    latitude = "N.A."
    longitude = "N.A."                                                                      
    education = "N.A."
    industry = "N.A."
    type = "N.A."
    
    metadata = get_title(html) + "\t" + get_employer(html) + "\t" + place + "\t" + latitude + "\t" + longitude + "\t" + get_date(html) + "\t" + get_deadline(html) + "\t" + education + "\t" + industry + "\t" + type 

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
            except (AttributeError, UnicodeEncodeError):                               # Exceptions, falls Stellenanzeige nicht mehr online ist/Fehler auftreten
                print("Fehler!")
                
           
main(dir, htmlpages)
    
