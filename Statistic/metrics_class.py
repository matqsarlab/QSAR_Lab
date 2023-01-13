#!/usr/bin/env python3.11

from sklearn.metrics import accuracy_score


def show_conf_matrix(cm):
    """Pokazuje charakterystyczne wielkosci
    w macierzy konfuzji
    cm - confusion_matrix"""
    tn, fp, fn, tp = cm.ravel()
    print(f"TN - True Negative: {tn}")
    print(f"FP - False Positive: {fp}")
    print(f"FN - False Negative: {fn}")
    print(f"TP - True Positive: {tp}")
    return 0


def accuracy(y_obs, y_pred):
    """Accuracy score = n_correct_pred/all_predictions * 100"""
    print(f"Accuracy = {accuracy_score(y_obs, y_pred)}")
    return 0


def fpr(cm):
    """Type I error - False Positive Rate
    fpr = fp / (fp + tn)"""
    tn, fp, _, _ = cm.ravel()
    return fp / (fp + tn)


def fnr(cm):
    """Type II error - False Negative Rate
    fnr = fn / (fn + tp)"""
    _, _, fn, tp = cm.ravel()
    return fn / (fn + tp)


def precision(cm):
    _, fp, _, tp = cm.ravel()
    """Precision - ile obserwacji przewidywanych jako pozytywne są w rzeczywistości pozytywne
    precision = tp / (tp + fp)"""
    return tp / (tp + fp)


def recall(cm):
    """Recall - jak wiele obserwacji z wzystkich poytywnych sklasyfikowaliśmy jako pozytywne
    recall = tp / (tp + fn)"""
    _, _, fn, tp = cm.ravel()
    return tp / (tp + fn)
