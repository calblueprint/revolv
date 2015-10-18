import csv

from django.http import HttpResponse
from django.views.generic import TemplateView
from revolv.base.models import RevolvUserProfile
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

        user_emails = RevolvUserProfile.objects.get_subscribed_to_newsletter().values_list("user__email", flat=True)
        context['subscribed_user_emails'] = user_emails
        return context


def admin_email_csv_download(request):
    """View for downloading the list of newsletter subscribers as a csv file.
    Accessed via AdministratorEmailView.
    """
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails.csv"'

    # gets users who are subscribed to the newsletter ordered by signup date
    subscribed_to_newsletter_ordered = RevolvUserProfile.objects.get_subscribed_to_newsletter()

    writer = csv.writer(response)
    writer.writerow(['Email', 'FirstName', 'LastName', 'DateJoined'])

    for revolvuserprofile in subscribed_to_newsletter_ordered:
        writer.writerow([revolvuserprofile.user.email, revolvuserprofile.user.first_name, revolvuserprofile.user.last_name, revolvuserprofile.user.date_joined])

    return response
