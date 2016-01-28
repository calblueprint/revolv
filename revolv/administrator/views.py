import csv

from django.http import HttpResponse
from django.views.generic import TemplateView
from revolv.base.models import RevolvUserProfile, NewsletterUser
from revolv.base.users import UserDataMixin
from revolv.base.utils import ProjectGroup
from revolv.base.views import BaseStaffDashboardView
from revolv.project.models import Project


class AdministratorDashboardView(BaseStaffDashboardView):
    """
    Basic view for the Administrator dashboard. Shows the list of projects that this
    ambassador owns. Also, shows drafted projects.
    """
    template_name = 'base/dashboard.html'
    role = "admin"

    def get_context_data(self, **kwargs):
        context = super(AdministratorDashboardView, self).get_context_data(**kwargs)

        context["project_dict"][ProjectGroup('Drafted Projects', "drafted")] = Project.objects.get_drafted()
        return context


class AdministratorEmailView(UserDataMixin, TemplateView):
    """View for the list of newsletter subscribers for the dashboard.
    """
    template_name = 'administrator/email.html'

    def get_context_data(self, **kwargs):
        context = super(AdministratorEmailView, self).get_context_data(**kwargs)

        user_profiles = RevolvUserProfile.objects.get_subscribed_to_newsletter()
        user_emails = list(user_profiles.values_list("user__email", flat=True))

        newsletter_users = NewsletterUser.objects.filter(subscribed=True).order_by('subscribed_date')
        user_emails += list(newsletter_user.values_list('email', flat=True))

        context['subscribed_user_emails'] = user_emails
        return context


def admin_email_csv_download(request):
    """View for downloading the list of newsletter subscribers as a csv file.
    Accessed via AdministratorEmailView.
    """
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails.csv"'

    users_subscribed = RevolvUserProfile.objects.get_subscribed_to_newsletter()
    newsletter_rows = [(u.user.email, u.user.first_name, u.user.last_name, u.user.date_joined) for u in users_subscribed]

    newsletter_users = NewsletterUser.objects.filter(subscribed=True).order_by('subscribed_date')
    # First and last name aren't available here, so we leave the fields blank.
    newsletter_rows += [(u.email, '', '', u.subscribed_date) for u in newsletter_users]

    writer = csv.writer(response)
    writer.writerow(['Email', 'FirstName', 'LastName', 'DateJoined'])
    writer.writerows(newsletter_rows)

    return response
