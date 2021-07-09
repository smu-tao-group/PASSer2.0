#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/25/2021
# Author: Hao Tian & Sian Xiao

import numpy as np


file_dir = "../analysis/feature.txt"
results = open(file_dir, "r").readlines()
featureNum = 19


importances = []
for i in range(0, len(results), featureNum+1):
    cur = []
    for j in range(featureNum):
        cur.append(float(results[i + j].strip().split(" ")[-1]))
    importances.append(cur)

importances = np.array(importances)

mean = np.mean(importances, axis = 0)
std = np.std(importances, axis = 0)

'''
mean = [ 0.00416667,  0.00016667, -0.00116667,  0.02016667,  0.005     ,
        0.0165    ,  0.0235    , -0.00033333,  0.00483333,  0.00166667,
        0.00166667,  0.003     ,  0.00183333, -0.0035    ,  0.0005    ,
        0.00183333, -0.0025    , -0.0005    ,  0.00116667]

std = [0.00421966, 0.00376017, 0.00291071, 0.01077678, 0.00506623,
       0.00704154, 0.04247254, 0.00235702, 0.00296742, 0.00213437,
       0.00221108, 0.0033665 , 0.00211476, 0.00556028, 0.00160728,
       0.00146249, 0.00489047, 0.00340343, 0.00285287]
'''

print(mean)
print(std)