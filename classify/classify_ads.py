#!/usr/bin/env python3

"""
Script for classifying job advertisements into target group categories.
Here, Computerlinguistik vs. Digital Humanities.

- For every ad, loads the distribution of concept area word counts.
- Then, loads the concept area weights by field (CL vs. DH)
- For every ad, multiplies the concept area counts with the weights; sums up the score.
- Looks at the distribution of scores for all ads.
- Classifies each ad into CL, DH, CL+DH, or neither.
"""


# === Import statements ===

import os
from os.path import join
import glob
import pandas as pd
import numpy as np


# === Parameters ===

datadir = join("/", "home", "christof", "Seafile", "DH-Lehre", "Projektseminar_Winter18", "Ergebnisse_und_Tabellen", "Ranking", "")
frequenciesfile = join(datadir, "frequency_for_later_ranking.csv")
weightsfile = join(datadir, "concept-weights.csv")
labelsfile = join(datadir, "Mapping_Konzepte.csv")
scoredadsfile = join(datadir, "ads_with_scores.csv")


# === Functions ===


def read_csv(csvfile):
    """
    Takes as input a CSV file, returns it as a DataFrame.
    """
    with open(csvfile, "r", encoding="utf8") as infile: 
        dataframe = pd.read_csv(infile, sep=",", index_col=0)
        #print(dataframe.head())
    return dataframe



def save_dataframe(dataframe, filename):
    """
    Takes a DataFrame and saves it as a CSV file.
    """
    with open(filename, "w", encoding="utf8") as outfile: 
        dataframe.to_csv(outfile, sep=",")


def prepare_ads(ads, labels): 
    """
    Uses the labels as column heads.
    """
    ads.columns = list(labels.loc[:,"label"])
    #print(ads.head())
    return ads


def prepare_weights(weights):
    """
    """
    clw = weights.loc[:,"Computerlinguistik"]
    dhw = weights.loc[:,"Digital Humanities"]
    weights = [clw, dhw]
    return weights


def apply_weights(ads, category, weights): 
    """
    Multiply the columns by the weights.
    See: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.mul.html#pandas.DataFrame.mul
    """
    weighted = ads.mul(weights, axis="columns")
    #print(weighted.head())
    return weighted
  


def combine_scores(weighted_cl, weighted_dh, scoredadsfile): 
    """
    Combine all individual concept scores into one score
    for each job advertisement, and combine the scores
    of CL and DH into one DataFrame. 
    Also, calculate the difference between the scores for
    CL and DH and sort the table by that difference.
    """
    combined_cl = np.sum(weighted_cl, axis="columns")
    combined_dh = np.sum(weighted_dh, axis="columns")
    combined = pd.concat([combined_cl, combined_dh], axis=1)
    combined.columns = ["score-cl", "score-dh"]
    # Add a column with the difference between the two scores
    combined["diff"] = combined["score-dh"] - combined["score-cl"]
    combined.sort_values(by="diff", ascending=False, inplace=True)
    # Add columns for whether the ad is relevant to dh and/or cl, depending on value of diff
    combined["label-cl"] = combined["diff"]
    combined.loc[combined["diff"] > 1, "label-cl"] = 0
    combined.loc[combined["diff"] <= 1, "label-cl"] = 1
    combined["label-dh"] = combined["diff"]
    combined.loc[combined["diff"] > -1, "label-dh"] = 1
    combined.loc[combined["diff"] <= -1, "label-dh"] = 0
    print(combined.head())
    save_dataframe(combined, scoredadsfile)
    return combined


# === Coordinating function ===

def main(frequenciesfile, weightsfile, labelsfile, scoredadsfile):
    """
    Coordinates the weighting scheme. 
    """
    # Read the labels file.
    labels = read_csv(labelsfile)
    # Read the ads file.
    ads = read_csv(frequenciesfile)
    # Prepare the ads file. 
    ads = prepare_ads(ads, labels)
    # Read the weights file.
    weights = read_csv(weightsfile)
    # Prepare the weights file.
    weights = prepare_weights(weights)
    # Apply the CL weights to the raw scores.
    weighted_cl = apply_weights(ads, "gewichte_cl", weights[0])
    # Apply the DH weights to the raw scores.
    weighted_dh = apply_weights(ads, "gewichte_dh", weights[1])
    # Compress the individual scores into one value per job.
    combined = combine_scores(weighted_cl, weighted_dh, scoredadsfile)
    
main(frequenciesfile, weightsfile, labelsfile, scoredadsfile)
