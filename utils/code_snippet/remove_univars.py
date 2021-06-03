
import pandas as pd

def remove_univars(dataframe):
    nunique_res = dataframe.nunique()
    to_remove = [n for n, v in enumerate(nunique_res) if v == 1 ]
    dataframe.drop(to_remove, axis=1, inplace=True)
    return dataframe

geral = remove_univars(geral)
