FROM python:3.10-slim

# Set working directory
WORKDIR /match_writer_service

# Copy code and requirements
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the listener
CMD ["python", "main.py"]
