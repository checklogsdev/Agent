FROM python:3.11-slim

LABEL maintainer="CheckLogs <hey@checklogs.dev>"
LABEL description="CheckLogs monitoring agent"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    psutil==5.9.6

# Copy agent script
COPY agent.py /app/agent.py
RUN chmod +x /app/agent.py

# Create healthcheck script
RUN echo '#!/bin/sh\nps aux | grep -v grep | grep agent.py > /dev/null && echo "OK" || exit 1' > /app/healthcheck && \
    chmod +x /app/healthcheck

# Create logs directory
RUN mkdir -p /var/log/checklogs

# Run as non-root user
RUN useradd -m -u 1000 checklogs
USER checklogs

# Start agent
CMD ["python3", "-u", "/app/agent.py"]