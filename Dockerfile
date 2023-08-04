# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main.py script into the container
COPY main.py .

# Set the command to run when the container starts
CMD ["python", "main.py", "-lat", "40.730610", "-lon", "-73.935242"]