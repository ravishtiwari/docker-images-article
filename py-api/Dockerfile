
# FROM python:3.11-slim

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements and install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy application code
# COPY . .

# # Create non-root user
# RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
# USER appuser

# # Expose port
# EXPOSE 8000

# # Run the application
# # CMD ["gunicorn", "main:app", "-c", "gunicorn_conf.py"]

FROM python:3.11-slim

# Metadata for reproducibility
LABEL maintainer="ravishtiwari"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set workdir early for layer caching
WORKDIR /app

# Install system dependencies (build essentials)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
    && apt-get purge --auto-remove -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies before copying full source (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source (after pip layer)
COPY . .

# Create and switch to non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose app port
EXPOSE 8000

# Entrypoint
CMD ["gunicorn", "main:app", "-c", "gunicorn_conf.py"]
