FROM python:3.13-alpine

WORKDIR /app

RUN apk update && apk add bind-tools

RUN pip install 'fastapi[standard]'

COPY main.py .

CMD ["fastapi", "run", "/app/main.py", "--port", "80"]

