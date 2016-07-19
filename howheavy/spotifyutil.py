import itertools

import spotipy
import spotipy.util

from . import app
from . import log
from .util import chunks


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


def get_recommendations(access_token, top_artists, limit=100, **kwargs):
    artist_ids = list(set([a['id'] for a in top_artists]))
    log.info('Number of artists used as seed:{}'.format(len(artist_ids)))
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

    tops = itertools.chain(get_top(access_token, time_range='short_term'),
                           get_top(access_token, time_range='medium_term'),
                           get_top(access_token, time_range='long_term'))
    recommendations = get_recommendations(
        access_token, tops, **kwargs)

    # Can't chunk an iterator

    # tracks_added = set()
    # for chunk in chunks(recommendations, 100):
    #     chunk = [t['uri'] for t in chunk]
    #     to_add = set(chunk).difference(tracks_added)
    #     spotify.user_playlist_add_tracks(
    #         user_id, playlist['id'], list(to_add))
    #     tracks_added = tracks_added.union(to_add)

    # Can't add one track at a time, too slow
    # for track in recommendations:
    #     if track['uri'] in tracks_added:
    #         continue
    #     spotify.user_playlist_add_tracks(
    #         user_id, playlist['id'], [track['uri']])
    #     tracks_added.add(track['uri'])

    # TODO: Find a way to make 100 track chunks while iterating
    track_uris = set([t['uri'] for t in recommendations])
    log.info('Number of tracks to be added:{}'.format(len(track_uris)))
    track_uris = chunks(list(track_uris), 100)

    for c in track_uris:
        spotify.user_playlist_add_tracks(
            user_id, playlist['id'], c)
