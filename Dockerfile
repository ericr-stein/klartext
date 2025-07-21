FROM python:3.10-slim

WORKDIR /app

# Install essential system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/machinelearningZH/zix_understandability-index
RUN python -m spacy download de_core_news_sm

# Copy application code
COPY _streamlit_app_v2/ /app/

# Create log directory
RUN mkdir -p /app/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose Streamlit port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "/app/simplify-language-streaming.py", "--server.port=8501", "--server.address=0.0.0.0"]
