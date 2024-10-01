# Start with a base image containing Python runtime
FROM --platform=linux/arm64  python:3.10-slim

# The maintainer of the Dockerfile
LABEL maintainer="Andrew Schwartz <andrew@mk-dir.com>"

# GCC fix
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends -o APT::Immediate-Configure=false gcc g++ make libpng-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

ENV MPLLOCALFREETYPE 1

# Set an environment variable to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED 1

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code from your host to your image filesystem.
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application
CMD ["watchmedo", "auto-restart", "--directory=/app", "--patterns=*.py", "--recursive", "--", "python", "main.py"]

# Cancel all orders
# CMD ["python", "cancel_all_orders.py"]

# Close all positions
# Also cancels orders
# CMD ["python", "close_all_positions.py"] 
# Does not cancels orders
# CMD ["python", "close_all_positions.py", "--cancel_orders", "False"] 
