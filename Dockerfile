# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including Tor and plotting libraries
RUN apt-get update && apt-get install -y \
    tor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY src/requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Create results directory for reports
RUN mkdir -p /app/results

# Expose Tor's SOCKS port
EXPOSE 9050

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting Tor service..."\n\
tor &\n\
echo "Waiting for Tor to initialize..."\n\
sleep 15\n\
echo "Running Tor Anonymous Network Analysis..."\n\
python main.py\n\
echo "Analysis complete. Check /app/results for reports."\n\
echo "Keeping container alive for potential re-runs..."\n\
# Keep the container running for healthcheck\n\
tail -f /dev/null' > /app/start.sh

RUN chmod +x /app/start.sh

# Start Tor service and run main.py
CMD ["/app/start.sh"]
