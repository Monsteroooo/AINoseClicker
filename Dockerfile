FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and sounds
COPY . .

# Expose REST API and Web UI port
EXPOSE 8088

# Default run command (runs interactive TUI with API enabled)
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8088"]
