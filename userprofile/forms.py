from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField

from collections import OrderedDict


class ProfileForm(forms.Form):
    full_name = forms.CharField(
        label='Full Name',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }
        ),
        error_messages={
            'max_length': _('Full Name must be less than 100 characters')
        }
    )
    bio = forms.CharField(
        label='Bio',
        required=False,
        max_length=160,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'bio',
                'placeholder': 'Enter your bio',
                'rows': '3',
            }
        ),
        error_messages={
            'max_length': _('Bio must be less than 160 characters')
        }
    )


class SignUpForm(forms.Form):

    captcha = ReCaptchaField(attrs={'theme': 'white'})

    def __init__(self, *args, **kwargs):
        fields_key_order = ['username', 'email', 'password1', 'password2', 'captcha']
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)

    def signup(self, request, user):
        pass