#!/usr/bin/env python3.11
import os

import pandas as pd
from QSAR_Lab.Adsorption_model.find_hyper import find_CrossV, find_train
from QSAR_Lab.spliter import split_x_to_n

# Load Data
X = pd.read_excel("./Data/My_Selected_X.xlsx", sheet_name=0, index_col=0)
y = pd.read_excel("./Data/data_dummies.xlsx", index_col=0, sheet_name=2)
X_train, X_test, y_train, y_test = split_x_to_n(X, y, sort=True)

# Parameters:
num = 0
cycle = 1000
ts1 = 3.5  # treshold1 - maksymalna roznica miedzy y_obs-y_pred dla
ts2 = 4.5
cv_t = 0.85
filename = "./FiltredModels/filtred.txt"
if not os.path.exists(filename):
    with open(filename, "w"):
        pass

# Start

while num < cycle:
    # Find AdaBoost randomstate parameter
    randnum = find_train(X_train, y_train, randInt=5000, treshold=ts1)
    # find Cross-Validation randomstate
    randcvnum = find_CrossV(
        X_train,
        y_train,
        rand=randnum,
        treshold=ts2,
        cv_tresh=cv_t,
        cycle=30,
        randInt=5000,
    )

    if randcvnum != "--":
        with open(filename, "a") as f:
            f.write(f"rand = {randnum}, rand_cv = {randcvnum}\n")

    if cv_t > 0.6:
        cv_t -= 0.01
    if ts1 < 6:
        ts1 += 0.01
    if ts2 < 8:
        ts2 += 0.01

    num += 1
    print(f"Cycle:{num}")


with open(filename, "a") as f:
    f.write(f"\n__________NEW____________\n")
print("Stop")
