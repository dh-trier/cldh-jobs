#Die Dtei wird Zeilenweise gelesen.
#in "final_list" array wird ein Token z.B. "Berlin" (in der Datei kann "Berlin" mehrmals vorkommen) nur einmal aufgenommen.
#Es entsteht ein Array ohne Dublikate
with open("orte_alle-org.txt", "r", encoding="utf-8") as file:
    final_list = []
    for line in file:
        if line not in final_list:
            final_list.append(line)
    print(final_list)
    
    #Aus Array "final_list" wird eine Liste erstellt
    liste = final_list
    stringliste = ""
    for i in liste:
        stringliste = stringliste+str(i)#+"\n"
        #print(stringliste)
        
with open('orte_alle_ohne_dublikate.txt', 'w', encoding="utf-8") as f:
    f.write(str(stringliste))
    f.close()
