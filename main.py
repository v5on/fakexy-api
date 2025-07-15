from flask import Flask, jsonify
import os
import json
import random

app = Flask(__name__)
DATA_DIR = "data"

@app.route('/api/address/<country_code>', methods=['GET'])
def get_random_address(country_code):
    filename = f"{country_code.lower()}.json"  # এখানে ছোট হাতে করলাম
    file_path = os.path.join(DATA_DIR, filename)

    print(f"Looking for: {file_path}")  # debug output

    if not os.path.exists(file_path):
        return jsonify({"error": "Country code not found"}), 404

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list) or len(data) == 0:
            return jsonify({"error": "No addresses found"}), 404

        random_address = random.choice(data)
        return jsonify(random_address)

    except Exception as e:
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
