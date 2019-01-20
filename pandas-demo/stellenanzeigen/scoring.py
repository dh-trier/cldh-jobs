#!/usr/bin/env python3

"""
Script for calculating scores for job advertisements
based on keyword classes and class weights. 
"""


# === Import statements ===

import os
from os.path import join
import glob
import pandas as pd
import numpy as np
from collections import Counter


# === Parameters ===

wdir = ""
adsfile = join(wdir, "jobs-and-concepts.csv")
weightsfile = join(wdir, "concept-weights.csv")
labelsfile = join(wdir, "labels.csv")

# === Functions ===


def read_csv(csvfile):
    """
    Takes as input a CSV file, returns it as a DataFrame.
    """
    with open(csvfile, "r", encoding="utf8") as infile: 
        dataframe = pd.read_csv(infile, sep=",", header=None)
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
    Uses the labels as column heads 
    and cleans up the dataframe a bit.
    """
    headings = list(["identifier"]) + (list(labels.loc[:,1]))
    ads.columns = headings
    ads = ads.set_index("identifier")
    ads = ads.replace({"(\[|\])":""}, regex=True)
    ads = ads.astype(int)
    #print(ads.head())
    # Save the raw weights into a clean CSV file. 
    save_dataframe(ads, "ads_raw.csv")
    return ads


def apply_bonus(ads): 
    """
    Input is the raw scores per add dataframe.
    Checks, for each ad, how many concepts classes are relevant. 
    Depending on the value, applies a weighting to all values.
    Outputs a dataframe with adjusted values.
    See: http://pandas.pydata.org/pandas-docs/version/0.23/groupby.html    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.mask.html    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.isna.html
    """
    # (1) Add a column with number of concepts used. 
    ads_masked = ads.mask(ads > 0)
    concept_counts = ads_masked.T.isnull().sum()
    concept_counts_dist = Counter(concept_counts)
    print("concept count distribution:\n", concept_counts_dist)
    #print(concept_counts)
    ads["concept_counts"] = concept_counts
    #print(ads.head())
    # (2) Depending on the count, apply a weighting to all values. 
    bonus_weights = {0:1, 1:1,2:1,3:1,4:2,5:2,6:2,7:1,8:1,9:1,10:1,11:1,12:1,13:1,14:1,15:1,16:1}
    ads = ads.groupby("concept_counts")
    newads = []
    for name, group in ads: 
        #print(name)
        weights = [bonus_weights[int(name)]]*16
        #print(weights)
        group = group.drop("concept_counts", axis="columns")
        group = group.mul(bonus_weights[int(name)], axis="rows")
        #print(group.head())
        newads.append(group)
    print(len(newads))
    newads = pd.concat(newads)
    print(newads.head())
    save_dataframe(newads, "ads_bonus.csv")
    return newads



def prepare_weights(weights, labels): 
    """
    Uses the labels as column heads 
    and cleans up the dataframe a bit.
    """
    headings = list(["category"]) + (list(labels.loc[:,1]))
    weights.columns = headings
    weights = weights.set_index("category")
    weights = weights.replace({"(\[|\]| )":""}, regex=True)
    weights["data-mining"] = weights["data-mining"].astype(float)
    weights["langzeitarchivierung"] = weights["langzeitarchivierung"].astype(float)
    weights = weights.T
    #print(weights.head())   
    return weights


def apply_weights(ads, category, weights): 
    """
    Multiply the columns by the weights.
    See: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.mul.html#pandas.DataFrame.mul
    """
    clweights = list(weights.loc[:,category])
    weighted = ads.mul(clweights, axis="columns")
    #print(weighted.head())
    return weighted


def combine_scores(weighted_cl, weighted_dh): 
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
    combined.columns = ["cl", "dh"]
    combined["diff"] = combined["dh"] - combined["cl"]
    combined.sort_values(by="diff", ascending=False, inplace=True)
    #print(combined.head())
    save_dataframe(combined, "ads_combined.csv")
    return combined


# === Coordinating function ===

def main(adsfile, weightsfile, labelsfile):
    """
    Coordinates the weighting scheme. 
    """
    # Read the labels file.
    labels = read_csv(labelsfile)
    # Read the ads file.
    ads = read_csv(adsfile)
    # Prepare the ads file. 
    ads = prepare_ads(ads, labels)
    # Add a bonus weight based on distribution
    ads = apply_bonus(ads)
    # Read the weights file.
    weights = read_csv(weightsfile)
    # Prepare the weights file.
    weights = prepare_weights(weights, labels)
    # Apply the CL weights to the raw scores.
    weighted_cl = apply_weights(ads, "gewichte_cl", weights)
    save_dataframe(weighted_cl, "ads_weighted_cl.csv")
    # Apply the DH weights to the raw scores.
    weighted_dh = apply_weights(ads, "gewichte_dh", weights)
    save_dataframe(weighted_dh, "ads_weighted_dh.csv")
    # Compress the individual scores into one value per job.
    combined = combine_scores(weighted_cl, weighted_dh)
    
main(adsfile, weightsfile, labelsfile)
