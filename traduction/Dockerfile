FROM python:3.12-slim as base-traduction

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

FROM base-traduction

COPY ./app /app

CMD ["fastapi", "dev", "app/main.py", "--port", "8090"]