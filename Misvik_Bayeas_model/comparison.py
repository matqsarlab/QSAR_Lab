#!/usr/bin/env python

import numpy as np
import pandas as pd


def observe(obs):
    obs_val = obs.loc[:, "y"].to_dict()
    # ton = tox or not
    ton = np.where(np.array(list(obs_val.values())) == 1, "Toxic", "Non-Toxic")

    table = pd.DataFrame(data=ton, index=obs_val.keys(), columns=["Observed Toxicity"])
    return table


def compare(obs, pred):
    def highlight_col(x):
        # copy df to new - original data are not changed
        df = x.copy()
        # set by condition
        mask1 = np.where(
            (df["Observed Toxicity"] == "Toxic")
            & (df["Predicted Toxicity"] == "Non-Toxic"),
            True,
            False,
        )
        mask2 = np.where(
            (df["Observed Toxicity"] == "Non-Toxic")
            & (df["Predicted Toxicity"] == "Toxic"),
            True,
            False,
        )
        d = {"Observed Toxicity": [], "Predicted Toxicity": []}
        for m1, m2 in zip(mask1, mask2):

            if m1 == False and m2 == False:
                d["Observed Toxicity"].append("background-color: white")
                d["Predicted Toxicity"].append("background-color: white")
            elif m1 == True:
                d["Observed Toxicity"].append("background-color: plum")
                d["Predicted Toxicity"].append("background-color: plum")
            elif m2 == True:
                d["Observed Toxicity"].append("background-color: cornflowerblue")
                d["Predicted Toxicity"].append("background-color: cornflowerblue")

        mask = pd.DataFrame(
            data=d,
            index=df.index,
        )
        return mask

    table = pd.concat([observe(obs), pred], axis=1)
    return table.style.apply(highlight_col, axis=None)
