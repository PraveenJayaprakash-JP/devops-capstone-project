# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port 8000
EXPOSE 8000

# Set entrypoint to gunicorn running main:app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
