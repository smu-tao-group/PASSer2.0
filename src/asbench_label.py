
import pandas as pd 
import glob
import os
import math
import numpy as np
import pickle
from extract_feature import extractPocket


file = './ASBench_Core_Diversity_Set/ASBench_Core_Diversity_Set.xls'
df = pd.read_excel(file)

chainID = df['Chain ID']
resID = df['Residue ID (PDB)']
pdbID = df['PDB ID'].to_list()
missing = 0

fileNames = glob.glob("./ASBench_Core_Diversity_Set/protein-modulator_complexes/*.pdb")
fileNames = sorted(fileNames)
minimum_dists = []
minimum_idxs = []

duplicate = set()

################
labels = []
features = []
#################

for i in range(len(fileNames)):
    #os.system("fpocket -f %s -k %s" %(fileNames[i], chainID[i]))
    while fileNames[i][-16:-12] != pdbID[0]:
        missing += 1
        pdbID.pop(0)
    pdbID.pop(0)
    if fileNames[i][-16:-12] in duplicate:
        continue
    duplicate.add(fileNames[i][-16:-12])
    protein = open(fileNames[i], "r").readlines()
    # ligand center of mass
    xs, ys, zs, cnt = 0, 0, 0, 0
    for line in protein:
        if line[:6] == "HETATM" and line[21] == chainID[i] and int(line[22:26]) == int(resID[i]):
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            xs += x
            ys += y
            zs += z
            cnt += 1
    xs /= cnt
    ys /= cnt
    zs /= cnt
    # find pocket
    pocket_dir = fileNames[i][:-4] + "_out/pockets/"
    pocket_names = glob.glob(pocket_dir + "*.pdb")
    pocket_names = sorted(pocket_names, key = \
        lambda x : int(x.split("pocket")[-1].split("_")[0]))
    # traverse all pockets
    min_dist, min_idx = float('inf'), -1
    for pp in range(len(pocket_names)):
        fileDirection = pocket_names[pp]
        pocket = open(fileDirection, "r").readlines()
        positions = []
        pocket_x, pocket_y, pocket_z, pocket_cnt = 0, 0, 0, 0
        for line in pocket:
            if line[:4] == "ATOM":
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                pocket_x += x
                pocket_y += y
                pocket_z += z
                pocket_cnt += 1
        pocket_x /= pocket_cnt
        pocket_y /= pocket_cnt
        pocket_z /= pocket_cnt
        dist = math.sqrt((pocket_x - xs) ** 2 + (pocket_y - ys) ** 2 + (pocket_z - zs) ** 2)
        if dist < min_dist:
            min_dist = dist
            min_idx = pp
    # print("min dist: %.2f" % min_dist)
    # print("position: %d" % (min_idx + 1))
    minimum_idxs.append(min_idx)
    minimum_dists.append(min_dist)

    #####################
    label = [0] * len(pocket_names)
    label[min_idx] = 1

    info_dir = fileNames[i][:-4] + "_out/"
    infofile = glob.glob(info_dir + "*.txt")[0]
    feature = extractPocket(infofile)
    
    assert len(label) == len(feature)
    labels.append(label)
    features.append(feature)

print(sum(len(lbl) for lbl in label))

# pickle.dump(labels, open("./labels_ASBench.pkl", "wb"))
# pickle.dump(features, open("./features_ASBench.pkl", "wb"))


##############


# minimum_dists = np.array(minimum_dists)
# minimum_idxs = np.array(minimum_idxs)

# minimum_idxs = np.delete(minimum_idxs, np.where(minimum_dists >= 10))


# import collections

# counter = collections.Counter(minimum_idxs)
# cnt = 0
# counter_percent = []
# for i in range(10):
#     cnt += counter[i]
#     counter_percent.append(cnt / len(minimum_idxs))


# labels = pickle.load(open("./classification/labels.pkl", "rb"))
# ori_counter = collections.Counter()

# for i in range(len(labels)):
#     for j in range(len(labels[i])):
#         if labels[i][j] == 1:
#             ori_counter[j] += 1

# cnt = 0
# ori_counter_percent = []
# for i in range(10):
#     cnt += ori_counter[i]
#     ori_counter_percent.append(cnt / len(minimum_idxs))



# import matplotlib.pyplot as plt

# plt.figure(figsize=(6, 4), dpi=300)
# plt.plot(counter_percent)
# plt.plot(ori_counter_percent)
# plt.legend(["counter", "ori 90"])
# plt.xlabel("position")
# plt.savefig("percent.png")




