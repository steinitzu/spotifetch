import logging

import spotipy
import spotipy.util
from flask import Flask
from flask_bootstrap import Bootstrap

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_envvar('HOWHEAVY_CONFIG_PATH')

bootstrap = Bootstrap(app)

from . import views
