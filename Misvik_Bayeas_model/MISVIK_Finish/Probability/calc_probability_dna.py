#!/usr/bin/env python
import pandas as pd
from QSAR_Lab.Misvik_Bayeas_model.calc_proba import Probability


def run_proba(data, name):
    print("-- " * 28, f"\n{name}\n" + "-- " * 28)
    for i, p in enumerate(pairs):
        ins = Probability(data, p)
        print(i + 1, ins.calc_proba)
    print("-- " * 28, "\n")
    return 0


pairs = [
    ["Soluble or not"],
    ["Spheroidal < 10nm"],
    ["Highly soluble"],
    ["Spheroidal 10 - 50 nm"],
    ["Elongated or not"],
    ["Soluble or not", "Elongated or not"],
    ["Soluble or not", "Highly soluble"],
    ["Spheroidal < 10nm", "Soluble or not"],
    ["Soluble or not", "Elongated or not", "Highly soluble"],
    ["Spheroidal < 10nm", "Soluble or not", "Highly soluble"],
    ["Elongated Length: > 5000 nm"],
    ["Soluble or not", "Spheroidal 10 - 50 nm", "Highly soluble"],
    ["Elongated or not", "Elongated Length: > 5000 nm"],
    [
        "Soluble or not",
        "Highly soluble",
        "Spheroidal 10 - 50 nm",
        "Unintentional presence of chemical individuals on the surface / Impurities Metalic",
    ],
    [
        "Elongated or not",
        "Elongated Length: > 5000 nm",
        "Unintentional presence of chemical individuals on the surface / Impurities Metalic",
    ],
    [
        "Elongated or not",
        "Elongated Length: > 5000 nm",
        "Unintentional presence of chemical individuals on the surface / Impurities Metalic",
        "< -30, 30 > mV",
    ],
    [
        "Soluble or not",
        "Highly soluble",
        "Spheroidal 10 - 50 nm",
        "Unintentional presence of chemical individuals on the surface / Impurities Metalic",
        "< -30, 30 > mV",
    ],
]

a549 = pd.read_excel("./Data/a549_data_dna.xlsx", sheet_name=0, index_col=0)
beas = pd.read_excel("./Data/beas_data_dna.xlsx", sheet_name=0, index_col=0)
hep72 = pd.read_excel("./Data/hepg2_data_dna.xlsx", sheet_name=0, index_col=0)

run_proba(a549, "A549")
run_proba(beas, "BEAS")
run_proba(hep72, "HepG2")
