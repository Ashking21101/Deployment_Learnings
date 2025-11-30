# 1) Base image: Python 3.10, small size
FROM python:3.10-slim

# 2) Set working directory inside the container
WORKDIR /app

# 3) Copy only requirements first (better for caching)
COPY requirements.txt .

# 4) Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy the rest of the backend code into the image
COPY . .

# 6) Expose port 8000 (FastAPI runs here)
EXPOSE 8000

# 7) Start the FastAPI server when the container runs
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
