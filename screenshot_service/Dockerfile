# screenshot_service/Dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt && playwright install chromium
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
