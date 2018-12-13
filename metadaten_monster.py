from bs4 import BeautifulSoup as bs
import glob
import re
import json
from os.path import join
import datetime

dir=""
htmlpages = join(dir, "html", "*.html") 

# html einlesen und mit Beautifulsoup parsen
def read_html(file): 
    with open(file, "r", encoding="utf8") as infile:
        html = infile.read()
        html = bs(html, "html.parser")
        return html

# gibt Metadaten einer Stellenanzeige als String zurück
def get_metadata(html):
    text = str(html.find('script', {'type' : 'application/ld+json'}))  # Suche nach <script type="application/ld+json">
    text = re.sub('</script>', "", text)
    text = re.sub('<script(.*?)>', "", text)
    y = json.loads(text)
    
    from generate_timestamp import timestamp
    timestamp = timestamp()
    
    id = "monster_" + timestamp   # monster_ + timestamp im Format Tag-Monat-Jahr-Stunde-Minute-Sekunden-Mikrosekunden
    title = str(y["title"])
    employer = str(y["identifier"]["name"])
    place = str(y["jobLocation"]["address"]["addressLocality"])
    latitude = str(y["jobLocation"]["geo"]["latitude"])
    longitude = str(y["jobLocation"]["geo"]["longitude"])
    date = str(y["datePosted"])
    deadline = "N.A."                                             # deadline wird bei monster nicht angegeben
    
    try:                                                         # Informationen sind nicht zu jeder Anzeige verfügbar
        education = str(y["educationRequirements"])
    except KeyError:
        education = "N.A."
    try:
        industry = str(y["industry"])    # industry enthält immer eine Liste
        industry = re.sub("[\[\]\']*", "", industry)         
                       
    except KeyError:
        industry = "N.A."
    try:
        type = str(y["employmentType"])    # employmentType enthält immer eine Liste
        type = re.sub("[\[\]\']*", "", type) 
    except KeyError:
       type = "N.A."
       
    
    # Erzeugung einer Zeile mit allen Metadaten für eine Stellenanzeige
    metadata = id + "\t" + title + "\t" + employer + "\t" + place + "\t" + latitude + "\t" + longitude + "\t" + date + "\t" + deadline + "\t" + education + "\t" + industry + "\t" + type 

    print(title)
    
    return metadata
                                        

def main(dir, htmlpages):
    with open('metadaten.csv', 'a') as csvfile:     # Metadatentabelle öffnen und ergänzen
        
        for file in glob.glob(htmlpages):
            try:
                html = read_html(file)            
                csvfile.writelines(get_metadata(html) + "\n")
            except (AttributeError, UnicodeEncodeError, json.decoder.JSONDecodeError):                               # Exceptions, falls Stellenanzeige nicht mehr online ist/ Fehler auftreten
                print("Fehler!")
           
main(dir, htmlpages)
    
