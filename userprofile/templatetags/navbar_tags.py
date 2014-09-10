from django import template
import re

register = template.Library()

@register.simple_tag
def active(request, pattern):
    # print re.search(pattern, request.path)
    if re.search(pattern, request.path):
        return 'active'
    else:
        return ''