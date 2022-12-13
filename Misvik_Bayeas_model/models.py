#!/usr/bin/env python3.11
import itertools

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
from sklearn.base import clone
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, precision_score, recall_score)


class CoreModel:
    def __init__(self, model, train, test, toxic, perm_num=2) -> None:
        self.train = train
        self.test = test
        self.toxic = toxic
        self.perm_num = perm_num
        self.clasificator_model = model
        self.__show = False
        self.__numberOfPlots = 5
        self.__show_raport = False
        self.__namesNMs = (
            train.index.tolist() + test.index.tolist() + toxic.index.tolist()
        )
        self.__predOnTest = False
        self.__percent = False
        self.__nmsTestDict = {k: [] for k in self.__namesNMs}
        self.__nmsTestDict_proba = self.__nmsTestDict.copy()
        CoreModel.modelKlas = []
        CoreModel.dataSets = {}

    @property
    def create_data_set(self):
        CoreModel.dataSets.clear()
        tox_list = self.toxic.index.tolist()

        x = itertools.combinations(tox_list, self.perm_num)
        c = 0

        for i in x:

            tox_list_c = tox_list.copy()

            [tox_list_c.remove(i[num]) for num in range(self.perm_num)]

            train_c = pd.concat([self.train, self.toxic.loc[tox_list_c]])
            test_c = pd.concat([self.test, self.toxic.loc[list(i)]])

            CoreModel.dataSets[f"set{c}"] = (train_c, test_c)
            c += 1
        print(f"CREATE_DATA - number of sets: {len(CoreModel.dataSets)}")
        return CoreModel.dataSets

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
    def numberOfPlots(self):
        return self.__numberOfPlots

    @numberOfPlots.setter
    def numberOfPlots(self, n):
        self.__numberOfPlots = n

    @property
    def show_raport(self):
        return self.__show_raport

    @show_raport.setter
    def show_raport(self, value):
        self.__show_raport = value

    @property
    def create_models(self):
        CoreModel.modelKlas.clear()
        data_sets = self.create_data_set
        print("__predOnTest GLOBAL: ", self.__predOnTest)

        for e, name in enumerate(data_sets):
            train = data_sets[name][0]
            test = data_sets[name][1]

            X_train = train.drop("y", axis=1)
            y_train = train["y"]

            X_test = test.drop("y", axis=1)
            y_test = test["y"]

            model = clone(self.clasificator_model)
            model.fit(X_train, y_train)
            CoreModel.modelKlas.append(model)

            if self.__predOnTest:
                y_test_pred = model.predict(X_test)

                for v, k in zip(y_test_pred, y_test.index):
                    self.__nmsTestDict[k].append(v)

            if self.__percent:
                y_test_pred = model.predict_proba(X_test)

                for v, k in zip(y_test_pred, y_test.index):
                    self.__nmsTestDict_proba[k].append(v)

            if self.__show:
                if e >= self.__numberOfPlots - 1:
                    self.__show = False

                model.predict(X_test)

                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                cm_train = confusion_matrix(y_train, y_train_pred)
                cm_test = confusion_matrix(y_test, y_test_pred)

                self.plot_confusion_matrix(cm_train, f"TRAIN {e+1}")
                if self.show_raport:
                    print(classification_report(y_train, y_train_pred))

                self.plot_confusion_matrix(cm_test, f"TEST {e+1}")
                if self.show_raport:
                    print(classification_report(y_test, y_test_pred))

        return

    @property
    def predOnTest(self):
        return self.__predOnTest

    @predOnTest.setter
    def predOnTest(self, value):
        self.__predOnTest = value

    @property
    def predict_on_test(self):
        self.__predOnTest = True

        print("__predOnTest from func: ", self.__predOnTest)
        exist = False
        for k in self.__nmsTestDict:
            if self.__nmsTestDict[k]:
                exist = True
                break
        mean = {}

        def calc_mean(obj, mean_dict):
            mean_dict[nm] = str(np.where(np.mean(obj[nm]) < 0.5, "Non-Toxic", "Toxic"))
            return mean_dict

        if exist:
            print("IF")
            for nm in self.__nmsTestDict:
                if self.__nmsTestDict[nm]:
                    calc_mean(self.__nmsTestDict, mean)
        else:
            _ = self.create_models
            print("ELSE")
            for nm in self.__nmsTestDict:
                if self.__nmsTestDict[nm]:
                    calc_mean(self.__nmsTestDict, mean)
        return pd.DataFrame(
            data=mean.values(), index=mean.keys(), columns=["Predicted Toxicity"]
        )

    def predict(self, X):
        nms = {nm: [] for nm in X.index}
        mean = {}
        for i in CoreModel.modelKlas:
            for nm, pred in zip(nms, i.predict(X)):

                nms[nm].append(pred)

        for nm in nms:
            mean[nm] = str(np.where(np.mean(nms[nm]) < 0.5, "Non-Toxic", "Toxic"))

        return pd.DataFrame(
            data=mean.values(), index=mean.keys(), columns=["Predicted Toxicity"]
        )

    @property
    def mean_calc(self):
        if CoreModel.modelKlas:
            data_sets = CoreModel.dataSets
        else:
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

        for name, model in zip(data_sets, CoreModel.modelKlas):
            train = data_sets[name][0]
            test = data_sets[name][1]

            X_train = train.drop("y", axis=1)
            y_train = train["y"]

            X_test = test.drop("y", axis=1)
            y_test = test["y"]

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

    @property
    def predOnTest_percent(self):
        return self.__percent

    @predOnTest_percent.setter
    def predOnTest_percent(self, value):
        self.__percent = value

    @property
    def predict_on_test_proba(self):
        self.__percent = True

        exist = False
        for k in self.__nmsTestDict_proba:
            if self.__nmsTestDict_proba[k]:
                exist = True
                break
        mean = {}

        def calc_mean(obj, mean_dict, nm):
            prob_toxic = [i[1] for i in obj[nm]]
            mean_dict[nm] = np.mean(prob_toxic)
            return mean_dict

        if exist:
            for nm in self.__nmsTestDict_proba:
                if self.__nmsTestDict_proba[nm]:
                    calc_mean(self.__nmsTestDict_proba, mean, nm)
        else:
            _ = self.create_models
            for nm in self.__nmsTestDict_proba:
                if self.__nmsTestDict_proba[nm]:
                    calc_mean(self.__nmsTestDict_proba, mean, nm)
        return pd.DataFrame(
            data=mean.values(), index=mean.keys(), columns=["Predicted Toxicity [%]"]
        )


class CombinationModel(CoreModel):
    def __init__(self, model, train, test, toxic, perm_num) -> None:
        super().__init__(model, train, test, toxic, perm_num)
        self.work = pd.concat([train, test])

    @property
    def create_data_set(self):

        Markers = [
            "DQ-12",
            "TiO2",
            "ZnO",
            "MWCNT",
            "BaSO4",
            "SiO2",
            "Ag",
            "CeO2",
            "Silver",
            "Mitsui",
        ]

        CoreModel.dataSets.clear()
        tox_list = self.toxic.index.tolist()

        toxCombList = list(itertools.combinations(tox_list, self.perm_num))

        work_index = self.train.index.tolist() + self.test.index.tolist()
        coreTestList = list(itertools.combinations(work_index, 4))

        c = 0

        def check(string, object):
            if object in string:
                return True
            else:
                return False

        def change_word(word):
            if word == "Silver":
                return "Ag"
            elif word == "Mitsui":
                return "MWCNT"
            else:
                return word

        for tcl in toxCombList:
            tcl = list(tcl)
            marker = {change_word(m) for m in Markers for t in tcl if m in t}
            for ctl in coreTestList:
                ctl = list(ctl)
                tl_c = tox_list.copy()
                wi_c = work_index.copy()
                text = "".join(ctl)
                result = [check(text, object) for object in marker]
                if not any(result):
                    [tl_c.remove(tcl[num]) for num in range(self.perm_num)]
                    [wi_c.remove(i) for i in ctl]

                    train_c = pd.concat([self.work.loc[wi_c], self.toxic.loc[tl_c]])
                    test_c = pd.concat([self.work.loc[ctl], self.toxic.loc[tcl]])

                    CoreModel.dataSets[f"set{c}"] = (train_c, test_c)
                    c += 1
        print(f"CREATE_DATA - number of sets: {len(CoreModel.dataSets)}")
        return CoreModel.dataSets

    def plot_confusion_matrix(self, cm, title):
        return super().plot_confusion_matrix(cm, title)

    @property
    def create_models(self):
        x = super().create_models
        return x

    @property
    def mean_calc(self):
        return super().mean_calc
