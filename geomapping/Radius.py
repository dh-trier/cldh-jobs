def methode_schoech(total_jobs):
    radius = float(((total_jobs)/8)+3)
    return radius

#Verteilt die Werte zwischen 5 und 50.
#Wert 444 muss nach dubletten Erkennung angepasst werden. 444 ist aktuell der groesste Wert.
def methode_rosch(total_jobs):
    radius = float((total_jobs-1)*45/((444-1)-1)+5)
    return radius