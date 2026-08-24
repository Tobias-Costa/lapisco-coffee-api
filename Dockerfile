from python:3.13

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE = 1

ENV PYTHONUNBUFFERED = 1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]