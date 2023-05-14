from django.db.models import query
from django.http import request
from django.template.defaultfilters import slugify
from phishing.models import URL
from django import forms
from django.db import models
from django.forms import fields
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import re
# from unidecode import unidecode
from icecream import ic


class URLForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        url = super().save(commit=False)
        #url.user = self.user
        url.save()

    class Meta:
        model = URL
        fields = ["url"]
        widgets = {
            'url': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }
