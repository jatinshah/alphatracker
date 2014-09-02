from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import itertools
import arrow
from urlparse import urlsplit
from datetime import timedelta

from content.forms import PostForm
from content.models import Post
from ranking.models import Stock


# Create your views here.
def recent(request, page=1):
    context = RequestContext(request)

    all_posts = Post.objects.order_by('-created_on')
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
        if post.post_type == 'link':
            post.domain = domain_name(post.url)

    context_dict = {
        'posts': posts
    }

    return render_to_response('content/feed.html', context_dict, context)


def post(request, slug):
    context = RequestContext(request)

    post = get_object_or_404(Post, slug=slug)

    post.created_on_humanize = arrow.get(post.created_on).humanize()

    if post.post_type == 'link':
        post.domain = domain_name(post.url)

    post.is_recent = (timezone.now() - post.created_on) < timedelta(days=1)
    user = request.user

    context_dict = {
        'post': post,
        'user': user
    }

    return render_to_response('content/post.html', context_dict, context)


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