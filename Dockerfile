FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile

RUN apt-get update && apt-get install -y libpq-dev && \
    pipenv install psycopg2

COPY . /app/

EXPOSE 8000

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
