
import pandas as pd

def remove_highcardinality(dataframe):
    nunique_res = dataframe.nunique()
    to_remove = [n for n, v in enumerate(nunique_res) if (float(v) / dataframe.shape[0]) * 100 <= 0.1]
    dataframe.drop(columns=dataframe.columns[to_remove], axis=1, inplace=True)
    return dataframe

geral = remove_highcardinality(geral)