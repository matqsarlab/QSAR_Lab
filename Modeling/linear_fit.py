import numpy as np

# least-square
def fit(y, y_pred, *args):
    """
    If you want fitting for diffrent range, use *args matrix
    """
    ls = np.polyfit(y, y_pred, 1)

    if args:
        fit_y = ls[0]*np.array(args).flatten() + ls[1]
    else:
        fit_y = ls[0]*y + ls[1]

    return fit_y

# Ideal fitting
def ideal_fit(y_train, y_train_pred):
    y_train = list(y_train)
    y_train_pred = list(y_train_pred.flatten())

    concate = y_train + y_train_pred

    x_min, x_max = np.min(concate), np.max(concate)
    return (x_min, x_max), (x_min, x_max)
