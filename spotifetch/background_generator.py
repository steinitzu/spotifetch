from . import celery
from .spotifyutil import PlaylistGenerator


@celery.task()
def background_generator(*args, **kwargs):
    gen = PlaylistGenerator(*args, **kwargs)
    puri = gen.generate_playlist()
    return puri
