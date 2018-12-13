from bs4 import BeautifulSoup as bs
import glob
import re
import json
from os.path import join
import datetime

dir=""
htmlpages = join(dir, "html","jobstairs","*.html") 

# html-Dateien einelesen und parsen
def read_html(file): 
    with open(file, "r", encoding="utf8") as infile:
        html = infile.read()
        html = bs(html, "html.parser")
        return html

# Extraktion der Metadaten:
def get_metadata(html):
    text = str(html.find('script', {'type' : 'application/ld+json'}))  # Suche nach <script type="application/ld+json">
    text = re.sub('</script>', "", text)
    text = re.sub('<script(.*?)>', "", text)
    y = json.loads(text)
    #print(y)
    
    # hier muss die ID noch angepasst werden, da 
    id = "jobstairs_" + datetime.datetime.now().strftime('%d%m%y%H%M%S%f')   # monster_ + timestamp im Format Tag-Monat-Jahr-Stunde-Minute-Sekunden-Mikrosekunden
    title = str(y["title"])
    #print(title)
    employer = str(y["hiringOrganization"]["name"])
    place = str(y["jobLocation"][0]["address"]["addressLocality"])
    latitude = str(y["jobLocation"][0]["geo"]["latitude"])
    longitude = str(y["jobLocation"][0]["geo"]["longitude"])
    date = str(y["datePosted"])                                                
    
    try:                                                        
        education = str(y["educationRequirements"])
    except KeyError:
        education = " "
    try:
        industry = str(y["industry"][0])    
    except KeyError:
        industry = " "
    try:
        type = str(y["employmentType"])
    except KeyError:
       type = " "
       
  #  url = re.search('<meta property="og:url" content="(.*?)"', str(html))
  #  url = str(url)
  #  print(url)
    
    # Erzeugung einer Zeile mit allen Metadaten für eine Stellenanzeige
    metadata = id + "\t" + title + "\t" + employer + "\t" + place + "\t" + latitude + "\t" + longitude + "\t" + date + "\t" + "" + "\t" + education + "\t" + industry + "\t" + type + "\t"

    print(title)
    
    return metadata
                                        

def main(dir, htmlpages):
    with open('metadaten_jobstairs.csv', 'w') as csvfile:
        
        # würde momentaten die schon vorhandene Tabelle überschreiben, wird angepasst
        csvfile.write("ID\tTitel\tArbeitgeber\tOrt\tBreitengrad\tLängengrad\tVeröffentlichungsdatum\tBewerbungsfrist\tBildungsstand\tJobbranche\tJobart\tDateipfad\n")
        
        for file in glob.glob(htmlpages):
            try:
                html = read_html(file)
                get_metadata(html)
                csvfile.writelines(get_metadata(html) + "\t" + file + "\n")
          # except AttributeError:                               # Exceptions, falls Stellenanzeige nicht mehr online ist/ Fehler auftreten
          #     print("Stellenanzeige nicht gefunden!")
            except UnicodeEncodeError:
                print("Fehler!")
            except json.decoder.JSONDecodeError:
                print("JSON-Fehler!")
           
main(dir, htmlpages)
    
