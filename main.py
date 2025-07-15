from flask import Flask, jsonify
import os
import json
import random

app = Flask(__name__)

DATA_DIR = "data"

@app.route('/api/address/<country_code>', methods=['GET'])
def get_random_address(country_code):
    file_path = os.path.join(DATA_DIR, f"{country_code.upper()}.json")
    
    if not os.path.exists(file_path):
        return jsonify({"error": "Country code not found"}), 404

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # ফাইলে একটা মাত্র টপ-লেভেল key থাকবে – দেশের নাম
        country_keys = list(data.keys())
        if not country_keys:
            return jsonify({"error": "No country data found"}), 404
        
        addresses = data[country_keys[0]]
        
        if not isinstance(addresses, list) or len(addresses) == 0:
            return jsonify({"error": "No addresses found"}), 404

        random_address = random.choice(addresses)
        return jsonify(random_address)

    except Exception as e:
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
