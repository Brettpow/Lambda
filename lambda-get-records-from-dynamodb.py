import boto3
import datetime
import os
import uuid
import time

from boto3.dynamodb.conditions import Attr

# Variables passed in from apigateway are under event
def lambda_handler(event, context):

    #Creating new record in DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    if event.get('queryStringParameters').get('date', False):
        arg = event['queryStringParameters']['date']
        entry = table.scan(
            FilterExpression=Attr('time').eq(arg)
        )
        item = entry['Items']
    if event.get('queryStringParameters').get('id', False):
        arg = event['queryStringParameters']['id']
        if arg=="*":
            entry = table.scan()
            itme = entry['Items']
        else:
            entry = table.get_item(
                Key={
                    'id': event['queryStringParameters']['id']
                }
            )
            item = entry['Item']
    if not event.get('queryStringParameters', False):
        arg = "Failed to pass arg"
        item = "empty"
    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": "Output from {}: {}".format(arg, item)
    }
    return resp
