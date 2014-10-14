from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from allauth.account.signals import email_confirmed, user_signed_up

from urllib import urlencode
from hashlib import md5


# Create your models here.
class UserProfile(models.Model):
    EMAIL_NOT_CONFIRMED = 'E'
    NEW_USER = 'N'
    FULL_ACCESS = 'F'
    STATUS = (
        (EMAIL_NOT_CONFIRMED, 'Unconfirmed Email'),
        (NEW_USER, 'New User'),
        (FULL_ACCESS, 'Full Access')
    )
    user = models.OneToOneField(User)

    full_name = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=160, blank=True)

    status = models.CharField(max_length=2,
                              choices=STATUS,
                              default=EMAIL_NOT_CONFIRMED)

    def __unicode__(self):
        return self.user.username

    @property
    def gravatar_url(self):
        default = 'retro'

        url = "http://www.gravatar.com/avatar/" + md5(self.user.email.lower()).hexdigest() + '?'
        url += urlencode({'d':default})

        return url



class Following(models.Model):
    user = models.ForeignKey(User, related_name='user')
    following = models.ForeignKey(User, related_name='following')

    active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username + '-->' + self.following.username


@receiver(email_confirmed)
def after_email_confirmed(sender, **kwargs):
    try:
        email_address = kwargs.get('email_address')
        user = User.objects.get(email=email_address.email)
        user_profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        print "Error: Email {0} confirmed for non-existent user".format(
            email_address.email
        )
        return
    except UserProfile.DoesNotExist:
        user_profile=UserProfile(user=user)

    user_profile.status = UserProfile.NEW_USER
    user_profile.save()


# Create user_profile object
@receiver(user_signed_up)
def after_signup(sender, **kwargs):
    user = kwargs.get('user')
    user_profile = UserProfile(user=user)
    user_profile.save()