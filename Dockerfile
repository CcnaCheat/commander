# Use official Python slim image (stable base for Railway)
FROM python:3.12-slim

# Install ffmpeg + opus (for Discord voice) via apt — this puts it in /usr/bin/ffmpeg
RUN apt-get update \
    && apt-get install -y ffmpeg libopus0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose (optional, for Discord it's not needed)
EXPOSE 80

# Run the bot
CMD ["python", "bot.py"]
