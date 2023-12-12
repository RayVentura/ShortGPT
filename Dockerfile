# Use an official Python runtime as the parent image
FROM python:3.11-bullseye
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    ghostscript \
    fonts-roboto \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# Update font cache
RUN fc-cache -f -v

RUN sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml
# Clean up APT when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Install any Python packages specified in requirements.txt
# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the local package directory content into the container at /app
COPY . /app

EXPOSE 31415

# Define any environment variables
# ENV KEY Value

# Print environment variables (for debugging purposes, you can remove this line if not needed)
RUN ["printenv"]

# Run Python script when the container launches
CMD ["python", "./runShortGPT.py"]