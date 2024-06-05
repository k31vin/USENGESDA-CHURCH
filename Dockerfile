# Use the official Python image as a base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install Flask and other dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 5000

# Define the command to run the Flask application when the container starts
CMD ["export FLASK_APP=application.py", "export FLASK_DEBUG=1", "flask run"]

# Build the Docker image
# docker build -t flask-app .
# Run the Docker container
# docker run -p 5000:5000 flask-app
