import json
import os
import random

DATA_DIR = "data"
KEY_DIR = "key"

def is_valid_api_key(provided_key: str) -> bool:
    if not provided_key or not os.path.exists(KEY_DIR):
        return False

    for filename in os.listdir(KEY_DIR):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(KEY_DIR, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("api_key") == provided_key:
                        return True
            except:
                continue
    return False

def handler(request):
    params = request.get("queryStringParameters", {})
    api_key = params.get("key")
    if not is_valid_api_key(api_key):
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Invalid or missing API key"})
        }

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
