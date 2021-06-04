
import pandas as pd

def outlier_calc(x):
    return (x<(x.quantile(0.25)-1.5*(x.quantile(0.75)-x.quantile(0.25))))|\
           (x>(x.quantile(0.75)+1.5*(x.quantile(0.75)-x.quantile(0.25))))

def profiling_numericals(df):
    """Profiling a numerical dataframe

    Args:
        df (dataframe): 

    Raises:
        RuntimeError: Error

    Returns:
        dataframe: A dataframe with numerical profiling
    """
    types = df.dtypes
    missing  = round( ( df.isnull().sum() / df.shape[0] ), 3) * 100
    min = df.apply(lambda x: round(x.min()))
    max = df.apply(lambda x: round(x.max()))
    mean = df.apply(lambda x: round(x.mean()))
    outliers= df.apply(lambda x: sum(outlier_calc(x)))
    return pd.DataFrame({'Types:':types,
                        'Missings%':missing,
                        'Min#': min,
                        'Max#': max,'mean': mean,
                        'Outliers#':outliers}).transpose()
