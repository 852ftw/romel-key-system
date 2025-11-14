from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "users.json"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    key = data.get("key", "").strip()

    if not key:
        return jsonify({"valid": False, "error": "Key vazia"}), 400

    users = load_users()
    for user_id, info in users.items():
        if info["key"] == key:
            return jsonify({
                "valid": True,
                "webhook": info["webhook"]
            })

    return jsonify({"valid": False, "error": "Key inválida"}), 404

@app.route('/')
def home():
    return "API do Romel Key System - ONLINE"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
