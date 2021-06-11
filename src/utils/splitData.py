#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/09/2021
# Author: Sian Xiao & Hao Tian

"""
The originally high dimensional data based on PDB ID will be flattened to pockets.
"""

import random
from typing import List, Tuple
import numpy as np


def splitTrain(Indexes: list, labels: List[List[int]], features: List[List[List[float]]], POS_NEG_RATIO: float, RANDOM_SEED: int) -> Tuple[np.ndarray, np.ndarray]:
    """split training data given POS_NEG_RATIO and RANDOM_SEED

    Args:
        Indexes (list): indices of training data
        labels (List[List[int]]): labels of 1 or 0
        features (List[List[List[float]]]): features collected
        POS_NEG_RATIO (float): ratio of positive and negative labels
        RANDOM_SEED (int): random seed for shuffle

    Returns:
        Tuple[np.ndarray, np.ndarray]: tuple of training data
    """

    x_train = []
    y_train = []

    for index in Indexes:
        # each protein with size of its pockets
        label: list = labels[index]

        # first find the positive label and cooresponding feature
        positiveLabelIndex = [ind for ind, lbl in enumerate(label) if lbl]
        for posIndex in positiveLabelIndex:
            x_train.append(features[index][posIndex])
            y_train.append(1)

        # randomly select features and labels from other negative points
        negativeLabelIndex = [ind for ind, lbl in enumerate(label) if not lbl]
        random.seed(RANDOM_SEED)
        random.shuffle(negativeLabelIndex)
        for negIndex in negativeLabelIndex[:POS_NEG_RATIO * len(positiveLabelIndex)]:
            x_train.append(features[index][negIndex])
            y_train.append(0)

        assert len(x_train) == len(y_train)

    return np.array(x_train), np.array(y_train)


def splitTest(Indexes: list, labels: List[List[int]], features: List[List[List[float]]]) -> Tuple[np.ndarray, np.ndarray]:
    """split test data

    Args:
        Indexes (list): indices of test data
        labels (List[List[int]]): labels of 1 or 0
        features (List[List[List[float]]]): features collected

    Returns:
        Tuple[np.ndarray, np.ndarray]: tuple of test data
    """

    x_test = []
    y_test = []

    for index in Indexes:
        curLabel = labels[index]
        curFeature = features[index]
        x_test.extend(curFeature)
        y_test.extend(curLabel)

    return np.array(x_test), np.array(y_test)

