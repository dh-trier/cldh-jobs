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
    text = str(html.find_all('script', {'type' : 'application/ld+json'})[-2])  # Infos zu Anzeige im vorletztem <script type="application/ld+json">
    text = re.sub('</script>', "", text)
    text = re.sub('<script(.*?)>', "", text)
    data = json.loads(text)
    
    id = "absolventa_" + datetime.datetime.now().strftime('%d%m%y%H%M%S%f')   # monster_ + timestamp im Format Tag-Monat-Jahr-Stunde-Minute-Sekunden-Mikrosekunden
    title = str(data["title"])
    employer = str(data["hiringOrganization"]["name"])
    place = str(data["jobLocation"]["address"]["addressLocality"])
    latitude = "N.A."
    longitude = "N.A."
    date = str(data["datePosted"])
    deadline = "N.A."                                             # deadline wird bei monster nicht angegeben
    education = "N.A."
    industry = "N.A."
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
    
