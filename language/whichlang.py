#!/usr/bin/env python3

"""
Script for recognizing the language of a text.
"""


# === Import statements ===

import os
import re
from os.path import join
import glob

from langdetect import detect
from polyglot.text import Text


# === Parameters ===

wdir = ""
test1 = "Das hier ist ein typischer Satz, finde ich." 
test2 = "This is a typical sentence, isn't it."
textpath = join(wdir, "txt", "*.txt") 


# === Functions ===

def test_detection(test1, test2): 
    ld = detect(test1) 
    print("langdetect", ld) 
    ld = detect(test2) 
    print("langdetect", ld) 
    text = Text(test1)
    pg = text.language.code  
    print("polyglot", pg) 
    text = Text(test2)
    pg = text.language.code  
    print("polyglot", pg) 


def read_file(textfile): 
    with open(textfile, "r", encoding="utf8") as infile: 
        text = infile.read()
    return text
    

def use_langdetect(text):
    plang = detect(text)
    return plang 


def use_polyglot(text):
    text = Text(text)
    plang = text.language.code  
    return plang 


def evaluate_detection(tlang, plang, correct, total):
    print(tlang, "---", plang)
    total += 1
    if plang == tlang: 
        correct +=1
    return correct, total


def main(test1, test2, textpath): 
    #test_detection(test1, test2)
    correct = 0
    total = 0
    print("true vs. predicted")
    for textfile in glob.glob(textpath):
        filename,ext = os.path.basename(textfile).split(".")
        #print(filename)
        tlang,identifier = re.split("=", filename)
        text = read_file(textfile) 
        plang = use_langdetect(text) # activate only one
        plang = use_polyglot(text)   # activate only one
        correct, total = evaluate_detection(tlang, plang, correct, total)
    performance = correct/total*100
    print("performance:", performance)
    
main(test1, test2, textpath)
