# Use the official Python image as base image
FROM python:3.10

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=career_development.settings
ENV DJANGO_DEBUG=False

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for build process
ARG GEMINI_API_KEY
ENV GEMINI_API_KEY=${GEMINI_API_KEY}

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the ports the app runs on
EXPOSE 8000 8001

# Run the Daphne server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "career_development.asgi:application"]
