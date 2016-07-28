from flask_wtf import Form
from wtforms import DecimalField, FloatField, BooleanField, StringField
from wtforms.widgets.core import HTMLString, html_params, escape

from . import log


tuneable_attrs = (
        'acousticness',
        'danceability',
        'energy',
        'instrumentalness',
        'liveness',
        'speechiness',
        'valence',
    )

class InlineButtonWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'submit')
        # Allow passing title= or alternately use field.description
        title = kwargs.pop('title', field.description or '')
        params = html_params(title=title, **kwargs)

        html = '<button %s><span>%s</span></button>'
        return HTMLString(html % (params, escape(field.label.text)))


class TextDisplayWidget(object):
    def __call__(self, field, **kwargs):
        kwargs['id'] = field.name
        kwargs['value'] = field._value()
        kwargs['name'] = field.name
        #kwargs['type'] = 'text'
        kwargs['class'] = 'not-a-textbox'
        kwargs['readonly'] = True
        params = html_params(**kwargs)
        log.info(params)
        html = '<input %s></input>'
        return HTMLString(html % (params))


class PlaylistGenerator(Form):
    playlist_name = StringField(render_kw={'placeholder':'Name your playlist'})
    time_range_short_term = BooleanField('Short term')
    time_range_medium_term = BooleanField('Medium term')
    time_range_long_term = BooleanField('Long term')
    followed_artists = BooleanField(
        'Use my followed artists')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.tuneable_fields = []
        self.time_range_fields = []
        for field in self:
            if field.type in ['CSRFTokenField', 'HiddenField']:
                continue
            elif field.name.startswith('time_range_'):
                self.time_range_fields.append(field)
            elif (field.name.startswith('min_') or
                  field.name.startswith('max_')):
                self.tuneable_fields.append(field)
            else:
                pass



for attr in tuneable_attrs:
    setattr(PlaylistGenerator, 'min_'+attr,
            FloatField(attr.capitalize(), default=0.0,
                       widget=TextDisplayWidget()))
    setattr(PlaylistGenerator, 'max_'+attr,
            FloatField('Max '+attr.capitalize(), default=1.0,
                       widget=TextDisplayWidget()))
