#!/usr/bin/env python3

"""
Script for getting plain text from PDF files.
See: https://textract.readthedocs.io/en/stable/index.html
"""

"""
Installation (on Ubuntu, for Python3): 
(1) Install required packages: apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libasound-dev libpulse-dev
(2) pip3 install pocketsphinx
(3) pip3 install textract
"""


# === Import statements ===

import os
import glob
import textract


# === Parameters ===

pdfs = os.path.join("pdf", "*.pdf")
txts = "txt"


# === Functions ===


def read_pdf(pdf):
    """
    Takes as input a PDF file, outputs a string object.
    Also, outputs the filename.
    """
    filename,ext = os.path.basename(pdf).split(".")
    text = textract.process(pdf, encoding="utf8").decode("utf8")
    return text, filename


def save_text(text, filename, txts): 
    """
    Saves the string to a file with the same filename as the input file.
    """
    with open(os.path.join(txts, filename + ".txt"), "w", encoding="utf8") as outfile: 
        outfile.write(text)


# === Coordinating function ===

def main(pdfs, txts):
    """
    Coordinates the PDF to TXT conversion for all files contained in the
    folder indicated in "pdfs". 
    Creates the output folder indicated in "txts", if necessary, 
    and saves all text files into that folder.
    """
    if not os.path.exists(txts): 
        os.makedirs(txts)
    for pdf in glob.glob(pdfs): 
        text, filename = read_pdf(pdf)
        save_text(text, filename, txts)
    
main(pdfs, txts)
