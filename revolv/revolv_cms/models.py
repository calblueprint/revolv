from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page


class MenuableMixin(object):
    def has_menuable_children(self):
        return self.get_children.filter(live=True, show_in_menus=True).exists()

    def get_menuable_children(self):
        return self.get_children.filter(live=True, show_in_menus=True)


class RevolvCustomPage(Page, MenuableMixin):
    body = RichTextField()
    search_name = "Custom Page"

    indexed_fields = ('body', )
    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname="full"),
    ]

    def get_href(self):
        return self.url


class RevolvLinkPage(Page, MenuableMixin):
    """
    A page that represents a link to another page. Since it is technically
    a "Page", it can go into menus and have children, but it does not have
    content. A RevolvLinkPage exists for menu headers which serve as only
    links to other pages, not pages themselves, and menu items that serve as
    outside links or links to pages that are not part of the CMS, like sign in
    or auth.
    """
    link_href = models.CharField(max_length=1024)
    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('link_href', classname="full")
    ]

    def get_href(self):
        return self.link_href
