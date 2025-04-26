FROM python:3.10-slim

ENV PORT=8080
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  g++ \
  && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir jupyter ipykernel

EXPOSE 8080

CMD ["python", "app.py"]