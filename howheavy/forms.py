from flask_wtf import Form
from wtforms import DecimalField, FloatField, BooleanField

tuneable_attrs = (
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
    time_range_short_term = BooleanField('Short term')
    time_range_medium_term = BooleanField('Medium term')
    time_range_long_term = BooleanField('Long term')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.tuneable_fields = []
        self.time_range_fields = []
        for field in self:
            if field.type in ['CSRFTokenField', 'HiddenField']:
                continue
            elif field.name.startswith('time_range_'):
                self.time_range_fields.append(field)
            else:
                self.tuneable_fields.append(field)


for attr in tuneable_attrs:
    setattr(PlaylistGenerator, 'min_'+attr,
            FloatField(attr.capitalize(), default=0.0))
    setattr(PlaylistGenerator, 'max_'+attr,
            FloatField('Max '+attr.capitalize(), default=1.0))
