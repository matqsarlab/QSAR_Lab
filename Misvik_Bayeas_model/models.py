#!/usr/bin/env python
import itertools

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, precision_score, recall_score)
from sklearn.naive_bayes import GaussianNB


class Make_models:
    def __init__(self, train, test, toxic, perm_num) -> None:
        self.train = train
        self.test = test
        self.toxic = toxic
        self.perm_num = perm_num
        self.__show = False
        self.__model = []

    @property
    def create_data_set(self):
        tox_list = self.toxic.index.tolist()
        data_sets = {}

        x = itertools.permutations(tox_list, self.perm_num)
        c = 0

        for i in x:

            tox_list_c = tox_list.copy()
            test_c = self.test.copy()

            [tox_list_c.remove(i[num]) for num in range(self.perm_num)]

            train_c = pd.concat([self.train, self.toxic.loc[tox_list_c]])
            test_c = pd.concat([self.test, self.toxic.loc[list(i)]])

            data_sets[f"set{c}"] = (train_c, test_c)
            c += 1
        return data_sets

    def plot_confusion_matrix(self, cm, title):
        cm = cm[::-1]
        cm = pd.DataFrame(cm, columns=["pred_0", "pred_1"], index=["true_1", "true_0"])

        fig = ff.create_annotated_heatmap(
            z=cm.values,
            x=list(cm.columns),
            y=list(cm.index),
            colorscale="ice",
            showscale=True,
            reversescale=True,
        )
        fig.update_layout(
            width=400,
            height=400,
            title=f"Confusion Matrix - Model {title}",
            font_size=16,
        )
        fig.show()
        return 0

    @property
    def show_models(self):
        return self.__show

    @show_models.setter
    def show_models(self, value):
        self.__show = value

    @property
    def create_models(self):
        data_sets = self.create_data_set
        for e, name in enumerate(data_sets):
            train = data_sets[name][0]
            test = data_sets[name][1]

            X_train = train.drop("y", axis=1)
            y_train = train["y"]

            X_test = test.drop("y", axis=1)
            y_test = test["y"]

            model = GaussianNB()
            model.fit(X_train, y_train)
            self.__model.append(model)

            model.predict(X_test)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            a_train = accuracy_score(y_train, y_train_pred)
            a_test = accuracy_score(y_test, y_test_pred)

            cm_train = confusion_matrix(y_train, y_train_pred)
            cm_test = confusion_matrix(y_test, y_test_pred)
            if self.__show == True:
                self.plot_confusion_matrix(cm_train, f"TRAIN {e+1}")

                print(f"Accuracy = {a_train}")

                tn, fp, fn, tp = cm_train.ravel()
                print(f"TN - True Negative: {tn}")
                print(f"FP - False Positive: {fp}")
                print(f"FN - False Negative: {fn}")
                print(f"TP - True Positive: {tp}")

                print(f"False Positive Rate Type I error = {fp / (fp + tn)}")
                print(f"False Negative Rate - Type II error = {fn / (fn + tp)}")

                # Precision - ile obserwacji przewidywanych jako pozytywne są w rzeczywistości pozytywne
                print(f"Precision = {tp / (tp + fp)}")

                # Recall - jak wiele obserwacji z wzystkich poytywnych sklasyfikowaliśmy jako pozytywne
                print(f"Recall = {tp / (tp + fn)}")

                print(classification_report(y_train, y_train_pred))

                self.plot_confusion_matrix(cm_test, f"TEST {e+1}")

                print(f"Accuracy = {a_test}")

                tn, fp, fn, tp = cm_test.ravel()
                print(f"TN - True Negative: {tn}")
                print(f"FP - False Positive: {fp}")
                print(f"FN - False Negative: {fn}")
                print(f"TP - True Positive: {tp}")

                print(f"False Positive Rate Type I error = {fp / (fp + tn)}")
                print(f"False Negative Rate - Type II error = {fn / (fn + tp)}")

                # Precision - ile obserwacji przewidywanych jako pozytywne są w rzeczywistości pozytywne
                print(f"Precision = {tp / (tp + fp)}")

                # Recall - jak wiele obserwacji z wzystkich poytywnych sklasyfikowaliśmy jako pozytywne
                print(f"Recall = {tp / (tp + fn)}")

                print(classification_report(y_test, y_test_pred))
        return 0

    def predict(self, X):
        nms = {nm: [] for nm in X.index}
        mean = {}
        for i in self.__model:
            for nm, pred in zip(nms, i.predict(X)):

                nms[nm].append(pred)

        for nm in nms:
            mean[nm] = str(np.where(np.mean(nms[nm]) <= 0.5, "Non-Toxic", "Toxic"))

        return pd.DataFrame(
            data=mean.values(), index=mean.keys(), columns=["Predicted Toxicity"]
        )

    @property
    def mean_calc(self):
        data_sets = self.create_data_set

        mean_precision_train = []
        mean_recall_train = []
        mean_accuracy_train = []
        mean_tn_train = []
        mean_fp_train = []
        mean_fn_train = []
        mean_tp_train = []

        mean_precision_test = []
        mean_recall_test = []
        mean_accuracy_test = []
        mean_tn_test = []
        mean_fp_test = []
        mean_fn_test = []
        mean_tp_test = []

        for name in data_sets:
            train = data_sets[name][0]
            test = data_sets[name][1]

            X_train = train.drop("y", axis=1)
            y_train = train["y"]

            X_test = test.drop("y", axis=1)
            y_test = test["y"]

            model = GaussianNB()
            model.fit(X_train, y_train)

            model.predict(X_test)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            a_train = accuracy_score(y_train, y_train_pred)
            a_test = accuracy_score(y_test, y_test_pred)

            cm_train = confusion_matrix(y_train, y_train_pred)
            cm_test = confusion_matrix(y_test, y_test_pred)

            tn, fp, fn, tp = cm_train.ravel()
            mean_tn_train.append(tn)
            mean_fp_train.append(fp)
            mean_fn_train.append(fn)
            mean_tp_train.append(tp)
            mean_accuracy_train.append(a_train)
            mean_precision_train.append(precision_score(y_train, y_train_pred))
            mean_recall_train.append(recall_score(y_train, y_train_pred))

            tn, fp, fn, tp = cm_test.ravel()
            mean_tn_test.append(tn)
            mean_fp_test.append(fp)
            mean_fn_test.append(fn)
            mean_tp_test.append(tp)
            mean_accuracy_test.append(a_test)
            mean_precision_test.append(
                precision_score(y_test, y_test_pred, average="macro")
            )
            mean_recall_test.append(recall_score(y_test, y_test_pred, average="micro"))

        print("TRAIN SET:")
        print(f"Accuracy = {np.mean(mean_accuracy_train)}")
        print(f"Precison = {np.mean(mean_precision_train)}")
        print(f"Recall = {np.mean(mean_recall_train)}")
        print(f"tn = {np.mean(mean_tn_train)}")
        print(f"fp = {np.mean(mean_fp_train)}")
        print(f"fn = {np.mean(mean_fn_train)}")
        print(f"tp = {np.mean(mean_tp_train)}")
        print("")

        print("TEST SET:")
        print(f"Accuracy = {np.mean(mean_accuracy_test)}")
        print(f"Precison = {np.mean(mean_precision_test)}")
        print(f"Recall = {np.mean(mean_recall_test)}")
        print(f"tn = {np.mean(mean_tn_test)}")
        print(f"fp = {np.mean(mean_fp_test)}")
        print(f"fn = {np.mean(mean_fn_test)}")
        print(f"tp = {np.mean(mean_tp_test)}")
        return 0
