import os

SECRET_KEY = os.getenv('HOWHEAVY_SECRET_KEY')

SPOTIFY_AUTHORIZATION_SCOPE = 'user-library-read user-top-read user-follow-read'
