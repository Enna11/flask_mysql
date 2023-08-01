# Use a specific Python version (e.g., 3.9-slim)
FROM python:3.9

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=iddirena \
    MYSQL_DATABASE=enameli

# Set the working directory in the container
WORKDIR /app

# Copy the files of your application into the container
COPY . .

# Install system dependencies (if needed)
# RUN apt-get update && apt-get install -y <system-packages>


# Install Python dependencies from requirements.txt

RUN apt install pkg-config
RUN pip3 install --no-cache-dir -r requirements.txt -v


# Expose the port on which your Flask application listens
EXPOSE 5000

# Command to start the Flask application when the container is executed
CMD ["python3", "app.py"]