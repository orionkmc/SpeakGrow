from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Apps
from .models import (UserProfile)


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'signin-email',
                'class': '''
                    cd-signin-modal__input cd-signin-modal__input--full-width cd-signin-modal__input--has-padding
                    cd-signin-modal__input--has-border
                ''',
                'placeholder': 'Username',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'signin-password',
                'class': '''
                    cd-signin-modal__input cd-signin-modal__input--full-width cd-signin-modal__input--has-padding
                    cd-signin-modal__input--has-border
                ''',
                'placeholder': 'contraseña',
            }
        )
    )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError(
                'Los datos de usuario no son correctos'
            )

        return self.cleaned_data


class UserRegisterForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        label='Username',
        required=True,
    )
    phone_number = forms.IntegerField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'signin-email',
                'placeholder': 'Phone Number',
            }
        )
    )
    short_description = forms.CharField(
        label='Username',
        required=True,
        widget=forms.Textarea(
            attrs={
                'id': 'signin-email',
                'placeholder': 'Short Description',
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username', 'password', 'email', 'first_name', 'last_name',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Username',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': 'Password',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Email',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last Name',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        fs = self.fields
        for f in fs:
            if f not in ['gender']:
                fs[f].widget.attrs['class'] = '''
                    cd-signin-modal__input cd-signin-modal__input--full-width cd-signin-modal__input--has-padding
                    cd-signin-modal__input--has-border
                '''

    def save(self, commit=True):
        data = self.cleaned_data
        try:
            user = User.objects.create(
                username=data['username'],
                password=make_password(data['password']),
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
            )

            UserProfile.objects.create(
                user=user,
                profile_picture=data['profile_picture'],
                phone_number=data['phone_number'],
                short_description=data['short_description'],
            )
        except Exception as e:
            raise e
