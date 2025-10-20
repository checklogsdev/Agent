FROM python:3.11-slim

LABEL maintainer="CheckLogs <support@checklogs.dev>"
LABEL description="CheckLogs Monitoring Agent - Collects and sends server metrics"

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY agent.py .
COPY healthcheck /app/healthcheck
RUN chmod +x /app/healthcheck

# Create directories for logs and state
RUN mkdir -p /var/log/checklogs /var/lib/checklogs

# Non-root user for security (optional but recommended)
RUN useradd -m -u 1000 checklogs && \
    chown -R checklogs:checklogs /app /var/log/checklogs /var/lib/checklogs

USER checklogs

# Health check
HEALTHCHECK --interval=60s --timeout=10s --retries=3 --start-period=30s \
    CMD ["/app/healthcheck"]

# Default environment variables (can be overridden)
ENV CHECKLOGS_API_HOST=api.checklogs.dev \
    COLLECT_INTERVAL=10 \
    LOG_LEVEL=INFO

# Run the agent
CMD ["python", "-u", "agent.py"]