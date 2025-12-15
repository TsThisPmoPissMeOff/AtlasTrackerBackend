# Use official Python slim image
FROM python:3.10-slim

# Install system dependencies: Tesseract OCR + build tools + OpenCV dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend code
COPY . /app

# Upgrade pip and install Python packages
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 10000 (or any port)
EXPOSE 10000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
