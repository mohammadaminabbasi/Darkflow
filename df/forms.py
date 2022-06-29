from django import forms

from songsapi.models import AudioStore


class AudioForm(forms.ModelForm):
    class Meta:
        model = AudioStore
        fields = ['record']
