import os

def check_namespaces_exists():
    with os.popen('kubectl get namespaces') as stream:
        cmd_result = stream.read()
    return cmd_result


def create_namespace():
    with os.popen('kubectl create namespace airflow') as stream:
        cmd_result = stream.read()
    return cmd_result


def check_helm_repo():
    with os.popen('helm version') as stream:
        cmd_result = stream.read()
    return cmd_result


def add_helm_repo():
    with os.popen('helm repo add apache-airflow https://airflow.apache.org') as stream:
        cmd_result = stream.read()
    return cmd_result


def update_helm_repo():
    with os.popen('helm repo update') as stream:
        cmd_result = stream.read()
    return cmd_result


def search_helm_airflow():
    with os.popen('helm search repo airflow') as stream:
        cmd_result = stream.read()
    return cmd_result


def install_helm_airflow():
    with os.popen('helm install airflow apache-airflow/airflow --namespace airflow --debug') as stream:
        cmd_result = stream.read()
    return cmd_result


def generate_values_yaml():
    with os.popen('helm show values apache-airflow/airflow > values.yaml') as stream:
        cmd_result = stream.read()
    return cmd_result


def upgrade_from_values():
    with os.popen('helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug') as stream:
        cmd_result = stream.read()
    return cmd_result