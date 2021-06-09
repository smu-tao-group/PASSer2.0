#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/08/2021
# Author: Hao Tian & Sian Xiao

import glob
import os
import pickle
import warnings

from utils.atomCount import atomCount
from utils.extractFeature import extractPocket


# read allosteric info and PDB list
alloInfo = open("../data/processedData/alloInfoClean.txt", 'r').readlines()
pdbsTemp = open("../data/processedData/downloads.txt", 'r').readlines()
pdbs = [line.strip() for line in pdbsTemp]


# label pockets with 1 or 0
# size = num of proteins
# size of each element = num of pockets in each protein
labels = []  # List[List[int]]

# FPocket features
# size = num of proteins
# size of each element = num of pockets in each protein * 19 features
features = []  # List[List[List[float]]]

# at least need 9 heavy atoms to be labeled as 1
# ref: mean value of heavy atoms in 20 amino acids = 9
n_atoms = 9


for i in range(len(pdbs)):
    pdb = pdbs[i]
    info = alloInfo[i]

    # all pocket names and sorted from first to last
    direction_pockets = "../data/pockets/%s_out/pockets/" % pdb
    fileNames = glob.glob(direction_pockets + "*.pdb")
    fileNames.sort(key=lambda x: int(x.split("pocket")[-1].split("_")[0]))

    counts = []
    for j in range(len(fileNames)):
        pocket = fileNames[j]
        counts.append(atomCount(pocket, info))

    # report if no pockets
    if len(counts) < 1:
        warnings.warn("no pocket detected in %s" % pdb)
        continue

    # report if no positive label
    if max(counts) < n_atoms:
        warnings.warn("no positive labels in %s" % pdb)
        continue

    cur_label = [1 if item >= n_atoms else 0 for item in counts]
    labels.append(cur_label)

    # collect FPocket features
    features_collections = "../data/pockets/%s_out/%s_info.txt" % (pdb, pdb)
    cur_feature = extractPocket(features_collections)
    features.append(cur_feature)

assert len(labels) == len(features)


# statistics
# num of proteins * num of pockets in each protein
total_labels = sum([len(item) for item in labels])
# num of label 1
positive_labels = sum([sum(item) for item in labels])
print("total of %d pockets, with %d positive labels accounting for %.2f%%"
      % (total_labels, positive_labels, positive_labels / total_labels * 100))


# prepare or clean ../data/classification/
if os.path.isdir("../data/classification/"):
    os.system("rm -r ../data/classification/*")
else:
    os.system("mkdir ../data/classification/")


# save labels and features
pickle.dump(labels, open("../data/classification/labels.pkl", "wb"))
pickle.dump(features, open("../data/classification/features.pkl", "wb"))

