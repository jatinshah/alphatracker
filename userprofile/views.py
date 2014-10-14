from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum

from userprofile.models import User, UserProfile, Following
from content.models import Post, PostVote, Comment
from content.views import domain_name
from userprofile.forms import ProfileForm
from userprofile.utils import ajax_login_required

from urllib import urlencode
from hashlib import md5
import json
import arrow


@ajax_login_required
def follow(request):
    response = {'authenticated': True}

    if request.is_ajax() and request.method == 'POST':
        following_username = request.POST['following_username']
        following_user = get_object_or_404(User, username=following_username)

        try:
            following = Following.objects.get(user=request.user, following=following_user)
            following.active = not following.active
            following.save(update_fields=['active'])
            response['following'] = following.active
        except Following.DoesNotExist:
            following = Following(user=request.user, following=following_user)
            following.save()
            response['following'] = following.active
        response['success'] = True
        return HttpResponse(
            json.dumps(response),
            content_type='application/json'
        )
    else:
        response['error'] = 'Invalid request'
        response['success'] = False
        return HttpResponse(
            json.dumps(response),
            content_type='application/json'
        )


def profile(request, username):
    context = RequestContext(request)

    user = get_object_or_404(User, username=username)
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        if request.user.is_authenticated():
            following = Following.objects.get(user=request.user, following=user)
            following_status = following.active
        else:
            following_status = False
    except Following.DoesNotExist:
        following_status = False

    following_count = Following.objects.filter(
        user=user, active=True).aggregate(Count('active'))['active__count']
    follower_count = Following.objects.filter(
        following=user, active=True).aggregate(Count('active'))['active__count']

    posts = Post.objects.filter(user=user, deleted=False).order_by('-created_on')

    for post in posts:
        post.created_on_humanize = arrow.get(post.created_on).humanize()
        if request.user.is_authenticated():
            try:
                post.vote = PostVote.objects.get(post=post,
                                                 user=request.user).vote
            except PostVote.DoesNotExist:
                post.vote = 0

        post.score = PostVote.objects.filter(post=post).aggregate(Sum('vote'))['vote__sum']
        if post.post_type == 'link':
            post.domain = domain_name(post.url)

        post.comments_count = Comment.objects.filter(post=post).count()

    context_dict = {
        'username': username,
        'user_profile': user_profile,
        'following': following_status,
        'following_count': following_count,
        'follower_count': follower_count,
        'posts': posts
    }

    return render_to_response('userprofile/profile.html', context_dict, context)


@login_required
def edit_profile(request):
    context = RequestContext(request)

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        edit_form = ProfileForm(request.POST)
        if edit_form.is_valid():
            data = edit_form.cleaned_data

            user_profile.full_name = data['full_name']
            user_profile.bio = data['bio']
            user_profile.save()

            return HttpResponseRedirect(
                reverse('userprofile.views.profile',
                        args=(),
                        kwargs={'username': request.user.username}))
        else:
            print edit_form.errors
    else:
        edit_form = ProfileForm({
            'full_name': user_profile.full_name,
            'bio': user_profile.bio
        })

    context_dict = {
        'edit_form': edit_form
    }

    return render_to_response('userprofile/edit.html', context_dict, context)
