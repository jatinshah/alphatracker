from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

from userprofile.models import User, UserProfile
from userprofile.forms import SignupForm, ProfileForm
from userprofile.utils import anonymous_required
from alphatracker.settings import LOGIN_REDIRECT_URL
from urllib import urlencode
from hashlib import md5


# Create your views here.
def gravatar_url(email, size=100):
    default = 'retro'

    url = "http://www.gravatar.com/avatar/" + md5(email.lower()).hexdigest() + '?'
    url += urlencode({'d':default, 's':size})

    return url


def profile(request, username):
    context = RequestContext(request)

    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get(user=user)

    context_dict = {
        'username': username,
        'user_profile': user_profile,
        'photo_url': gravatar_url(user.email)
    }

    return render_to_response('userprofile/profile.html', context_dict, context)


@login_required
def edit_profile(request):
    context = RequestContext(request)

    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        edit_form = ProfileForm(request.POST)
        if edit_form.is_valid():
            data = edit_form.cleaned_data
            UserProfile.objects.filter(user=request.user).update(
                full_name=data['full_name'],
                bio=data['bio'])
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

@anonymous_required
def signup(request):
    context = RequestContext(request)

    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,
                                password=password)
            user_profile = UserProfile.objects.create(user=user)
            user_profile.save()

            if user:
                login(request, user)
                return HttpResponseRedirect(LOGIN_REDIRECT_URL)
            else:
                print 'LOGIN: Invalid login details: {0}, {1}'.format(
                    username,
                    password)
        else:
            print signup_form.errors
    else:
        signup_form = SignupForm()

    context_dict = {'signup_form': signup_form}

    return render_to_response('userprofile/signup.html', context_dict, context)

