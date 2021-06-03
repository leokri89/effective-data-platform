
from sklearn.feature_selection import SelectKBest, SelectPercentile, f_regression

def get_relevant_numin_numtarget(X, y, percentage_features=90, absolute_features=None):    
    if absolute_features:
        if absolute_features > len(X.columns):
            absolute_features = len(X.columns)
        fs = SelectKBest(score_func=f_regression, k=absolute_features)
    else:    
        fs = SelectPercentile(score_func=f_regression, percentile=percentage_features)
    
    fs.fit(X, y)
    data = [[X.columns[n], v, fs.scores_[n], fs.pvalues_[n]] for n, v in enumerate(fs.get_support())]
    result = pd.DataFrame(data , columns=['column','selected','score','pvalue'])
    return result

teste = geral[~geral['SalePrice'].isna()]

#get 20 features of relevant features in data
get_relevant_numin_numtarget(teste[var_numerica].fillna(0), teste['SalePrice'], absolute_features=20)

#Get 90% of relevant features in data
get_relevant_numin_numtarget(teste[var_numerica].fillna(0), teste['SalePrice'], percentage_features=90)

