import numpy as np

## ----------------- Spliter Function -------------------------
def split_x_to_n(X, y, n=3):
    lenght = len(X)
    train = []
    test = []
    for row in range(lenght):
        #print(row % n)
        if ((row % n) < n-1):
            train.append(row)
        else:
            test.append(row)
    last_train = np.max(train)
    last_val = np.max(test)
    if (np.max(train) < np.max(test)):
        train.pop()
        test.pop()
        train.append(last_val)
        test.append(last_train)

    return X.iloc[train], X.iloc[test], y.iloc[train], y.iloc[test]
