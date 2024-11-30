# Use an official Python runtime as the parent image
FROM python:3.11-bullseye

# Update APT and install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    imagemagick \
    ghostscript \
    fonts-roboto \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Update font cache
RUN fc-cache -f -v

# Modify ImageMagick policy file to remove restrictions
RUN sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml

# Set the working directory in the container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Upgrade pip and install necessary packages first
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir Cython numpy

# Install other Python dependencies with legacy resolver
RUN pip install --no-cache-dir -r requirements.txt --use-deprecated=legacy-resolver

# Copy the entire application code into the container
COPY . .

# Expose the application port
EXPOSE 31415

# Command to run the Python script when the container launches
CMD ["python", "runShortGPT.py"]
