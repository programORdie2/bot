# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /

# Copy the application files into the working directory
COPY . /

EXPOSE 8080
# Install the application dependencies
RUN pip install -U discord.py

# Define the entry point for the container
CMD ["python", "main.py"]
