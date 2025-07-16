from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import os
import json
import random

app = FastAPI()
DATA_DIR = "data"
KEY_DIR = "key"

def is_valid_api_key(provided_key: str) -> bool:
    if not provided_key:
        return False

    if not os.path.exists(KEY_DIR):
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

@app.get("/api/address/{country_code}")
def get_random_address(country_code: str, request: Request):
    api_key = request.query_params.get("key")
    if not is_valid_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    filename = f"{country_code.lower()}.json"
    file_path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Country code not found")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list) or len(data) == 0:
            raise HTTPException(status_code=404, detail="No addresses found")

        random_address = random.choice(data)
        return JSONResponse(content=random_address)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

@app.get("/api/countries")
def list_countries(request: Request):
    api_key = request.query_params.get("key")
    if not is_valid_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    if not os.path.exists(DATA_DIR):
        raise HTTPException(status_code=500, detail="Data directory not found")

    countries_info = []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(DATA_DIR, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
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
        "total": len(countries_info),
        "countries": countries_info
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
