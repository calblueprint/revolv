from django import template
from revolv.revolv_cms.models import RevolvLinkPage

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_cms_root_page(context):
    """
    Get the site's root wagtail page.
    See https://github.com/torchbox/wagtaildemo/blob/master/demo/templatetags/demo_tags.py
    """
    return context['request'].site.root_page


def has_menu_children(parent_page):
    """
    Return whether the given wagtail Page has children that are showable in a menu.
    """
    return parent_page.get_children().filter(live=True, show_in_menus=True).exists()


def get_menu_children_with_template_data(parent_page):
    """
    Return the children of the given wagtail Page that are live and
    showable in menus, with extra data on each page about whether they
    have children or not. This is useful for rendering menus, particularly
    when you want to check if a top level menu item has children and as such
    should be rendered with a dropdown second level menu.

    Setting an attribute on the pages is kind of hacky, but otherwise
    we would have to do a whole other variable in the templace, which is
    even grosser. Also, this is what wagtail does in their demo app: see
    https://github.com/torchbox/wagtaildemo/blob/a772fd74c2602d193afc725499a14c4b0fd2da65/demo/templatetags/demo_tags.py#L33
    """
    children = parent_page.get_children().filter(live=True, show_in_menus=True)
    for child in children:
        child.has_menu_children = has_menu_children(child)
    return children


def partial_menu_context(context, parent_page):
    """
    Render a context to pass to a two-level menu of wagtail pages.
    This is used both by partial_nav_menu and partial_footer_menu.
    """
    child_pages = get_menu_children_with_template_data(parent_page)
    return {
        "menu_pages": child_pages,
        "request": context["request"]  # we must pass this along for other tags that need it
    }


@register.assignment_tag()
def num_menu_pages(parent_page):
    """
    Return the number of top level pages for the nav and footer menus.

    Usage:
        {% num_menu_pages request.site.root_page as menu_pages_count %}
        ... do something with menu_pages count ...
    """
    return get_menu_children_with_template_data(parent_page).count()


@register.inclusion_tag("revolv_cms/tags/partial_nav_menu.html", takes_context=True)
def partial_nav_menu(context, parent_page):
    """
    A tag which renders a nav bar <ul> to two levels of child pages for
    a given parent page. See the template (partial_nav_menu.html) for
    structure of rendered content. Tag may be used as such:

    {% partial_nav_menu page %}

    :parent_page: the wagtail Page to render as the root of the menu.
        Note that the root page itself will not be rendered, and instead
        the children of the root page of the menu will be treated as the
        menu items.

    :context: necessary for tags within partial_nav_menu.html that have
        takes_context=True.
    """
    return partial_menu_context(context, parent_page)


@register.inclusion_tag("revolv_cms/tags/partial_footer_menu.html", takes_context=True)
def partial_footer_menu(context, parent_page):
    """
    A tag which renders the footer bar as a series of <div>s which are
    assumed to be columns in a foundation row. See partial_footer_menu.html
    Can be used as:

    {% partial_nav_menu request.site.root_page %}

    See partial_nav_menu for documentation on arguments - the only difference
    between the nav menu and the footer menu is the HTML structure/formatting.
    """
    return partial_menu_context(context, parent_page)


@register.assignment_tag()
def get_menu_children(parent_page):
    """
    Template tag for getting the children of a given page. Useful when
    rendering menus.
    """
    return get_menu_children_with_template_data(parent_page)


@register.assignment_tag(takes_context=True)
def link_href(context, page):
    """
    Return the url that this page defines. If it is a RevolvCustomPage,
    this will return the page's url as defined by its link_href. If not,
    it will simply return the page's regular url.
    """
    # specific_class gives us the page as the most specific subclass (in this case,
    # either RevolvCustomPage or RevolvLinkPage)
    if page.specific_class is RevolvLinkPage:
        return RevolvLinkPage.objects.get(pk=page.id).link_href
    else:
        # see https://github.com/torchbox/wagtail/blob/master/wagtail/wagtailcore/templatetags/wagtailcore_tags.py#L12
        return page.relative_url(context['request'].site)


@register.simple_tag
def commented_email(email):
    """
    Given an email, return that email interspersed with an html in order
    to break spam email parsers.
    """
    if not email or len(email) < 2:
        return ""
    else:
        halfway = len(email) / 2  # floor to integer
        return email[:halfway] + "<!-- this comment here to break email parsers -->" + email[halfway:]
