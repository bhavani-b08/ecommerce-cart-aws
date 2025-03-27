import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("CartTable")

def lambda_handler(event, context):
    user_id = event["queryStringParameters"]["userId"]
    
    # Query DynamoDB to get items for the given user
    response = table.query(
        KeyConditionExpression="userId = :uid",
        ExpressionAttributeValues={":uid": user_id}
    )

    items = response.get("Items", [])
    
    # Calculate total cart count
    cart_count = sum(int(item.get("quantity", 1)) for item in items)  # Convert quantity to int
    print("Items found:", len(response["Items"]))
    return {
    "statusCode": 200,
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    },
    "body": json.dumps({"cartCount": cart_count})
}
