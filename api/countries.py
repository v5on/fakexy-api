import os
import json

DATA_DIR = "data"

def handler(request):
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
