from itertools import chain

from django.views.generic import TemplateView
from revolv.base.users import UserDataMixin
from revolv.project.models import Project


class AdministratorDashboardView(UserDataMixin, TemplateView):
    """Basic view for the Administrator dashboard.
    """
    template_name = 'administrator/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AdministratorDashboardView, self).get_context_data(**kwargs)
        context['proposed_projects'] = Project.objects.get_proposed()
        context['active_projects'] = Project.objects.get_active()
        context['completed_projects'] = Project.objects.get_completed()
        context['all_projects'] = list(chain(context['proposed_projects'],
                                             context['active_projects'], context['completed_projects']))
        return context
