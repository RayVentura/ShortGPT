# Use an official Python runtime as the parent image
FROM python:3.10-slim-bullseye

# Set environment variables to optimize Python and Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for FFmpeg and other ShortGPT requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Install any Python packages specified in requirements.txt
# Copy requirements file
COPY requirements.txt .

# update pip to prevent errors and warnings
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local package directory content into the container at /app
COPY . /app

EXPOSE 31415

# Define any environment variables
# ENV KEY Value

# Print environment variables (for debugging purposes, you can remove this line if not needed)
RUN ["printenv"]

# Run Python script when the container launches
CMD ["python", "-u", "./runShortGPT.py"]