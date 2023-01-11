import pandas as pd
import smogn


def synth_smoth(
        data: pd.DataFrame, y: str, samp_method: str = "extreme", rel_coef: float = 1.5
) -> pd.DataFrame:
    df2 = data.reset_index()
    smogn_set = smogn.smoter(data=df2, y=y, samp_method=samp_method, rel_coef=rel_coef)
    index = smogn_set.columns[0]
    smogn_set[index] = [
        str(j) + "_smogn_" + str(i) for i, j in zip(smogn_set.index, smogn_set["index"])
    ]
    smogn_set.set_index(index, inplace=True)
    return smogn_set
