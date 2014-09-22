from django.http import HttpResponse

from functools import wraps
from json import dumps


def ajax_login_required(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_function(request, *args, **kwargs)
        json = dumps({'authenticated': False})
        return HttpResponse(json, content_type='application/json')
    return wrapper