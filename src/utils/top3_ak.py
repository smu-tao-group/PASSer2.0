import numpy as np



def top3(y_pred_probs, y_true):
    one, two, three = 0, 0, 0
    for i in range(len(y_true)):
        probs = y_pred_probs[i]
        trues = y_true[i]

        prob = trues.index(1)
        probs.sort(key=lambda x: -x)

        if probs.index(prob) == 1:
            one += 1
            two += 1
            three += 1
        elif probs.index(prob) == 2:
            two += 1
            three += 1
        elif probs.index(prob) == 3:
            three += 1

    oneProb = one / len(y_true) * 100
    twoProb = two / len(y_true) * 100
    threeProb = three / len(y_true) * 100

    return oneProb, twoProb, threeProb 
