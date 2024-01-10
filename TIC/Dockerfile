# Use Python 3.7 Alpine base image
FROM python:3.7-alpine

# Set the working directory in the container
WORKDIR /app

# Copy python requirements file to install dependencies
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code to working directory
COPY . .

# Expose port for Flask app
EXPOSE 5000 

# Set environment variables 
ENV FLASK_ENV=development

# Run flask application
CMD ["flask", "run", "--host=0.0.0.0"]