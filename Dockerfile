# Use the official Python image from the Docker Hub
FROM mcr.microsoft.com/playwright/python:v1.45.1-jammy

# Set the working directory in the container
WORKDIR /app

# Install the dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# install playwright
RUN playwright install --with-deps webkit

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
