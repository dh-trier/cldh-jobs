Ziel: Eine Liste mit Ort, Anzahl der CL-Jobs, Anzahl der DH-Jobs und gesamtanzahl zu erstellen.
Beispiel:
	place;jobs-cl;jobs-dh;jobs
	Karlsruhe;1;0;1
	Nürnberg;1;1;2

Schritt 1.
Dazu werden 3 Listen benötigt:

Liste 1. Alle Ortsangaben (CL+DH) aus Metadatentabelle
Beispiel:
	Karlsruhe
	Nürnberg
	Berlin
	Konstanz
	Hannover
	Köln
	Hamburg
	München
	München
	Stuttgart
	Nürnberg
	Frankfurt am Main

Liste 2. Alle Ortsangaben nur für CL 
Beispiel:
	Karlsruhe
	Nürnberg
	Berlin
	Konstanz
	Hannover
	Köln
	Hamburg

Liste 3. Alle Ortsangaben nur für DH 
Beispiel:
	München
	München
	Stuttgart
	Nürnberg
	Frankfurt am Main


Schritt 2.
Mit dem Skript "dublikate-entfernen.py" wird eine neue Liste aus Liste 1 erstellt. 
Dabei werden die Dublikate aus Liste 1 entfernt.

Schritt 3.
Mit dem Skript "geo-daten-erstellen.py" wird die entgültige Liste erstellt und als CSV datei gespeichert.
Beispiel:
	place;jobs-cl;jobs-dh;jobs
	Karlsruhe;1;0;1
	Nürnberg;1;1;2
	Berlin;1;0;1
	Konstanz;1;0;1
	Hannover;1;0;1
	Köln;1;0;1
	Hamburg;1;0;1
	München;0;2;2
	Stuttgart;0;1;1
	Frankfurt am Main;0;1;1
