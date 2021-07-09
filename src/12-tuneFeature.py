#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/25/2021
# Author: Hao Tian & Sian Xiao

import os


pos_neg_ratio = 5
stacking = 1
time = 4
file_dir = "../analysis/feature.txt"


# prepare ../analysis/
if not os.path.isdir("../analysis/"):
    os.system("mkdir ../analysis/")


# clear results.txt
open(file_dir, "wb").close()


# use different random seeds
for seed in [15, 61, 80, 87, 97]:
    print(pos_neg_ratio, stacking, seed)
    os.system("python 11-feature.py %d %d %d %s %s" %(pos_neg_ratio, stacking, seed, file_dir, time))

