# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install production dependencies.
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY backend/ ./backend/

# Change working directory to backend so uvicorn can find app.main
WORKDIR $APP_HOME/backend

# Run the web service on container startup using uvicorn.
# Use $PORT environment variable supplied by Google Cloud Run.
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
