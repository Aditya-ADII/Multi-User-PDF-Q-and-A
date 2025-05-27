FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Install numpy first to avoid conflicts
RUN pip install --no-cache-dir numpy==1.23.1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set up the app
RUN mkdir -p /app/uploads && chmod -R 777 /app/uploads
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]