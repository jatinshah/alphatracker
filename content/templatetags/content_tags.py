from django import template

register = template.Library()

@register.simple_tag
def vote_class(widget, vote):
    if widget == 'up' and vote == 1:
        return 'text-primary'
    elif widget == 'down' and vote == -1:
        return 'text-primary'
    else:
        return 'text-muted'

@register.simple_tag
def comment_class(widget, vote):
    if widget == 'up' and vote == 1:
        return 'text-primary'
    elif widget == 'down' and vote == -1:
        return 'text-primary'
    else:
        return 'text-muted'