# Forecasting Microservice (.ipynb based)

This directory contains the Jupyter notebook that performs time-series forecasting on GitHub issue data using:

- LSTM (Long Short-Term Memory)
- Prophet
- StatsModel (SARIMAX)

## Notebook Name

- `GitHub_Repos_Issues_Forecasting.ipynb`

## Purpose

The notebook is responsible for:

1. Parsing GitHub issue data (usually preloaded within the notebook).
2. Running three forecasting models (LSTM, Prophet, StatsModel).
3. Plotting results and saving figures into folders:
   - `/charts`
   - `/Tensorflow_LSTM`
   - `/Prophet`
   - `/StatsModel`
4. Uploading those images to Google Cloud Storage (when triggered via Flask or `run-notebook` API).

## .env Setup (for local Flask runner)

Create a `.env` file in the root directory **(for Flask or local execution)**:

my Bucket name - forecasting-image-bucket

```env
GITHUB_TOKEN=your_github_token
BUCKET_NAME=your_gcs_bucket_name
BASE_IMAGE_PATH=https://storage.googleapis.com/your_gcs_bucket_name/
GOOGLE_APPLICATION_CREDENTIALS=your_service_account_key.json
```

> Replace values with your actual value

## Run Locally

If you want to run the notebook-triggering service locally:

```bash
python app.py
```

It will launch on:

```
http://localhost:8080/run-notebook
```

## Docker Support

You can containerize this service (Flask wrapper) for deployment:

```bash
bash push.sh
```

## Cloud Deployment

This notebook and/or Flask API can be deployed to Google Cloud Run, enabling scalable prediction serving via HTTP.

URL - https://forecast-562422992160.us-central1.run.app
API - https://forecast-562422992160.us-central1.run.app/run-notebook

---

## Output Structure

When the notebook completes successfully, it generates plots and stores them under:

```
charts/
Tensorflow_LSTM/
Prophet/
StatsModel/
```

Each folder holds figures for one prediction technique.
