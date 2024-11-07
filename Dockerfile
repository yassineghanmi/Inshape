FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1

# Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
