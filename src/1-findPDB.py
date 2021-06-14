#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/13/2021
# Author: Hao Tian & Sian Xiao

import os


# info from original allosteric database (ASD)
with open("../data/sourceData/ASD_Release_201909_AS.txt", 'r') as fh:
    alloInfoOri = fh.readlines()
    alloInfo = [line.split("\t") for line in alloInfoOri]
    allPDBs = [line[4] for line in alloInfo[1:]]


# read 90 pdbs picked
with open("../data/sourceData/pdbs.txt", 'r') as fh:
    pdbs = fh.readlines()
    pdbs = [line.strip() for line in pdbs]
    assert len(pdbs) == 90


# check if PDBs missed in original files
downloads = []
alloInfoClean = []
count = 0

for pdb in pdbs:
    if pdb not in allPDBs:
        count += 1
    else:
        index = allPDBs.index(pdb)
        ''' 1Z8D and 1CE8 should pair with the
            modulator on the next line
            according to reference'''
        if pdb == "1Z8D" or pdb == "1CE8":
            index += 1
        alloInfoClean.append(alloInfoOri[index + 1])  # one for headline
        downloads.append(pdb)

print("total of %d missing" % count)


# prepare ../data/processedData/
if not os.path.isdir("../data/processedData/"):
    os.system("mkdir ../data/processedData")

# copy pdbIDs to downloads.txt
with open("../data/processedData/downloads.txt", 'w') as fh:
    length = len(downloads)
    for i, pdb in enumerate(downloads):
        fh.write(pdb) if i == length - 1 else fh.write(pdb + '\n')

# create clean version of alloInfo
with open("../data/processedData/alloInfoClean.txt", 'w') as fh:
    for info in alloInfoClean:
        fh.write(info)

