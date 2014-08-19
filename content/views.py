from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response


# Create your views here.
def index(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('content/index.html', context_dict, context)


def link(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('content/link.html', context_dict, context)


def text(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('content/text.html', context_dict, context)


def submit(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('content/submit.html', context_dict, context)