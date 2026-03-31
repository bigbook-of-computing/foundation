FROM python:3.11-slim

WORKDIR /docs

# Install build dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Build the site
RUN mkdocs build

# Serve the site (optional, can be overridden)
EXPOSE 8000
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
