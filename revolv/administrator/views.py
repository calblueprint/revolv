from django.views.generic import TemplateView

from revolv.base.users import UserDataMixin
from revolv.base.models import RevolvUserProfile
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
        context['subscribed_user_emails'] = RevolvUserProfile.objects.get_subscribed_to_newsletter()
        return context
