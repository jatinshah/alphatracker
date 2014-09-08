from django import forms
from userprofile.models import User, UserProfile
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
            'max_length': 'Full Name must be less than 100 characters'
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
            'max_length': 'Bio must be less than 160 characters'
        }
    )


class SignupForm(forms.ModelForm):
    MIN_LENGTH = 8  # Minimum password length

    repeat_password = forms.CharField(label='Repeat Password',
                                      required=True,
                                      widget=forms.PasswordInput(
                                          attrs={'class': 'form-control',
                                                 'placeholder': 'Repeat password'}),
                                      error_messages={'required': 'Please repeat your password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter username',
                       'autofocus': 'true'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter email'}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter password'})
        }
        error_messages = {
            'username': {
                'required': _('Please choose a username.'),
            },
            'email': {
                'required': _('Please enter your email.'),
            },
            'password': {
                'required': _('Please enter a password.'),
            }
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if self.instance.username == username:
            return username
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            'Username already taken',
            code='unique',
        )

        return username

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data['repeat_password']

        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']

            if password and repeat_password and password != repeat_password:
                raise forms.ValidationError(
                    "Passwords don't match",
                    code='password_mismatch'
                )

        return repeat_password

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < self.MIN_LENGTH:
            raise forms.ValidationError(
                'Password must be at least {0} characters'.format(self.MIN_LENGTH),
                code='password_length'
            )

        # At least one letter and one digit
        all_alpha = all([c.isalpha() for c in password])
        all_digits = all([c.isdigit() for c in password])
        if all_alpha or all_digits:
            raise forms.ValidationError(
                'Use at least one letter and one digit',
                code='password_alphanumeric'
            )
        return password