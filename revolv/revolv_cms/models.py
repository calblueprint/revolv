from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtailsettings import BaseSetting, register_setting


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


@register_setting
class MainPageSettings(BaseSetting):
    """
    Editable settings for the homepage.

    See https://wagtailsettings.readthedocs.org/en/latest/settings.html
    """
    site_tagline = models.CharField(
        max_length=100,
        help_text="The tagline for the site, which will be shown large and centered over the animated cover video.",
        default="WE'RE SAVING TOMORROW"
    )
    site_subheading = models.TextField(
        help_text="The description text that will be shown after the site tagline - a brief (one sentence) introduction to what RE-volv is and how donors can help.",
        default="When you donate to RE-volv's solar projects, you are making a lasting impact on the environment and the world around you."
    )
    learn_button_text = models.CharField(
        max_length=50,
        help_text="The label on the 'Learn more button'. E.g. 'Learn about how RE-volv works'",
        default="Learn about how RE-volv works"
    )
    current_project_heading = models.CharField(
        max_length=50,
        help_text="The heading to display above the featured project on the homepage, e.g. 'Our current project'",
        default="OUR CURRENT PROJECT"
    )
    how_it_works_heading = models.CharField(
        max_length=50,
        help_text="The heading to display above the 'Learn about how RE-volv works' section on the homepage, e.g. 'Learn about how RE-volv works'",
        default="HOW RE-VOLV WORKS"
    )
    how_it_works_intro = models.TextField(
        help_text="Intro paragraph for the 'Learn about how RE-volv works' section of the homepage.",
        default="Climate change is among the most alarming environmental issues the world faces today."
    )
    how_it_works_tagline = models.CharField(
        max_length=200,
        help_text="Large heading directly before the infograph portion of the homepage. e.g. 'How would your donation help?'",
        default="How would your donation to RE-volv help?"
    )
    how_it_works_pitch = models.CharField(
        max_length=200,
        help_text="Large text directly before the call to action donation button at the bottom of the hompage, e.g. 'Be part of something great.'",
        default="Be a part of something great."
    )
    call_to_action_button_text = models.CharField(
        max_length=50,
        help_text="The label on the green call to action button at the bottom of the homepage.",
        default="Start contributing"
    )


@register_setting
class FooterSettings(BaseSetting):
    """Editable settings for the RE-volv footer."""
    contact_heading = models.CharField(
        max_length=50,
        help_text="The heading to display in the footer menu above the contact information. Probably just 'Contact'",
        default="Contact"
    )
    contact_email = models.EmailField(
        max_length=200,
        help_text="The email address to display in the contact info section of the footer menu.",
        default="info@re-volv.org"
    )
    contact_phone_number = models.CharField(
        max_length=30,
        help_text="The phone number to display in the contact info section of the footer menu. e.g. 415.314.7719",
        default="415.314.7719"
    )
    contact_address_line_1 = models.CharField(
        max_length=150,
        help_text="The first line of the address to display in the contact info section of the footer menu.",
        default="972 Mission St. Suite 500"
    )
    contact_address_line_2 = models.CharField(
        max_length=150,
        help_text="The second line of the address to display in the contact info section of the footer menu.",
        default="San Francisco, CA 94103"
    )


@register_setting
class LoginPageSettings(BaseSetting):
    """Editable settings for the RE-volv login page."""
    heading = models.CharField(
        max_length=50,
        help_text="The heading text of the login page. e.g. 'Welcome back!'",
        default="Welcome back!"
    )
    heading_for_donation = models.CharField(
        max_length=30,
        help_text="The heading text of the login page when specifically directed there as a consequence of clicking a donate button when not logged in. e.g. 'Please log in to donate'",
        default="Login to donate"
    )
    login_paragraph = RichTextField(
        help_text="The paragraph of text to be shown under the heading on the login page, but before the links to the register page and the forgot password page.",
        default="<p>Log in to see the impact you've had on communities that use renewable solar energy.</p>"
    )
    login_paragraph_for_donation = RichTextField(
        help_text="The paragraph of text to be shown under the heading on the login page, but specifically when the user is directed to the login page as a result of clicking a donate button when not logged in.",
        default=""
    )
    button_text = models.CharField(
        max_length=30,
        help_text="The text on the actual login button, e.g. 'Log in'",
        default="Log in"
    )


@register_setting
class SignupPageSettings(BaseSetting):
    """Editable settings for the RE-volv signup (user regisration) page."""
    heading = models.CharField(
        max_length=50,
        help_text="The heading text of the sign up page. e.g. 'Welcome!'",
        default="Welcome!"
    )
    signup_paragraph = RichTextField(
        help_text="The paragraph of text to be shown under the heading on the sign up page, but before the link to the login page.",
        default="<p>Start investing in renewable solar energy by signing up for an account.</p>"
    )
    button_text = models.CharField(
        max_length=30,
        help_text="The text on the actual sign up button, e.g. 'Sign up'",
        default="Sign Up"
    )
