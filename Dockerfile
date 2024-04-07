# Use the Ubuntu 22.04 base image
FROM ubuntu:22.04

# Set environment variable for Flask
ENV FLASK_APP=webserver

# Update packages and install necessary dependencies
RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get install -y gcc && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Compile Plantri
RUN gcc -o plantri -O4 ./plantri54/plantri.c

# Expose port 5000 for Flask
EXPOSE 5000

# Start the Flask web server
CMD ["flask", "run", "--host=0.0.0.0"]
