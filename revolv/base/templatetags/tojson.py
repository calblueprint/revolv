import json

from django import template

register = template.Library()


@register.filter
def tojson(value):
    return json.dumps(value)
