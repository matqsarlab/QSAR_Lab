#!/usr/bin/env python3.10
import numpy as np
import pandas as pd
from load_data import loadData
from sklearn.feature_selection import (SelectKBest, VarianceThreshold,
                                       f_regression, mutual_info_regression,
                                       r_regression)
from sklearn.preprocessing import StandardScaler

"""
------------------------------------------------------------------------------------
Metoda pzowalajaca wybrac zestaw najbardzie odpowiednich 
deskrytporow. Wykorzystywane sa testy z instancji SelectKBest
oraz mutual_info_regression:
       * SelectKBest f_regression
       * SelectKBest r_regression
       * mutual_info_regression n_neighbors(5)
------------------------------------------------------------------------------------


 - SelectKBest          -   Funckcja przyjmujaca dwa array'e X i y, zwraca
                            array (scores, pvalues) lub pojedynczy array (scores) 
                            ______________________________________________________
                        *   sklearn.feature_selection.SelectKBest
                            ******************************************************

    * f/r_regression    -   Szybki model liniowy do testowania efektu pojedynczego
                            regresora, wykorzystuje jednowymiarowe testy regresji
                            liniowej, ktore zwracają statystyki F i wartości p.
                            
                            *** roznica miedzy f_regression a r_regression:
                            -----------------------------------------------------
                            f_regression wywodzi się z r_regression i uszereguje 
                            cechy w tej samej kolejności, jeśli wszystkie cechy 
                            są dodatnio skorelowane z wartością docelową.
                            ______________________________________________________
                        *   sklearn.feature_selection.f_regression
                            ******************************************************

                            -----------------------------------------------------

 - mutual_info_regres.  -   Oszacowanie wzajemnej informacji miedzy dwoma 
                            ciaglymi obiektami (X -> y).
                            ______________________________________________________
                        *   sklearn.feature_selection.mutual_info_regression
                        *   https://en.wikipedia.org/wiki/Mutual_information
                        *   (www) Comparison of F-test and mutual information
                            ******************************************************

 - varianceSelect       -   Opis
"""


def data(set="dragon"):
    X_train, X_test, y_train, y_test = loadData()

    X = pd.concat([X_train, X_test])
    y = np.append(y_train, y_test)

    dragon = X_train.loc[:, :"Hamaker"].columns
    gaussian = X_train.loc[:, "Number of rotable bonds / Å^2":].columns

    X_dragon = X[dragon]
    X_gaussian = X[gaussian]

    if set == "dragon":
        return X_dragon
    elif set == "gaussian":
        return X_gaussian
    else:
        return y


def scaler(X) -> pd.DataFrame:
    model = StandardScaler()
    Z = model.fit_transform(X)
    return pd.DataFrame(Z, columns=X.columns, index=X.index)


def varianceSelect(X, threshold=0.0) -> pd.DataFrame:
    selector = VarianceThreshold(threshold=threshold)
    selector.fit(X)
    name = selector.get_feature_names_out()
    return X[name]


def descrSelect(X, y, num=20, method=f_regression) -> pd.DataFrame:
    model = SelectKBest(method, k=num)
    model.fit(X, y)
    name = model.get_feature_names_out()
    return X[name]


def show_desriptors(name, num=None):
    X = data(set=name)
    y = data(set="y")

    X = varianceSelect(X, threshold=0.8 * (1 - 0.8))

    number = 3
    dragon1 = descrSelect(scaler(X), y, method=f_regression, num=number)
    dragon2 = descrSelect(scaler(X), y, method=r_regression, num=number)
    mi = mutual_info_regression(scaler(X), y, n_neighbors=5, random_state=42)
    mutual_info = pd.Series(mi)
    mutual_info.index = X.columns
    mutual_info.sort_values(ascending=False, inplace=True)

    x = list(dragon1.columns)
    y = list(dragon2.columns)
    if num:
        z = list(mutual_info.iloc[:num].index)
    else:
        z = list(mutual_info.iloc[:].index)
    result = list(set(x + y + z))
    result.sort()
    print(result)
    print(len(result))


show_desriptors("gaussian")
show_desriptors("dragon", 3)
