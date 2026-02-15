# Use the official Python 3.11 slim image as the base.
# The "slim" variant is a minimal Debian image with Python pre-installed,
# keeping the final image small (~150 MB instead of ~900 MB for the full image).
FROM python:3.11-slim

# Set the working directory inside the container.
# All subsequent commands (COPY, RUN, CMD) will execute relative to /app.
WORKDIR /app

# Copy only the requirements file first.
# Docker builds images in layers. If requirements.txt has not changed since
# the last build, Docker reuses the cached layer and skips the pip install
# step entirely. This dramatically speeds up rebuilds when you only change
# application code.
COPY requirements.txt .

# Install Python dependencies.
# --no-cache-dir tells pip not to store downloaded packages locally,
# which keeps the image size smaller.
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code into the container.
# Because this layer comes after the pip install layer, changing your
# Python source code will NOT trigger a re-install of all dependencies.
COPY . .

# Document that the container listens on port 8000 at runtime.
# This is informational -- it does not actually publish the port.
# You still need -p 8000:8000 when running the container.
EXPOSE 8000

# Define the command that runs when the container starts.
# uvicorn serves the FastAPI app, listening on 0.0.0.0 so that
# requests from outside the container (i.e., your host machine) can reach it.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]