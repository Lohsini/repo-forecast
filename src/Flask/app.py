import os
from flask import Flask, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Cloud Run Notebook URL that generates charts
NOTEBOOK_API_URL = os.environ.get("NOTEBOOK_API_URL")


@app.route("/")
def home():
    return "Welcome to the Forecast Microservice API. Use /api/forecast to run predictions."


@app.route("/api/forecast", methods=["GET"])
def trigger_forecast():
    try:
        res = requests.get(NOTEBOOK_API_URL)
        if res.status_code != 200:
            return jsonify({"error": "Notebook failed", "details": res.text}), 500

        notebook_output = res.json()
        return jsonify({
            "message": "Forecast completed via notebook",
            "images": notebook_output.get("uploaded_images", {})
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
