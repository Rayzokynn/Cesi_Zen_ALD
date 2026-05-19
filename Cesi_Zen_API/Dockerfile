FROM python:3.12-slim
# Set the working directory in the container
WORKDIR /app
# Install system dependencies for MySQL client and code linting
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*
# Install pylint and pylint-django for code linting
RUN pip install pylint pylint-django
# Copy the requirements file and install Python dependencies
COPY requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the entire project into the container
COPY . .
# Expose the port that the Django development server will run on
EXPOSE 8000
# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
