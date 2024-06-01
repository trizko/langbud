FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN apk add --no-cache git
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "src/main.py"]