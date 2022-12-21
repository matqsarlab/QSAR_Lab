#!/usr/bin/env python3.11

import numpy as np
import pandas as pd
from QSAR_Lab.spliter import split_x_to_n
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import ShuffleSplit, cross_val_score

# Parameters reader
file = open("./FiltredModels/filtred.txt")
x_file_name = "./Data/My_Selected_X.xlsx"
content = file.readlines()
file.close()

rand = None
rand_cv = None
l_r_train = []
l_r_test = []
l_cv = []

for line in range(len(content)):
    param = content[line - 1].split()
    if "rand" in param:
        rand = int(param[2].replace(",", ""))
        rand_cv = int(param[5])

    # Load Data
    X = pd.read_excel(x_file_name, sheet_name=0, index_col=0)
    y = pd.read_excel("./Data/data_dummies.xlsx", index_col=0, sheet_name=2)
    X_train, X_test, y_train, y_test = split_x_to_n(X, y, sort=True)

    # Create Model
    model = AdaBoostRegressor(random_state=rand, n_estimators=100)
    model.fit(np.array(X_train), y_train)
    y_train_pred = model.predict(np.array(X_train))
    y_test_pred = model.predict(np.array(X_test))

    # Cross-Validation
    kfold = ShuffleSplit(n_splits=5, test_size=0.25, random_state=rand_cv)
    scores = cross_val_score(model, X_train, y_train, cv=kfold)
    l_cv.append(scores.mean())
    l_r_train.append(model.score(np.array(X_train), y_train))
    l_r_test.append(model.score(np.array(X_test), y_test))

d = {"R^2": l_r_train, "R_test^2": l_r_test, "Rcv": l_cv}

df = pd.DataFrame(d)
df.sort_values(by="R_test^2", inplace=True, ascending=False)
print(df)
