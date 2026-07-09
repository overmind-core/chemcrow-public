FROM python:3.10
WORKDIR /app

RUN pip install --no-cache-dir \
    rdkit-pypi==2022.3.1 \
    OpenNMT-py==2.2.0 \
    "numpy<2.0.0" \
    flask \
    gdown

COPY app.py .
RUN touch input.txt
RUN mkdir -p models \
    && gdown 1ywJCJHunoPTB5wr6KdZ8aLv7tMFMBHNy -O models/USPTO480k_model_step_400000.pt

EXPOSE 5000
CMD ["python", "app.py"]
