import os

SECRET_KEY = os.getenv('HOWHEAVY_SECRET_KEY')

auth_scopes = [
    'user-library-read',
    'user-top-read',
    'user-follow-read',
    'playlist-modify-private'
    ]

SPOTIFY_AUTHORIZATION_SCOPE = ' '.join(auth_scopes)
