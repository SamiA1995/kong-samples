# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional: for building some Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly (merged from requirements.txt)
RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    jinja2 \
    python-multipart \
    requests \
    openai \
    pytest \
    httpx

# Copy application code
COPY ..

# Expose FastAPI port
EXPOSE 80000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]