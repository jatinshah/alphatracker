from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from ranking.models import Stock


# Create your models here.
class Post(models.Model):
    POST_TYPES = (('link', 'Link'), ('article', 'Article'))
    TREND_TYPES = (('bull', 'bull'), ('bear', 'bear'))

    user = models.ForeignKey(User)

    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='link')
    stock = models.ForeignKey(Stock, null=True, on_delete=models.PROTECT)
    trend = models.CharField(max_length=5, choices=TREND_TYPES, default='bull')

    title = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    slug = models.SlugField(unique=True, max_length=200)
    text = models.TextField(blank=True)

    active = models.BooleanField(default=True)
    last_active_on = models.DateTimeField(null=True)

    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '[' + self.post_type + '] (' + self.stock.symbol + ') ' + self.title

    def get_absolute_url(self):
        return reverse('content.views.post', args=[self.slug,])


class PostVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    vote = models.SmallIntegerField(default=0)

    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '(' + str(self.vote) + ')' + '[' + self.user.username + ']' + '{' + unicode(self.post) +'}'


# class CommentVotes(models.Model):
#     pass
class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.PROTECT)
    user = models.ForeignKey(User)

    text = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '[' + self.post.title[:20] + '...](' + self.user.username + ') ' + self.text