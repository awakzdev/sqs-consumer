FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python","run.py", "Flask"]
