
FROM python:3
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the files of my application into the container
COPY . .
 
# Install Python dependencies from requirements.txt
 
RUN apt install pkg-config
RUN pip3 install --no-cache-dir -r requirements.txt -v
 
# Expose the port on which my Flask application listens
EXPOSE 5000
 
# Command to start the Flask application when the container is executed
CMD ["python3", "app.py"]
