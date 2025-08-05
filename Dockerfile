FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies system-wide
RUN uv pip install --system .

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application directly
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
