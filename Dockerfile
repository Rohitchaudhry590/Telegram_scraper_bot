FROM python:3.11-slim

WORKDIR /app

# Dependencies install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code copy
COPY . .

# Database persistence volume (posted.db only)
VOLUME ["/app/posted.db"]

CMD ["python", "main.py"]
