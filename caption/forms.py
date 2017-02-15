from django.contrib.contenttypes import forms
from .models import Youtube


class YoutubeForm(forms.ModelForm):
    class Meta:
        model = Youtube
        exclude = ['media_type', 'updated_by', 'created_by', 'played']
