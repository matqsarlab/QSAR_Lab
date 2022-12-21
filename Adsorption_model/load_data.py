#!/usr/bin/env python3
import numpy as np
import pandas as pd
from QSAR_Lab.spliter import split_x_to_n


def loadData():
    X_dragon = pd.read_excel("../Data/data_dummies.xlsx", index_col=0, sheet_name=0)
    X_gaussian = pd.read_excel("../Data/data_dummies.xlsx", index_col=1, sheet_name=1)
    X_gaussian.drop("Nazwa oryginalnego pliku", axis=1, inplace=True)

    X_gaussian["FDH_horiz_mean"] = (
        pd.DataFrame(
            X_gaussian[
                [
                    "FDH 1 (finite dipole horizontal) (kcal/mol)",
                    "FDH 2 (finite dipole horizontal) (kcal/mol)",
                ]
            ]
        ).sum(axis=1)
        / 2
    )
    X_gaussian.drop(
        [
            "FDH 1 (finite dipole horizontal) (kcal/mol)",
            "FDH 2 (finite dipole horizontal) (kcal/mol)",
        ],
        axis=1,
        inplace=True,
    )

    y = pd.read_excel("../Data/data_dummies.xlsx", index_col=0, sheet_name=2)

    X = X_dragon.copy()

    X[X_gaussian.columns] = np.nan

    for i in X.index:
        for j in X_gaussian.index:
            if j in i:
                X.loc[i, X_gaussian.columns] = X_gaussian.loc[j].values

    conc = pd.concat([X, y], axis=1)
    conc.sort_values(by=["Ads_Energy"], axis=0, inplace=True)

    X_train, X_test, y_train, y_test = split_x_to_n(X, y)

    y_train = np.array(y_train).ravel()
    y_test = np.array(y_test).ravel()
    return X_train, X_test, y_train, y_test
