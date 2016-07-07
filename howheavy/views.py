import os
import ast
import json

import spotipy
from flask import redirect, url_for, request, session

from . import app, log
from spotifyutil import get_top


@app.route('/')
def index():
    return '<html><a href="/app_authorize">Start app</a></html>'


def get_spotify_oauth():
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
    auth = spotipy.oauth2.SpotifyOAuth(
        client_id, client_secret, redirect_uri,
        scope=app.config['SPOTIFY_AUTHORIZATION_SCOPE'])
    return auth


@app.route('/app_authorize')
def app_authorize():
    token = session.get('spotify_auth_token')
    log.debug('Token:{}'.format(token))
    if token:
        return redirect(url_for('app_start'))
    else:
        auth = get_spotify_oauth()
        auth_url = auth.get_authorize_url()
        return redirect(auth_url)


@app.route('/callback')
def callback():
    """
    The spotify redirect uri should lead here.
    Get an access_token and add it to session.
    """
    auth = get_spotify_oauth()
    code = auth.parse_response_code(request.url)
    token = auth.get_access_token(code)
    session['spotify_access_token'] = token['access_token']
    return redirect(url_for('app_authorize'))


@app.route('/app_start')
def app_start():
    token = session['spotify_access_token']
    sp = spotipy.Spotify(auth=token)
    return str(sp.current_user())
