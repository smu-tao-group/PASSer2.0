#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/08/2021
# Author: Hao Tian & Sian Xiao

import warnings


def extractPocket(fileDirection: str) -> list:
    """extract pocket features calculated by FPocket

    Args:
        fileDirection (str): file location '../data/pockets/{pdb}_out/{pdb}_info.txt'

    Returns:
        list: features of each pocket for a certain PDB, size is number of pockets, size of each element is 19 (number of feature)
    """

    pocket = open(fileDirection + "", "r").readlines()
    pocket_num = len(pocket) // 21

    # collection of features of all pockets
    features = []

    for index in range(pocket_num):
        # feature for current pocket
        cur_feature = []
        cur = pocket[index * 21: (index + 1) * 21]
        for line in cur[1:-1]:
            cur_feature.append(float(line.split("\t")[2][:-1]))
        if len(cur_feature) == 18:
            warnings.warn("potential error in features of %s" % fileDirection)
        features.append(cur_feature)

    return features
