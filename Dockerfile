# syntax=docker/dockerfile:1

# Use an official Python runtime as a parent image.
# Version updated to match uv.lock 'requires-python = ">=3.13"'.
# 'slim' is a good choice for keeping the image size down.
FROM python:3.13-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure output is sent straight to the terminal without buffering.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install uv, then use it to install dependencies from requirements.txt.
# This is done in a separate step to leverage Docker's layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir uv && \
    uv pip install --no-cache -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# Command to run the application using a production-ready WSGI server like Gunicorn.
# This assumes you have a 'wsgi.py' file with an 'app' instance.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]