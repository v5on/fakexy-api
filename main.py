from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

def scrape_fakexy(country_code: str):
    url = f"https://www.fakexy.com/fake-address-generator-{country_code.lower()}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return {"error": f"Invalid country code or site unavailable: {country_code}"}

        soup = BeautifulSoup(res.text, 'html.parser')

        tables = soup.find_all("table", class_="table")
        if len(tables) < 3:
            return {"error": "Not enough data tables found in page"}

        # 1st table: Address
        address_rows = tables[0].find_all("tr")
        data = {}
        for row in address_rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                data[cols[0].text.strip()] = cols[1].text.strip()

        # 2nd table: Matched Person
        for row in tables[1].find_all("tr"):
            cols = row.find_all("td")
            if len(cols) == 2:
                data[cols[0].text.strip()] = cols[1].text.strip()

        # 3rd table: Credit Card Info
        for row in tables[2].find_all("tr"):
            cols = row.find_all("td")
            if len(cols) == 2:
                data[cols[0].text.strip()] = cols[1].text.strip()

        return data

    except Exception as e:
        return {"error": str(e)}

@app.get("/scrape/{country_code}")
def get_fake_data(country_code: str):
    data = scrape_fakexy(country_code)
    return JSONResponse(content=data)
