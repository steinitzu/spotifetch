import os
import time

import spotipy
import flask
from flask import redirect, url_for, request, session, render_template
from flask import Response
from flask import stream_with_context

from . import app, log
from .spotifyutil import get_saved_tracks
from .spotifyutil import get_spotify_oauth, refresh_token
from . import spotifyutil
from . import forms


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    return '<html><a href="/app_authorize">Start app</a></html>'


@app.route('/app_authorize')
def app_authorize():
    token = session.get('spotify_token')
    if token:
        return redirect(url_for('app_start'))
    else:
        auth = get_spotify_oauth()
        auth_url = auth.get_authorize_url()
        return redirect(auth_url)


# Spotify oauth callback url
@app.route('/callback')
def callback():
    """
    The spotify redirect uri should lead here.
    Get an access_token and add it to session.
    """
    auth = get_spotify_oauth()
    code = auth.parse_response_code(request.url)
    token = auth.get_access_token(code)
    session['spotify_token'] = token
    return redirect(url_for('app_authorize'))


@app.route('/app_start')
def app_start():
    return redirect(url_for('playlist_generator',))


@app.route('/playlist_generator', methods=['GET', 'POST'])
def playlist_generator():
    token = session.get('spotify_token')
    if not token:
        return redirect(url_for('app_authorize'))
    form = forms.PlaylistGenerator(request.form)
    if form.validate_on_submit():
        log.info('token:{}'.format(token))
        refresh_token(token)
        return '<br/>'.join(
            ['{}: {}'.format(key, value) for key, value in form.data.items()])
        filter_kwargs = {}
        filter_kwargs['time_range'] = []
        log.debug('Filter kwargs:{}'.format(filter_kwargs))
        for field in form.time_range_fields:
            if field.data:  # is True
                filter_kwargs['time_range'].append(
                    field.name[len('time_range_'):])
        if not filter_kwargs['time_range']:
            filter_kwargs['time_range'] += [
                'short_term', 'medium_term', 'long_term']

        for field in form.tuneable_fields:
            key = field.name
            value = field.data
            if value < 0 or value > 1:
                continue
            if key.startswith('min_') and value == 0:
                continue
            if key.startswith('max_') and value == 1.0:
                continue
            filter_kwargs[key] = value
        spotifyutil.generate_playlist(token, **filter_kwargs)
        return redirect(url_for('index'))
    return render_template(
        'playlist_generator.html', token=session['spotify_token'],
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
