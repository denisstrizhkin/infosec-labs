FROM python:3.13-alpine

WORKDIR /app

RUN pip install 'fastapi[standard]'

COPY main.py .

CMD ["fastapi", "run", "/app/main.py", "--port", "80"]

