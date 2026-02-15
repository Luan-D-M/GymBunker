FROM python:3.13-slim

# Prevents Python from writing .pyc files to disc (useless in containers)
ENV PYTHONDONTWRITEBYTECODE=1
# Force the stdout and stderr streams to be unbuffered --> Ensures logs shows up immediately. 
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

# Caching strategy: if the code is changed, this line won't execute again.
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]