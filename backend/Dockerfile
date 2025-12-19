# 1. Base Image
FROM python:3.10-slim

# 2. Set working directory to /code
# (আগে হয়ত /app ছিল, এখন /code দিচ্ছি যাতে কনফ্লিক্ট না হয়)
WORKDIR /code

# 3. Install System Dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# 4. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Copy the Application Code
# এই লাইনটিই আসল ফিক্স। এটি 'app' ফোল্ডারটিকে হুবহু কপি করবে।
COPY ./app ./app

# 6. Set PYTHONPATH
# পাইথনকে বলে দিচ্ছি কোথায় মডিউল খুঁজতে হবে
ENV PYTHONPATH=/code

# 7. Start Command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]