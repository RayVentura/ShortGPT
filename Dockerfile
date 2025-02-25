# Use an official Python runtime as the parent image
FROM python:3.10-slim-bullseye

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    python3-dev \
    libatlas-base-dev \
    && apt-get clean

# Set the working directory in the container to /app
WORKDIR /app

# Copy requirements.txt first (to optimize cache usage)
COPY requirements.txt .

# Upgrade pip before installing dependencies
RUN python -m pip install --upgrade pip

# Install dependencies, this will use cache if requirements.txt hasn't changed
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

EXPOSE 31415

# Print environment variables (for debugging purposes, can be removed)
# RUN printenv

# Run Python script when the container launches
CMD ["python", "-u", "./runShortGPT.py"]
