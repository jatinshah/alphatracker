from django import template
import re

register = template.Library()

@register.simple_tag
def active(request, pattern):
    pattern = re.compile('^' + pattern + '$')
    if re.match(pattern, request.path):
        return 'active'
    else:
        return ''