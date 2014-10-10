from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.contrib import messages

import itertools
import arrow
import json
from urlparse import urlsplit
from datetime import timedelta, datetime, date

from content.forms import PostForm, CommentForm
from content.models import Post, Comment, PostVote, CommentVote
from ranking.models import Stock
from userprofile.utils import ajax_login_required, get_user_permissions, ajax_moderator_required
from userprofile.models import Following
from alphatracker.settings import CONTENT_URL, MODERATORS, SLUG_MAX_LENGTH
from alphatracker.utils import mixpanel_track


# Up/Down vote on comment
@ajax_login_required
def vote_comment(request):
    response = {'authenticated': True}

    if request.is_ajax() and request.method == 'POST':
        post_slug = request.POST['post_slug']
        comment_slug = request.POST['comment_slug']
        vote = request.POST['vote']

        try:
            vote = sorted((-1, int(vote), 1))[1]
        except ValueError:
            response['error'] = 'Invalid vote'
            response['success'] = False
            return HttpResponse(
                json.dumps(response),
                content_type='application/json'
            )

        post = get_object_or_404(Post, slug=post_slug)
        comment = get_object_or_404(Comment,post=post, slug=comment_slug)

        try:
            comment_vote = CommentVote.objects.get(comment=comment, user=request.user)
            if comment_vote.vote * vote < 0 or comment_vote.vote == 0:
                comment_vote.vote = vote
            elif comment_vote.vote * vote > 0:
                comment_vote.vote = 0
            comment_vote.save(update_fields=['vote'])
        except CommentVote.DoesNotExist:
            comment_vote = CommentVote(comment=comment,
                                       user=request.user,
                                       vote=vote)
            comment_vote.save()

        response['success'] = True
        return HttpResponse(
            json.dumps(response),
            content_type='application/json')
    else:
        response['error'] = 'Invalid request'
        return HttpResponse(
            json.dumps(response),
            content_type='application/json')

# Up/Down vote on a post
@ajax_login_required
def vote_post(request):
    response = {'authenticated': True}

    if request.is_ajax() and request.method == 'POST':
        slug = request.POST['slug']
        vote = request.POST['vote']

        try:
            vote = sorted((-1, int(vote), 1))[1]
        except ValueError:
            response['error']='Invalid vote'
            response['success'] = False
            return HttpResponse(
                json.dumps(response),
                content_type='application/json'
            )

        post = get_object_or_404(Post, slug=slug)

        try:
            post_vote = PostVote.objects.get(post=post, user=request.user)
            if post_vote.vote * vote < 0 or post_vote.vote == 0:
                post_vote.vote = vote
                post.votes += 1
            elif post_vote.vote * vote > 0:
                post_vote.vote = 0
                post.votes -= 1

            post_vote.save(update_fields=['vote'])

        except PostVote.DoesNotExist:
            post_vote = PostVote(post=post, user=request.user, vote=vote)
            post.votes += 1

            post_vote.save()

        post.save(update_fields=['votes'])
        response['success'] = True
        return HttpResponse(
            json.dumps(response),
            content_type='application/json')
    else:
        response['error'] = 'Invalid request'
        return HttpResponse(
            json.dumps(response),
            content_type='application/json')


def top_ideas(request, time_frame='today', page=1):
    context = RequestContext(request)

    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    time_frame_map = {
        'today': datetime(today.year, today.month, today.day),
        'this_week': datetime(start_week.year, start_week.month, start_week.day),
        'this_month': datetime(today.year, today.month, 1),
        'this_quarter': datetime(today.year, 3 * (today.month/3) + 1, 1),
        'this_year': datetime(today.year, 1, 1),
        'all': datetime(1970, 1, 1)
    }

    if time_frame in time_frame_map.keys():
        all_posts = Post.objects.filter(
            deleted=False,
            flagged=False,
            created_on__gte=time_frame_map[time_frame]
        ).order_by('-log_votes', '-post_performance')
    else:
        raise Http404

    # Paginate
    paginator = Paginator(all_posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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
        'posts': posts,
        'path': CONTENT_URL + 'top_ideas/' + time_frame + '/'
    }

    return render_to_response('content/top_ideas.html', context_dict, context)


@login_required
def get_following(request, page=1):
    return get_feed(request, page=page, order='follow')


def get_feed(request, page=1, order='recent'):
    context = RequestContext(request)

    if order == 'recent':
        all_posts = Post.objects.filter(
            deleted=False,
            flagged=False).order_by('-created_on')
    elif order == 'trending':
        all_posts = Post.objects.filter(
            deleted=False,
            flagged=False
        ).order_by('-created_on')   # TODO: modify ordering
    elif order == 'follow':
        following = Following.objects.filter(user=request.user, active=True)
        following_users = [f.following for f in following]
        all_posts = Post.objects.filter(
            user__in=following_users,
            deleted=False,
            flagged=False).order_by('-created_on')

    paginator = Paginator(all_posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # Last page if out of range
        posts = paginator.page(paginator.num_pages)

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
        'posts': posts,
        'path': CONTENT_URL + order + '/'
    }

    if order == 'recent':
        return render_to_response('content/recent.html', context_dict, context)
    elif order == 'trending':
        return render_to_response('content/trending.html', context_dict, context)
    elif order == 'follow':
        return render_to_response('content/follow.html', context_dict, context)


def post(request, slug, error_messages=None):
    context = RequestContext(request)

    if not error_messages:
        comment_form = CommentForm(initial={'slug': slug})

    post = get_object_or_404(Post, slug=slug)
    if post.deleted:
        raise Http404

    post.created_on_humanize = arrow.get(post.created_on).humanize()

    if request.user.is_authenticated():
        can_comment = get_user_permissions(request, post)['can_comment']
        try:
            post.vote = PostVote.objects.get(post=post, user=request.user).vote
        except PostVote.DoesNotExist:
            post.vote = 0
    else:
        can_comment = None

    post.score = PostVote.objects.filter(post=post).aggregate(Sum('vote'))['vote__sum']

    if post.post_type == 'link':
        post.domain = domain_name(post.url)
    post.is_recent = (timezone.now() - post.created_on) < timedelta(days=1)

    moderator = request.user.username in MODERATORS

    all_comments = Comment.objects.filter(post=post).order_by('-created_on')
    for comment in all_comments:
        comment.created_on_humanize = arrow.get(comment.created_on).humanize()
        if request.user.is_authenticated():
            try:
                comment.vote = CommentVote.objects.get(comment=comment,
                                                       user=request.user).vote
            except CommentVote.DoesNotExist:
                comment.vote = 0

        comment.score = CommentVote.objects.filter(comment=comment).aggregate(Sum('vote'))['vote__sum']

    context_dict = {
        'post': post,
        'user': request.user,
        'can_comment': can_comment,
        'comments': all_comments,
        'comment_form': comment_form,
        'moderator': moderator
    }

    return render_to_response('content/post.html', context_dict, context)


@login_required
def add_comment(request):
    context = RequestContext(request)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            post_slug = comment_form.cleaned_data['slug']
            post = get_object_or_404(Post, slug=post_slug)
            text = comment_form.cleaned_data['text']

            # Get commenting permission for the specific post
            permissions = get_user_permissions(request, post)
            # Create comment slug
            comment_slug = orig_slug = slugify(text)[:SLUG_MAX_LENGTH].strip('-')
            for x in itertools.count(1):
                if not Comment.objects.filter(post=post, slug=comment_slug).exists():
                    break
                comment_slug = '%s-%d' % (orig_slug[:SLUG_MAX_LENGTH - len(str(x)) - 1], x)

            if permissions['can_comment']:
                comment = Comment.objects.create(
                    post=post,
                    user=request.user,
                    slug=comment_slug,
                    text=text
                )
                comment.save()
                mixpanel_track(
                    request.user.username,
                    'Comment',
                    {'Post': post_slug, 'Post User': post.user.username}
                )
        else:
            print comment_form.errors['text'][0]
            post_slug = comment_form.cleaned_data['slug']

        return HttpResponseRedirect(
            reverse('content.views.post',
                    args=(),
                    kwargs={'slug': post_slug}))
    else:
        return redirect('/c/')


@login_required
def submit(request):
    context = RequestContext(request)

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        permissions = get_user_permissions(request)

        if post_form.is_valid() and permissions['can_post']:
            user = request.user
            data = post_form.cleaned_data

            post_type = data['post_type']
            symbol = data['symbol']
            trend = data['trend']
            title = data['title']

            stock = Stock.objects.get(symbol=symbol)

            # Create slug
            slug = orig_slug = slugify(title)[:SLUG_MAX_LENGTH].strip('-')
            for x in itertools.count(1):
                if not Post.objects.filter(slug=slug).exists():
                    break
                slug = '%s-%d' % (orig_slug[:SLUG_MAX_LENGTH - len(str(x)) - 1], x)

            if post_type == 'link':
                url = data['url']
                text = data['summary']
                post = Post.objects.create(
                    user=user,
                    post_type=post_type,
                    trend=trend,
                    stock=stock,
                    title=title,
                    slug=slug,
                    url=url,
                    text=text
                )
            elif post_type == 'article':
                text = data['text']
                post = Post.objects.create(
                    user=user,
                    post_type=post_type,
                    trend=trend,
                    stock=stock,
                    title=title,
                    slug=slug,
                    text=text
                )
            post.save()
            mixpanel_track(request.user.username, 'Post', {'Type': post_type})
            return redirect(post)
        else:
            # Add message to be displayed
            if not permissions['email_confirmed']:
                messages.error(
                    request,
                    'Please confirm your email before making a submission'
                )
            elif not permissions['can_post']:
                messages.error(
                    request,
                    'You have reached your daily or monthly limit on submissions'
                )
            print post_form.errors
    else:
        post_form = PostForm()

    context_dict = {'form': post_form}

    return render_to_response('content/submit.html', context_dict, context)


@ajax_moderator_required
def delete_post(request):
    response = {'authenticated': True,
                'success': False}

    if request.is_ajax() and request.method == 'POST':
        slug = request.POST['slug']
        post = get_object_or_404(Post, slug=slug)

        if not post.deleted:
            post.deleted = True
            post.deleted_on = datetime.now()
            post.save()

        response['success'] = True

        return HttpResponse(
            json.dumps(response),
                content_type='application/json'
        )

    else:
        response['error'] = 'Invalid request'
        return HttpResponse(
            json.dumps(response),
            content_type='application/json'
        )


@ajax_moderator_required
def flag_post(request):
    response = {'authenticated': True,
                'success': False}

    if request.is_ajax() and request.method == 'POST':
        slug = request.POST['slug']
        post = get_object_or_404(Post, slug=slug)

        if not post.flagged:
            post.flagged = True
            post.flagged_on = datetime.now()
            post.save()

        response['success'] = True

        return HttpResponse(
            json.dumps(response),
                content_type='application/json'
        )

    else:
        response['error'] = 'Invalid request'
        return HttpResponse(
            json.dumps(response),
            content_type='application/json'
        )


@ajax_moderator_required
def delete_comment(request):
    response = {'authenticated': True,
                'success': False}

    if request.is_ajax() and request.method == 'POST':
        post_slug = request.POST['post_slug']
        comment_slug = request.POST['comment_slug']

        post = get_object_or_404(Post, slug=post_slug)
        comment = get_object_or_404(Comment,post=post, slug=comment_slug)

        if not comment.deleted:
            comment.deleted = True
            comment.deleted_on = datetime.now()
            comment.save()

        response['success'] = True

        return HttpResponse(
            json.dumps(response),
                content_type='application/json'
        )
    else:
        response['error'] = 'Invalid request'
        return HttpResponse(
            json.dumps(response),
            content_type='application/json'
        )


def domain_name(url):
    if urlsplit(url).scheme:
        domain = urlsplit(url).netloc
    else:
        domain = urlsplit('//' + url).netloc
    if domain.split('.')[0] == 'www':
        domain = '.'.join(domain.split('.')[1:])

    return domain