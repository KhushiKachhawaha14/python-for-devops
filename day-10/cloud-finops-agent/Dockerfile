# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install boto3 strands psutil

# Copy your script into the container
COPY finops_agent.py .

# Run the agent when the container starts
CMD ["python", "finops_agent.py"]