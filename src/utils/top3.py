#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/12/2021
# Author: Sian Xiao & Hao Tian

from typing import List, Tuple
import numpy as np


def top3(y_pred_probs: np.ndarray, testIndex: list, labels: List[List[int]]) -> Tuple[float, float, float]:
    """calculate probabilities that correct pocket is within top 1 or 2 or 3

    Args:
        y_pred_probs (np.ndarray): predicted probabilities
        testIndex (list): indices of test data
        labels (List[List[int]]): labels of 1 or 0

    Returns:
        Tuple[float, float, float]: probabilities that a positive label was predicted as top 1 or 2 or 3
    """

    pass
    startIndex, endIndex = 0, 0
    ans = []

    for index in testIndex:
        curLabels = labels[index]
        numPockets = len(labels[index])
        endIndex += numPockets
        curProb = y_pred_probs[startIndex:endIndex]
        preOrder = [[i] for i in range(numPockets)]
        # np.shape(curProb) = (-1,2), in descending order
        curRank = sorted(np.hstack((curProb, preOrder)), key=lambda x: -x[0])

        for i in range(numPockets):
            if curLabels[i] == 1:
                for j in range(len(curRank)):
                    if curRank[j][-1] == i:
                        ans.append(j + 1)
        startIndex += numPockets

    one = ans.count(1)
    two = ans.count(2)
    three = ans.count(3)

    posLabel = len(ans)
    oneProb = one / posLabel * 100
    twoProb = (one + two) / posLabel * 100
    threeProb = (one + two + three) / posLabel * 100

    return oneProb, twoProb, threeProb
