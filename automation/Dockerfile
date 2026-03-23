FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    iptables \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash sde
USER sde
WORKDIR /home/sde/automation

# Copy requirements and install Python dependencies
COPY --chown=sde:sde requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy automation code
COPY --chown=sde:sde . .

# Copy firewall initialization script
COPY --chown=sde:sde init-firewall.sh /home/sde/init-firewall.sh
USER root
RUN chmod +x /home/sde/init-firewall.sh
USER sde

# Set Python path to include user site-packages
ENV PATH="/home/sde/.local/bin:${PATH}"

# Entry point runs firewall script
ENTRYPOINT ["/home/sde/init-firewall.sh"]
CMD ["python", "pipeline.py"]
