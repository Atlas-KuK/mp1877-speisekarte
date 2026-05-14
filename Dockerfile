FROM python:3.11-slim

# Install system dependencies for OCR and PDF processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libtesseract-dev \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY menu_qa_app.py .
COPY templates/ ./templates/

# Create upload directory
RUN mkdir -p /tmp/uploads

# Set environment variables
ENV FLASK_APP=menu_qa_app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port (Railway will set PORT env var)
EXPOSE 5000

# Start app
CMD ["python", "menu_qa_app.py"]
