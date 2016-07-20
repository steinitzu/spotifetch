from flask_wtf import Form
from wtforms import DecimalField, FloatField

filter_attrs = (
        'acousticness',
        'danceability',
        'energy',
        'instrumentalness',
        'liveness',
        'loudness',
        'speechiness',
        'valence',
    )


class PlaylistGenerator(Form):
    pass

for attr in filter_attrs:
    setattr(PlaylistGenerator, 'min_'+attr,
            FloatField('Min '+attr))
    setattr(PlaylistGenerator, 'max_'+attr,
            FloatField('Max '+attr))
