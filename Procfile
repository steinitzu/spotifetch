web: gunicorn spotifetch:app --worker-class gevent
worker: celery worker -A spotifetch:celery
