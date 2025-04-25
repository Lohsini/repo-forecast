import os
from flask import Flask, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import json
from google.cloud import storage

load_dotenv()

app = Flask(__name__)
CORS(app)

NOTEBOOK_API_URL = os.environ.get("NOTEBOOK_API_URL")
BASE_IMAGE_PATH = os.environ.get("BASE_IMAGE_PATH")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

client = storage.Client()


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


def fetch_gcs_image_urls(folder):
    urls = []
    bucket = client.bucket(BUCKET_NAME)

    if folder:
        blobs = bucket.list_blobs(prefix=f"{folder}/")
    else:
        blobs = bucket.list_blobs()

    for blob in blobs:
        if blob.name.endswith(".png") or blob.name.endswith(".jpg"):
            urls.append(BASE_IMAGE_PATH + blob.name)
    return urls


@app.route("/")
def home():
    return "Welcome to the Forecast Microservice API. Use /api/forecast or /api/bucket/<folder>"


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


@app.route("/api/bucket", methods=["GET"])
def get_all_bucket_images():
    try:
        folders = ["Prophet", "StatsModel",
                   "Tensorflow_LSTM", "charts"]
        all_data = {}

        for folder in folders:
            urls = fetch_gcs_image_urls(folder)
            all_data[folder] = urls

        structured_data = organize_forecast_data(all_data)

        return jsonify({
            "message": "Fetched images from all model folders",
            "data": structured_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
