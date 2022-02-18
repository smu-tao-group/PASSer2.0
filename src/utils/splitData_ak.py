"""
The originally high dimensional data based on PDB ID will be flattened to pockets.
"""

from typing import List, Tuple
import numpy as np


def splitTrain(Indexes: list, labels: List[List[int]], features: List[List[List[float]]], NUM: float) -> Tuple[np.ndarray, np.ndarray]:
    """split training data given POS_NEG_NUM and RANDOM_SEED
    Args:
        Indexes (list): indices of training data
        labels (List[List[int]]): labels of 1 or 0
        features (List[List[List[float]]]): features collected
        NUM (float): number of first n pockets used
    Returns:
        Tuple[np.ndarray, np.ndarray]: tuple of training data
    """

    x_train = []
    y_train = []

    for index in Indexes:
        # each protein with size of its pockets
        label: list = labels[index]
        feature = features[index]

        n = label.index(1) # find positive
        if n < NUM: # postive in first NUM pockets
            y_train.extend(label[:NUM])
            x_train.extend(feature[:NUM])
        else:
            y_train.append(1)
            x_train.append(feature[n])
            y_train.extend(label[:NUM-1])
            x_train.extend(feature[:NUM-1])

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