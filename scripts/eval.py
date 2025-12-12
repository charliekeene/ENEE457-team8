import pandas as pd
import io

WINDOW_SECONDS = 10

ids = []
truth = []

with open("logs/ids.log", 'r') as file:
    for line in file:
        if line.strip():
            ids.append(float(line.split(' ')[0]))
with open("logs/controller.log", 'r') as file:
    for line in file:
        if line.strip():
            truth.append(float(line.split(' ')[0]))

TP_lst = []
FP_lst = set(ids)
FN_lst = []

for attack_time in truth:
    detected = False
    for detect_time in ids:
        if detect_time > attack_time and detect_time < (attack_time + WINDOW_SECONDS):
            detected = True
            FP_lst.remove(detect_time)
    if detected: TP_lst.append(attack_time)
    else: FN_lst.append(attack_time)
FP_lst = list(FP_lst)

TP = len(TP_lst)
FP = len(FP_lst)
FN = len(FN_lst)
precision = TP/(TP+FP)
recall = TP/(TP+FN)
f1 = (2*precision*recall)/(precision+recall)

print(f"True Positives: {TP}")
print(f"False Positives: {FP}")
print(f"False Negatives: {FN}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")