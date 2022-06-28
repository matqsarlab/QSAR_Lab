import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import matrix_power
from sklearn.preprocessing import StandardScaler


def Williams_plot(X_train, X_test,y_train, y_test, y_train_pred, y_test_pred):
    """Aplicability Domain"""
    Xt = X_train
    Yt = y_train
    XT_y_pred = y_train_pred

    Xv = X_test
    Yv = y_test
    XV_y_pred = np.array(y_test_pred)
    XV_y_pred = XV_y_pred.reshape(-1)

    nawias = matrix_power((np.dot(Xt.T, Xt)), -1)

    """Train"""
    h_indexes = []
    for idx in Xt.index.values:
        xi_t = np.asarray(Xt.loc[idx]).T
        xi = np.asarray(Xt.loc[idx])
        hi = np.dot(xi_t.dot(nawias), xi)
        h_indexes.append(hi)
    res = np.zeros(len(Yt))

    for x in range(0, len(Yt)):
        res[x] += np.array(Yt)[x]-XT_y_pred[x]

    scaler3 = StandardScaler()
    r = res.reshape(-1, 1)
    st_res = scaler3.fit_transform(r)
    h_k = (3 * (len(Xt.columns) + 1))/len(Xt.index)
    print("h_k =", h_k)
    """Train"""

    """Test"""
    h_indexes_v = []
    for idx in Xv.index.values:
        xi_t = np.asarray(Xv.loc[idx]).T
        xi = np.asarray(Xv.loc[idx])
        hi_v = np.dot(xi_t.dot(nawias), xi)
        h_indexes_v.append(hi_v)
    res_v = np.zeros(len(Yv))

    for x in range(0, len(Yv)):
        res_v[x] += np.array(Yv)[x]-XV_y_pred[x]
        pass

    st_res_v = scaler3.transform(res_v.reshape(-1, 1))
    """Test"""

    return h_indexes, st_res, h_indexes_v, st_res_v, h_k
