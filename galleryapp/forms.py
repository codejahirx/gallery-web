from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from galleryapp.models import CustomUser, Album


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'mobile_number',)


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'description', 'image', 'original_price', 'offer_price')
        labels = {'original_price': 'Original price $', 'offer_price': 'Offer price $'}
