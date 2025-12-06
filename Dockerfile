FROM python:3.12-slim

# Install ffmpeg + opus via apt (goes to /usr/bin/ffmpeg → always found)
RUN apt-get update && \
    apt-get install -y ffmpeg libopus0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
