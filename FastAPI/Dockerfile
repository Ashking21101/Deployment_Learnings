From python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# docker is listening inside the container on port 8000, the port mentioned here will be on right side of the 'docker run -p...' command
# the port on right side always remain same  


# Quick rules to remember
# Right side (: after) = port your app listens on inside Docker container
# Left side = port you use on your machine