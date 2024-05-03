# poetry install --no-root
# poetry add eventlet flower -G test
# docker run -d --name redis_db -p 6379:6379 redis / docker compose up -d
# py manage.py makemigrations
# py manage.py migrate
# py manage.py runserver
# celery -A app_jull worker -l info -P eventlet
# celery -A app_jull flower --broker=redis://localhost:6379/0 --address='127.0.0.1' -l info --pool=eventlet
# celery -A app_jull beat -l info
# localhost:8000
