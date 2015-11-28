from django import template
from revolv.settings import SITE_URL, MEDIA_SERVE_LOCALLY, SHARETHIS_PUBLISHER_ID
register = template.Library()


@register.filter
def fullmediaurl(value):
    """
    Return full url of media file if we are on local environment.
    For aws media.url would return full url so we can skip it
    """
    if MEDIA_SERVE_LOCALLY:
        if not value.startswith('http'):
            return SITE_URL + value

    return value


@register.simple_tag
def sharethis_pub_id():
    """
    return ShareThis publisher id
    """
    return SHARETHIS_PUBLISHER_ID