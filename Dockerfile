FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py sqs-load-generator.py ./

CMD ["python","run.py", "Flask"]
