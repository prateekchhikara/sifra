# Use the official lightweight Python image.
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Metadata as labels
LABEL maintainer="Prateek Chhikara <prateekchhikara24@gmail.com>"

RUN apt-get update

RUN apt install -y vim

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit when the container launches
CMD ["streamlit", "run", "gui.py", "--server.port=8501", "--server.address=0.0.0.0"]