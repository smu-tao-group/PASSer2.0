#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/05/2021
# Author: Hao Tian & Sian Xiao

import os


# read ID and chain info for PDBs
pdbsTemp = open("../data/processedData/downloads.txt", "r").readlines()
pdbs = [line.strip() for line in pdbsTemp]

chainsTemp = open("../data/sourceData/ASD_chains.txt", "r").readlines()
chains = [line.strip() for line in chainsTemp]


# prepare or clean ../data/pockets/
if os.path.isdir("../data/pockets/"):
    os.system("rm -r ../data/pockets/*")
else:
    os.system("mkdir ../data/pockets/")


# find possible pockets
count = 0

for i in range(len(pdbs)):
    pdbID = pdbs[i]
    chain = chains[i]
    # run FPocket
    os.system("fpocket -f ../data/pdbs/%s.pdb -k %s" % (pdbID, chain))
    count += 1
    print(count)
    os.system("mv ../data/pdbs/%s_out ../data/pockets/" % pdbID)

