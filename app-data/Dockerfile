# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY app.py /app
COPY training /app/training
COPY requirements.txt /app
COPY modules /app/modules

# Install dependencies
RUN pip install -r requirements.txt
RUN python3 training/training.py

# Run the application
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "120"]
CMD ["app:app"]
