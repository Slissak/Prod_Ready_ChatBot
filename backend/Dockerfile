# --- Stage 1: Build the dependencies ---
# Use a full Python image to have access to build tools
FROM python:3.12 as builder

# Set the working directory
WORKDIR /app

# Create and activate a virtual environment
# This isolates dependencies and keeps the final image clean
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy ONLY the requirements file to leverage Docker's caching
COPY requirements.txt .

# Install dependencies into the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Create the final production image ---
# Use a slim image for a smaller footprint
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy your application code
COPY ./app ./app

# Set the path to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port your app will run on
EXPOSE 8000

# Set the command to run your application in production
# We use the full path to your app's entry point.
# We remove '--reload' and add '--host 0.0.0.0' to allow traffic from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
