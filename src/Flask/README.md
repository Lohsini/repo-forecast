# Forecast Backend (Flask)

This Flask microservice serves two main purposes:

1. **Trigger a Cloud Run-hosted Jupyter notebook** that runs time-series forecasting models and stores output charts in Google Cloud Storage (GCS).
2. **Directly access previously uploaded forecast images** from GCS for faster retrieval without triggering model execution.

## Features

- `GET /api/forecast`  
  Triggers the Jupyter notebook (via Cloud Run) to run forecasts using models like **LSTM**, **Prophet**, and **Statsmodels**.  
  Returns structured JSON containing organized URLs of forecast images (grouped by model/folder).
- `GET /api/bucket`  
  Returns "Prophet", "StatsModel", "Tensorflow_LSTM", "charts" folders from GCS, structured and grouped automatically.

## Additional Details

- Uses `.env` file to manage:
  - `NOTEBOOK_API_URL` (Cloud Run endpoint)
  - `BASE_IMAGE_PATH` (Public GCS URL prefix)
  - `BUCKET_NAME` (Name of your GCS bucket)
- Auto-structured data with child/parent forecast relationships (e.g., different forecast variants under one chart)
- CORS enabled for frontend integration (e.g., React apps)
- On notebook failure, will **fallback to last successful result** from `backup.json`

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
flask
flask-cors
requests
python-dotenv
```

## .env Setup

Create a `.env` file in the root directory:

```env
NOTEBOOK_API_URL=https://your-notebook-cloudrun-url/run-notebook
BUCKET_NAME=your_gcs_bucket_name
BASE_IMAGE_PATH=https://storage.googleapis.com/your_gcs_bucket_name/
GOOGLE_APPLICATION_CREDENTIALS=your_service_account_key.json
```

> Replace with your actual deployed notebook endpoint.

## Run Locally

```bash
python app.py
```

Default port is `5000`. You can access:

```
http://localhost:5000/api/forecast
http://localhost:5000/api/bucket
```

## Docker Support

You can containerize the Flask app for deployment:

```bash
bash push.sh
```

## Cloud Deployment

Can be deployed to Google Cloud Run or other container services.

URL - https://flask-562422992160.us-central1.run.app
API - https://flask-562422992160.us-central1.run.app/api/forecast
API - https://flask-562422992160.us-central1.run.app/api/bucket

---
