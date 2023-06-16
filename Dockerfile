# Start with a base image containing Python runtime
FROM python:3.10-slim

# The maintainer of the Dockerfile
LABEL maintainer="Andrew Schwartz <andrew@mk-dir.com>"

# GCC fix
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends -o APT::Immediate-Configure=false gcc g++

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code from your host to your image filesystem.
COPY . .

# Run the application
CMD ["python", "trading_bot.py"]
