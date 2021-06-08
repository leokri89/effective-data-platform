
from datetime import datetime

import pandas as pd


def datetime_convert(year, month, day):
    try:
        return datetime(year=int(year), month=int(month), day=int(day))
    except:
        return datetime(year=1900, month=1, day=1)


df = pd.DataFrame({ 'col1': ['20210115','20210116','20210117','20210118'] })
df['DATPRG'] = df['DATPRG'].apply(lambda x: datetime_convert(x[:4], x[4:6], x[6:8]))