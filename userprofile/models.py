from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    #photo
    website = models.URLField(blank=True)
    bio = models.CharField(max_length=160, blank=True)

    # following & followers
    # performance
    # rank

    def __unicode__(self):
        return self.user.username