from django import forms
from django.utils.translation import ugettext_lazy as _


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