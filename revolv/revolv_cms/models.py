from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page


class RevolvCustomPage(Page):
    body = RichTextField()
    search_name = "Custom Page"

    indexed_fields = ('body', )


RevolvCustomPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('body', classname="full"),
]
