from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<media>[\w-]{3})/(?P<i_id>[0-9]+)/$', views.view_item, name='view-item'),  # View item
    url(r'^(?P<media>[\w-]{3})/(?P<i_id>[0-9]+)/play/$', views.play_item, name='play-item'),  # Play item
    url(r'^(?P<media>[\w-]{3})/add/$', views.edit_item, name='add-item'),  # Add item
    url(r'^(?P<media>[\w-]{3})/(?P<i_id>[0-9]+)/edit/$', views.edit_item, name='edit-item'),  # Edit item
    url(r'^(?P<media>[\w-]{3})/(?P<i_id>[0-9]+)/captions/$', views.edit_captions, name='edit-captions'),  # Edit captions
    url(r'^(?P<media>[\w-]{3})/(?P<i_id>[0-9]+)/cue/$', views.cue_captions, name='cue-captions'),  # Cue captions
    url(r'^ajax/cue_in/$', views.cue_in, name='cue_in'),  # Handle cue in
    url(r'^ajax/cue_out/$', views.cue_out, name='cue_out'),  # Handle cue out
]
