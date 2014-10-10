from django.db.models import Sum

from content.models import Post, PostVote


def update_votes():
    for post in Post.objects.filter(deleted=False, flagged=False):
        votes = PostVote.objects.filter(post=post).aggregate(Sum('vote'))['vote__sum']
        if votes is not None:
            post.votes = votes
            post.save()


def run(*args):
    update_votes()