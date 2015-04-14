from itertools import chain

from django.views.generic import TemplateView
from revolv.base.users import UserDataMixin
from revolv.project.models import Project


class AmbassadorDashboardView(UserDataMixin, TemplateView):
    """Basic view for the Ambassador dashboard.
    """
    template_name = 'base/dashboard.html'

    def get_context_data(self, **kwargs):
        # context = super(AdministratorDashboardView, self).get_context_data(**kwargs)
        context = super(AmbassadorDashboardView, self).get_context_data(**kwargs)
        user_projects = Project.objects.owned_projects(self.user)

        project_dict = {}
        project_dict[('Drafted Projects', "drafted")] = Project.objects.get_drafted(user_projects)
        project_dict[('Proposed Projects', "proposed")] = Project.objects.get_proposed(user_projects)
        project_dict[('Active Projects', "active")] = Project.objects.get_active(user_projects)
        project_dict[('Completed Projects', "completed")] = Project.objects.get_completed(user_projects)
        context["project_dict"] = project_dict
        context["all_projects"] = list(chain(*(project_dict.values())))
        context["role"] = "ambassador"

        # TODO: active proces processing
        if len(context['all_projects']) > 0:
            context['active_project'] = int(self.request.GET['active_project']) if 'active_project' in self.request.GET else context['all_projects'][0].id
        return context
