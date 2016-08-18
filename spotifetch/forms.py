import logging

from flask_wtf import Form
from wtforms import DecimalField, FloatField, BooleanField, StringField, IntegerField
from wtforms.widgets.core import HTMLString, html_params, escape

from . import app, log


tuneable_attrs = (
    dict(name='acousticness', min=0.0, max=1.0,
         step=0.01,
         field_type=FloatField),
    dict(name='danceability', min=0.0, max=1.0,
         step=0.01,
         field_type=FloatField),
    dict(name='energy', min=0.0, max=1.0,
         step=0.01,
         field_type=FloatField),
    dict(name='instrumentalness', min=0.0, max=1.0,
         step=0.01,
         field_type=FloatField),
    dict(name='liveness', min=0.0, max=1.0,
         step=0.01,
         field_type=FloatField),
    dict(name='speechiness', min=0.0, max=1.0,
         step=0.01,
         field_type=FloatField),
    dict(name='valence', min=0.0, max=1.0,
         step=0.01,
         field_type=FloatField),
    dict(name='popularity', min=0, max=100,
         step=1,
         field_type=IntegerField),
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
        html = '<input %s></input>'
        return HTMLString(html % (params))


class PlaylistGenerator(Form):
    playlist_name = StringField(render_kw={'placeholder':'Name your playlist'})
    time_range_short_term = BooleanField('My top 50 artists: ~4 weeks back')
    time_range_medium_term = BooleanField('My top 50 artists: ~6 months back')
    time_range_long_term = BooleanField('My top 50 artists: several years back')
    followed_artists = BooleanField(
        'My followed artists')
    saved_album_artists = BooleanField(
        'My saved album artists')

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
    setattr(PlaylistGenerator,
            'min_'+attr['name'],
            attr['field_type'](attr['name'].capitalize(),
                               default=attr['min'],
                               widget=TextDisplayWidget(),
                               render_kw={
                                   'default': attr['min'],
                                   'step': attr['step'],
                                   'field_type': str(attr['field_type'].__name__)}))
    setattr(PlaylistGenerator,
            'max_'+attr['name'],
            attr['field_type']('Max '+attr['name'].capitalize(),
                               default=attr['max'],
                               widget=TextDisplayWidget(),
                               render_kw={
                                   'default': attr['max'],
                                   'step': attr['step'],
                                   'field_type': str(attr['field_type'].__name__)}))
