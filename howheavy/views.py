import os
import time

import spotipy
import flask
from flask import redirect, url_for, request, session, render_template
from flask import Response
from flask import stream_with_context

from . import app, log
from .spotifyutil import get_saved_tracks
from . import spotifyutil
from . import forms


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    return '<html><a href="/app_authorize">Start app</a></html>'


def get_spotify_oauth():
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
    log.info(app.config['SPOTIFY_AUTHORIZATION_SCOPE'])
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
    return redirect(url_for('playlist_generator',))


@app.route('/playlist_generator', methods=['GET', 'POST'])
def playlist_generator():
    form = forms.PlaylistGenerator(request.form)
    log.info(form.errors)
    if form.validate_on_submit():
        # TODO: need to allow None input to pass validation
        token = session['spotify_access_token']
        filter_kwargs = {}
        for key, value in form.data.items():
            if value < 0:
                continue
            filter_kwargs[key] = value
        spotifyutil.generate_playlist(token, **filter_kwargs)
        return redirect(url_for('index'))
    return render_template(
        'playlist_generator.html', token=session['spotify_access_token'],
        form=form)


@app.route('/generate_playlist', methods=['GET', 'POST'])
def generate_playlist():
    data = request.get_json()
    token = request.args.get('token') or session['spotify_access_token']
    spotifyutil.generate_playlist(token, **data)
    return 'Yo'


def jsonify_generator(generator):
    count = 0
    for row in generator:
        yield flask.json.dumps(row)+'\r'
        count += 1


@app.route('/saved_tracks', methods=['GET'])
def saved_tracks():
    token = request.args['token']
    tracks = get_saved_tracks(token)
    r = Response(jsonify_generator(tracks),
                 mimetype='application/json')
    #r.headers['Keep-Alive'] = 10
    return r


@app.route('/tinker')
def tinker():
    return render_template('tinker.html', token=session['spotify_access_token'])


@app.route('/tinker.json', methods=['GET'])
def tinker_json():
    return flask.json.dumps({'test1':1, 'test2':2})
