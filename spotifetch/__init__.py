__version__ = 0.1

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
import time

from flask import Flask
from flask_bootstrap import Bootstrap
from celery import Celery

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_envvar('HOWHEAVY_CONFIG_PATH')


def make_celery(app):
    celery = Celery(__name__,
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)


@celery.task()
def sleepy_test(a, b):
    for i in range(100):
        print 'sleeping {} second'.format(i)
        time.sleep(1)
    return a + b


handler = RotatingFileHandler(
    os.path.join(app.config['LOG_DIRECTORY'], '{}.log'.format(__name__)),
    maxBytes=100000, backupCount=10)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(msecs)d-%(levelname)s-%(module)s:%(lineno)d:%(message)s')
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.INFO)

bootstrap = Bootstrap(app)


@app.context_processor
def inject_variables():
    return dict(utcnow=datetime.utcnow)



from . import views
