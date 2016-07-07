import spotipy
import spotipy.util

from . import app


def get_token(username):
    scope = app.config['SPOTIFY_AUTHORIZATION_SCOPE']
    token = spotipy.util.prompt_for_user_token(username,
                                               scope=scope)

    return token


def spotipy_with_token(username):
    return spotipy.Spotify(auth=get_token(username))


def iterate_results(username, endpoint, *args, **kwargs):
    sp = spotipy_with_token(username)
    func = getattr(sp, endpoint)
    result = func(*args, **kwargs)
    while True:
        for item in result['items']:
            yield item
        if result['next']:
            result = sp.next(result)
        else:
            break


def get_saved_tracks(username):
    return iterate_results(username, 'current_user_saved_tracks')


def get_top(username, top_type='artists', time_range='medium_term'):
    endpoint = 'current_user_top_{}'.format(top_type)
    return iterate_results(username,
                           endpoint,
                           time_range=time_range)
