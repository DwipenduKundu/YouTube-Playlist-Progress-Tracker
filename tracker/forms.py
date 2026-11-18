from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Choose a username',
                'autocomplete': 'username'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
    
    password1 = forms.CharField(
    widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Create a password',
        'autocomplete': 'new-password'
        })
    )

    password2 = forms.CharField(
    widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Confirm your password',
        'autocomplete': 'new-password'
        })
    )

class PlaylistForm(forms.Form):

    playlist_url = forms.URLField(
        label="YouTube Playlist URL",
        max_length=500,
        widget=forms.URLInput(attrs={
            'class': 'playlist-input',
            'placeholder': 'Paste your YouTube playlist URL here'
        })
    )

    def clean_playlist_url(self):
        url = self.cleaned_data['playlist_url']

        if 'youtube.com/playlist' not in url:
            raise forms.ValidationError(
                'Please enter a valid YouTube playlist URL.'
            )

        if 'list=' not in url:
            raise forms.ValidationError(
                'Playlist ID is missing from the URL.'
            )

        return url

