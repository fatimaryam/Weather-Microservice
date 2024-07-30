# Dockerfile for the weather microservice
FROM python:3.9-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV API_KEY=9e26b6849844370389437ea21e9b334c
ENV DATABASE_URL=postgresql://postgres:postgres@postgres:5432/weather_db

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]