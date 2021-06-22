#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/22/2021
# Author: Sian Xiao & Hao Tian

"""
Every single data point (11 lines):
    1 False 0
    f1 > 0.5230769230769231
    accuracy > 0.9362139917695473
    precision > 0.425
    recall > 0.68
    f1 > 0.5538461538461538
    accuracy > 0.9409368635437881
    precision > 0.47368421052631576
    recall > 0.6666666666666666
    probs > 44.444 74.074 74.074

"""

import numpy as np

from utils.stats import readData, readProb


file_dir = "../analysis/ratio.txt"
results = open(file_dir, "r").readlines()
infoLen = 11
ratios = 11  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]
seeds = 10  # seed in range(0, 100, 10)
single = len(results) // ratios


stats = []  # List[List[List[float]]]: val_f1, val_pre, val_rec, test_f1, test_pre, test_rec, prob1, prob2, prob3
for ratio in range(ratios):
    cur = []
    for seed in range(seeds):
        temp = results[ratio*single + seed *
                       infoLen: ratio*single + (seed+1)*infoLen]
        val_f1 = readData(temp[1])
        val_precision = readData(temp[3])
        val_recall = readData(temp[4])
        test_f1 = readData(temp[5])
        test_precision = readData(temp[7])
        test_recall = readData(temp[8])
        probs = readProb(temp[9])
        cur.append([val_f1, val_precision, val_recall,
                    test_f1, test_precision, test_recall, *probs])
    stats.append(cur)
stats = np.array(stats)


# print results
print("validation results in f1, precision and recall")
for index in [0, 1, 2]:
    mean = np.mean(stats[:, :, index], axis=1)
    std = np.std(stats[:, :, index], axis=1)
    print(mean)
    print(std)

ratio = 5  # notice ratio 5 is the best
ind = 4 # index of ratio 5
print('testing results')
for index in [3, 4, 5]:
    mean = np.mean(stats[ind, :, index], axis=0)
    std = np.std(stats[ind, :, index], axis=0)
    print(mean)
    print(std)

print("top3 probs")
for index in [6, 7, 8]:
    mean = np.mean(stats[ind, :, index], axis=0)
    std = np.std(stats[ind, :, index], axis=0)
    print(mean)
    print(std)

