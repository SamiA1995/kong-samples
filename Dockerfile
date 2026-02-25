FROM python:3.11-slim
WORKDIR /app

# Copy backend and UI templates
COPY app.py /app/
COPY templates/ /app/templates

# Install dependencies
RUN pip install fastapi uvicorn jinja2

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]