FROM python:3.12-slim as base-traduction

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

FROM base-traduction

RUN mkdir /saved_model

COPY ./app /app

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]