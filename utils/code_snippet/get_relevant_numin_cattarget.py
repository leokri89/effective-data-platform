
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, SelectPercentile, f_regression, f_classif

X, y = make_classification(n_samples=100, n_features=20, n_informative=2)

def get_relevant_numin_cattarget(X, y, percentage_features=90, absolute_features=None):
    if absolute_features:
        if absolute_features > len(X.columns):
            absolute_features = len(X.columns)
        fs = SelectKBest(score_func=f_classif, k=absolute_features)
    else:    
        fs = SelectPercentile(score_func=f_classif, percentile=percentage_features)
    
    fs.fit(X, y)
    data = [[X.columns[n], v, fs.scores_[n], fs.pvalues_[n]] for n, v in enumerate(fs.get_support())]
    result = pd.DataFrame(data , columns=['column','selected','score','pvalue'])
    return result

get_relevant_numin_cattarget(pd.DataFrame(X), y, 10)
