from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Sum

import itertools
import arrow
import json
from urlparse import urlsplit
from datetime import timedelta

from content.forms import PostForm, CommentForm
from content.models import Post, Comment, PostVote
from ranking.models import Stock
from userprofile.utils import ajax_login_required
from userprofile.models import Following
from alphatracker.settings import BASE_URL

# Up/Down vote on a post
@ajax_login_required
def vote_ajax(request):
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
            elif post_vote.vote * vote > 0:
                post_vote.vote = 0
            post_vote.save(update_fields=['vote'])
        except PostVote.DoesNotExist:
            post_vote = PostVote(post=post, user=request.user, vote=vote)
            post_vote.save()

        response['success'] = True
        return HttpResponse(
            json.dumps(response),
            content_type='application/json')
    else:
        response['error'] = 'Invalid request'
        return HttpResponse(
            json.dumps(response),
            content_type='application/json')

@login_required
def get_myfeed(request, page=1):
    return get_feed(request, page=page, order='myfeed')


#TODO: Handle empty feed scenario for My Feed (Following = 0 or no posts)
def get_feed(request, page=1, order='recent'):
    context = RequestContext(request)

    if order == 'recent':
        all_posts = Post.objects.order_by('-created_on')
    elif order == 'trending':
        all_posts = Post.objects.order_by('-created_on')   # TODO: modify ordering
    elif order == 'myfeed':
        print 'Hello'
        following = Following.objects.filter(user=request.user, active=True)
        following_users = [f.following for f in following]
        print following_users
        all_posts = Post.objects.filter(user__in=following_users).order_by('-created_on')
        print all_posts

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
                post.vote = PostVote.objects.get(post=post, user=request.user).vote
            except PostVote.DoesNotExist:
                post.vote = 0

        post.score = PostVote.objects.filter(post=post).aggregate(Sum('vote'))['vote__sum']
        if post.post_type == 'link':
            post.domain = domain_name(post.url)
        post.comments_count = Comment.objects.filter(post=post).count()

    context_dict = {
        'posts': posts,
        'path': BASE_URL + order + '/'
    }

    if order == 'recent':
        return render_to_response('content/recent.html', context_dict, context)
    elif order == 'trending':
        return render_to_response('content/trending.html', context_dict, context)
    elif order == 'myfeed':
        return render_to_response('content/myfeed.html', context_dict, context)


def post(request, slug, error_messages=None):
    context = RequestContext(request)

    if not error_messages:
        comment_form = CommentForm(initial={'slug': slug})

    post = get_object_or_404(Post, slug=slug)
    post.created_on_humanize = arrow.get(post.created_on).humanize()

    if request.user.is_authenticated():
        try:
            post.vote = PostVote.objects.get(post=post, user=request.user).vote
        except PostVote.DoesNotExist:
            post.vote = 0

    post.score = PostVote.objects.filter(post=post).aggregate(Sum('vote'))['vote__sum']

    if post.post_type == 'link':
        post.domain = domain_name(post.url)
    post.is_recent = (timezone.now() - post.created_on) < timedelta(days=1)


    user = request.user

    all_comments = Comment.objects.filter(post=post).order_by('-created_on')
    for comment in all_comments:
        comment.created_on_humanize = arrow.get(comment.created_on).humanize()

    context_dict = {
        'post': post,
        'user': user,
        'comments': all_comments,
        'comment_form': comment_form
    }

    return render_to_response('content/post.html', context_dict, context)


@login_required
def add_comment(request):
    context = RequestContext(request)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            slug = comment_form.cleaned_data['slug']
            post = get_object_or_404(Post, slug=slug)
            text = comment_form.cleaned_data['text']
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )
            comment.save()
        else:
            print comment_form.errors['text'][0]
            slug = comment_form.cleaned_data['slug']

        return HttpResponseRedirect(
            reverse('content.views.post',
                    args=(),
                    kwargs={'slug': slug}))
    else:
        return redirect('/c/')


@login_required
def submit(request):
    context = RequestContext(request)

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            user = request.user
            data = post_form.cleaned_data

            post_type = data['post_type']
            symbol = data['symbol']
            trend = data['trend']
            title = data['title']

            stock = Stock.objects.get(symbol=symbol)

            # Create slug
            max_length = Post._meta.get_field('slug').max_length
            slug = orig_slug = slugify(title)[:max_length].strip('-')

            for x in itertools.count(1):
                if not Post.objects.filter(slug=slug).exists():
                    break
                slug = '%s-%d' % (orig_slug[:max_length - len(str(x)) - 1], x)

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
            return redirect(post)
        else:
            print post_form.errors
    else:
        post_form = PostForm()

    context_dict = {'form': post_form}

    return render_to_response('content/submit.html', context_dict, context)


def domain_name(url):
    if urlsplit(url).scheme:
        domain = urlsplit(url).netloc
    else:
        domain = urlsplit('//' + url).netloc
    if domain.split('.')[0] == 'www':
        domain = '.'.join(domain.split('.')[1:])

    return domain