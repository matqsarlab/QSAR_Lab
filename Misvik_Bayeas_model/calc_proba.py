#!/usr/bin/env python
import numpy as np
import pandas as pd


class Probability:
    def __init__(self, data, col_names):
        self.data = data
        self.col_names = col_names

    @property
    def cut(self):
        names = ["y"] + self.col_names
        return self.data[names]

    @property
    def condition(self):
        txt = ""
        cut = self.cut

        for i in self.col_names:
            txt += f"(cut['{i}'] == 1) & "

        return eval(f"cut[{txt[:-3]}]")

    @property
    def calc_proba(self):
        try:
            x = len(self.condition)
            y = np.count_nonzero(self.condition["y"] == 1)
            return "Probability: '{}' = {}".format(", ".join(self.col_names), y / x)

        except ZeroDivisionError as err:
            return print("Handling run-time error:", err)


"""
INSTRUKCJA:

data = pd.read_excel("./Data_a549.xlsx", sheet_name=0, index_col=0)

x1 = ["Soluble or not"]
pairs = [
    ["Soluble or not"],
    ["Spheroidal 10 - 50 nm"],
    ["Elongated or not"],
    ["Length: > 5000 nm"],
    ["Length: > 5000 nm"],
    ["Soluble or not", "Spheroidal 10 - 50 nm"],
    ["Elongated or not", "Length: > 5000 nm"],
    [
        "Soluble or not",
        "Spheroidal 10 - 50 nm",
        "Unintentional presence of chemical individuals on the surface / Impurities Metalic",
    ],
    [
        "Elongated or not",
        "Length: > 5000 nm",
        "Unintentional presence of chemical individuals on the surface / Impurities Metalic",
    ],
    [
        "Elongated or not",
        "Length: > 5000 nm",
        "Unintentional presence of chemical individuals on the surface / Impurities Metalic",
        "< -30, 30 > mV",
    ],
    [
        "Soluble or not",
        "Spheroidal 10 - 50 nm",
        "Unintentional presence of chemical individuals on the surface / Impurities Metalic",
        "< -30, 30 > mV",
    ],
]


for i, p in enumerate(pairs):
    ins = Probability(data, p)
    print(ins.condition)
    print(i + 1, ins.calc_proba)
"""
