from django import forms
from .models import Youtube, Translation


class YoutubeForm(forms.ModelForm):
    class Meta:
        model = Youtube
        exclude = ['media_type', 'updated_by', 'created_by', 'played']


class TranslationAddForm(forms.ModelForm):
    class Meta:
        model = Translation
        exclude = ['item', 'updated_by', 'created_by']
        widgets = {'title': forms.TextInput(attrs={'placeholder': 'Title'})}
