# Forecast Microservice (Flask)

This Flask microservice is designed to trigger a cloud-hosted Jupyter notebook (via Cloud Run) that generates forecast charts using time-series models like LSTM, Prophet, and StatsModel. The notebook runs predictions and uploads output images to Google Cloud Storage.

## Features

- GET `/api/forecast`: Triggers notebook execution and returns URLs of generated forecast images
- Uses `.env` to manage Cloud Run endpoint
- Returns JSON with organized URLs of charts (grouped by method/folder)
- Cross-origin enabled (for frontend React access)

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
```

> Replace with your actual deployed notebook endpoint.

## Run Locally

```bash
python app.py
```

Default port is `5000`. You can access:

```
http://localhost:5000/api/forecast
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

---
