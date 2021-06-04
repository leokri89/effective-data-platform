
def clean_null_columns(df, threshold):
    """Profiling a numerical dataframe

    Args:
        df (dataframe): 

    Raises:
        RuntimeError: Error

    Returns:
        dataframe: A dataframe without columns above threshold of null
    """
    col_list = (~(df.isnull().sum() / df.shape[0]  * 100 > threshold)).tolist()
    return df.iloc[:,col_list].copy()

workset = clean_null_columns(df, 80)
