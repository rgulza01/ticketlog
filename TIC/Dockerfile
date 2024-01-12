# Use Python 3.6 or later as a base image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy python requirements file to install dependencies
COPY TIC/requirements.txt ./

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy application code to working directory
COPY . .

# Expose port for Flask app
EXPOSE 5000 

# Create an entrypoint
ENTRYPOINT ["python", "app.py"]