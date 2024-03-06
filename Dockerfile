FROM python:3.11.8-alpine3.19

# Set the working directory inside the container to /app
WORKDIR /app

# Copy requirements.txt from the host to /app/requirements.txt in the container
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the current directory from the host to /app in the container
COPY . /app

# Expose port 5000 to allow external access to the Flask application
EXPOSE 5000

# Set the FLASK_RUN_HOST environment variable to 0.0.0.0 to allow external access
ENV FLASK_RUN_HOST=0.0.0.0

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint script as the entrypoint for the container
# ENTRYPOINT ["./entrypoint.sh"]

CMD ["flask", "run"]