import os
import time

import spotipy
import flask
from flask import redirect, url_for, request, session, render_template
from flask import Response

from . import app, log
from spotifyutil import get_saved_tracks


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
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
    token = session.get('spotify_access_token')
    full_token = session.get('spotify_full_token')
    log.debug('Token:{}'.format(full_token))
    if token and full_token['expires_at'] > time.time():
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
    session['spotify_full_token'] = token
    return redirect(url_for('app_authorize'))


@app.route('/app_start')
def app_start():
    return redirect(url_for('saved_tracks'))


def jsonify_generator(generator):
    count = 0
    for row in generator:
        log.debug('Row count:{}'.format(count))
        count += 1
        yield flask.json.dumps(row)


@app.route('/saved_tracks', methods=['GET'])
def saved_tracks():
    token = session['spotify_access_token']
    tracks = get_saved_tracks(token)
    return Response(jsonify_generator(tracks),
                    mimetype='application/json')
