# backend/Dockerfile (The Final, Guaranteed Version)
FROM python:3.9-slim

# 1. Set the working directory, this is where our app will live
WORKDIR /app

# 2. Copy requirements first to leverage Docker cache
# This assumes requirements.txt is in the 'backend' folder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the application code from the local 'app' sub-directory
# The '.' at the end means copy the CONTENTS of 'app' into the WORKDIR (/app)
# This creates the correct structure: /app/main.py, /app/api, etc.
COPY ./app .

# 4. Command to run the application. Uvicorn will find 'main.py' in the current WORKDIR.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
