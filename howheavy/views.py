import time
import logging

from flask import redirect, url_for, request, session, render_template
from flask import Response, jsonify

from . import app, log
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
    token = session['spotify_token']
    if not token:
        return redirect(url_for('app_authorize'))
    session['spotify_token'] = token = refresh_token(token)
    log.info('token:{}'.format(token['access_token']))
    form = forms.PlaylistGenerator(request.form)

    if request.method == 'POST':
        log.info('Form was posted')
        log.info(form.data)
        kw = {}
        kw['playlist_name'] = (
            form.playlist_name.data or 'Generated playlist')

        kw['top_artists_time_range'] = []

        for field in form.time_range_fields:
            if field.data:  # is True
                kw['top_artists_time_range'].append(
                    field.name[len('time_range_'):])

        kw['followed_artists'] = form.followed_artists.data


        if not kw['followed_artists'] and not kw['top_artists_time_range']:
            msg = 'Please check at least one of the checkboxes and try again :)'
            return msg, 400, {'Content-Type': 'text/plain'}
            return render_template(
                'playlist_generator.html',
                token=session['spotify_token']['access_token'],
                form=form)

        kw['tuneable'] = {}

        for field in form.tuneable_fields:
            key = field.name
            value = field.data
            if value < 0 or value > 1:
                continue
            # Ignore fields with 0 or 1 values since they make no difference
            if key.startswith('min_') and value == 0:
                continue
            if key.startswith('max_') and value == 1.0:
                continue
            kw['tuneable'][key] = value
        puri = spotifyutil.generate_playlist(token['access_token'], **kw)
        return puri, 200, {'Content-Type': 'text/plain'}
    return render_template(
        'playlist_generator.html',
        token=session['spotify_token']['access_token'],
        form=form)
