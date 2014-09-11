from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    full_name = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=160, blank=True)

    def __unicode__(self):
        return self.user.username


class Following(models.Model):
    user = models.ForeignKey(User, related_name='user')
    following = models.ForeignKey(User, related_name='following')

    active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username + '-->' + self.following.username