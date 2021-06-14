#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/14/2021
# Author: Hao Tian & Sian Xiao

"""
    No stacking, tuning ratio with different seeds.
"""

import os


file_dir = "../analysis/ratio.txt"
pos_neg_ratio = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20]


# prepare ../analysis/
if not os.path.isdir("../analysis/"):
    os.system("mkdir ../analysis/")


# clear results.txt
open(file_dir, "wb").close()


for ratio in pos_neg_ratio:
    # not set stacking
    stacking = 0
    # use different random seeds
    for seed in range(0, 100, 10):
        print(ratio, stacking, seed)
        os.system("python 5-autoML.py %d %d %d %s" %(ratio, stacking, seed, file_dir))

