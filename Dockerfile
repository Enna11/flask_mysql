# Use a specific Python version (e.g., 3.9-slim)
FROM python:3.9-slim

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=iddirena \
    MYSQL_DATABASE=enameli

# Set the working directory in the container
WORKDIR /app

# Copy the files of your application into the container
COPY . .

# Install system dependencies (if needed)
# RUN apt-get update && apt-get install -y <system-packages>

# Create and activate a virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your Flask application listens
EXPOSE 5000

# Command to start the Flask application when the container is executed
CMD ["python3", "app.py"]