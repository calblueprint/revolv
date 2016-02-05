from django import template
from django.conf import settings
register = template.Library()


@register.filter
def fullmediaurl(value):
    """
    TODO: determine if we really need this
    """
    if not value.startswith('http'):
        return settings.SITE_URL + value

    return value


@register.simple_tag
def sharethis_pub_id():
    """
    return ShareThis publisher id
    """
    return settings.SHARETHIS_PUBLISHER_ID
