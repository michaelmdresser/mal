from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    chosen_name = forms.CharField(max_length=255, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'chosen_name', 'email', 'password1', 'password2', )

class ProfileUpdateForm(forms.Form):
    chosen_name_updated = forms.CharField(max_length=255)

class AddAnimeForm(forms.Form):
    english_name = forms.CharField(max_length=200)
    japanese_name = forms.CharField(max_length=200)

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=255)

class AddToGroupForm(forms.Form):
    username = forms.CharField()