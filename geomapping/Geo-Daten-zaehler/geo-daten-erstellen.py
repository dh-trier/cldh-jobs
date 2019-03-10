import re
#Daten werden Zeile fuer Zeile eingelesen

jobs_ohne_dublikate = open("orte_alle_ohne_dublikate.txt", encoding="utf-8")
jobs_ohne_dublikate = jobs_ohne_dublikate.readlines()

jobs = open("orte_alle-org.txt", encoding="utf-8")
jobs = jobs.readlines()

CL_jobs = open("orte_CL.txt", encoding="utf-8")
CL_jobs = CL_jobs.readlines()

DH_jobs = open("orte_DH.txt", encoding="utf-8")
DH_jobs = DH_jobs.readlines()

#Newline (\n) wird entfernt
jobs_ohne_dublikate= list(map(lambda x:x.strip(),jobs_ohne_dublikate))
jobs= list(map(lambda x:x.strip(),jobs))
CL_jobs= list(map(lambda x:x.strip(),CL_jobs))
DH_jobs= list(map(lambda x:x.strip(),DH_jobs))



#print(jobs_ohne_dublikate)
#print(jobs)
#print(CL_jobs)
#print(DH_jobs)


output=[]
i=0
#Fuer jedes Token "x" aus jobs_ohne_dublikate werden CL, DH und "gesamt" jobs gezaehlt und in output array hinzugefuegt
for x in jobs_ohne_dublikate:
    if i < len(jobs_ohne_dublikate):
        
        count_CL = CL_jobs.count(x)
        count_DH = DH_jobs.count(x)
        count_jobs = jobs.count(x)
        output_token = x+';0;0;'+str(count_jobs)
        #output_token = x+';'+str(count_CL)+';'+str(count_DH) +';'+ str(count_jobs)
        output.append(output_token)
        
    i+=1
#print(output)

#Aus Array "output" wird eine Liste erstellt
stringliste = ""
for i in output:
    stringliste = stringliste+str(i)+"\n"
    #print(stringliste)
        
with open('cities-and-jobs_new.csv', 'w', encoding="utf-8") as f:
    f.write("place;jobs-cl;jobs-dh;jobs"+"\n")
    f.write(str(stringliste))
    f.close()