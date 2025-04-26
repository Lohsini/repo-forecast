# CS587 HW5 GitHub Repositories Time-Series Forecasting Platform

## Overview

This project presents a comprehensive analytics and forecasting application built to track and predict activity across a selected list of open-source GitHub repositories. It integrates data retrieval, visualization, and time-series forecasting to provide actionable insights into issue trends, contributions, and repository health.

Leveraging a microservice architecture with React (Frontend), Flask (Backend), and Python-based forecasting tools, the system allows users to view historical repository metrics and explore future trends using three forecasting models: TensorFlow/Keras LSTM, Facebook Prophet, and StatsModels.

---

## Key Features

- **Data Retrieval:** Automatically fetches 2-month history of GitHub repository data via the GitHub API.
- **Visualization:** Generates comparative charts for issues, stars, forks, and contribution metrics.
- **Forecasting:** Applies three different models (LSTM, Prophet, StatsModel) to forecast:
  - Issues, Pull Requests, Commits, Branches, Contributors, Releases
- **Model Comparison:** Final report includes comparative analysis and a recommendation for the best-performing forecasting model.
- **Deployment:** Fully containerized and deployed on Google Cloud using Docker, with separate React and Flask microservices.

---

## Repositories Analyzed

#### Repositories

1. [meta-llama/llama3](https://github.com/meta-llama/llama3)
2. [ollama/ollama](https://github.com/ollama/ollama)
3. [langchain-ai/langchain](https://github.com/langchain-ai/langchain)
4. [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
5. [microsoft/autogen](https://github.com/microsoft/autogen)
6. [openai/openai-cookbook](https://github.com/openai/openai-cookbook)
7. [elastic/elasticsearch](https://github.com/elastic/elasticsearch)
8. [milvus-io/pymilvus](https://github.com/milvus-io/pymilvus)

#### Models Used

- TensorFlow/Keras LSTM
- Facebook Prophet
- StatsModel SARIMAX

#### Output

Plots are saved to GCS under:

- `/charts/`
- `/Tensorflow_LSTM/`
- `/Prophet/`
- `/StatsModel/`

---

### Environment Setup

#### Flask Backend

```bash
pip install -r requirements.txt
```

#### React Frontend

```bash
cd src/React
npm install
npm start
```

#### Forecasting Notebook Service

A Jupyter notebook (`GitHub_Repos_Issues_Forecasting.ipynb`) performs time-series forecasts for GitHub issues data.

#### .env Example (optional for local Flask trigger)

```env
GITHUB_TOKEN=your_github_token
BUCKET_NAME=your_gcs_bucket_name
BASE_IMAGE_PATH=https://storage.googleapis.com/your_gcs_bucket_name/
GOOGLE_APPLICATION_CREDENTIALS=your_service_account_key.json
```

#### Local Run (optional Flask API)

```bash
python app.py
```

Access:

```
http://localhost:8080/run-notebook
```

#### Deployment Example

- URL: https://forecast-562422992160.us-central1.run.app
- API: https://forecast-562422992160.us-central1.run.app/run-notebook

---

### 2. Flask Backend

This Flask microservice serves two main purposes:

- **Trigger a Jupyter Notebook** to run forecasting models and upload charts to GCS.
- **Direct Access** to previously generated forecast images stored in GCS.

#### Key Endpoints

- `GET /api/forecast`: Trigger forecast execution, return URLs of generated forecast images.
- `GET /api/bucket`: List folders (Prophet, StatsModel, Tensorflow_LSTM, charts) in GCS.

#### Local Run

```bash
cd src/Flask
python app.py
```

Access:

```
http://localhost:5000/api/forecast
http://localhost:5000/api/bucket
```

#### .env Example

```env
NOTEBOOK_API_URL=https://your-notebook-cloudrun-url/run-notebook
BUCKET_NAME=your_gcs_bucket_name
BASE_IMAGE_PATH=https://storage.googleapis.com/your_gcs_bucket_name/
GOOGLE_APPLICATION_CREDENTIALS=your_service_account_key.json
```

#### Docker Support

```bash
bash push.sh
```

#### Deployment Example

- URL: https://flask-562422992160.us-central1.run.app
- API: https://flask-562422992160.us-central1.run.app/api/forecast
- API: https://flask-562422992160.us-central1.run.app/api/bucket

---

### 3. React Frontend

Provides interactive visualization of GitHub data and forecast results.

#### Local Development

```bash
cd src/React
npm install
npm start
```

Visit:

```
http://localhost:3000
```

#### Docker Support

```bash
bash push.sh
```

#### Deployment Example

- URL: https://react-562422992160.us-central1.run.app

---
