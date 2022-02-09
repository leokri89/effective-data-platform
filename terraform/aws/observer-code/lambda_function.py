import json
import boto3
import os


def lambda_handler(event, context):
    try:
        client = boto3.client('sns')

        for record in event['Records']:
            key = record.get('s3').get('object').get('key')
            bucket = record.get('s3').get('bucket').get('name')
            command = record.get('eventName')

            client.publish(
                TopicArn=[value for item, value in os.environ.items() if item.lower() == 'topicarn'][0],
                Message=json.dumps(record),
                MessageAttributes={
                    'key': {'DataType':'String', 'StringValue':key},
                    'bucket': {'DataType':'String', 'StringValue':bucket},
                    'command': {'DataType':'String', 'StringValue':command}
                    }
            )
        return {
            'statusCode': 200,
            'message': 'ok'
            }
    except Exception as e:
        return {
            'statusCode': 404,
            'message': str(e)
            }

        