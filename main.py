from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from collections import OrderedDict
import os, json, random

app = FastAPI()

API_OWNER = "Mahir Labib"
API_UPDATES = "https://t.me/bro_bin_lagbe"

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set templates folder
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/address")
def get_address(code: str = Query(...)):
    file_path = os.path.join("data", f"{code.lower()}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Country code not found")

    with open(file_path, "r", encoding="utf-8") as f:
        addresses = json.load(f, object_pairs_hook=OrderedDict)

    if not addresses:
        raise HTTPException(status_code=404, detail="No addresses found for this country")

    raw = random.choice(addresses)

    result = OrderedDict()
    result["api_owner"] = API_OWNER
    result["api_updates"] = API_UPDATES
    for key, val in raw.items():
        result[key] = val

    return JSONResponse(content=result)


@app.get("/api/countries")
def get_country_list():
    data_dir = "data"
    country_list = []

    try:
        for filename in os.listdir(data_dir):
            if filename.endswith(".json"):
                code = filename.replace(".json", "").upper()
                with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    country_name = data[0]["country"] if data and "country" in data[0] else code
                    country_list.append({
                        "country": country_name,
                        "country_code": code
                    })

        return {
            "total": len(country_list),
            "countries": country_list,
            "api_owner": API_OWNER,
            "api_updates": API_UPDATES
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
