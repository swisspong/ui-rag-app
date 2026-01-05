# Use the official Python image as the base image
FROM python:3.12-slim

# Install system dependencies for psycopg2
RUN apt-get update -y; \
    apt-get upgrade -y; \
    apt-get install -y\
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    # apt-get install -y libpq-dev && \

# Create a non-root user for security
# RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN useradd -m appuser

# Set the working directory in the container
WORKDIR /app

ENV PYTHONPATH=/app:$PYTHONPATH

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app /home/appuser

# Switch to the non-root user
USER appuser

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Command to run the FastAPI application in production mode
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--workers", "4","src/interfaces/http/server.py"]
