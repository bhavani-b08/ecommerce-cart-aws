import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("CartTable")  

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"]) if "body" in event and isinstance(event["body"], str) else event["body"]

        user_id = body.get("userId")
        product_id = body.get("productId")
        quantity = body.get("quantity", 1)

        if not user_id or not product_id:
            return {
                "statusCode": 400,
                "headers": {  
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({"error": "Missing userId or productId"})
            }

        # ✅ Update quantity if item exists, otherwise insert new item
        table.update_item(
            Key={"userId": user_id, "productId": product_id},
            UpdateExpression="SET quantity = if_not_exists(quantity, :start) + :inc",
            ExpressionAttributeValues={
                ":start": 0,
                ":inc": quantity
            },
            ReturnValues="UPDATED_NEW"
        )

        return {
            "statusCode": 200,
            "headers": {  
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "Item added to cart!"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {  
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": str(e)})
        }
