import boto3
import datetime
import os
import uuid
import time

def lambda_handler(event, context):
    output = ""
    number = int(event['queryStringParameters']['number'])
    if number % 3 == 0:
        output += "fizz"
    if number % 5 == 0:
        output += "buzz"

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": "Brett Powell, {}".format(output)
    }
    #Creating new record in DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    # Getting which table to write to
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    table.put_item(
        Item={
            # Making a unique ID
            'id' : str(uuid.uuid4()),
            # Date stamp
            'time' : datetime.date.today().strftime("%m-%d-%y"),
            # Number that was passed in
            'input' : number,
            # Response including fizz/buzz/fizzbuzz
            'response' : resp
        }
    )
    return resp
