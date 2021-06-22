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


from typing import List


def readData(line: str) -> float:
    """read data number from lines

    Args:
        line (str): every line containing data number

    Returns:
        float: data number
    """

    return float(line.split(">")[-1].strip())


def readProb(line: str) -> List[float]:
    """read probability numbers from lines

    Args:
        line (str): line containing probability numbers

    Returns:
        List[float]: probability numbers in list
    """

    return list(map(float, line.split(">")[-1].strip().split(" ")))

