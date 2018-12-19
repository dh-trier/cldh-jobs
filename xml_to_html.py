import requests
from xml.dom import minidom
import glob
import os.path
import datetime

# Metadatentabelle als csv Datei
with open('metadaten.csv', 'a') as csvfile:
    csvfile.write(
        "ID#Keyword#URL\n")

for filename in glob.glob('/Users/evgenia/Desktop/Python/DH Projekt/xml/monster/*.xml'):
    print(filename)
    mydoc = minidom.parse(filename)
    urls = mydoc.getElementsByTagName('url')

# Dateiname
    file = os.path.split(filename)
    file = os.path.splitext(file[1])[0]

# Für ID-Generierung wird das erste Element von einem Dateinamen und das aktuelle Datum genutzt
    id = file.split('-')[0] + '_' + datetime.datetime.now().strftime('%d-%m-%y-%H-%M-%S-%f')
# Keyword wird aus dem Dateinamen genommen, als Split-Element wird dabei Bindestrich verwendet
    index = file.find('-')
    keyword = file[index+1::]


    i = 0
    for elem in urls:
        if i < 100:
            # Metadatentabelle als csv-Datei wird angelegt und Spaltenlaben werden erzeugt
            with open('metadaten.csv', 'a') as csvfile:
                csvfile.write(
                    f'{id}#{keyword}#{elem.firstChild.data}\n')  
            # Neue html Datei für jede Anzeige
            f = open('/Users/evgenia/Desktop/Python/DH Projekt/monster_html/%s.html' % id, 'w', encoding='utf-8')
            r = requests.get(elem.firstChild.data)
            f.write(r.text)
            id = file.split('-')[0] + '_' + datetime.datetime.now().strftime('%d-%m-%y-%H-%M-%S-%f')
        i += 1


print("+++__________________________success__________________________+++")