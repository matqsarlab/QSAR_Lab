import numpy as np
import pandas as pd


## ----------------- Spliter Function -------------------------
def split_x_to_n(X, y, n=3, sort=True):
    def sortV(X, y):
        df = pd.concat([X, y], axis=1)
        if type(y) is pd.Series:
            name = y.name
        else:
            name = y.columns[0]
        df.sort_values(by=name, inplace=True)
        return df

    if sort == True:
        data = sortV(X=X, y=y)
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
    lenght = len(X)
    train = []
    test = []
    for row in range(lenght):
        # print(row % n)
        if (row % n) < n - 1:
            train.append(row)
        else:
            test.append(row)
    last_train = np.max(train)
    last_val = np.max(test)
    if np.max(train) < np.max(test):
        train.pop()
        test.pop()
        train.append(last_val)
        test.append(last_train)

    return X.iloc[train], X.iloc[test], y.iloc[train], y.iloc[test]
