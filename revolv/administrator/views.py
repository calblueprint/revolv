import csv
from itertools import chain

from django.http import HttpResponse
from django.views.generic import TemplateView

from revolv.base.models import RevolvUserProfile
from revolv.base.users import UserDataMixin
from revolv.project.models import Project


class AdministratorDashboardView(UserDataMixin, TemplateView):
    """Basic view for the Administrator dashboard. Shows the list of projects.
    """
    template_name = 'administrator/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AdministratorDashboardView, self).get_context_data(**kwargs)
        context['proposed_projects'] = Project.objects.get_proposed()
        context['active_projects'] = Project.objects.get_active()
        context['completed_projects'] = Project.objects.get_completed()
        context['all_projects'] = list(chain(context['proposed_projects'],
                                             context['active_projects'], context['completed_projects']))
        if len(context['all_projects']) > 0:
            context['active_project'] = int(self.request.GET['active_project']) if 'active_project' in self.request.GET else context['all_projects'][0].id
        return context


class AdministratorEmailView(UserDataMixin, TemplateView):
    """View for the list of newsletter subscribers for the dashboard.
    """
    template_name = 'administrator/email.html'

    def get_context_data(self, **kwargs):
        context = super(AdministratorEmailView, self).get_context_data(**kwargs)
        context['subscribed_user_emails'] = RevolvUserProfile.objects.get_subscribed_to_newsletter()
        return context


def admin_csv_download(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails.csv"'

    subscribed_to_newsletter_ordered = RevolvUserProfile.objects.get_subscribed_to_newsletter_ordered()

    writer = csv.writer(response)
    writer.writerow(['Email', 'DateJoined'])

    for revolvuserprofile in subscribed_to_newsletter_ordered:
        writer.writerow([revolvuserprofile.user.email, revolvuserprofile.user.date_joined])

    return response
