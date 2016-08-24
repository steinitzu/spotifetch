import time
import logging
from collections import OrderedDict

from flask import redirect, url_for, request, session, render_template
from flask import jsonify
from flask import make_response

from . import app, log
from .spotifyutil import get_spotify_oauth, refresh_token
from . import spotifyutil
from . import forms
from .background_generator import background_generator
from . import sleepy_test


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


@app.route('/user_data')
def user_data():
    token = session.get('spotify_token')
    if not token:
        return redirect(url_for('app_authorize'))
    session['spotify_token'] = token = refresh_token(token)
    log.info('token:{}'.format(token['access_token']))

    t = token['access_token']
    data = {}
    data['artists'] = OrderedDict()
    data['current_user'] = spotifyutil.get_current_user(t)
    for tr in ('short_term', 'medium_term', 'long_term'):
        data['artists']['top_artists_'+tr] = spotifyutil.get_top(
            t, top_type='artists', time_range=tr)
    data['artists']['followed_artists'] = spotifyutil.get_followed_artists(t)
    return render_template('user_data.html',
                           user_data=data)


@app.route('/playlist_generator', methods=['GET', 'POST'])
def playlist_generator():
    token = session.get('spotify_token')
    if not token:
        return redirect(url_for('app_authorize'))
    session['spotify_token'] = token = refresh_token(token)
    log.info('token:{}'.format(token['access_token']))
    form = forms.PlaylistGenerator(request.form)

    if request.method == 'POST':
        log.info('Posted form fata: {}'.format(form.data))
        kw = {}
        kw['playlist_name'] = (
            form.playlist_name.data or 'Generated playlist')

        kw['top_artists_time_range'] = []

        for field in form.time_range_fields:
            if field.data:  # is True
                kw['top_artists_time_range'].append(
                    field.name[len('time_range_'):])

        kw['followed_artists'] = form.followed_artists.data
        kw['saved_album_artists'] = form.saved_album_artists.data

        if (not kw['followed_artists']
            and not kw['top_artists_time_range']
            and not kw['saved_album_artists']):
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
            if key.startswith('min_'):
                if value <= field.default:
                    continue
            elif key.startswith('max_'):
                if value >= field.default:
                    continue
            kw['tuneable'][key] = value

        task = background_generator.delay(token['access_token'], **kw)
        return make_response(
            jsonify({'task_id': task.id}), 202)
    return render_template(
        'playlist_generator.html',
        token=session['spotify_token']['access_token'],
        form=form)


@app.route('/task_status')
def task_status():
    task_id = request.args.get('task_id')
    task = background_generator.AsyncResult(task_id)
    return jsonify({'task_id': task_id,
                    'status': task.status, 'result': task.result})
