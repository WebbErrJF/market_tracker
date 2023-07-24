FROM python:3.11-alpine
WORKDIR /market_tracker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY market_tracker/ .
