import os
import json

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

    countries_info = []

    if not os.path.exists(DATA_DIR):
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Data directory not found"})
        }

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            path = os.path.join(DATA_DIR, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        first_entry = data[0]
                        countries_info.append({
                            "country": first_entry.get("country", "Unknown"),
                            "country_code": first_entry.get("country_code", filename.replace(".json", "").upper())
                        })
            except:
                continue

    return {
        "statusCode": 200,
        "body": json.dumps({
            "total": len(countries_info),
            "countries": countries_info
        })
    }
