FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

EXPOSE 8000
# Start app
CMD ["gunicorn", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]


