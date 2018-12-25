from bs4 import BeautifulSoup as bs
import glob

for document in glob.glob('D:/DH/absolventa_html/*.html'):  #Pfad aendrn!
    html = open(document, 'r', encoding="utf8")
    soup = bs(html, "html.parser")
    #print(soup.prettify())                                	#dokument für lesen öffnen und Strukturieren des Dokumentes

    file_txt = document.replace('.html', '.txt')           	#Ordner für Speichern des Textes wird erstellt, und der Name der Datei von HTML wird übernommen 
    f = open(file_txt, 'w', encoding="utf8")

    for script in soup(["script", "style"]):				#löscht alle "Style" Elemente
        script.extract()									

    for header in soup.find_all("h2"):						# Markiert alle H2 Elemente 
        header.insert_before("#")

    for bridges in soup.find_all("br"):						#Markiert alle br Elemente, sie werden manchmal an Stelle von Listen benutzt
        bridges.insert_before('*')

    for lines in soup.find_all("li"):						#Markiert alle li(Listen)
        lines.insert_before('**')

    text = soup.get_text()									#eigentliche Textextraktion
    lines = (line.strip() for line in text.splitlines())						#Text wird in Zeilen aufgeteilt
																				#Jede neue Überschrift fängt mit neuer Zeile an
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))	
																				# Leere Zeile werden gelöscht
    text = '\n'.join(chunk for chunk in chunks if chunk)							

    #print(text)
    f.write(text)


