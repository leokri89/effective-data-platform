import sys
import time
import json
import boto3


from botocore.exceptions import ClientError


def redshift_execute_statement(client, bu, cluster_identifier, sql):
    try:
        execute_response = client.execute_statement(
            ClusterIdentifier=cluster_identifier,
            Database=f'{bu}_sandbox',
            DbUser=f'{bu}_user',
            Sql=sql
        )
    except ClientError as e:
        print(f'ERROR: {e}')
        return None
    else:
        return execute_response


def get_query_status(client, query_id):
    try:
        describe_response = client.describe_statement(Id=query_id)
    except ClientError as e:
        print(f'ERROR: {e}')
        return None
    else:
        return describe_response


def create_user(client, bu, usernames, superuser, cluster_identifier):

    for username in usernames:

        if superuser:
            queries = [
                f"CREATE USER {username} PASSWORD 'Mudar_123' CREATEUSER;"
            ]
        else:
            queries = [
                f"CREATE USER {username} WITH PASSWORD 'Mudar_123';",
                f"ALTER GROUP {bu}_group ADD USER {username};",
                f"ALTER DEFAULT PRIVILEGES FOR USER {username} GRANT ALL PRIVILEGES ON TABLES TO GROUP {bu}_group;"
            ]

        for query in queries:

            execute_response = redshift_execute_statement(
                client, bu, cluster_identifier, query)

            if execute_response is not None:
                query_status = get_query_status(
                    client, execute_response["Id"])
                if 'PASSWORD' in query:
                    print(
                        f'Running query:\n{query.replace("Mudar_123", "********")}')
                else:
                    print(f'Running query:\n{query}')

            while query_status["Status"] == "STARTED" or query_status["Status"] == "SUBMITTED" or query_status["Status"] == "PICKED":
                time.sleep(2)
                query_status = get_query_status(
                    client, execute_response["Id"])
                if query_status is not None:
                    print(f'Query status: {query_status["Status"]}')
                    if query_status["Status"] == "FAILED":
                        print(query_status["Error"])
                        raise Exception({query_status["Error"]})


def reset_user_password(client, bu, usernames, cluster_identifier):
    for username in usernames:

        query = f"ALTER USER {username} PASSWORD 'Mudar_123';"

        execute_response = redshift_execute_statement(
            client, bu, cluster_identifier, query)

        if execute_response is not None:

            query_status = get_query_status(client, execute_response["Id"])

            if 'PASSWORD' in query:
                print(
                    f'Running query:\n{query.replace("Mudar_123", "********")}')
            else:
                print(f'Running query:\n{query}')

            while query_status["Status"] == "STARTED" or query_status["Status"] == "SUBMITTED" or query_status["Status"] == "PICKED":
                time.sleep(2)
                query_status = get_query_status(client, execute_response["Id"])
                if query_status is not None:
                    print(f'Query status: {query_status["Status"]}')
                    if query_status["Status"] == "FAILED":
                        print(query_status["Error"])
                        raise Exception({query_status["Error"]})


def disable_user(client, bu, usernames, cluster_identifier):
    for username in usernames:
        query = f"ALTER USER {username} PASSWORD DISABLE;"
        execute_response = redshift_execute_statement(
            client, bu, cluster_identifier, query)
        if execute_response is not None:
            query_status = get_query_status(client, execute_response["Id"])
            print(f'Running query:\n{query}')
            while query_status["Status"] == "STARTED" or query_status["Status"] == "SUBMITTED" or query_status["Status"] == "PICKED":
                time.sleep(2)
                query_status = get_query_status(
                    client, execute_response["Id"])
                if query_status is not None:
                    print(f'Query status: {query_status["Status"]}')
                    if query_status["Status"] == "FAILED":
                        print(query_status["Error"])
                        raise Exception({query_status["Error"]})


def main():
    bu = sys.argv[1]
    usernames = sys.argv[2].replace(" ", "").split(",")
    operation = sys.argv[3]
    superuser = eval(sys.argv[4].capitalize())

    cluster_identifier = f"taurus-sandbox-{bu}"

    client = boto3.client(
        'redshift-data', region_name='us-east-1', verify=True)

    if operation == 'create':
        create_user(client, bu, usernames, superuser, cluster_identifier)
    elif operation == 'reset':
        reset_user_password(client, bu, usernames, cluster_identifier)
    elif operation == 'disable':
        disable_user(client, bu, usernames, cluster_identifier)
    else:
        print("Unknow operation")


if __name__ == "__main__":
    main()
