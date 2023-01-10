from time import sleep, time

import boto3
import click


def waiter(func):
    def wrapper(*args, **kwargs):
        sleep(10)
        return func(*args, **kwargs)
    return wrapper

def restore_table(
                client,
                SnapshotIdentifier,
                SourceSchemaName,
                SourceTableName,
                TargetSchemaName,
                NewTableName,
                ClusterIdentifier='bi-microservices-dm',
                DatabaseName='datamart'
                ):
    response = client.restore_table_from_cluster_snapshot(
        ClusterIdentifier=ClusterIdentifier,
        SnapshotIdentifier=SnapshotIdentifier,
        SourceDatabaseName=DatabaseName,
        SourceSchemaName=SourceSchemaName,
        SourceTableName=SourceTableName,
        TargetDatabaseName=DatabaseName,
        TargetSchemaName=TargetSchemaName,
        NewTableName=NewTableName,
        EnableCaseSensitiveIdentifier=False)
    return response.get('TableRestoreStatus',{}).get('TableRestoreRequestId','')

@waiter
def get_restore_status(client, TableRestoreRequestId, ClusterIdentifier='bi-microservices-dm'):
    status = client.describe_table_restore_status(
        ClusterIdentifier=ClusterIdentifier,
        TableRestoreRequestId=TableRestoreRequestId
    )
    return status.get('TableRestoreStatusDetails',[{}])[0].get('Status','UNKNOWN')


"python app.py --access_key=\"${}\" --secret_key=\"${}\" --snapshot-identifier=\"${}\" --source-schema=\"${}\" --source-table=\"${}\" --target-schema=\"${}\" --target-table=\"${}\""
@click.command()
@click.option('--access_key', required=True, type=str, hide_input=True)
@click.option('--secret_key', required=True, type=str, hide_input=True)
@click.option('--snapshot-identifier', required=True, type=str)
@click.option('--source-schema', required=True, type=str)
@click.option('--source-table', required=True, type=str)
@click.option('--target-schema', required=True, type=str)
@click.option('--target-table', required=True, type=str)
def main(*args, **kwargs):
    ACCESS_KEY = kwargs['access_key']
    SECRET_KEY = kwargs['secret_key']
    ClusterIdentifier = 'bi-microservices-dm'
    DatabaseName = 'datamart'
    SnapshotIdentifier = kwargs['snapshot_identifier']
    SourceSchemaName = kwargs['source_schema']
    SourceTableName = kwargs['source_table']
    TargetSchemaName = kwargs['target_schema']
    NewTableName = kwargs['target_table']
    client = boto3.client(
        'redshift',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    TableRestoreRequestId = restore_table(client,SnapshotIdentifier,SourceSchemaName,SourceTableName,TargetSchemaName,NewTableName)
    max_timeout_s = 3
    start_time = time()
    while True:
        status = get_restore_status(client, ClusterIdentifier, TableRestoreRequestId)
        if status in ['SUCCEEDED','FAILED','CANCELED']:
            print(status)
            break
        if (time() - start_time) > max_timeout_s:
            print(f'Timeout com status {status}')
            break
