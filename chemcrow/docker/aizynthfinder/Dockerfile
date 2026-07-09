FROM python:3.9-slim
WORKDIR /app

# cgrtools-plus (pulled by aizynthfinder[all]) compiles C extensions and needs gcc
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Base package is enough for aizynthcli; [all] pulls optional deps that fail on slim images
RUN pip install --no-cache-dir \
    aizynthfinder \
    onnxruntime \
    flask

COPY config.yml app.py ./
RUN download_public_data .

EXPOSE 5000
CMD ["python", "app.py"]
