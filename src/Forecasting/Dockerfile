FROM python:3.10-slim

ENV PORT 8080

WORKDIR /app

# Install system dependencies needed for Prophet (with cmdstanpy)
RUN apt-get update && apt-get install -y \
  gcc \
  g++ \
  && apt-get clean

COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install jupyter

EXPOSE 8080

CMD ["python", "app.py"]
