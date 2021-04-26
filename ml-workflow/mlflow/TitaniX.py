
"""
Para iniciar o servidor de MLFLOW execute o seguinte comando:
mlflow server ^
--backend-store-uri sqlite:///mlflow.db ^
--default-artifact-root s3://lk-lambda-functions/mlflow/ ^
--host 0.0.0.0

Requisitos:
- Credenciais da AWS configurada com acesso ao Bucket de artefatos
- URL com credenciais de acesso ao banco de dados de metadata

Variaveis de ambiente
- export AWS_DEFAULT_REGION=my_region
- export AWS_ACCESS_KEY_ID=access_key
- export AWS_SECRET_ACCESS_KEY=secret_key

Referencia
- https://www.mlflow.org/docs/latest/tracking.html#mlflow-tracking-servers
"""

import pickle

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import accuracy_score

import mlflow

def main():
    remote_server_uri = "http://localhost:5000"
    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment("/TitaniX")

    dpath = r"F:\DataScience\mlflow\titanic\train.csv"
    data = pd.read_csv(dpath)

    with mlflow.start_run():
        feature = ['Pclass','Sex','SibSp','Parch']

        X = pd.get_dummies(data[feature].copy())
        y = data['Survived'].copy()

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        model = LogisticRegressionCV(cv=10)
        model.fit(X_train, y_train)
        
        log_validation(model, X_test, y_test)


def log_validation(model, X_test, y_test):
    predictions = model.predict(X_test)
    val_score = accuracy_score(y_test, predictions)

    params = model.get_params()
    for k, item in enumerate(feature):
        params['coef_' + item] = model.coef_[0][k]

    params['final'] = 1
    mlflow.log_metric("validation score", val_score)
    mlflow.log_params(params)

    pickle.dump(model, open('model.pkl', 'wb'))
    mlflow.log_artifacts("F:\\DataScience\\mlflow\\titanic\\", artifact_path='dataset')
    mlflow.sklearn.log_model(model, 'model')


if __name__ == "__main__":
    main()
    