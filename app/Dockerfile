FROM python:3.13.14-alpine3.24

WORKDIR /app

COPY requirements.txt .

RUN apk upgrade --no-cache

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]