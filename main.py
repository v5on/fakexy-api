from flask import Flask, jsonify, request, render_template
from collections import OrderedDict
import json
import random
import os

app = Flask(__name__)

# Constants
API_OWNER = "Mahir Labib"
API_UPDATES = "https://t.me/bro_bin_lagbe"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/address', methods=['GET'])
def get_address():
    country_code = request.args.get('code', '').upper()

    if not country_code:
        return jsonify({
            "error": "Country code is required",
            "api_owner": API_OWNER,
            "api_updates": API_UPDATES
        }), 400

    file_path = os.path.join('data', f"{country_code.lower()}.json")

    try:
        with open(file_path, 'r') as file:
            addresses = json.load(file, object_pairs_hook=OrderedDict)  # 👈 এখানেই ম্যাজিক

        if not addresses:
            return jsonify({
                "error": "No addresses found for this country code",
                "api_owner": API_OWNER,
                "api_updates": API_UPDATES
            }), 404

        raw = random.choice(addresses)

        # Add owner info at the top
        response_data = OrderedDict()
        response_data["api_owner"] = API_OWNER
        response_data["api_updates"] = API_UPDATES

        for key, value in raw.items():
            response_data[key] = value  # 😎 Preserve exact order

        return jsonify(response_data)

    except FileNotFoundError:
        return jsonify({
            "error": "Country code not found",
            "api_owner": API_OWNER,
            "api_updates": API_UPDATES
        }), 404

    except Exception as e:
        return jsonify({
            "error": str(e),
            "api_owner": API_OWNER,
            "api_updates": API_UPDATES
        }), 500

@app.route('/api/countries', methods=['GET'])
def get_country_list():
    data_dir = 'data'
    country_list = []

    try:
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                country_code = filename.replace('.json', '').upper()
                with open(os.path.join(data_dir, filename), 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0 and "country" in data[0]:
                        country_name = data[0]["country"]
                    else:
                        country_name = country_code  # fallback
                    country_list.append({
                        "country": country_name,
                        "country_code": country_code
                    })

        return jsonify({
            "total": len(country_list),
            "countries": country_list,
            "api_owner": API_OWNER,
            "api_updates": API_UPDATES
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "api_owner": API_OWNER,
            "api_updates": API_UPDATES
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error</title>
        <style>
            body {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                color: #333;
            }
            .error-message {
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="error-message">Error: Wrong Endpoint</div>
    </body>
    </html>
    ''', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
