from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from userprofile.models import User
from userprofile.forms import SignupForm
from userprofile.utils import anonymous_required


# Create your views here.
def profile(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('userprofile/profile.html', context_dict, context)


@anonymous_required
def signup(request):
    context = RequestContext(request)

    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/c/')
            else:
                print 'LOGIN: Invalid login details: {0}, {1}'.format(username, password)
        else:
            print signup_form.errors
    else:
        signup_form = SignupForm()

    context_dict = {'signup_form': signup_form}

    return render_to_response('userprofile/signup.html', context_dict, context)

