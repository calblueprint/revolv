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
        blank=True,
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
        blank=True,
        help_text="The paragraph of text to be shown under the heading on the login page, but before the links to the register page and the forgot password page.",
        default="<p>Log in to see the impact you've had on communities that use renewable solar energy.</p>"
    )
    login_paragraph_for_donation = RichTextField(
        blank=True,
        help_text="The paragraph of text to be shown under the heading on the login page, but specifically when the user is directed to the login page as a result of clicking a donate button when not logged in.",
        default=""
    )
    button_text = models.CharField(
        max_length=30,
        help_text="The text on the actual login button, e.g. 'Log in'",
        default="Log in"
    )

    content_panels = [
        FieldPanel('login_paragraph', classname="full"),
        FieldPanel('login_paragraph_for_donation', classname="full"),
    ]


@register_setting
class SignupPageSettings(BaseSetting):
    """Editable settings for the RE-volv signup (user regisration) page."""
    heading = models.CharField(
        max_length=50,
        help_text="The heading text of the sign up page. e.g. 'Welcome!'",
        default="Welcome!"
    )
    signup_paragraph = RichTextField(
        blank=True,
        help_text="The paragraph of text to be shown under the heading on the sign up page, but before the link to the login page.",
        default="<p>Start investing in renewable solar energy by signing up for an account.</p>"
    )
    tos_paragraph = RichTextField(
        blank=True,
        help_text="The paragraph to display directly after the form but before the sign up button. Should include a link to the Terms of Service page.",
        default="<p>Signing up for an account means joining the RE-volv community and agreeing to the <a href='/tos/'>terms of service</a>. RE-volv will never store credit card information and will never give your information to third parties. Welcome!</p>"
    )
    button_text = models.CharField(
        max_length=30,
        help_text="The text on the actual sign up button, e.g. 'Sign up'",
        default="Sign Up"
    )

    content_panels = [
        FieldPanel('signup_paragraph', classname="full"),
    ]


@register_setting
class ProjectPageSettings(BaseSetting):
    """Editable settings for the RE-volv project page."""
    donors_wording = models.CharField(
        max_length=20,
        help_text="The wording that will be displayed after the number of donors to the project the user is viewing. For example, 'donors' or 'contributors'.",
        default="donors"
    )


@register_setting
class PaymentModalSettings(BaseSetting):
    """Editable settings for the payment modal on the project page."""
    payment_modal_paragraph = RichTextField(
        blank=True,
        help_text="Optional: a paragraph which will appear above the credit card entry areas of the donation modal on the project page. Use this as another opportunity to assure the user of the security of the payments.",
        default=""
    )
    confirm_payment_paragraph = RichTextField(
        blank=True,
        help_text="Optional: a paragraph which will appear above the submit button of the donation confirmation modal on the project page. Use this as another opportunity to assure the user of the security of the payments.",
        default=""
    )

    content_panels = [
        FieldPanel('payment_modal_paragraph', classname="full"),
    ]

@register_setting
class DashboardImpactSettings(BaseSetting):
    """Editable settings for the 'My Impact' section of the dashboard page."""
    impact_statistics_header_text = models.CharField(
        max_length = 90,
        help_text = "The heading above the statistics in the 'My Impact' section of the dashboard, e.g. 'Thank you for contributing! Your contribution has...'.",
        default= 'Thank you for contributing! Your contribution has...'
    )

    description_section_explanation = ' There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.'

    repayment_statistic_top_description_text = models.CharField(
        blank=True,
        max_length = 20,
        help_text = "The top section of the description of the repayments statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= 'earned'
    )

    repayment_statistic_bottom_description_text = models.CharField(
        blank=True,
        max_length = 20,
        help_text = "The bottom section of the description of the repayments statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= 'in repayments'
    )

    project_count_statistic_top_description_text = models.CharField(
        blank=True,
        max_length = 20,
        help_text = "The top section of the description of the project count statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= 'contributed to'
    )

    project_count_statistic_bottom_description_text = models.CharField(
        blank=True,
        max_length = 20,
        help_text = "The bottom section of the description of the project count statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= ''
    )

    carbon_dioxide_statistic_top_description_text = models.CharField(
        blank=True,
        max_length = 20,
        help_text = "The top section of the description of the carbon dioxide statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= 'saved'
    )

    carbon_dioxide_statistic_bottom_description_text = models.CharField(
        blank=True,
        max_length = 20,
        help_text = "The bottom section of the description of the carbon dioxide statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= 'of carbon dioxide'
    )

    last_statistic_description_text = models.CharField(
        blank=True,
        max_length = 100,
        help_text = "The description of the bottom right icon on the 'My Impact' section of the dashboard. Unlike the other statistics on this page, this last section only has one text field.",
        default= 'Help us save the world by going solar!'
    )

    trees_saved_statistic_top_description_text = models.CharField(
        blank=True,
        max_length = 20,
        help_text = "The top section of the description of the trees saved statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= 'saved'
    )

    trees_saved_statistic_bottom_description_text = models.CharField(
        blank = True,
        max_length = 20,
        help_text = "The bottom section of the description of the trees saved statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= ''
    )

    kwh_statistic_top_description_text = models.CharField(
        blank=True,
        max_length = 20,
        help_text = "The top section of the description of the kilowatt-hours statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= 'generated'
    )

    kwh_statistic_bottom_description_text  = models.CharField(
        blank = True,
        max_length = 20,
        help_text = "The bottom section of the description of the kilowatt-hours saved statistic on the 'My Impact' section of the dashboard." + description_section_explanation,
        default= 'of electricity'
    )

@register_setting
class DashboardSettings(BaseSetting):
    """Editable settings for the dashboard page."""

    category_preferences_header_text = models.CharField(
        max_length = 100,
        help_text = "The heading of category preferences section in the 'My Impact' section of the dashboard.",
        default= 'What type of projects should we invest your repayments in next?'
    )

    category_preferences_explanation_header_text = models.CharField(
        max_length = 50,
        help_text = "The header of the category preference explanation in the 'My Impact' section of the dashboard.",
        default= "What's going on?"
    )

    category_preferences_explanation_paragraph = RichTextField(
        help_text="A paragraph which will appear below the category preference options on the 'My Impact' section on the dashboard to explain to the user what category preferences mean.",
        default="<p>Your donation to RE-volv has been invested in a revolving fund. Money from the fund is used to place solar equipment on community buildings. Over time, the community pays RE-volv back. These repayments are invested in even more solar projects. A fraction of the repayments from a solar investment originates from your investment. Your preferences directly affect where that chunk of money is invested.</p>"
    )

@register_setting
class ProjectStatisticsSettings(BaseSetting):
    """Editable settings for statistics about projects (see revolv.project.stats)"""
    kilowatt_description = models.CharField(
        max_length=50,
        help_text="A description of the concept of kilowatts of power that a project generates, to be displayed as a statistic on the dashboard or project pages. e.g. 'Kilowatt power output'",
        default="Kilowatt power output"
    )
    dollars_saved_description = models.CharField(
        max_length=50,
        help_text="A description of the dollars that a project will save in elctricity costs per month, to be displayed as a statistic on the dashboard or project pages. e.g. 'Dollars saved per month'",
        default="Dollars saved per month"
    )
    carbon_saved_description = models.CharField(
        max_length=50,
        help_text="A description of the pounds of carbon that will be saved by a project per month, to be displayed as a statistic on the dashboard or project pages. e.g. 'Carbon emissions saved per month'",
        default="Carbon emissions saved per month"
    )
    trees_description = models.CharField(
        max_length=50,
        help_text="A description of the acres of trees which, if planted, would provide equivalent savings to a project, to be displayed as a statistic on the dashboard or project pages. e.g. 'Equivalent carbon savings in trees'",
        default="Equivalent carbon savings of trees"
    )
    automobile_miles_description = models.CharField(
        max_length=50,
        help_text="A description of the equivalent automobile miles which, if driven, would produce the same amount of carbon that a project will save per month, to be displayed as a statistic on the dashboard or project pages. e.g. 'Equivalent carbon in automobile miles'",
        default="Equivalent carbon in automobile miles"
    )
