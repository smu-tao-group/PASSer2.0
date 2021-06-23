#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 06/14/2021
# Author: Hao Tian & Sian Xiao

"""
    Run this file as 'python 5-autoML.py {pos_neg_ratio} {stacking} {file_dir} {RANDOM_SEED} {time}'
"""

import pickle
import random
import sys
import warnings

import numpy as np
from autogluon.tabular import TabularDataset, TabularPredictor

import utils.splitData as splitData
import utils.top3 as top3


# turn off warnings
warnings.filterwarnings('ignore')


# load data
labels = pickle.load(open("../data/classification/labels.pkl", "rb"))
features = pickle.load(open("../data/classification/features.pkl", "rb"))


# read args
pos_neg_ratio = int(sys.argv[1])
stacking = bool(int(sys.argv[2]))
RANDOM_SEED = int(sys.argv[3])
file_dir = sys.argv[4] if len(sys.argv) >= 5 else None
time = int(sys.argv[5]) if len(sys.argv) >= 6 else 2


# random shuffle PDBs
index = [i for i in range(len(labels))]
random.seed(RANDOM_SEED)
random.shuffle(index)


# train: validate: test = 0.6: 0.2: 0.2
TRAINRATIO = 0.6
TRAINSIZE = int(len(index) * TRAINRATIO)
VALIDRATIO = 0.2
VALIDSIZE = int(len(index) * VALIDRATIO)
TESTRATIO = 0.2
TESTSIZE = len(index) - TRAINSIZE - VALIDSIZE

trainIndex = index[:TRAINSIZE]
validIndex = index[TRAINSIZE:(TRAINSIZE + VALIDSIZE)]
testIndex = index[(TRAINSIZE + VALIDSIZE):]


# split data as needed
if pos_neg_ratio <= 20:
    # ? use part of the data
    x_train, y_train = splitData.splitTrain(
        trainIndex, labels, features, pos_neg_ratio, RANDOM_SEED)
else:
    # ? use full size
    x_train, y_train = splitData.splitTest(trainIndex, labels, features)

x_val, y_val = splitData.splitTest(validIndex, labels, features)
x_test, y_test = splitData.splitTest(testIndex, labels, features)


# process the data for model training
train_data = np.concatenate((x_train, y_train.reshape(-1, 1)), axis=1)
valid_data = np.concatenate((x_val, y_val.reshape(-1, 1)), axis=1)
test_data = np.concatenate((x_test, y_test.reshape(-1, 1)), axis=1)

train_data = TabularDataset(train_data)
valid_data = TabularDataset(valid_data)
test_data = TabularDataset(test_data)

train_data.columns = [str(i) for i in range(1, 21)]
valid_data.columns = [str(i) for i in range(1, 21)]
test_data.columns = [str(i) for i in range(1, 21)]


# fit models
if not stacking:
    predictor = TabularPredictor(label="20", eval_metric='accuracy').fit(
        train_data, time_limit=60*time, tuning_data=valid_data
    )
else:
    predictor = TabularPredictor(label="20", eval_metric='accuracy').fit(
        train_data, time_limit=60*time, auto_stack=True
    )

# individual models performance
#leaderboard = predictor.leaderboard(test_data)


# validation results
y_val_label = valid_data['20']
y_val_nolab = valid_data.drop(columns=['20'])

y_pred_val = predictor.predict(y_val_nolab)
perf_val = predictor.evaluate_predictions(
    y_true=y_val_label, y_pred=y_pred_val, auxiliary_metrics=True)


# testing results
y_test_label = test_data['20']
y_test_nolab = test_data.drop(columns=['20'])

y_pred_test = predictor.predict(y_test_nolab)
perf_test = predictor.evaluate_predictions(
    y_true=y_test_label, y_pred=y_pred_test, auxiliary_metrics=True)


# calculate top 3 probabilities
y_pred_probs = predictor.predict_proba(y_test_nolab).to_numpy()
y_pred_probs = y_pred_probs[:, 1].reshape(-1, 1)

probs = top3.top3(y_pred_probs, testIndex, labels)


# if no file dir is given, quit early
if not file_dir:
    quit()


# write to results
results = open(file_dir, "a")

# head
results.write(str(pos_neg_ratio) + " ")
results.write(str(stacking) + " ")
results.write(str(RANDOM_SEED) + " ")
results.write(str(time) + "\n")

metrics = ['f1', 'accuracy', 'precision', 'recall']

# write validation results
for key in metrics:
    val = perf_val[key]
    results.write(str(key) + ' > ' + str(val) + '\n')

# write testing results
for key in metrics:
    val = perf_test[key]
    results.write(str(key) + ' > ' + str(val) + '\n')

results.write("probs > %.3f %.3f %.3f\n" % probs)
results.write("\n")
results.close()
