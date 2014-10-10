from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from math import log10

from ranking.models import Stock


# Create your models here.
class Post(models.Model):
    POST_TYPES = (('article', 'Article'), ('link', 'Link'))
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

    flagged = models.BooleanField(default=False)
    flagged_on = models.DateTimeField(null=True)

    stock_performance = models.FloatField(default=0)
    post_performance = models.FloatField(default=0)
    performance_updated_on = models.DateTimeField(null=True)

    votes = models.IntegerField(default=0)
    log_votes = models.IntegerField(default=-1)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '[' + self.post_type + '] (' + self.stock.symbol + ') ' + self.title

    def get_absolute_url(self):
        return reverse('content.views.post', args=[self.slug, ])

    def save(self, *args, **kwargs):
        if self.votes <= 0:
            self.log_votes = -1
        else:
            self.log_votes = log10(self.votes)

        if self.trend == 'bear':
            self.post_performance = (-1) * self.stock_performance
        else:
            self.post_performance = self.stock_performance

        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.PROTECT)
    user = models.ForeignKey(User)
    slug = models.SlugField(max_length=200)

    text = models.TextField()

    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '[' + self.post.title[:20] + '...](' + self.user.username + ') ' + self.text[:50]

    class Meta:
        unique_together = ('post', 'slug')


class PostVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    vote = models.SmallIntegerField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '(' + str(self.vote) + ')' + '[' + self.user.username + ']' + '{' + unicode(self.post) + '}'


class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    vote = models.SmallIntegerField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '(' + str(self.vote) + ')' + '[' + self.user.username + ']' + '{' + unicode(self.comment) + '}'
