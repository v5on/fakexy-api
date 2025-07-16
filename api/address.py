import json
import os
import random

DATA_DIR = "data"

def handler(request):
    params = request.get("queryStringParameters", {})
    country_code = params.get("country_code", "").lower()
    filename = f"{country_code}.json"
    file_path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(file_path):
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Country code not found"})
        }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list) or len(data) == 0:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "No addresses found"})
                }
            random_address = random.choice(data)
            return {
                "statusCode": 200,
                "body": json.dumps(random_address)
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to load data: {str(e)}"})
        }
