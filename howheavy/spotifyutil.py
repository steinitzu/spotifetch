import itertools
import time
import os
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util

from . import app, log
from .util import chunks
from .util import dict_get_nested


def get_spotify_oauth():
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
    log.info(app.config['SPOTIFY_AUTHORIZATION_SCOPE'])
    auth = ExtendedOAuth(
        client_id, client_secret, redirect_uri,
        scope=app.config['SPOTIFY_AUTHORIZATION_SCOPE'])
    return auth


def token_is_expired(token):
    return token['expires_at'] < time.time()


def refresh_token(token):
    if token_is_expired(token):
        log.info('Token expired, refreshing:{}'.format(token['access_token']))
        auth = get_spotify_oauth()
        return auth._refresh_access_token(token['refresh_token'])
    else:
        return token


class ExtendedOAuth(SpotifyOAuth):
    def __init__(self, *args, **kwargs):
        SpotifyOAuth.__init__(self, *args, **kwargs)
        self.token_info = None

    def get_access_token(self, code):
        """
        Overrides get_access_token to store
        the token in an instance variable after creation.
        """
        self.token_info = SpotifyOAuth.get_access_token(
            self, code)
        return self.token_info

    def get_stored_token(self):
        """
        Get self.token_info, refreshing the token if needed.
        """
        is_expired = self._is_token_expired(self.token_info)
        if self.token_info:
            if is_expired:
                self.token_info = self._refresh_access_token(
                    self.token_info['refresh_token'])
            return self.token_infon


def iterate_results(spotify, endpoint, *args, **kwargs):
    sp = spotify
    func = getattr(sp, endpoint)
    try:
        target_key = kwargs.pop('target_key')
    except KeyError:
        target_key = 'items'
    try:
        next_key = kwargs.pop('next_key')
    except KeyError:
        next_key = 'next'

    result = func(*args, **kwargs)
    while True:
        itemlist = dict_get_nested(target_key, result)
        for item in itemlist:
            yield item
        try:
            next_url = dict_get_nested(next_key, result)
        except KeyError:
            break
        if next_url:
            result = sp._get(next_url)
        else:
            break


def get_saved_tracks(access_token):
    spotify = spotipy.Spotify(auth=access_token)
    return iterate_results(spotify, 'current_user_saved_tracks', limit=50)


def get_top(access_token, top_type='artists', time_range='medium_term'):
    spotify = spotipy.Spotify(auth=access_token)
    endpoint = 'current_user_top_{}'.format(top_type)
    return iterate_results(spotify,
                           endpoint,
                           time_range=time_range,
                           limit=50)


def get_all_top(access_token, top_type='artists'):
    return itertools.chain(
        get_top(access_token, top_type=top_type, time_range='short_term'),
        get_top(access_token, top_type=top_type, time_range='medium_term'),
        get_top(access_token, top_type=top_type, time_range='long_term'))


def get_followed_artists(access_token):
    spotify = spotipy.Spotify(auth=access_token)
    return iterate_results(spotify,
                           'current_user_followed_artists',
                           target_key=['artists', 'items'],
                           next_key=['artists', 'next'],
                           limit=50)


def get_recommendations(access_token, seed_artists, limit=100, **kwargs):
    artist_ids = list(set([a['id'] for a in seed_artists]))
    log.info('Number of artists used as seed:{}'.format(len(artist_ids)))
    log.info('Tuneables:{}'.format(kwargs))
    spotify = spotipy.Spotify(auth=access_token)
    endpoint = 'recommendations'
    gens = []
    for artist in artist_ids:
        gens.append(
            iterate_results(spotify,
                            endpoint,
                            target_key='tracks',
                            seed_artists=[artist],
                            limit=limit,
                            **kwargs))
    log.info('Number of track generators:{}'.format(len(gens)))
    return itertools.chain(*gens)


artist_seeds = [
    'top_artists_short_range',
    'top_artists_medium_range',
    'top_artists_long_range',
    'followed_artists'
    ]


def generate_playlist(access_token, **kwargs):
    log.info('Generating playlist')
    sp = spotipy.Spotify(auth=access_token)
    user_id = sp.current_user()['id']
    playlist_name = kwargs.get('playlist_name', 'Generated playlist')

    playlist = sp.user_playlist_create(
        user_id, playlist_name, public=True)

    seed_gens = []

    if kwargs.get('followed_artists'):
        seed_gens.append(
            get_followed_artists(access_token))

    for tr in kwargs['top_artists_time_range']:
        seed_gens.append(
            get_top(access_token, top_type='artists', time_range=tr))

    seed_gens = itertools.chain(*seed_gens)

    recommendations = get_recommendations(
        access_token, seed_gens, limit=50, **kwargs['tuneable'])

    added = set()
    queue = []

    for track in recommendations:
        uri = track['uri']
        if uri in added:
            # No duplicates
            continue
        queue.append(uri)
        if len(queue) == 100:
            # Can only add 100 tracks at a time through the spotify api
            sp.user_playlist_add_tracks(
                user_id, playlist['id'], queue)
            added.update(queue)
            queue = []
    # Add any remaining tracks to the playlist
    if queue:
        sp.user_playlist_add_tracks(
            user_id, playlist['id'], queue)
    return playlist['uri']
