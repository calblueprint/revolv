from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page


class RevolvCustomPage(Page):
    """
    A CMS page representing a web page that the RE-volv administrators might
    be able to dynamically update, such as "About Us", "Former Projects",
    etc.

    How wagtail works is that there exists a hierarchy of pages, and each page
    inherits from Page like this one does (there's one root page for every site).
    Pages can have children that are of any subclass of Page, and thus RevolvCustomPages
    can be at any level in the menu hierarchy which we need for both the header
    and footer menus.
    """
    body = RichTextField()
    search_name = "Custom Page"

    indexed_fields = ('body', )
    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname="full"),
    ]


class RevolvLinkPage(Page):
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
