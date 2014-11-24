from django.views.generic import TemplateView
from revolv.base.users import UserDataMixin
from revolv.project.models import Project


class AmbassadorDashboardView(UserDataMixin, TemplateView):
    """Basic view for the Ambassador dashboard.
    """
    template_name = 'ambassador/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AmbassadorDashboardView, self).get_context_data(**kwargs)
        user_projects = Project.objects.owned_projects(self.user)
        context['drafted_projects'] = Project.objects.get_drafted(user_projects)
        context['proposed_projects'] = Project.objects.get_proposed(user_projects)
        context['active_projects'] = Project.objects.get_active(user_projects)
        context['completed_projects'] = Project.objects.get_completed(user_projects)
        return context
