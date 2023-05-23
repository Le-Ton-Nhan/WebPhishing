from .models import URL
from django import forms
from django.contrib.auth.models import User

class URLForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        url = super().save(commit=False)
        url.user = self.user
        url.save()

    def showURL(self, commit=False):
        url = super().save(commit)
        return url.url
    class Meta:
        model = URL
        fields = ['url']
        widgets = {
            'url': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }
