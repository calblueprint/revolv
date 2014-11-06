from django.views.generic import TemplateView
from revolv.base.users import UserDataMixin
from revolv.project.models import Project


class DonorDashboardView(UserDataMixin, TemplateView):
    """Basic view for the Donor dashboard.
    """
    template_name = 'donor/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DonorDashboardView, self).get_context_data(**kwargs)
        context['donated_projects'] = Project.objects.donated_projects(self.user_profile)
        return context
