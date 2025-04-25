# CS587 HW5: GitHub Repo Analytics & Forecasting

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

1. [meta-llama/llama3](https://github.com/meta-llama/llama3)
2. [ollama/ollama](https://github.com/ollama/ollama)
3. [langchain-ai/langchain](https://github.com/langchain-ai/langchain)
4. [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
5. [microsoft/autogen](https://github.com/microsoft/autogen)
6. [openai/openai-cookbook](https://github.com/openai/openai-cookbook)
7. [elastic/elasticsearch](https://github.com/elastic/elasticsearch)
8. [milvus-io/pymilvus](https://github.com/milvus-io/pymilvus)

---
