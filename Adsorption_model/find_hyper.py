#!/usr/bin/env python3

import numpy as np
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import ShuffleSplit, cross_val_score


def deviat(y_obs, y_pred, treshold=3.0):
    """Sprawdza odchylenie wartosci przewidzianego punktu od punktu obserwowanego.
    Jesli znajduje sie jakas predykcja, ktorej wartosc znacznie odbiega od obserwacji,
    to zwraca True.

    Jesli pojawi sie przynajmniej jeden znaczaco duzy blad ("abs(i-j) > treshold"), petla
    zostaje przerwana, a wartosc parametru "check" zmieniona jest na `True`.

    *** Parametr `check` ma znaczenie w dalszej czesci (metoda find_train) - jesli funkcja
    deviat nie znajdzie znaczacego grubego bledu (abs(i-j) > treshold), zostanie zwrocony
    i odpowiedni hiperparametr `random_state` (patrz '*' w opisie `find_train`).

    y_obs, y_pred - odpowiednio wartosci y: obserwowalna i przewidziana
    treshold      - maksymalny dopuszczalny blad, liczony jako roznica miedzy wartoscia
                    y_obs i y_pred (wartosc bezwzgledna)."""
    check = False

    for i, j in zip(y_obs, y_pred):
        if abs(i - j) > treshold:
            check = True
            break
    return check


# Find Training
def find_train(X, y, randInt=1000, treshold=3.0):
    """Find hyperparameter for AdaBoostRegressor (random_state)

    * - jesli zostanie dobrany odpowiednia wartosc hiperparametru `random_state` to
        petla `while` zostanie przerwana i zwrocona odpowiednia wartosc `rand`."""
    check = True
    while check:
        rand = np.random.randint(0, randInt)
        model = AdaBoostRegressor(random_state=rand, n_estimators=100)
        model.fit(X, y)
        y_pred = model.predict(X)

        check = deviat(y_obs=y, y_pred=y_pred, treshold=treshold)
        return rand


# Cross-Validation
def find_CrossV(X, y, rand, treshold=6.0, cv_tresh=0.5, cycle=1000, randInt=1000):
    """Znajduje odpowiedni podzial setu treningowego (ShuffleSplit), tak by zostalo spelnione
    kryterium cross validation. Dodatkowo sprawdzane jest odchylenie wartoci przewidzianej (y_pred)
    od wartosci oczekiwanej (y_obs) przy pomocy funkcji deviat (sekcja '*' wyzej).

    Sprawdzane sa dwa warunki (cond1 i cond2):
        cond1 - `True` jesli wartosc srednia Rcv^2 (dla wszyskich foldow) jest wyzsza niz wartosc
                krytyczna (`cv_tresh`),
        cond2 - `True` jesli wartosc abs(y_obs-y_pred) dla wszystkich punktow jest mniejsza niz
                wartosc krytyczna `treshold`.

        a)    - Jesli cond1 & cond2 == True --> petla przerwana i zwrocona jest wartosc rand_cv
        b)    - Jesli wykona wartosc cykli (cycle) zostanie przekroczona, to petla sie przerwie,
                a zwrocona wartosc rand_cv to `--`.
    ------------------------------------------------------------------------------------------------------
    cycle     - ilosc cykli, ktore przechodzi petla while, w poszukiwaniu odpowiednich wartosci
                hiperparametrow.
    randInt   - zakres z jakiego wyszukiwany jest `rand_cv`"""
    c = 0
    scores = np.array
    X = np.array(X)

    while True:
        rand_cv = np.random.randint(0, randInt)
        model = AdaBoostRegressor(random_state=rand, n_estimators=100)
        kfold = ShuffleSplit(n_splits=5, test_size=0.25, random_state=rand_cv)
        scores = cross_val_score(model, X, y, cv=kfold)

        # Condition 1 & 2:
        cond1 = False
        cond2 = False
        cond_ = []
        if scores.mean() >= cv_tresh:
            cond1 = True

            for train, test in kfold.split(X):
                X_tn, X_tst, y_tn, y_tst = (
                    X[train],
                    X[test],
                    y[train],
                    y[test],
                )
                model = AdaBoostRegressor(random_state=rand, n_estimators=100)
                model.fit(X_tn, y_tn)

                y_tst_pred = model.predict(X_tst)

                cond_.append(deviat(y_obs=y_tst, y_pred=y_tst_pred, treshold=treshold))

        cond2 = not any(cond_)
        c += 1
        if c >= cycle:
            rand_cv = "--"
            break

        elif cond1 and cond2:
            break

    return rand_cv
