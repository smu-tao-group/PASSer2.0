# -*- coding: utf-8 -*-
# 06/04/2021
# Author: Hao Tian & Sian Xiao


import requests
import os


# read pdbs that need to download
with open("../data/processedData/downloads.txt", 'r') as fh:
    pdbs = fh.readlines()
    pdbs = [line.strip() for line in pdbs]


# prepare or clean ../data/pdbs/
if os.path.isdir("../data/pdbs/"):
    os.system("rm -r ../data/pdbs/*")
else:
    os.system("mkdir ../data/pdbs/")


# download pdb
for pdbID in pdbs:
    rcsb = "https://files.rcsb.org/download/"
    url = rcsb + pdbID + ".pdb"
    r = requests.get(url)
    open("../data/pdbs/%s.pdb" % pdbID, "wb").write(r.content)
