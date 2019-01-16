#!/usr/bin/env python3

"""
Script for counting words using pandas.
Takes a collection of text files as input. 
Produces word count statistics for all texts. 
"""


# === Import statements ===

import os
import re
from os.path import join
import glob
import pandas as pd
import numpy as np
from collections import Counter


# === Parameters ===

wdir = ""
txtfiles = join(wdir, "txt", "*.txt")
countsfile = join(wdir, "word-counts.csv")

# === Functions ===

def save_dataframe(dataframe, filename):
    """
    Takes a DataFrame and saves it as a CSV file.
    """
    with open(filename, "w", encoding="utf8") as outfile: 
        dataframe.to_csv(outfile, sep=",")


def read_txt(txtfile):
    """
    Takes as input a TXT file.
    Returns it as a string.
    """
    with open(txtfile, "r", encoding="utf8") as infile: 
        text = infile.read()
    #print(text[0:100])
    return text


def tokenize_text(text):
    """    
    Takes as input the raw string text. 
    Performs some cleaning and tokenization.
    Returns a list of tokens.
    """
    text = re.sub("_", "", text)
    text = text.lower()
    tokens = re.split("\W+", text)
    tokens = [t for t in tokens if t]
    #print(tokens[0:10])
    return tokens


def count_tokens(tokens, filename): 
    """
    Input is a list of tokens.
    Counts how many time each type appears in the text.
    Output is a series with counts.
    """
    wordcounts = Counter(tokens)
    #print(wordcounts)
    wordcounts = pd.Series(wordcounts, name=filename)
    #print(wordcounts.head())
    return wordcounts


def create_dataframe(allcounts): 
    """
    Input is a dictionary. 
    Output is a dataframe. 
    (Also saves the dataframe to CSV.)
    """
    allcounts = pd.DataFrame(allcounts)
    allcounts = allcounts.fillna(0)
    save_dataframe(allcounts, "0-absolute.csv")
    return allcounts



def relative_freqs(allcounts): 
    """
    Input is a dataframe of absolute word counts. 
    Calculates the length of each text
    and divides all counts by the length of the corresponding text.
    Output is a dataframe of relative word frequencies.
    """
    #print(allcounts.head())
    lengths = np.sum(allcounts, axis="index")
    #print(lengths)
    relfreqs = allcounts.div(lengths, axis="columns").mul(100)
    #print(relfreqs.head())
    save_dataframe(relfreqs, "1-relfreqs.csv")
    return relfreqs


def descriptive_statistics(relfreqs): 
    """
    Input is a dataframe of relative word frequencies. 
    Calculates the mean frequency of each word in the texts. 
    Calculates the standard deviation of each word across texts.
    Adds them to the dataframe.
    """ 
    relfreqs["mean"] = np.mean(relfreqs, axis="columns")
    #print(relfreqs.loc[:,"mean"])
    relfreqs["stdev"] = np.std(relfreqs, axis="columns")
    #print(relfreqs.loc[:,"stdev"])
    relfreqs = relfreqs.sort_values(by="mean", ascending=False)
    #print(relfreqs.head())
    return relfreqs


def make_zscores(relfreqs): 
    """
    Input is dataframe of relative word frequencies with mean and stdev.
    Output is a dataframe of zscores. 
    """
    means = relfreqs.loc[:,"mean"]
    stdevs = relfreqs.loc[:,"stdev"]
    relfreqs = relfreqs.drop(["mean", "stdev"], axis="columns")
    #print(means.head())
    #print(stdevs.head())
    #print(relfreqs.head())
    normalized = relfreqs.sub(means, axis="index")
    save_dataframe(normalized, "2-normalized.csv")
    #print(normalized.head())
    zscores = normalized.div(stdevs, axis="index")
    save_dataframe(zscores, "3-zscores.csv")
    #print(zscores.head())
    return zscores



# === Coordinating function ===

def main(txtfiles, countsfile):
    """
    Coordinates the word counting script.
    """
    allcounts = {}
    for txtfile in glob.glob(txtfiles):
        filename,ext = os.path.basename(txtfile).split(".")
        print(filename)
        text = read_txt(txtfile)
        tokens = tokenize_text(text)
        counts = count_tokens(tokens, filename)
        allcounts[filename] = counts
    allcounts = create_dataframe(allcounts)
    relfreqs = relative_freqs(allcounts)
    relfreqs = descriptive_statistics(relfreqs)
    zscores = make_zscores(relfreqs)

main(txtfiles, countsfile)
