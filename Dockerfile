# Use an official Python runtime as the parent image
FROM python:3.11-bullseye

RUN apt-get update && apt-get install -y curl \
    wget

# Install ffmpeg and ImageMagick
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Set the working directory in the container to /app
WORKDIR /app

# Copy the local package directory content into the container at /app
COPY . /app

# Install any Python packages specified in requirements.txt
#RUN pip install --upgrade shortgpt
#RUN pip install gradio==3.38.0

#COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 31415

# Define any environment variables
# ENV KEY Value

RUN ["printenv"]

# Run  Python script when the container launches
# CMD ["python", "./example-short-gpt.py"]
CMD ["python", "./runShortGPT.py"]