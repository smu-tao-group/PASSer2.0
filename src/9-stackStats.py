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


file_dir = "../analysis/stack.txt"
results = open(file_dir, "r").readlines()
infoLen = 11


stats = []  # List[List[float]]: val_f1, val_pre, val_rec, test_f1, test_pre, test_rec, prob1, prob2, prob3
for i in range(0, len(results), infoLen):
    temp = results[i, i+infoLen]
    val_f1 = readData(temp[1])
    val_precision = readData(temp[3])
    val_recall = readData(temp[4])
    test_f1 = readData(temp[5])
    test_precision = readData(temp[7])
    test_recall = readData(temp[8])
    probs = readProb(temp[9])
    stats.append([val_f1, val_precision, val_recall,
                  test_f1, test_precision, test_recall, *probs])


top_n = 10

print("validation results")
stats = sorted(stats, key=lambda x: -x[0])
stats = np.array(stats)
print(np.mean(stats[:top_n, :3], axis=0))
print(np.std(stats[:top_n, :3], axis=0))

top_n = 10

print("testing results")
stats = sorted(stats, key=lambda x: -x[3])
stats = np.array(stats)
print(np.mean(stats[:top_n, 3:6], axis=0))
print(np.std(stats[:top_n, 3:6], axis=0))

top_n = 10

print("validation results")
stats = sorted(stats, key=lambda x: -x[8])
stats = np.array(stats)
print(np.mean(stats[:top_n, 6:], axis=0))
print(np.std(stats[:top_n, 6:], axis=0))

