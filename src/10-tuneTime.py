#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/22/2021
# Author: Hao Tian & Sian Xiao

"""
    Stacking, pos_neg_ratio is 5. Tuning time with different seeds.
"""

import os


file_dir = "../analysis/time.txt"
pos_neg_ratio = 5
stacking = 1


# prepare ../analysis/
if not os.path.isdir("../analysis/"):
    os.system("mkdir ../analysis/")


# clear results.txt
open(file_dir, "wb").close()


for time in range(1, 11):
    for seed in [0, 5, 10, 15]:
        print(pos_neg_ratio, stacking, seed, time)
        os.system("python 5-autoML.py %d %d %d %s %d" %(pos_neg_ratio, stacking, seed, file_dir, time))

