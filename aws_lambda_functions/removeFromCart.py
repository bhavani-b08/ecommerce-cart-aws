import boto3
import json

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CartTable')

def lambda_handler(event, context):
    print("Received Event:", json.dumps(event))  # Debugging log

    headers = {
        "Access-Control-Allow-Origin": "*",  # Allow all origins
        "Access-Control-Allow-Methods": "OPTIONS, POST, GET, DELETE",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # Ensure the request body is present
    body = event.get('body', '{}')

    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'message': 'Invalid JSON format'})
        }

    # Extract parameters
    user_id = body.get('userId')
    product_id = body.get('productId')

    if not user_id or not product_id:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'message': 'Both userId and productId are required'})
        }

    try:
        # Fetch the current quantity from the cart
        response = table.get_item(Key={'userId': user_id, 'productId': product_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'Item not found in cart'})
            }

        current_quantity = response['Item'].get('quantity', 1)

        if current_quantity > 1:
            # Reduce the quantity by 1
            table.update_item(
                Key={'userId': user_id, 'productId': product_id},
                UpdateExpression="SET quantity = quantity - :val",
                ExpressionAttributeValues={":val": 1}
            )
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Quantity decreased by 1'})
            }
        else:
            # Remove item from the cart
            table.delete_item(Key={'userId': user_id, 'productId': product_id})
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Item removed from cart'})
            }
    except Exception as e:
        print("Error:", str(e))  # Log the error
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
