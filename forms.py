from django import forms

from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Score , Chauffeur , Post
from django.apps import apps







class SmsChauffeur(forms.ModelForm):
    class Meta:
        model= Chauffeur
        fields=['name' , 'date_of_birth', 'car' , 'num_phone' ]




class HomePost(forms.Form):
    post=forms.CharField















