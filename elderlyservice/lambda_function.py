# Onno: Needed to turn 'get' in to FaaS, not used if we only deploy locally
from elderly_service import get_elderly_user
import json

def lambda_handler(event, context):
    elderly_id = int(event['pathParameters']['elderly_id'])
    body, status_code = get_elderly_user(elderly_id)
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
