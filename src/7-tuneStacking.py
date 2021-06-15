#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/15/2021
# Author: Hao Tian & Sian Xiao

"""
    Stacking, pos_neg_ratio is 5 with different seeds.
"""

import os


file_dir = "../analysis/stack.txt"
pos_neg_ratio = 5
stacking = 1


# prepare ../analysis/
if not os.path.isdir("../analysis/"):
    os.system("mkdir ../analysis/")


# clear results.txt
open(file_dir, "wb").close()


# use different random seeds
for seed in range(0, 100, 10):
    print(pos_neg_ratio, stacking, seed)
    os.system("python 5-autoML.py %d %d %d %s" %(pos_neg_ratio, stacking, seed, file_dir))

