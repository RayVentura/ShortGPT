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

# Copy requirements file
COPY requirements.txt .

# Upgrade pip before installing dependencies
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local package directory content into the container at /app
COPY . /app

EXPOSE 31415

# Define any environment variables
# ENV KEY Value

# Print environment variables (for debugging purposes, can be removed)
RUN printenv

# Run Python script when the container launches
CMD ["python", "-u", "./runShortGPT.py"]
