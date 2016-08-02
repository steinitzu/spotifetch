__version__ = 0.1

import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_envvar('HOWHEAVY_CONFIG_PATH')

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

from . import views
