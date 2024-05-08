FROM python:3.11

WORKDIR /.

COPY poetry.lock $APP_HOME/poetry.lock
COPY pyproject.toml $APP_HOME/pyproject.toml

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & celery -A app_jull beat -l info & celery -A app_jull worker -l info -P eventlet"]


