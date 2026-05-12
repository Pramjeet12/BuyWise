FROM python:3.10-slim-bookworm

WORKDIR /app

# Install required OS packages in one layer and clean apt cache.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       libsm6 \
       libxext6 \
       unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better layer caching.
COPY requirements.txt .
RUN grep -v "^-e \.$" requirements.txt > requirements-docker.txt \
    && pip install --no-cache-dir -r requirements-docker.txt

# Copy project files.
COPY . .

# Install local package after source code is available.
RUN pip install --no-cache-dir -e .

CMD ["python", "app.py"]
