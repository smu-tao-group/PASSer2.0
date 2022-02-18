"""
Run this file as 'python 5-autoML.py {pos_neg_ratio} {stacking} {file_dir} {RANDOM_SEED} {time}'
"""

import pickle
import random
import sys
import warnings
import pandas as pd
import numpy as np
import autokeras as ak
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import utils.splitData_ak as splitData
import utils.top3 as top3


# turn off warnings
warnings.filterwarnings('ignore')


# load data
labels = pickle.load(open("./labels.pkl", "rb"))
features = pickle.load(open("./features.pkl", "rb"))


# read args
num_of_labels = int(sys.argv[1])
RANDOM_SEED = int(sys.argv[2])
file_dir = sys.argv[3] if len(sys.argv) >= 4 else None
MAX_TRAIL = int(sys.argv[4]) if len(sys.argv) >= 5 else 20
EPOCH = int(sys.argv[5]) if len(sys.argv) >= 6 else 20
THRESHOLD = float(sys.argv[6]) if len(sys.argv) >= 7 else 0.5


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
x_train, y_train = splitData.splitTrain(trainIndex, labels, features, num_of_labels)
x_val, y_val = splitData.splitTest(validIndex, labels, features)
x_test, y_test = splitData.splitTest(testIndex, labels, features)


# process the data for model training
train_data = np.concatenate((x_train, y_train.reshape(-1, 1)), axis=1)
valid_data = np.concatenate((x_val, y_val.reshape(-1, 1)), axis=1)
test_data = np.concatenate((x_test, y_test.reshape(-1, 1)), axis=1)

train_data = pd.DataFrame(train_data)
valid_data = pd.DataFrame(valid_data)
test_data = pd.DataFrame(test_data)

train_data.columns = [str(i) for i in range(1, 21)]
valid_data.columns = [str(i) for i in range(1, 21)]
test_data.columns = [str(i) for i in range(1, 21)]


# build model
reg = ak.StructuredDataRegressor(overwrite=True, max_trials=MAX_TRAIL, seed=RANDOM_SEED)
reg.fit(x_train, y_train, epochs=EPOCH)


# validation results
y_val_label = valid_data['20']
y_prob_val = reg.predict(x_val).reshape(-1,)
y_pred_val = (y_prob_val > THRESHOLD).astype(np.int)


# testing results
y_test_label = test_data['20']
y_prob_test = reg.predict(x_test).reshape(-1,)
y_pred_test = (y_prob_test > THRESHOLD).astype(np.int)


# metrics
perf_val = dict()
perf_val['f1'] = f1_score(y_true=y_val_label, y_pred=y_pred_val)
perf_val['accuracy'] = accuracy_score(y_true=y_val_label, y_pred=y_pred_val)
perf_val['precision'] = precision_score(y_true=y_val_label, y_pred=y_pred_val)
perf_val['recall'] = recall_score(y_true=y_val_label, y_pred=y_pred_val)

perf_test = dict()
perf_test['f1'] = f1_score(y_true=y_test_label, y_pred=y_pred_test)
perf_test['accuracy'] = accuracy_score(y_true=y_test_label, y_pred=y_pred_test)
perf_test['precision'] = precision_score(y_true=y_test_label, y_pred=y_pred_test)
perf_test['recall'] = recall_score(y_true=y_test_label, y_pred=y_pred_test)

probs = top3.top3_ak(y_prob_test, testIndex, labels)


# if no file dir is given, quit early
if not file_dir:
    quit()


# write to results
results = open(file_dir, "a")

# head
results.write(str(num_of_labels) + " ")
results.write(str(RANDOM_SEED) + " ")
results.write(str(EPOCH) + "\n")


# write validation results
metrics = ['f1', 'accuracy', 'precision', 'recall']

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