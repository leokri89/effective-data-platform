import boto3

def handler(event, context):
    session = boto3.Session()

    dynamo = session.client('dynamodb')
    res = dynamo.get_item(
        TableName='check',
        Key={
            'key': {'N' : '0'}
        }
    )
    print(res)


handler('event','context')