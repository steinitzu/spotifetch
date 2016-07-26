import itertools
import time
import os
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util

from . import app
from . import log
from .util import chunks



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


def get_token(username):
    scope = app.config['SPOTIFY_AUTHORIZATION_SCOPE']
    token = spotipy.util.prompt_for_user_token(username,
                                               scope=scope)

    return token


def spotipy_with_token(username):
    return spotipy.Spotify(auth=get_token(username))


def iterate_results(spotify, endpoint, *args, **kwargs):
    sp = spotify
    func = getattr(sp, endpoint)
    try:
        target_key = kwargs.pop('target_key')
    except KeyError:
        target_key = 'items'
    result = func(*args, **kwargs)
    while True:
        for item in result[target_key]:
            yield item
        if result.get('next'):
            result = sp.next(result)
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


def generate_playlist(access_token, **kwargs):
    """
    Generate and save a playlist using top artists.
    All tuneable track attributes described at:
    https://developer.spotify.com/web-api/get-recommendations/
    are supported as kwargs.
    """
    spotify = spotipy.Spotify(auth=access_token)
    user_id = spotify.current_user()['id']
    name = 'howheavy_playlist'
    playlist = spotify.user_playlist_create(
        user_id, name, public=False)
    log.debug('Playlist_id:{}'.format(playlist['id']))

    log.debug('Kwargs for playlist generation:{}'.format(kwargs))
    time_range = kwargs.pop('time_range')
    tops = itertools.chain(
        *[get_top(access_token, top_type='artists', time_range=tr)
          for tr in time_range])
    # tops = get_all_top(access_token, top_type='artists')

    recommendations = get_recommendations(
        access_token, tops, limit=50, **kwargs)

    added = set()
    queue = []

    for track in recommendations:
        uri = track['uri']
        if uri in added:
            continue
        queue.append(uri)
        if len(queue) == 100:
            spotify.user_playlist_add_tracks(
                user_id, playlist['id'], queue)
            added.update(queue)
            queue = []
    # Add any remaining tracks to the playlist
    if queue:
        spotify.user_playlist_add_tracks(
            user_id, playlist['id'], queue)






    # TODO: Find a way to make 100 track chunks while iterating
    # track_uris = set([t['uri'] for t in recommendations])
    # log.info('Number of tracks to be added:{}'.format(len(track_uris)))
    # track_uris = chunks(list(track_uris), 100)

    # for c in track_uris:
    #     spotify.user_playlist_add_tracks(
    #         user_id, playlist['id'], c)
