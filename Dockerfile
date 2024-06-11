FROM python:3.12-alpine

WORKDIR /usr/src/app

RUN apk add postgresql-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# reload should not be in prod
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
