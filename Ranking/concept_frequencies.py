import stringdist as dist           # Levenshtein-Distanz
import json                         # Konvertierung von und in JSON-Format
import re                           # reguläre Ausdrücke
import os                           # operating system dependent functionality
from more_itertools import locate   # zurückgeben aller Indizes für ein bestimmtes Objekt in einem Iterable
import glob                         # durchlaufen von Ordnern
from os.path import join            # zusammenfügen von Dateipfaden
import itertools

def read_text(path):
    """ Öffnet eine Textdatei und gibt den Inhalt zurück. """
    #print(path)
    with open(path, encoding="utf-8") as f:
        content = f.read()
        content = re.sub('\\n', ' ', content)
    return content


def tokenize(text):
    """
        Wandelt einen Text um in eine Liste aus Token, wobei die in non_alpha
        enthaltenen Satzzeichen ignoriert werden.
    """
    lower_text = text.lower()
    lower_text = re.sub("c#", "csharp", lower_text)
    tokenized = re.split("\W", lower_text)
    tokenized_text = ['c#' if token == 'csharp' else token for token in tokenized if token]

    #print(tokenized_text)

    return tokenized_text


def compare_word_concept(concept, word):
    """
        Überprüft ob Konzept(teilbegriff) und das aktuelle Wort identisch sind
        bzw. alternativ wird, sofern die Anfangsbuchstaben identisch sind und
        die Wortlänge größer als 6 Zeichen beträgt, die Levenshtein-Distanz
        berechnet. Überschreitet diese einen bestimmten Wert nicht, wird dies
        als Übereinstimmung gewertet.
    """
    if concept == word:
        return 1
    elif concept[0] == word[0] and len(word) > 6:
        distance = dist.levenshtein(word, concept)
        if distance <= int(len(word) / 3):
            return 1
        else:
            return 0


def conceptgroup_to_dictionary(concept_group):
    """
        Die übergebene Liste von Konzeptphrasen wird überführt in ein Dictionary, wobei die Phrase
        als Key verwendet wird und 0 standarmäßig als Wert festgelegt wird. Handelt es sich um eine
        Mehrwort-Phrase, so werden die einzelnen Begriffe mit einem Leerzeichen dazwischen konkateniert.
        Ansonsten wird das einzelne Wort verwendet.
    """
    arr = []
    for concept in concept_group:
        word = ''
        if len(concept) == 1:
            arr.append(concept[0])  # da alle Konzeptphrasen in einer Liste stehen, muss bei Einwortphrasen
                                    # das erste Element der Liste ausgewählt werden
        else:
            for i in range(len(concept)):
                word += concept[i]
                if i < (len(concept)-1):    # sofern noch ein Element folgt, hänge ein Leerzeichen an
                    word += ' '
            arr.append(word)
    dictionary = {}
    for a in arr:
        dictionary[a] = 0
    #print(dictionary)
    return dictionary


def conceptgroup_to_partmatch(concept_group):
    """
        Wandelt die Liste der Begriffe eines Konzepts um in ein Dictionary. Jedes einzelne Wort
        der Konzeptphrasen wird als ein Key initialisiert mit dem Wert [0], wobei 0 der Counter
        für das Vorkommen des Wortes ist und die Indexe der Wortvorkommen im Text später an die
        Liste angehängt werden.

        Bsp.: concept_list = [['web', 'technologien'], ['web', 'design'], ...]
        dictionary = {'web': [0], 'technologien': [0], 'web': [0], 'design': [0], ...}
        """
    dictionary = {}
    for concept in concept_group:
        if len(concept) > 1:
            for i in range(len(concept)):
                dictionary[concept[i]] = [0]

    return dictionary


def concept_complete(a, b):
    """
        Diese Methode wird verwendet, um festzustellen, ob und wie oft zwei Teilbegriffe eines Konzepts
        im Text nahe beieinanderstehen, d.h. der Index der Wörter im Text sollte sich nur um +/-3 unterscheiden.
    """
    count = 0
    indices = []
    for x in a:
        for y in b:
            if abs(x - y) <= 3:     # berechnet den Betrag der beiden Werte
                count += 1
                indices.append(x)
                indices.append(y)
                del b[b.index(y)]   # der Indexwert y wird gelöscht, um diesen nicht erneut
                                    # zur Distanzberechnung zu verwenden
                break

    return indices


def concept_in_text(tokenlist, conceptgroup):  # Konzeptbegriffe als Parameter übergeben
    """
    Überprüft ob ein Konzeptwort im Text zu finden ist.
    Hierzu wird auch die Levenshtein-Distanz berechnet, um kleine Unterschiede zwischen den Strings abzufangen.
    Bei Mehrwort-Wörtern wird geprüft, ob die zusammengehörigen Wörter in entsprechender Reihenfolge im Text vorkommen
    mit einer erlaubten Distanz von 3?
    """

    counting = conceptgroup_to_dictionary(conceptgroup)  # in diesem Dictionary werden die Häufigkeiten der einzelnen Konzeptphrasen
                                                    # im gegebenen Text festgehalten

    dictionary = {}     # dient dem Mapping von der concept-Liste auf die Konzeptphrase von counting
    keys = list(counting.keys())
    """
        Hier wird ein Dictionary angelegt, dass das Mapping zwischen den Konzeptphrasen der Liste
        und dem Dictionary mit den einzeln konkatenierten Phrasenbestandteilen vornimmt. 
        So kann einfach die Liste in einen String überführt werden, der widerum den Key als Wert liefert 
        für das counting-Dictionary, in dem gezählt wird, wie oft eine Konzeptphrase im Text vorkommt.
    """
    for x in range(len(conceptgroup)):
        #print(str(x), keys[i])
        dictionary[str(conceptgroup[x])] = keys[x]

    part_match = conceptgroup_to_partmatch(conceptgroup)  # ein Dictionary für die einzelnen Begriffe und deren Vorkommen wird angelegt

    for word in tokenlist:
        for concept in conceptgroup:
            if len(concept) == 1:
                if compare_word_concept(concept[0], word) == 1:
                    counting[dictionary[str(concept)]] += 1
            elif len(concept) > 1:
                for part in concept:
                    if word in tokenlist:
                            if compare_word_concept(part, word) == 1:
                                part_match[part][0] += 1
                                indices = list(locate(tokenlist, lambda x: x == word))
                                for index in indices:
                                    if index not in part_match[part][1:]:
                                        part_match[part].append(index)

    #print(part_match)

    """
        Hier werden die Indizes der Teilbegriffe der Konzepte abgeglichen, um zu gucken, 
        ob diese im Text nah beieinanderstehen. Das Resultat (die Liste der matchenden 
        Indizes) wird für den weiteren Vergleich, bei mehr als 2 Term-langen Phrasen,
        verwendet. Schließlich wird die Häufigkeit der Vorkommen des Konzepts in counting
        aufaddiert, indem die Länge der Index-Liste durch 2 geteilt wird 
        (Es finden sich stets zwei matchende Indexe in der Liste pro 1 Vorkommen).
        
    """
    for concept in conceptgroup:
        if len(concept) > 1:
            a = part_match[concept[0]][1:]
            b = part_match[concept[1]][1:]
            indices = concept_complete(a, b)

            if len(concept) > 2:
                c = part_match[concept[2]][1:]
                indices = concept_complete(indices, c)

                if len(concept) > 3:
                    d = part_match[concept[3]][1:]
                    indices = concept_complete(indices, d)

                    if len(concept) > 4:
                        e = part_match[concept[4]][1:]
                        indices = concept_complete(indices, e)

            counting[dictionary[str(concept)]] += int((len(indices) / 2))

    return counting


"""
Konzeptzuordnung:

'0' = data mining
'1' = sprachdialogsysteme
'2' = maschinelles lernen
'3' = programmierung
'4' = markup
'5' = semantic web
'6' = computerlinguistik
'7' = softskills
'8' = korpuslinguistik
'9' = datenbank
'10' = digitalisierung
'11' = geisteswissenschaften
'12' = digital humanities
'13' = webdesign
'14' = digitale edition
'15' = langzeitarchivierung
"""


dictionary_concepts = {}


with open('Konzeptliste_CL_DH.json') as f:
    data = json.load(f)

print(data)

stopwords = read_text('stopwortliste.txt')
stopword_list = stopwords.split()

dir = ""
txt_files = join(dir, "TXT", "*.txt")
#print(txt_files)

for file in glob.glob(txt_files):
    base = os.path.basename(file)                   # trennt Basis vom Dateipfad ab
    id = str(os.path.splitext(base)[0])             # trennt Extension ab

    text = read_text(join(dir, "TXT", base))
    #print(text)
    tokens = tokenize(text)
    #print(tokens)

    token_list = [token for token in tokens if token not in stopword_list]

    print(token_list)

    key_dict = {}
    for key in data:
        key_dict[key] = concept_in_text(token_list, data[key])
    dictionary_concepts[id] = key_dict

    count = [0] * 16
    i = 0
    for cg in key_dict:
        for val in key_dict[cg].values():
            count[i] += val
        i += 1

    with open('frequency_for_later_ranking.csv', 'a') as csv_file:
        csv_file.write(id + ',')
        for j in range(16):
            csv_file.write(str(count[j]))
            if j < 15:
                csv_file.write(',')
            else:
                csv_file.write('\n')

    print(dictionary_concepts)


with open('frequency_counts.json', 'w') as json_file:
    json_file.write(json.dumps(dictionary_concepts))