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
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.filter_fields = []
        for field in self:
            if field.type in ['CSRFTokenField', 'HiddenField']:
                continue
            self.filter_fields.append(field)


for attr in filter_attrs:
    setattr(PlaylistGenerator, 'min_'+attr,
            FloatField('Min '+attr.capitalize(), default=0.0))
    setattr(PlaylistGenerator, 'max_'+attr,
            FloatField('Max '+attr.capitalize(), default=1.0))
