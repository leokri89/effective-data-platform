
def value_mapper(df, fieldlist, value_dict):
    for col in fieldlist:
        df[col] = df[col].map(value_dict).fillna(0)
    return df

workset = value_mapper(workset,
                       ['ExterQual','ExterCond','BsmtQual','BsmtCond','HeatingQC','KitchenQual','FireplaceQu','GarageQual','GarageCond'],
                       {'Po':1,'Fa': 2,'TA': 3,'Gd': 4,'Ex': 5})

workset = value_mapper(workset,
                       ['BsmtFinType1','BsmtFinType2'],
                       {'GLQ': 6,'ALQ': 5,'BLQ': 4, 'Rec': 3, 'LwQ': 2, 'UnF': 1, 'NA': 0})

workset = value_mapper(workset,
                       ['GarageFinish'],
                       {'Fin': 3, 'RFn': 2, 'UnF': 1, 'NA': 0})

workset = value_mapper(workset,
                       ['CentralAir'],
                       {'Y': 1, 'N': 0})
