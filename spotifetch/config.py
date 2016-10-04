import os

SECRET_KEY = os.getenv('SPOTIFETCH_SECRET_KEY')

CELERY_BROKER_URL = os.environ['CLOUDAMQP_URL']
CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


TEMPLATES_AUTO_RELOAD = True

auth_scopes = [
    'user-library-read',
    'user-top-read',
    'user-follow-read',
    'playlist-modify-public'
    ]

SPOTIFY_AUTHORIZATION_SCOPE = ' '.join(auth_scopes)


SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = os.environ['SPOTIFY_REDIRECT_URI']

this_dir = os.path.dirname(__file__)

with open(os.path.join(this_dir, 'genre_seeds.txt')) as f:
    SPOTIFY_GENRE_SEEDS = f.read().splitlines()
