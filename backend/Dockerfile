# 1. Base Image
FROM python:3.10-slim

# 2. Set working directory to /code (Not /app to avoid conflict)
WORKDIR /code

# 3. Install System Dependencies (Optional but good for Postgres)
RUN apt-get update && apt-get install -y libpq-dev gcc

# 4. Install Python Dependencies
# We copy requirements first to cache them
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Copy the Application Code
# This is the MAGIC STEP: We copy the 'app' folder INTO /code/app
COPY ./app ./app

# 6. Set PYTHONPATH
# This tells Python to look for modules inside /code
ENV PYTHONPATH=/code

# 7. Start Command
# Uvicorn looks for 'app.main' inside /code
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]