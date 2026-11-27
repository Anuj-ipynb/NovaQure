FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install system dependencies required by RDKit, C++ extensions, and health check
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxrender1 \
    libxext6 \
    libgomp1 \
    libgl1 \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install lightweight CPU-only PyTorch (reduces image size by ~4GB)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install application dependencies
COPY requirements.docker.txt .
RUN pip install --no-cache-dir -r requirements.docker.txt

# Copy datasets and trained model checkpoints
COPY datasets/ ./datasets/
COPY models/ ./models/

# Copy application code (both backend and app packages)
COPY backend/ ./backend/
COPY app/ ./app/

# Create data and output directories with write permissions
RUN mkdir -p /app/data /app/outputs/artifacts && chmod -R 777 /app/data /app/outputs

EXPOSE 8000

HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
