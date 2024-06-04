# Use Python 3.11 image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Copy the requirements_test file into the container
COPY requirements_test.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt -r requirements_test.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port FastAPI is running on
EXPOSE 3000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
