
def profiling_categoricals(df):
    """Profiling a numerical dataframe

    Args:
        df (dataframe): 

    Raises:
        RuntimeError: Error

    Returns:
        dataframe: A dataframe with categorical profiling
    """
    types = df.dtypes
    missing  = round( ( df.isnull().sum() / df.shape[0] ), 3) * 100
    uniques = df.apply(lambda x: x.unique())
    return pd.DataFrame({'Types:': types,
                         'Missings%': missing,
                         'Uniques': uniques})
