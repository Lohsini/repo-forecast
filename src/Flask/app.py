import os
from flask import Flask, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

NOTEBOOK_API_URL = os.environ.get("NOTEBOOK_API_URL")


def organize_forecast_data(uploaded_images):
    organized = {}
    for model, urls in uploaded_images.items():
        organized[model] = {}

        for url in urls:
            filename = url.split("/")[-1]

            if model == "charts":
                organized[model][filename] = {
                    "main": url,
                    "children": {}
                }
                continue

            if (
                filename.endswith("_forecast.png")
                and filename.count("_") <= 3
            ):
                organized[model][filename] = {
                    "main": url,
                    "children": {}
                }
                continue

            if "_forecast_" in filename:
                base_key = filename.split("_forecast_")[0] + "_forecast.png"
                repo_key = filename.replace(base_key.replace(
                    ".png", "_"), "").replace(".png", "")
                organized[model].setdefault(
                    base_key, {"main": None, "children": {}})
                organized[model][base_key]["children"][repo_key] = url
            else:
                organized[model][filename] = {
                    "main": None,
                    "children": {}
                }

    return organized


@app.route("/")
def home():
    return "Welcome to the Forecast Microservice API. Use /api/forecast to get structured forecast results."


@app.route("/api/forecast", methods=["GET"])
def get_forecast_images():
    try:
        res = requests.get(NOTEBOOK_API_URL)
        if res.status_code != 200:
            return jsonify({"error": "Notebook failed", "details": res.text}), 500

        notebook_output = res.json()
        raw_data = notebook_output.get("uploaded_images", {})
        structured_data = organize_forecast_data(raw_data)

        return jsonify({
            "message": "Forecast completed and structured successfully",
            "data": structured_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
