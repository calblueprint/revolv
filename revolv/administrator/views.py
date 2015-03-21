from itertools import chain

from django.views.generic import TemplateView
from revolv.base.models import RevolvUserProfile
from revolv.base.users import UserDataMixin
from revolv.project.models import Project


class AdministratorDashboardView(UserDataMixin, TemplateView):
    """Basic view for the Administrator dashboard. Shows the list of projects.
    """
    template_name = 'base/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AdministratorDashboardView, self).get_context_data(**kwargs)
        project_dict = {}
        project_dict[('Proposed Projects', "proposed")] = Project.objects.get_proposed()
        project_dict[('Active Projects', "active")] = Project.objects.get_active()
        project_dict[('Completed Projects', "completed")] = Project.objects.get_completed()
        context["project_dict"] = project_dict
        context['all_projects'] = list(chain(*(project_dict.values())))
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
