from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder=".", static_url_path="")

API_URL = "https://spam-saroj.vercel.app/spam"
API_KEY = os.getenv("SAROJ_API_KEY", "SAROJ")
TIMEOUT = 30

@app.get("/")
def index():
    return send_from_directory(".", "index.html")

@app.get("/api/spam")
def spam_proxy():
    uid = request.args.get("uid", "").strip()
    server_name = request.args.get("server_name", "ind").strip().lower()

    if not uid:
        return jsonify({"status": "error", "message": "UID is required"}), 400

    if len(uid) > 64:
        return jsonify({"status": "error", "message": "UID is too long"}), 400

    params = {
        "uid": uid,
        "server_name": server_name,
        "key": API_KEY,
    }

    try:
        r = requests.get(API_URL, params=params, timeout=TIMEOUT)
        try:
            data = r.json()
        except ValueError:
            data = {"raw_response": r.text}

        return jsonify(data), r.status_code

    except requests.RequestException as exc:
        return jsonify({
            "status": "error",
            "message": "Unable to reach upstream API",
            "details": str(exc),
        }), 502

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
