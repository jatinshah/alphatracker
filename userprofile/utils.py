from django.http import HttpResponse

from functools import wraps
import json
from datetime import datetime, timedelta

from userprofile.models import UserProfile
from content.models import Post, PostVote
from alphatracker.settings import MODERATORS


def ajax_login_required(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_function(request, *args, **kwargs)
        else:
            response = {'authenticated': False}
            return HttpResponse(
                json.dumps(response),
                content_type='application/json'
            )

    return wrapper


def ajax_moderator_required(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        response = {
            'authenticated': request.user.is_authenticated
        }
        if request.user.is_authenticated and request.user.username in MODERATORS:
            return view_function(request, *args, **kwargs)
        else:
            response['success'] = False
            return HttpResponse(
                json.dumps(response),
                content_type='application/json'
            )

    return wrapper


def get_user_permissions(request, post=None):
    permissions = {}
    try:
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.status == UserProfile.EMAIL_NOT_CONFIRMED:
            permissions['email_confirmed'] = False
        else:
            permissions['email_confirmed'] = True

        if user_profile.status == UserProfile.NEW_USER:
            user_posts = Post.objects.filter(user=request.user)
            votes_received = PostVote.objects.filter(
                post__in=user_posts,
                vote__in=[1, -1]
            ).exclude(
                user=request.user
            ).count()

            if votes_received >= 25:
                user_profile.status = UserProfile.FULL_ACCESS
                user_profile.save()

        if user_profile.status == UserProfile.FULL_ACCESS:
            permissions['new_user'] = False
        else:
            permissions['new_user'] = True

        posts_1d = Post.objects.filter(
            user=request.user,
            created_on__gte=datetime.now()-timedelta(days=1)
        ).count()
        posts_30d = Post.objects.filter(
            user=request.user,
            created_on__gte=datetime.now()-timedelta(days=30)
        ).count()

        postvotes_1d = PostVote.objects.filter(
            user=request.user,
            vote__in=[1,-1],
            created_on__gte=datetime.now()-timedelta(days=1)
        ).count()

        postvotes_30d = PostVote.objects.filter(
            user=request.user,
            vote__in=[1,-1],
            created_on__gte=datetime.now()-timedelta(days=30)
        ).count()

        if permissions['new_user']:
            if post:
                permissions['can_comment'] = (request.user.username == post.user.username)
            else:
                permissions['can_comment'] = False
            if permissions['email_confirmed'] and posts_1d < 5 and posts_30d < 25:
                permissions['can_post'] = True
            else:
                permissions['can_post'] = False
            permissions['can_vote'] = postvotes_1d < 5 and postvotes_30d < 50
        else:
            permissions['can_comment'] = True
            permissions['can_post'] = True
            permissions['can_vote'] = postvotes_1d < 25 and postvotes_30d < 250

        return permissions
    except UserProfile.DoesNotExist:
        return None